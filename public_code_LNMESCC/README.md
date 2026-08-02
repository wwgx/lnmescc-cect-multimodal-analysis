# LNMESCC CE-CT Multimodal Analysis

Code accompanying: *Progressive Multimodal Fusion of Contrast-Enhanced CT for Preoperative Prediction of Lymph Node Metastasis in Thoracic Esophageal Squamous Cell Carcinoma: A Single-Center Retrospective Development and Internal Validation Study*.

## Scope

This repository contains the final analysis code used for the manuscript:

- training-only selection of the 2-, 3-, and 4-mm peritumoral margins;
- construction of Rad-score, DL-score, and Hab-score;
- progressive Models 1-4 and internal-test evaluation;
- ROC, calibration, decision-curve, SHAP, reclassification, fixed-threshold, and sensitivity analyses;
- habitat-number diagnostics for Supplementary Figure S1.

The repository deliberately excludes individual-level clinical data, imaging data, habitat feature matrices, sample identifiers, and patient-level prediction files.

## Requirements

- Python 3.9.25
- The packages listed in `requirements.txt`
- Graphviz installed on the operating system only if the optional workflow-figure cell is restored or run separately.

Create an environment and install the dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

Open `notebooks/01_final_analysis.ipynb` and run all cells from top to bottom. Results are written to `results/`, which is ignored by Git because some outputs can contain patient-level information.

## Data access

The source datasets contain clinical and imaging information and are not included. The required directory layout and column conventions are described in `data/README.md`. Approved users may either place authorized data under `data/` or set the `LNMESCC_DATA_DIR` environment variable to the authorized data directory.

## Included non-identifying artifacts

- `model_artifacts/`: final score coefficients and Model 4 coefficients used in Supplementary Tables S2A-S2B.
- `figures/`: aggregate BIC and silhouette metrics plus the script for Supplementary Figure S1.
- `aggregate_results/`: non-identifying tables used to cross-check the reported results.

## Important interpretation note

The manuscript reports an internally tested, single-center model. The code and locked coefficients do not establish clinical readiness. Individual-level data remain subject to ethics approval and institutional authorization.

## Before Public Release

1. Run the notebook once in a clean environment with the authorized data.
2. Confirm that every reported value and figure matches the submitted manuscript.
3. Review `git status` and confirm that no files under `data/` or patient-level prediction files are staged.
4. Add a license approved by the authors and institution before making the repository public.
5. Create a tagged release and archive it through Zenodo or another DOI service; add the DOI to the manuscript's data-and-code availability statement.
