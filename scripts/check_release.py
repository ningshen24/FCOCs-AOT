#!/usr/bin/env python3
"""Lightweight release integrity checks for the public repository package."""
from pathlib import Path
import csv
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    "README.md",
    "CITATION.cff",
    "models/specifications/models.json",
    "data/source/supplementary materials1.xlsx",
    "data/source_csv/Table_S1.csv",
    "data/source_csv/Table_S9.csv",
    "data/processed/mouse_qstr_modeling.csv",
    "data/processed/rat_qstr_modeling.csv",
    "data/descriptors/mouse_padel_alvadesc_cleaned.tsv",
    "data/descriptors/rat_padel_alvadesc_cleaned.tsv",
    "models/orange/Mouse_QSTR-ML.ows",
    "models/orange/Rat_QSTR-ML.ows",
    "docs/ORANGE_WORKFLOW_AUDIT.md",
    "docs/DATA_CHECKS.md",
]
missing = [p for p in required if not (ROOT / p).exists()]
if missing:
    raise SystemExit("Missing required files: " + ", ".join(missing))

# Regenerate/check model and workflow validation outputs.
subprocess.run([sys.executable, str(ROOT / "scripts/verify_models.py")], check=True)
subprocess.run([sys.executable, str(ROOT / "scripts/check_descriptor_matrices.py")], check=True)
subprocess.run([sys.executable, str(ROOT / "scripts/audit_orange_workflows.py")], check=True)

# Rat q-RASTR Q2_LOO must be synchronized to the author-confirmed value 0.8057.
models = json.loads((ROOT / "models/specifications/models.json").read_text(encoding="utf-8"))
q2 = float(models["rat_qrastr"]["reported_validation"]["Q2_LOO"])
if abs(q2 - 0.8057) > 1e-12:
    raise SystemExit(f"Rat q-RASTR models.json Q2_LOO is {q2}, expected 0.8057")
with (ROOT / "results/rat_model_performance_reported.csv").open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))
rq = next(r for r in rows if r["model"] == "q-RASTR")
if abs(float(rq["Q2_LOO"]) - 0.8057) > 1e-12:
    raise SystemExit("Rat q-RASTR reported-performance Q2_LOO is not 0.8057")

# Corrected supplementary CSV exports must not retain formula-error strings.
for name in ["Table_S1.csv", "Table_S9.csv"]:
    text = (ROOT / "data/source_csv" / name).read_text(encoding="utf-8-sig")
    for token in ["#NAME?", "#REF!", "#DIV/0!", "#VALUE!", "#N/A"]:
        if token in text:
            raise SystemExit(f"{name} still contains spreadsheet error token {token}")
if "18725" not in (ROOT / "data/source_csv/Table_S9.csv").read_text(encoding="utf-8-sig"):
    raise SystemExit("Table S9 export does not contain CID 18725")

# All recorded Orange reconciliation rows must now be resolved.
with (ROOT / "models/orange/workflow_vs_reported_discrepancies.csv").open(encoding="utf-8-sig", newline="") as f:
    recon = list(csv.DictReader(f))
if not recon or any(r.get("status") != "resolved" for r in recon):
    raise SystemExit("Orange workflow reconciliation table contains unresolved rows")

print("Release integrity checks passed.")
