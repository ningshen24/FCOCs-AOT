# Orange workflow audit

Two revised Orange workflow files are included under `models/orange/`. They preserve the ML workflow topology and the final saved learner settings used for release. The exact installed Orange3 package/add-on version is **not encoded unambiguously in both `.ows` files** and should still be recorded from the original modeling environment if available.

## Files

- `Mouse_QSTR-ML.ows`
- `Rat_QSTR-ML.ows`
- `workflow_settings_extracted.json`: machine-readable settings parsed without executing Orange.
- `workflow_settings_extracted.csv`: flattened learner settings.
- `workflow_vs_reported_discrepancies.csv`: reconciliation table showing that the previously identified Table S6/final-QSTR conflicts are now resolved.

## Saved workflow topology

Both workflows contain training and external-test File widgets feeding SVM, Gradient Boosting, kNN, Random Forest, Neural Network, Linear Regression, XGBoost (through the Gradient Boosting widget), and Stochastic Gradient Descent learners. Learners feed `Test and Score` and `Predictions`; the external-test File widget supplies test/prediction data.

The File widgets still contain local Windows path history. These paths must be relinked when opening the workflows on another computer. The repository provides species-specific ML inputs in `data/processed/mouse_ml_input.csv` and `data/processed/rat_ml_input.csv`.

## Final saved QSTR feature contexts

### Mouse

`AATS3p`, `F10[C-O]`, `minHBint3`, `P_VSA_charge_10`, `P_VSA_charge_14`, `SM1_Dzm`

### Rat

`AATSC7i`, `CATS2D_08_DL`, `ChiA_X`, `F06[C-N]`, `P_VSA_charge_10`

The Rat workflow can still contain `F01[C-N]` in older saved widget-history/context strings. The revised current/final feature context contains `F06[C-N]`, consistent with the final Rat QSTR equation, Table S2 and `rat_ml_input.csv`. Historical strings are preserved only as provenance.

## Previously conflicting settings — now resolved

| Setting | Table S6 / final input | Revised Mouse `.ows` | Revised Rat `.ows` | Status |
|---|---:|---:|---:|---|
| NN neurons | 2000 | 2000 | 2000 | Resolved |
| NN replicable training | Enabled | True | True | Resolved |
| SVM numerical tolerance | 0.01 | 0.01 | 0.01 | Resolved |
| Rat C-N descriptor | F06[C-N] | — | F06[C-N] | Resolved |

The machine-readable reconciliation is in `models/orange/workflow_vs_reported_discrepancies.csv`.

## Version note

One Rat workflow historical path contains `E:/Orange 3.40.0/...`, which suggests that Orange 3.40.0 may have been installed in at least one environment. This repository does **not** promote that path string to authoritative software-version metadata because the Mouse workflow and workflow schema do not independently confirm the exact installed package/add-on version.

## Security / extraction note

Orange `.ows` files can contain pickled widget state. `scripts/audit_orange_workflows.py` does **not** execute or unpickle those payloads. It parses XML literal learner properties and uses `pickletools` only for non-executing inspection of saved text strings such as paths and variable names.
