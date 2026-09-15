# Data consistency checks performed during repository preparation

This file records cross-checks among the supplied manuscript, dedicated model workbooks, supplementary workbook, cleaned descriptor matrices and Orange workflows. The repository now uses the latest author-corrected supplementary workbook and revised Orange `.ows` files.

## Check 1 — Mouse QSTR CID 12442 descriptor-row shift

**Status:** reconciled in the processed/released modeling data; the dedicated Mouse-QSTR source workbook still contains the original shifted row.

In `FCOCs-AOT-Mouse-QSTR.xlsx`, PubChem CID **12442** contains a column shift after `AATS3p`. The author-supplied supplementary Table S1 and cleaned merged Mouse PaDEL+alvaDesc descriptor matrix agree on the internally consistent final values:

| Descriptor | Final value |
|---|---:|
| AATS3p | 2.635932 |
| F10[C-O] | 0 |
| minHBint3 | 0 |
| P_VSA_charge_10 | 0 |
| P_VSA_charge_14 | 1.819749 |
| SM1_Dzm | 3.641801 |

Using these values with the published equation restores the reported model statistics: training `R² ≈ 0.8626`, training `MAE ≈ 0.1983`, and test `RMSE ≈ 0.3377`.

**Remaining release note:** either correct the dedicated source workbook row before final publication or explicitly document that the released processed table/supplement contains the authoritative corrected row.

## Check 2 — Mouse QSTR CID 3026 endpoint

**Status:** resolved.

The earlier supplementary Table S1 value for CID **3026** was `0.997062`, while the dedicated Mouse-QSTR workbook and cleaned merged descriptor matrix give the experimental endpoint as **1.90**. The latest author-corrected supplementary workbook now also records **1.90**. The processed modeling table, supplementary source and descriptor matrix are therefore aligned.

## Check 3 — Rat q-RASTR Q²_LOO

**Status:** resolved; authoritative value confirmed by the author as **0.8057**.

The dedicated `FCOCs-AOT-Rat-q-RASTR.xlsx` validation sheet reports `Q²_LOO = 0.8057`. `results/rat_model_performance_reported.csv`, `models/specifications/models.json` and the repository documentation have been synchronized to **0.8057**.

## Check 4 — Exact software versions still incomplete

The exact **alvaDesc** version remains absent. The exact installed **Orange3 package/add-on version** is also not encoded unambiguously in both `.ows` files. A Rat workflow path hint contains `Orange 3.40.0`, but a local path string is not treated as authoritative version metadata. Exact versions should be recorded from the original modeling environment if available.

## Check 5 — Cleaned descriptor-matrix integrity and QSTR cross-check

The merged descriptor tables were checked as tab-separated files:

- Mouse: 94 rows × 4749 columns; no blank/NA cells.
- Rat: 96 rows × 4783 columns; no blank/NA cells.
- Both raw merged headers contain the label `CID` twice. The first `CID` column is the PubChem compound identifier; a later numeric field is also labeled `CID`. The repository preserves the original header and verification scripts address the first `CID` field explicitly.

All 63 Mouse and 67 Rat final QSTR compounds are present. For the final QSTR-selected descriptors and experimental endpoint, values agree with the processed modeling tables within ≤1e-5 absolute difference.

## Check 6 — Orange workflow versus Table S6/final QSTR inputs

**Status:** resolved for the previously identified final-setting conflicts.

The revised Mouse and Rat `.ows` workflows now store:

- NN hidden layer: **2000** neurons;
- NN replicable training: **True / Enabled**;
- SVM numerical tolerance: **0.01**;
- Rat final C-N descriptor context: **`F06[C-N]`**.

These match Table S6 and the final Rat QSTR/ML input definition. Historical widget context strings can still contain older entries such as `F01[C-N]`; the audit reports those separately as provenance and does not treat them as the final Rat feature set.

## Check 7 — Table S9 no-output cell

**Status:** resolved.

Earlier supplementary Table S9 cell `L14` (CID **18725**) contained `#NAME?`. The author confirmed that this represents a case with **no output value**, and the latest supplementary workbook records the cell as `-`. A full workbook scan detects no remaining `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?` or `#N/A` cells.

## Check 8 — Reproduction of final linear equations

The released descriptor/modeling tables reproduce the stored QSTR/q-RASTR/iQTTR predictions within ordinary coefficient-rounding tolerance (approximately 10⁻³). Independent training-set OLS refits recover the reported coefficients to the displayed precision.
