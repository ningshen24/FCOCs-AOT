#!/usr/bin/env python3
"""Create species-specific ML input files from the reconciled QSTR tables."""
from __future__ import annotations
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = {
    "mouse": ("mouse_qstr_modeling.csv", ["AATS3p", "F10[C-O]", "minHBint3", "P_VSA_charge_10", "P_VSA_charge_14", "SM1_Dzm"]),
    "rat": ("rat_qstr_modeling.csv", ["AATSC7i", "CATS2D_08_DL", "ChiA_X", "F06[C-N]", "P_VSA_charge_10"]),
}

for species, (fn, descriptors) in CONFIG.items():
    src = ROOT / "data/processed" / fn
    with src.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    fields = ["CID", "status", "experimental_pLD50"] + descriptors
    out = ROOT / "data/processed" / f"{species}_ml_input.csv"
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in fields})
    print(f"Wrote {out.relative_to(ROOT)}")
