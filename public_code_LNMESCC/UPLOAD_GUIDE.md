# Upload Guide

## GitHub desktop route

1. Install GitHub Desktop and sign in to the account that should own the repository.
2. Select **File > Add local repository** and choose this `public_code_LNMESCC` directory.
3. If GitHub Desktop reports that the directory is not a repository, select **Create a repository**. Use a public name such as `lnmescc-cect-multimodal-analysis`.
4. Inspect the changed-file list. Do not commit anything under `data/`, `results/`, or any file containing patient IDs or predictions.
5. Enter the summary `Initial public analysis code release` and select **Commit to main**.
6. Select **Publish repository**, set visibility to **Public**, and publish.
7. On GitHub, create a release tagged `v1.0.0`. Archive that release with Zenodo and add the resulting DOI to the manuscript before submission.

## Command-line route

From this folder, run:

```powershell
git init
git add README.md requirements.txt .gitignore CITATION.cff data model_artifacts figures notebooks
git status
git commit -m "Initial public analysis code release"
git branch -M main
git remote add origin https://github.com/ACCOUNT/lnmescc-cect-multimodal-analysis.git
git push -u origin main
```

Create the empty GitHub repository before running the last two commands. Verify the `git status` output before each commit: it must not contain clinical spreadsheets, imaging data, NIfTI/DICOM files, masks, or patient-level prediction CSVs.
