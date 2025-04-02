# UMAP Projection: Positive Controls vs Experimental Samples

This script performs UMAP dimensionality reduction on a merged dataset containing both **positive control samples** and **experimental sample types**. For each experimental sample (`SIS`, `UBM`, `Cardiac`), a UMAP projection is generated against the control group (`M0`, `M1`, `M2`) to visually compare clustering in reduced 2D space.

---



This dataset must include:
- A `sample_type` column identifying which rows are `M0`, `M1`, `M2`, `SIS`, `UBM`, or `Cardiac`.
- Numerical feature columns for UMAP.
- Metadata columns that are excluded during analysis (e.g., Well ID, Row, etc.).

---

## Output

UMAP plots are saved as `.png` files in:


You will get one PNG per experimental sample:
- `umap_projection_SIS.png`
- `umap_projection_UBM.png`
- `umap_projection_Cardiac.png`

Each plot shows:
- The experimental group (`SIS`, `UBM`, or `Cardiac`)
- The positive controls (`M0`, `M1`, `M2`)
- A UMAP 2D scatterplot colored by sample type

---

## What the Script Does

1. **Loads the merged dataset**  
   - Checks that `sample_type` column exists  
   - Displays first few rows and column names

2. **Defines groups**  
   - Positive controls: `M0`, `M1`, `M2`  
   - Experimental samples: `SIS`, `UBM`, `Cardiac`

3. **Prepares feature data**  
   - Drops metadata columns: `Well ID`, `Row`, `Column`, etc.  
   - Selects only rows for positive controls + one experimental type at a time  
   - Drops rows with missing feature values

4. **Runs UMAP**  
   - Parameters:
     - `n_neighbors=5`
     - `min_dist=0.3`
     - `n_components=2`
     - `random_state=42`
   - Reduces feature data to 2D

5. **Plots results**  
   - Uses `seaborn.scatterplot()` for visualization  
   - Colors samples by `sample_type`  
   - Saves a high-res `.png` file for each experimental type

---

## Dependencies

Install these Python libraries before running:

```bash
pip install pandas matplotlib seaborn umap-learn
