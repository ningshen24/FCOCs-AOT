#!/usr/bin/env python3
"""Verify released linear model equations against released descriptors and stored predictions."""
from __future__ import annotations
import csv
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "models" / "specifications" / "models.json"
OUT = ROOT / "results" / "verification_summary.csv"

MODEL_FILES = {
    "mouse_qstr": ("mouse_qstr_modeling.csv", "experimental_pLD50"),
    "rat_qstr": ("rat_qstr_modeling.csv", "experimental_pLD50"),
    "mouse_qrastr": ("mouse_qrastr_modeling.csv", "experimental_pLD50"),
    "rat_qrastr": ("rat_qrastr_modeling.csv", "experimental_pLD50"),
    "mouse_to_rat_iqttr": ("mouse_to_rat_iqttr_modeling.csv", "rat_experimental_pLD50"),
    "rat_to_mouse_iqttr": ("rat_to_mouse_iqttr_modeling.csv", "mouse_experimental_pLD50"),
}


def load_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def predict(rows, spec):
    p = np.full(len(rows), float(spec["intercept"]), dtype=float)
    for name, coef in spec["coefficients"].items():
        p += float(coef) * np.array([float(r[name]) for r in rows])
    return p


def r2_corr(y, p):
    """Squared Pearson correlation, matching R2/R2ext convention reported in source files."""
    return float(np.corrcoef(y, p)[0, 1] ** 2)


def main():
    specs = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    summary = []
    for key, (filename, ycol) in MODEL_FILES.items():
        rows = load_csv(ROOT / "data" / "processed" / filename)
        spec = specs[key]
        pred = predict(rows, spec)
        stored = np.array([float(r["stored_prediction"]) for r in rows])
        y = np.array([float(r[ycol]) for r in rows])
        train = np.array([r["status"].lower().startswith("train") for r in rows])
        test = ~train
        max_delta = float(np.max(np.abs(pred - stored)))
        # Coefficients in the source workbooks are displayed with finite decimal precision.
        passed = max_delta <= 0.003
        rec = {
            "model": key,
            "n": len(rows),
            "n_train": int(train.sum()),
            "n_test": int(test.sum()),
            "max_abs_equation_vs_stored_prediction": max_delta,
            "train_R2_corr_squared": r2_corr(y[train], pred[train]),
            "train_MAE": float(np.mean(np.abs(y[train] - pred[train]))),
            "test_R2_corr_squared": r2_corr(y[test], pred[test]),
            "test_RMSE": float(np.sqrt(np.mean((y[test] - pred[test]) ** 2))),
            "test_MAE": float(np.mean(np.abs(y[test] - pred[test]))),
            "equation_reproduces_stored_predictions": passed,
        }
        summary.append(rec)
        print(
            f"{key:24s} n={len(rows):3d} max|Δpred|={max_delta:.6g} "
            f"train R2={rec['train_R2_corr_squared']:.4f} "
            f"test R2={rec['test_R2_corr_squared']:.4f} "
            f"test RMSE={rec['test_RMSE']:.4f} {'PASS' if passed else 'FAIL'}"
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)

    if not all(r["equation_reproduces_stored_predictions"] for r in summary):
        raise SystemExit("One or more model equations failed the prediction-reproduction tolerance.")
    print(f"\nWrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
