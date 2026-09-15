# FCOCs-AOT

**Reproducibility repository for:** *FCOCs-AOT: An Online Predictor for Assessing the Acute Oral Toxicity of Food-Contact Organic Chemicals (FCOCs) using QSTR, q-RASTR, Machine learning and iQTTR methodologies*

This repository contains the source data, cleaned merged PaDEL+alvaDesc descriptor matrices, processed modeling tables, QSARINS project files, original Orange `.ows` workflows, q-RASTR-derived descriptors, machine-learning settings, interspecies models, external predictions, prioritization results, and verification scripts supporting the FCOCs-AOT manuscript.

The repository layout follows the reproducibility expectations of the *Journal of Cheminformatics* and the organization used by recent computational toxicology / cheminformatics papers that publish data and code through GitHub with an archival release (for example, Zenodo).

## Scientific scope

FCOCs-AOT predicts acute oral toxicity of phthalate ester (PAE)- and bisphenol (BP)-related food-contact organic chemicals in mouse and rat. The study combines:

1. **QSTR/MLR models** built in QSARINS 2.2.4.
2. **q-RASTR models** using optimized read-across settings and RASAR descriptors, followed by MLR modeling in QSARINS.
3. **Machine-learning models** (RF, NN, kNN, gradient boosting, XGBoost, SGD and SVM) implemented in Orange3 from descriptors selected in the best QSTR models.
4. **Mouse–rat and rat–mouse iQTTR models** built in QSARINS.
5. **True-external prediction and prediction-reliability-index (PRI) prioritization** for large sets of previously untested FCOCs.

The modeled endpoint is:

`pLD50 = -log10(LD50 [mol/kg])`

## Repository map

```text
FCOCs-AOT-GitHub/
├── README.md
├── CITATION.cff
├── environment.yml
├── requirements.txt
├── .github/workflows/verify.yml
├── data/
│   ├── source/                 # Original Excel supporting/model workbooks
│   ├── source_csv/             # CSV exports of Tables S1–S9
│   ├── descriptors/            # Cleaned merged PaDEL+alvaDesc descriptor matrices
│   └── processed/              # Analysis-ready modeling and descriptor tables
├── models/
│   ├── qsarins/                # Original .qsi project/model files
│   ├── orange/                 # Original .ows workflows + extracted settings/audit
│   └── specifications/         # Machine-readable equations and settings
├── results/                    # Model statistics, external predictions, PRI, top-ranked compounds
├── scripts/                    # Independent verification, prediction and data-preparation scripts
├── examples/                   # Example descriptor input/output for command-line prediction
├── docs/                       # Workflow, data dictionary, software, checks, reproducibility notes
└── LICENSES/                   # Licensing guidance for repository release
```

## Quick verification

Create an environment and run the independent equation checks:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python scripts/verify_models.py
```

A successful run writes `results/verification_summary.csv` and confirms that the published QSTR/q-RASTR/iQTTR equations reproduce the supplied predictions within rounding tolerance.

To apply any released linear equation to a descriptor CSV, use `scripts/predict.py`; see `examples/`.

For an optional independent OLS refit from the released training subsets:

```bash
python scripts/refit_mlr_models.py
```

## Main data products

| File | Content |
|---|---|
| `data/source/supplementary materials1.xlsx` | Original supporting-information workbook (Tables S1–S9) |
| `data/source_csv/Table_S1.csv` … `Table_S9.csv` | Machine-readable CSV exports of all supporting tables |
| `data/processed/mouse_qstr_modeling.csv` | Mouse QSTR modeling set, split, endpoint and selected descriptors |
| `data/processed/rat_qstr_modeling.csv` | Rat QSTR modeling set, split, endpoint and selected descriptors |
| `data/processed/mouse_qrastr_modeling.csv` | Mouse q-RASTR modeling set with final selected descriptors |
| `data/processed/rat_qrastr_modeling.csv` | Rat q-RASTR modeling set with final selected descriptors |
| `data/processed/mouse_rasar_descriptors.csv` | Mouse RASAR/read-across derived descriptor table |
| `data/processed/rat_rasar_descriptors.csv` | Rat RASAR/read-across derived descriptor table |
| `data/processed/*_iqttr_*.csv` | Mouse↔rat iQTTR modeling and true-external data |
| `data/descriptors/mouse_padel_alvadesc_cleaned.tsv` | User-supplied cleaned merged Mouse PaDEL+alvaDesc descriptor matrix (94 compounds × 4749 columns) |
| `data/descriptors/rat_padel_alvadesc_cleaned.tsv` | User-supplied cleaned merged Rat PaDEL+alvaDesc descriptor matrix (96 compounds × 4783 columns) |
| `data/processed/ml_hyperparameters.csv` | ML hyperparameters reported in Table S6 |
| `models/orange/Mouse_QSTR-ML.ows`, `Rat_QSTR-ML.ows` | Original Orange workflow files supplied by the authors |
| `models/orange/workflow_settings_extracted.*` | Non-executing extraction of saved learner settings |
| `models/orange/workflow_vs_reported_discrepancies.csv` | Reconciliation status between Table S6/final QSTR inputs and the revised saved Orange workflows |
| `models/specifications/models.json` | Equations, coefficients, validation statistics and RA settings |
| `results/*_external_PRI.csv` | External predictions and PRI outputs |

## Core model equations

The exact machine-readable specifications are in `models/specifications/models.json`.

### Mouse QSTR

```text
pLD50 = 3.0833
        - 1.0392 AATS3p
        - 0.0345 F10[C-O]
        + 0.1250 minHBint3
        + 0.0516 P_VSA_charge_10
        - 0.0358 P_VSA_charge_14
        + 0.4676 SM1_Dzm
```

### Rat QSTR

```text
pLD50 = 294.0931
        - 0.6438 AATSC7i
        + 0.1078 CATS2D_08_DL
        - 293.7069 ChiA_X
        + 0.0758 F06[C-N]
        + 0.0668 P_VSA_charge_10
```

The q-RASTR and iQTTR equations are documented in `docs/MODEL_CARD.md` and `models/specifications/models.json`.

## Reproducibility boundary for third-party software

The repository **does not redistribute third-party executables**. Molecular descriptors were generated with PaDEL-Descriptor 2.18 and alvaDesc; the released `data/descriptors/` files are the authors' merged, cleaned descriptor outputs after removal of empty/NA values, not copies of the software. PaDEL-Descriptor is described by its original publication as free/open-source software, whereas alvaDesc is proprietary/commercial software; the exact alvaDesc version still needs to be recorded.

For q-RASTR, intermediate descriptors were generated with Auto_RA_Optimizer v1.0, Read-Across v4.1 and RASAR-Desc-Calc v3.0.2 from the DTC Laboratory software page. At the time this repository package was prepared, the DTC site marked Read-Across v4.1 and RASAR-Desc-Calc v3.0.2 as restricted/licensed downloads. QSARINS is also distributed separately by its authors.

To preserve verifiability without redistributing restricted/proprietary software, this repository releases the cleaned descriptor matrices, exact derived RA/RASAR descriptors, selected model descriptors, equations, parameters, train/test membership, predictions, original `.qsi` files, and original Orange `.ows` workflows. See `docs/REPRODUCIBILITY.md`, `docs/SOFTWARE_AND_VERSIONS.md`, and `docs/ORANGE_WORKFLOW_AUDIT.md`.

**Important for Journal of Cheminformatics submission:** the journal's current Research Article guidance requires third parties to be able to reproduce research without registration/login barriers or incompatible licensing for required software. Authors should therefore resolve the licensing/open-reproduction status of the restricted software steps before submission, or provide an openly licensed reimplementation of those calculations.

## Online predictor

The manuscript reports the FCOCs-AOT web predictor at:

http://atpt-bjut.magicmed.cn/atpt-bjut/index
