# Data dictionary

## Common fields

| Field | Meaning |
|---|---|
| `CID` | PubChem Compound ID |
| `status` | Model split membership (`Train`, `Test`, or true-external where applicable) |
| `experimental_pLD50` | Experimental acute oral toxicity endpoint, `-log10(LD50 [mol/kg])` |
| `stored_prediction` | Prediction reported in the dedicated model workbook |
| `Predicted endpoint` | Predicted pLD50 in original supporting tables |
| `Residual` | Model residual as reported by the source workbook/table |
| `HAT i/i` | Leverage used for applicability-domain assessment |
| `PRI` | Prediction Reliability Index reported for true-external predictions |

## Mouse QSTR descriptors

- `AATS3p`
- `F10[C-O]`
- `minHBint3`
- `P_VSA_charge_10`
- `P_VSA_charge_14`
- `SM1_Dzm`

## Rat QSTR descriptors

- `AATSC7i`
- `CATS2D_08_DL`
- `ChiA_X`
- `F06[C-N]`
- `P_VSA_charge_10`

## Mouse q-RASTR descriptors

- `Abs MaxPos-MaxNeg`
- `B02[C-S]`
- `P_VSA_charge_10`
- `sm1(GK)[Banerjee-Roy similarity coefficient 1]`
- `SP-2`
- `SPC-4`

## Rat q-RASTR descriptors

- `CATS2D_08_DL`
- `Eig06_EA(dm)`
- `JGI10`
- `P_VSA_charge_10`
- `PW3`

For detailed chemical/descriptor definitions and references, see the original source workbooks and manuscript. Descriptor naming is preserved exactly because it is needed for reproducibility.

## Source CSV exports

`data/source_csv/Table_S1.csv` through `Table_S9.csv` are faithful, machine-readable exports from the latest author-corrected supplementary workbook. They therefore include the corrected CID 3026 Mouse endpoint (`1.90`) and the Table S9 no-output marker (`-`) for CID 18725 documented in `DATA_CHECKS.md`.

`data/processed/` contains the reconciled analysis-ready tables used by the verification scripts.


## Cleaned merged descriptor matrices

`data/descriptors/mouse_padel_alvadesc_cleaned.tsv` and `rat_padel_alvadesc_cleaned.tsv` are author-supplied merged PaDEL+alvaDesc descriptor matrices after empty/NA values were removed. They preserve the original descriptor column names. They are not labeled by per-descriptor software provenance, so the repository does not infer which program generated every individual column.

- Mouse: 94 compounds × 4749 columns, no blank/NA cells detected.
- Rat: 96 compounds × 4783 columns, no blank/NA cells detected.

The first identifier/endpoint columns include `CID` and ` -logLD50`. Both merged files also contain a later numeric field whose original header is again `CID`. This duplicate source label is preserved intentionally; scripts use the **first** `CID` column as the PubChem compound identifier and do not silently rename the later field.

## Orange workflow artifacts

`models/orange/` contains the two revised original `.ows` files plus non-executing extracted settings. The final saved NN/SVM settings now agree with `data/processed/ml_hyperparameters.csv`/Table S6, and the Rat final feature context contains `F06[C-N]`. Historical widget contexts can retain older variable strings; these are reported separately in `docs/ORANGE_WORKFLOW_AUDIT.md`.
