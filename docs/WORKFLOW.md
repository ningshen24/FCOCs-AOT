# Reproducible workflow

This document maps the manuscript workflow to released repository inputs and outputs.

## 1. Acute oral toxicity data collection and endpoint transformation

**Manuscript:** Section 2.1

- Acute oral LD50 data were collected from PubChem for mouse and rat.
- LD50 values were converted to mol/kg and transformed as `pLD50 = -log10(LD50 [mol/kg])`.
- Final modeling sets contain 63 mouse compounds and 67 rat compounds.
- Twenty-seven chemicals shared by both species were used for iQTTR modeling.

**Repository:**

- Original supporting data: `data/source/supplementary materials1.xlsx`
- Machine-readable exports: `data/source_csv/Table_S1.csv`, `Table_S2.csv`, `Table_S3.csv`
- Clean modeling tables: `data/processed/mouse_qstr_modeling.csv`, `rat_qstr_modeling.csv`

## 2. Molecular descriptor calculation and preprocessing

**Manuscript:** descriptor calculation / preprocessing methods

- 2D molecular descriptors were generated with PaDEL-Descriptor 2.18 and alvaDesc.
- The authors merged the two descriptor outputs and removed columns/entries with empty or NA values before downstream modeling.
- Constant, near-constant and highly correlated variables were subsequently filtered before model development as described in the manuscript.

**Repository:**

- `data/descriptors/mouse_padel_alvadesc_cleaned.tsv`: cleaned merged Mouse descriptor matrix, 94 compounds × 4749 columns.
- `data/descriptors/rat_padel_alvadesc_cleaned.tsv`: cleaned merged Rat descriptor matrix, 96 compounds × 4783 columns.
- These files are **cleaned merged descriptor matrices**, not raw untouched software exports.
- All 63 final Mouse QSTR compounds and 67 final Rat QSTR compounds are present in these matrices. Selected descriptor values agree with `data/processed/*_qstr_modeling.csv` within ordinary export/rounding tolerance.
- The final selected descriptor values used by the released models remain in `data/processed/` for compact reproducibility.

## 3. QSTR modeling in QSARINS 2.2.4

**Manuscript:** QSTR methods

- Train/test ratio approximately 3:1.
- Candidate splitting strategies: ordered response (ORes), ordered structure (OStr), and random (Rnd).
- MLR fitted by ordinary least squares.
- Genetic algorithm descriptor selection; maximum six variables; population 200; mutation rate 20%; 500 iterations; `Q²_LOO` used as fitness.
- Internal and external validation and applicability-domain analysis conducted in QSARINS.

**Repository:**

- Model files: `models/qsarins/mouse-QSTR.qsi`, `rat-QSTR.qsi`
- Equations/settings: `models/specifications/models.json`
- Modeling tables: `data/processed/mouse_qstr_modeling.csv`, `rat_qstr_modeling.csv`
- Verification: `scripts/verify_models.py`, `scripts/refit_mlr_models.py`

## 4. q-RASTR workflow

**Manuscript:** Section 2.7

1. Optimize read-across settings with Auto_RA_Optimizer v1.0.
2. Perform similarity/read-across calculations with Read-Across v4.1.
3. Generate RASAR descriptors with RASAR-Desc-Calc v3.0.2.
4. Combine derived RA/RASAR descriptors with conventional molecular descriptors.
5. Fit q-RASTR MLR models in QSARINS 2.2.4.

**Final settings recovered from supplied files:**

| Species | Similarity | Close source compounds | Kernel parameter |
|---|---|---:|---|
| Mouse | Gaussian kernel (GK) | 6 | sigma = 0.5 |
| Rat | Laplacian kernel (LK) | 3 | gamma = 0.75 |

**Repository:**

- Derived RASAR descriptors: `data/processed/mouse_rasar_descriptors.csv`, `rat_rasar_descriptors.csv`
- Final q-RASTR modeling tables: `data/processed/mouse_qrastr_modeling.csv`, `rat_qrastr_modeling.csv`
- QSARINS files: `models/qsarins/mouse q-RASTR.qsi`, `rat q-RASTR.qsi`
- Full specifications: `models/specifications/models.json`

The proprietary/restricted executables are not redistributed. See `docs/REPRODUCIBILITY.md`.

## 5. Machine-learning models

**Manuscript:** Section 2.8

Models implemented in Orange3:

- Random forest (RF)
- Neural network (NN)
- k-nearest neighbors (kNN)
- Gradient boosting (GB)
- XGBoost (XGB)
- Stochastic gradient descent (SGD)
- Support vector machine/regression (SVM/SVR)

The ML inputs are based on the descriptors selected in the optimal species-specific QSTR model. Hyperparameters reported in Table S6 are released in `data/processed/ml_hyperparameters.csv`.

The original Orange workflows are now released as `models/orange/Mouse_QSTR-ML.ows` and `models/orange/Rat_QSTR-ML.ows`. Their GUI topology and literal learner settings can be inspected without Orange using `models/orange/workflow_settings_extracted.json/csv` and `scripts/audit_orange_workflows.py`.

The revised `.ows` files now match Table S6 for NN neurons (2000), replicable training (`True`/Enabled) and SVM tolerance (0.01). The current Rat saved context contains the final `F06[C-N]` descriptor. Historical context strings, including an older `F01[C-N]` entry, may remain embedded in widget history and are reported as provenance only. The exact Orange3 package/add-on version remains incompletely documented; see `docs/ORANGE_WORKFLOW_AUDIT.md`.

## 6. Interspecies QSTR/iQTTR

**Manuscript:** iQTTR section

- 27 shared chemicals.
- 20 training + 7 test compounds.
- Both mouse→rat and rat→mouse linear models.

**Repository:**

- `models/qsarins/mouse-rat iQTTR.qsi`
- `models/qsarins/rat-mouse iQTTR.qsi`
- `data/processed/mouse_to_rat_iqttr_modeling.csv`
- `data/processed/rat_to_mouse_iqttr_modeling.csv`
- `data/processed/*_iqttr_external.csv`
- `results/*_iqttr_PRI.csv`

## 7. True-external prediction and PRI

The optimized models were applied to previously untested PAE/BP-related FCOCs, followed by a prediction reliability index (PRI) assessment.

**Repository:**

- Mouse QSTR: `results/mouse_external_PRI.csv`
- Rat QSTR: `results/rat_external_PRI.csv`
- iQTTR: `results/mouse_to_rat_iqttr_PRI.csv`, `rat_to_mouse_iqttr_PRI.csv`
- Top-ranked predictions: `results/mouse_top10_predicted.csv`, `rat_top10_predicted.csv`

## 8. Mechanistic interpretation

Descriptor definitions and mechanistic interpretation remain in the supplied manuscript and source model workbooks. Final descriptor names and coefficients are machine-readable in `models/specifications/models.json`.
