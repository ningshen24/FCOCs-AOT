# Reproducibility statement and boundary

## What can be independently reproduced from this repository

Without using the original GUI software, a third party can:

- reconstruct all released QSTR, q-RASTR and iQTTR linear equations;
- reproduce equation predictions from the released final descriptor values;
- independently refit the MLR coefficients from the released train/test splits;
- inspect the cleaned merged PaDEL+alvaDesc descriptor matrices used as upstream descriptor data;
- inspect the original Orange `.ows` workflows and their saved learner settings;
- inspect the selected descriptors, RA kernel settings, neighbor counts, validation statistics, applicability-domain thresholds and external predictions;
- reproduce the repository-level consistency checks through `scripts/verify_models.py` and `scripts/refit_mlr_models.py`.

## What is not fully open from the supplied archive

The complete *generation* of all molecular/read-across descriptors is not fully self-contained because the study used third-party software that is distributed separately. In particular, the historical Read-Across v4.1 and RASAR-Desc-Calc v3.0.2 entries on the DTC Laboratory page are marked as restricted/licensed downloads.

This repository therefore **does not redistribute** those executables. It instead publishes the generated descriptors and all downstream model inputs.

The same principle applies to QSARINS: `.qsi` files are provided, but the QSARINS executable is not bundled.

## Journal of Cheminformatics compatibility issue

The current *Journal of Cheminformatics* Research Article guidance states that research/software must be entirely reproducible by third parties and that data/software/algorithms needed for reproduction must be accessible without registration/login and under appropriate open licensing; software source code is expected for software articles.

Because the q-RASTR descriptor-generation step depends on restricted third-party programs, the authors should resolve this before submission. Suitable options include:

1. provide an independently implemented, openly licensed script that reproduces the exact RA/RASAR descriptors;
2. obtain/confirm a license status that satisfies the journal's reproduction requirement and document it explicitly; or
3. discuss the dependency with the journal editors before submission and clearly delineate which results are reproducible from openly released intermediate data.

Option 1 provides the strongest reproducibility package.

## Descriptor-generation reproducibility boundary

The repository now includes the authors' two merged, cleaned PaDEL+alvaDesc descriptor matrices. They are downstream **outputs** after merging and removal of empty/NA values, not the untouched raw exports from each descriptor program. This makes the numerical descriptor inputs auditable even when a third party does not have alvaDesc. PaDEL-Descriptor is described by its original publication as free/open source, while alvaDesc is proprietary/commercial and is not redistributed here. The exact alvaDesc version is still missing.

## ML reproducibility boundary

The revised original Orange `.ows` workflows are included, so learner topology and saved settings are auditable. The settings that previously conflicted with Table S6 have been synchronized: both workflows now store NN 2000 neurons, `replicable=True`, and SVM tolerance 0.01, and the current Rat contexts contain the final descriptor `F06[C-N]`.

The `.ows` files still contain local File-widget paths that must be relinked on another computer, and historical widget context can retain older variable strings such as `F01[C-N]`. The non-executing audit reports these historical strings separately so they are not confused with the final input definition. The exact installed Orange3 package/add-on version is still not encoded unambiguously in both workflows; a Rat path hint contains `Orange 3.40.0`, but the repository does not treat a path string as authoritative version metadata.

Accordingly, the repository now supports final-parameter auditing and reuse of the saved workflow graph, while exact bit-for-bit ML reruns still depend on reconstructing the original Orange software environment and relinking the data files. See `docs/ORANGE_WORKFLOW_AUDIT.md`.

## Archival recommendation

After final checks:

1. push this repository to GitHub;
2. connect the repository to Zenodo;
3. create a versioned release corresponding to the submitted/accepted manuscript;
4. cite the Zenodo DOI in the manuscript Data Availability statement and `CITATION.cff`.
