# Software and versions

| Step | Software | Version recorded in supplied files | Release/reproducibility note |
|---|---|---|---|
| Descriptor calculation | PaDEL-Descriptor | 2.18 | Original publication describes PaDEL-Descriptor as free/open source; software binary is not bundled because the repository only needs to distribute the generated descriptor outputs |
| Descriptor calculation | alvaDesc | **Not recorded in supplied files** | Proprietary/commercial software; exact version must be filled before submission; executable is not redistributed |
| QSTR/q-RASTR/iQTTR MLR | QSARINS | 2.2.4 | Distributed separately by University of Insubria authors |
| RA optimization | Auto_RA_Optimizer | 1.0 | DTC Laboratory software |
| Read-across | Read-Across | 4.1 | DTC site currently identifies this historical release as restricted |
| RASAR descriptor generation | RASAR-Desc-Calc | 3.0.2 | DTC site currently identifies this historical release as restricted |
| Machine learning | Orange3 | **Exact package version not encoded unambiguously in both supplied `.ows` files** | Revised Mouse/Rat workflows are released under `models/orange/` and now match Table S6 for the previously conflicting NN/SVM settings; a Rat historical path hint contains `Orange 3.40.0`, but this is not treated as authoritative version metadata |
| PRI calculation | PRI implementation | **Not unambiguously recorded** | Add exact tool/script/version before submission |

## Descriptor matrix provenance

The repository includes two author-supplied merged descriptor tables after PaDEL+alvaDesc outputs were combined and empty/NA values removed:

- `data/descriptors/mouse_padel_alvadesc_cleaned.tsv` — 94 rows × 4749 columns.
- `data/descriptors/rat_padel_alvadesc_cleaned.tsv` — 96 rows × 4783 columns.

These are cleaned merged matrices, not raw per-software exports. No PaDEL or alvaDesc executable is included.

## URLs / citations

- QSARINS: https://dunant.dista.uninsubria.it/qsar/?page_id=37
- DTC Laboratory software: https://sites.google.com/jadavpuruniversity.in/dtc-lab-software/home
- Orange: https://orangedatamining.com/
- PaDEL-Descriptor publication: Yap CW. *PaDEL-descriptor: an open source software to calculate molecular descriptors and fingerprints.* J Comput Chem. 2011;32(7):1466–1474. DOI: 10.1002/jcc.21707
- alvaDesc: https://www.alvascience.com/alvadesc/

## Missing-version policy

Do not guess missing software versions. A public reproducibility package should record exact versions, operating-system assumptions where relevant, and any extension/add-on versions affecting model behavior. The `.ows` workflow schema/widget-state versions are not a reliable substitute for the exact installed Orange3 package version.
