#!/usr/bin/env python3
"""Safely audit and extract settings from the released Orange .ows workflows.

The script does not execute or unpickle Orange widget state. XML literal learner
properties are parsed with ``ast.literal_eval``; pickled widget payloads are only
inspected with ``pickletools`` to recover text strings such as file paths and
saved variable names.
"""
from pathlib import Path
import ast
import base64
import csv
import json
import pickletools
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORANGE_DIR = ROOT / "models" / "orange"
RESULTS_DIR = ROOT / "results"
OUT_CHECK = RESULTS_DIR / "orange_workflow_check.csv"
OUT_JSON = ORANGE_DIR / "workflow_settings_extracted.json"
OUT_CSV = ORANGE_DIR / "workflow_settings_extracted.csv"
OUT_RECON = ORANGE_DIR / "workflow_vs_reported_discrepancies.csv"

CONFIG = {
    "mouse": {
        "path": ORANGE_DIR / "Mouse_QSTR-ML.ows",
        "expected_features": ["AATS3p", "F10[C-O]", "minHBint3", "P_VSA_charge_10", "P_VSA_charge_14", "SM1_Dzm"],
        "legacy_watch": [],
    },
    "rat": {
        "path": ORANGE_DIR / "Rat_QSTR-ML.ows",
        "expected_features": ["AATSC7i", "CATS2D_08_DL", "ChiA_X", "F06[C-N]", "P_VSA_charge_10"],
        "legacy_watch": ["F01[C-N]"],
    },
}

DROP_KEYS = {"savedWidgetGeometry", "controlAreaVisible", "auto_apply", "learner_name", "__version__"}


def pickle_strings(text):
    data = base64.b64decode("".join((text or "").split()))
    out = []
    for op, arg, _ in pickletools.genops(data):
        if op.name in {"SHORT_BINUNICODE", "BINUNICODE", "UNICODE"} and isinstance(arg, str):
            out.append(arg)
    return out


def clean_value(value):
    if isinstance(value, bytes):
        return None
    if isinstance(value, dict):
        return {k: clean_value(v) for k, v in value.items() if k not in DROP_KEYS and not isinstance(v, bytes)}
    if isinstance(value, (list, tuple)):
        return [clean_value(v) for v in value if not isinstance(v, bytes)]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def flatten(prefix, value):
    if isinstance(value, dict):
        for k, v in value.items():
            yield from flatten(f"{prefix}.{k}" if prefix else k, v)
    else:
        yield prefix, value


workflows = []
flat_rows = []
check_rows = []
recon_rows = []

for species, cfg in CONFIG.items():
    root = ET.parse(cfg["path"]).getroot()
    scheme_version = root.attrib.get("version")
    nodes = {int(n.attrib["id"]): dict(n.attrib) for n in root.find("nodes")}
    props_xml = {int(p.attrib["node_id"]): p for p in root.find("node_properties")}

    all_strings = []
    strings_by_node = {}
    learner_props = {}
    node_records = []

    for nid, nd in sorted(nodes.items()):
        node_records.append({
            "id": str(nid),
            "name": nd.get("name", ""),
            "qualified_name": nd.get("qualified_name", ""),
            "project_name": nd.get("project_name", ""),
            "version": nd.get("version", ""),
            "title": nd.get("title", ""),
            "position": nd.get("position", ""),
        })

    for nid, p in props_xml.items():
        fmt = p.attrib.get("format")
        if fmt == "pickle":
            try:
                ss = pickle_strings(p.text)
            except Exception:
                ss = []
            strings_by_node[nid] = ss
            all_strings.extend(ss)
        elif fmt == "literal":
            try:
                val = ast.literal_eval(p.text)
            except Exception:
                continue
            if isinstance(val, dict):
                learner_props[str(nid)] = clean_value(val)

    missing = [x for x in cfg["expected_features"] if x not in all_strings]
    if missing:
        raise SystemExit(f"{species}: final feature strings missing from saved workflow context: {missing}")

    svm = learner_props.get("1", {})
    nn = learner_props.get("10", {})
    if abs(float(svm.get("tol")) - 0.01) > 1e-12:
        raise SystemExit(f"{species}: SVM tolerance is not 0.01")
    if str(nn.get("hidden_layers_input")) != "2000":
        raise SystemExit(f"{species}: NN hidden layer is not 2000")
    if bool(nn.get("replicable")) is not True:
        raise SystemExit(f"{species}: NN replicable flag is not True")

    def xlsx_paths(nid):
        return [s for s in strings_by_node.get(nid, []) if s.lower().endswith((".xlsx", ".xls", ".tab", ".csv"))]

    train_paths = xlsx_paths(0)
    test_paths = xlsx_paths(8)
    version_hints = sorted({s for s in all_strings if "Orange 3." in s})
    legacy_mentions = [x for x in cfg["legacy_watch"] if x in all_strings]
    targets = [x for x in all_strings if x.strip().lower() in {"-logld50", "pld50", "p_ld50", "pld50 "}]

    workflows.append({
        "species": species,
        "workflow_file": cfg["path"].name,
        "scheme_version": scheme_version,
        "exact_orange3_package_version": None,
        "orange_version_path_hints": version_hints,
        "saved_training_path_hint": train_paths[0] if train_paths else None,
        "saved_test_path_hint": test_paths[0] if test_paths else None,
        "final_qstr_features": cfg["expected_features"],
        "legacy_context_feature_mentions": legacy_mentions,
        "saved_target_strings": sorted(set(targets)),
        "nodes": node_records,
        "learner_properties_by_node_id": learner_props,
    })

    for nid_s, val in learner_props.items():
        nid = int(nid_s)
        raw_name = nodes.get(nid, {}).get("name", f"node_{nid}")
        display_name = raw_name
        if raw_name == "Gradient Boosting" and isinstance(val, dict) and val.get("method_index") == 1:
            display_name = "XGBoost (Gradient Boosting widget)"
        for key, v in flatten("", val):
            flat_rows.append({"species": species, "learner": display_name, "parameter": key, "value": v})

    check_rows.extend([
        {"species": species, "check": "workflow XML parses", "saved_value": "yes", "status": "PASS"},
        {"species": species, "check": "final QSTR feature context present", "saved_value": "; ".join(cfg["expected_features"]), "status": "PASS"},
        {"species": species, "check": "saved NN neurons", "saved_value": nn.get("hidden_layers_input"), "status": "PASS"},
        {"species": species, "check": "saved NN replicable", "saved_value": nn.get("replicable"), "status": "PASS"},
        {"species": species, "check": "saved SVM tolerance", "saved_value": svm.get("tol"), "status": "PASS"},
    ])
    if legacy_mentions:
        check_rows.append({"species": species, "check": "legacy context strings", "saved_value": "; ".join(legacy_mentions), "status": "INFO_ONLY"})

    recon_rows.extend([
        {"species": species, "item": "Neural network number of neurons", "reported_or_qstr_value": "2000", "saved_ows_value": str(nn.get("hidden_layers_input")), "status": "resolved", "note": "Revised OWS matches Table S6."},
        {"species": species, "item": "Neural network replicable training", "reported_or_qstr_value": "Enabled", "saved_ows_value": str(nn.get("replicable")), "status": "resolved", "note": "True corresponds to replicable training enabled."},
        {"species": species, "item": "SVM numerical tolerance", "reported_or_qstr_value": "0.01", "saved_ows_value": str(svm.get("tol")), "status": "resolved", "note": "Revised OWS matches Table S6."},
    ])

# Rat descriptor reconciliation row.
rat_strings = []
rat_root = ET.parse(CONFIG["rat"]["path"]).getroot()
for p in rat_root.find("node_properties"):
    if p.attrib.get("format") == "pickle":
        try:
            rat_strings.extend(pickle_strings(p.text))
        except Exception:
            pass
recon_rows.append({
    "species": "rat",
    "item": "Rat ML descriptor linked to C-N atom pair",
    "reported_or_qstr_value": "F06[C-N]",
    "saved_ows_value": "F06[C-N]",
    "status": "resolved",
    "note": "Revised workflow contains the final F06[C-N] context; legacy F01[C-N] strings remain only in historical saved contexts.",
})

OUT_JSON.write_text(json.dumps({"workflows": workflows}, indent=2, ensure_ascii=False), encoding="utf-8")
with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["species", "learner", "parameter", "value"])
    w.writeheader(); w.writerows(flat_rows)
with OUT_RECON.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["species", "item", "reported_or_qstr_value", "saved_ows_value", "status", "note"])
    w.writeheader(); w.writerows(recon_rows)
with OUT_CHECK.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["species", "check", "saved_value", "status"])
    w.writeheader(); w.writerows(check_rows)

print(f"Orange workflow audit passed; revised workflows align with Table S6; wrote {OUT_CHECK.relative_to(ROOT)}")
