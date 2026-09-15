# Licensing note

A public *Journal of Cheminformatics* reproducibility repository should carry explicit open licenses for material the authors have the right to license. Because this package includes PubChem-derived values, generated descriptor outputs, third-party project/workflow formats, and outputs from software with different licenses, the authors should confirm rights for each category before publication.

Recommended structure after legal/data-rights review:

- **Repository-authored scripts:** OSI-approved license such as MIT/BSD-3-Clause/Apache-2.0.
- **Original text/data created by the authors:** Creative Commons license such as CC BY 4.0, consistent with journal guidance and upstream data terms.
- **Third-party software/executables:** never redistribute unless the original license explicitly permits it.

## Descriptor software

- **PaDEL-Descriptor 2.18:** its original 2011 publication describes it as free/open-source software. The repository nevertheless does not need to bundle the executable; it releases the generated merged descriptor matrix.
- **alvaDesc:** proprietary/commercial software. No executable, license key, installer, or vendor code is included. Only the authors' generated descriptor values are included; confirm that public redistribution of those output data is compatible with the applicable license/terms.

## Other third-party software

QSARINS and DTC Lab tools are not redistributed. Original `.qsi` and `.ows` project/workflow files are included as research artifacts, not as copies of the corresponding software.

No third-party executables are included in this repository package.
