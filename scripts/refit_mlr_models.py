#!/usr/bin/env python3
"""Independently refit OLS coefficients on released training subsets and compare with reported coefficients."""
from __future__ import annotations
import csv
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SPEC = json.loads((ROOT / "models/specifications/models.json").read_text(encoding="utf-8"))
OUT = ROOT / "results" / "ols_refit_coefficients.csv"

CONFIG = {
    "mouse_qstr": ("mouse_qstr_modeling.csv", "experimental_pLD50"),
    "rat_qstr": ("rat_qstr_modeling.csv", "experimental_pLD50"),
    "mouse_qrastr": ("mouse_qrastr_modeling.csv", "experimental_pLD50"),
    "rat_qrastr": ("rat_qrastr_modeling.csv", "experimental_pLD50"),
    "mouse_to_rat_iqttr": ("mouse_to_rat_iqttr_modeling.csv", "rat_experimental_pLD50"),
    "rat_to_mouse_iqttr": ("rat_to_mouse_iqttr_modeling.csv", "mouse_experimental_pLD50"),
}


def read(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    records = []
    for key, (fn, ycol) in CONFIG.items():
        rows = read(ROOT / "data/processed" / fn)
        tr = [r for r in rows if r["status"].lower().startswith("train")]
        names = list(SPEC[key]["coefficients"])
        X = np.array([[float(r[n]) for n in names] for r in tr], dtype=float)
        y = np.array([float(r[ycol]) for r in tr], dtype=float)
        beta = np.linalg.lstsq(np.column_stack([np.ones(len(X)), X]), y, rcond=None)[0]
        reported = [float(SPEC[key]["intercept"])] + [float(SPEC[key]["coefficients"][n]) for n in names]
        terms = ["Intercept"] + names
        for term, fit, rep in zip(terms, beta, reported):
            records.append({
                "model": key,
                "term": term,
                "refit_coefficient": float(fit),
                "reported_coefficient": rep,
                "absolute_difference": float(abs(fit-rep)),
            })
        maxdiff = max(abs(beta - np.array(reported)))
        print(f"{key:24s} max coefficient difference = {maxdiff:.6g}")

    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(records[0]))
        w.writeheader(); w.writerows(records)
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
