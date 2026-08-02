# Aggregate Manuscript Outputs

This directory contains aggregate tables used to cross-check the manuscript results. These files do not contain patient identifiers or row-level predictions.

Excluded on purpose:

- patient-level prediction CSV files;
- raw clinical workbooks;
- imaging files, masks, and feature matrices;
- any file containing original patient identifiers.

The authoritative way to reproduce these outputs is to run `notebooks/01_final_analysis.ipynb` with approved access to the study data.
