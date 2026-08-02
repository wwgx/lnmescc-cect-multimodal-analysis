# Data Layout

No patient-level data are distributed with this repository.

For an approved reproduction, provide the following files in this directory, or point `LNMESCC_DATA_DIR` to a directory with the same layout:

```text
data/
  Clean_Train_Set.xlsx
  Clean_Val_Set.xlsx
  Rad+DL_Cleaned_Features.xlsx
  Habitat_Raw/
    t_Habitat_1.xlsx ... t_Habitat_4.xlsx
    p2_Habitat_1.xlsx ... p2_Habitat_4.xlsx
    p3_Habitat_1.xlsx ... p3_Habitat_4.xlsx
    p4_Habitat_1.xlsx ... p4_Habitat_4.xlsx
```

The two clinical workbooks must contain `ID` and `Target`. The final progressive models use `c_Tumor_Size` and the clinical T-stage field used in the study dataset. The radiomics/deep-learning workbook must include a patient identifier in its first column, `MaskType`, and the precomputed feature columns. Every habitat workbook must include a patient identifier in its first column.

The published code is not a substitute for the institutional data-access process. Do not add raw DICOM, NIfTI, masks, clinical workbooks, feature matrices, or files containing real patient identifiers to a public repository.
