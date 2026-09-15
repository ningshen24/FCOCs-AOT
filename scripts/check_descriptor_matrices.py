#!/usr/bin/env python3
"""Validate the released cleaned PaDEL+alvaDesc descriptor matrices.

The matrices are user-supplied merged descriptor tables after removal of empty/NA
values. This script verifies basic integrity and checks that final QSTR-selected
features for all modeling compounds agree with the reconciled processed tables
within rounding tolerance.
"""
from pathlib import Path
import csv
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "descriptor_matrix_check.csv"

CONFIG = {
    "mouse": {
        "matrix": ROOT / "data/descriptors/mouse_padel_alvadesc_cleaned.tsv",
        "model": ROOT / "data/processed/mouse_qstr_modeling.csv",
        "features": ["AATS3p", "F10[C-O]", "minHBint3", "P_VSA_charge_10", "P_VSA_charge_14", "SM1_Dzm"],
        "expected_rows": 94,
        "expected_cols": 4749,
    },
    "rat": {
        "matrix": ROOT / "data/descriptors/rat_padel_alvadesc_cleaned.tsv",
        "model": ROOT / "data/processed/rat_qstr_modeling.csv",
        "features": ["AATSC7i", "CATS2D_08_DL", "ChiA_X", "F06[C-N]", "P_VSA_charge_10"],
        "expected_rows": 96,
        "expected_cols": 4783,
    },
}


def as_float(x):
    return float(str(x).strip())


def load_tsv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        fields = next(reader)
        rows = list(reader)
    return fields, rows


def load_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames or [], list(reader)


summary = []
for species, cfg in CONFIG.items():
    fields, rows = load_tsv(cfg["matrix"])
    if len(rows) != cfg["expected_rows"] or len(fields) != cfg["expected_cols"]:
        raise SystemExit(f"{species}: unexpected descriptor matrix shape {len(rows)} x {len(fields)}")
    duplicate_headers = sorted({name for name in fields if fields.count(name) > 1})
    # The supplied merged exports intentionally contain two columns named CID:
    # column 1 is the compound identifier, while a later numeric field is also
    # labelled CID. Preserve the original header and address required fields by
    # column position rather than silently renaming them.
    unexpected_dups = [x for x in duplicate_headers if x != "CID"]
    if unexpected_dups:
        raise SystemExit(f"{species}: unexpected duplicate header fields: {unexpected_dups}")
    blanks = sum(1 for row in rows for v in row if v is None or str(v).strip() == "" or str(v).strip().lower() in {"na", "nan"})
    if blanks:
        raise SystemExit(f"{species}: {blanks} blank/NA cells detected")

    first_index = {}
    for i, name in enumerate(fields):
        first_index.setdefault(name, i)
    required = ["CID", " -logLD50"] + cfg["features"]
    missing_fields = [x for x in required if x not in first_index]
    if missing_fields:
        raise SystemExit(f"{species}: required fields missing from descriptor matrix: {missing_fields}")
    matrix_by_cid = {str(row[first_index["CID"]]).strip(): row for row in rows}
    _, model_rows = load_csv(cfg["model"])
    missing = [r["CID"] for r in model_rows if str(r["CID"]).strip() not in matrix_by_cid]
    if missing:
        raise SystemExit(f"{species}: modeling CIDs missing from descriptor matrix: {missing[:10]}")

    max_diff = 0.0
    n_compared = 0
    for mr in model_rows:
        cid = str(mr["CID"]).strip()
        fr = matrix_by_cid[cid]
        # endpoint cross-check
        diff = abs(as_float(mr["experimental_pLD50"]) - as_float(fr[first_index[" -logLD50"]]))
        max_diff = max(max_diff, diff)
        n_compared += 1
        for feat in cfg["features"]:
            diff = abs(as_float(mr[feat]) - as_float(fr[first_index[feat]]))
            max_diff = max(max_diff, diff)
            n_compared += 1
    if max_diff > 1e-5:
        raise SystemExit(f"{species}: selected descriptor mismatch exceeds tolerance: {max_diff}")

    summary.append({
        "species": species,
        "rows": len(rows),
        "columns": len(fields),
        "blank_or_na_cells": blanks,
        "duplicate_header_fields": ";".join(duplicate_headers),
        "modeling_compounds_checked": len(model_rows),
        "values_compared": n_compared,
        "max_abs_difference": f"{max_diff:.8g}",
        "status": "PASS",
    })

with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(summary[0]))
    w.writeheader(); w.writerows(summary)

print(f"Descriptor matrix checks passed; wrote {OUT.relative_to(ROOT)}")
