#!/usr/bin/env python3
"""Apply a released linear FCOCs-AOT equation to a CSV containing its required descriptors."""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECS = json.loads((ROOT / "models/specifications/models.json").read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, choices=sorted(SPECS))
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    spec = SPECS[args.model]
    required = list(spec["coefficients"])
    with args.input.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
        if not rows:
            raise SystemExit("Input CSV has no data rows")
        missing = [c for c in required if c not in rows[0]]
        if missing:
            raise SystemExit("Missing required columns: " + ", ".join(missing))
        fields = list(rows[0]) + ["predicted_pLD50"]
    for r in rows:
        p = float(spec["intercept"])
        for name, coef in spec["coefficients"].items():
            p += float(coef) * float(r[name])
        r["predicted_pLD50"] = f"{p:.10g}"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)
    print(args.output)


if __name__ == "__main__":
    main()
