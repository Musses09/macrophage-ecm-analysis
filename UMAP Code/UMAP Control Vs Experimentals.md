# UMAP Visualization: Experimental vs Positive Control Groups

This script performs dimensionality reduction using **UMAP** to compare how each experimental ECM treatment group (SIS, UBM, Cardiac) clusters relative to positive controls (M0, M1, M2). It creates individual 2D plots for each comparison and saves them as PNG files.

---

## What It Does

1. **Loads a Preprocessed Dataset**
   - Source: `merged_dataset_with_sample_type.csv`
   - Must include a `sample_type` column with labels like `M0`, `UBM`, `Cardiac`, etc.

2. **Defines Sample Groups**
   - Positive Controls: `M0`, `M1`, `M2`
   - Experimental Groups: `SIS`, `UBM`, `Cardiac`

3. **Prepares Feature Columns**
   - Excludes metadata columns such as:
     - `Well ID`, `Unique ID`, `Row`, `Column`, `Field`, etc.
   - Retains only numerical features for UMAP projection

4. **Runs UMAP for Each Comparison**
   - For each experimental group, filters the dataset to include:
     - That group + all three positive controls
   - Applies UMAP (2D) to reduce dimensionality
   - Generates a scatter plot colored by `sample_type`

5. **Saves the Output**
   - Each plot is saved as a `.png` in the `test run` folder
   - Filenames follow this format:
     ```
     umap_projection_SIS.png
     umap_projection_UBM.png
     umap_projection_Cardiac.png
     ```

---

## UMAP Parameters Used

```python
umap.UMAP(
    n_neighbors=5,
    min_dist=0.3,
    n_components=2,
    random_state=42
)
