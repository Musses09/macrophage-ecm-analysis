# Validation Visualization: Silhouette Score Analysis for PCA and UMAP

This script generates a visual summary of clustering validation scores using the **silhouette score** metric. It compares PCA and UMAP dimensionality reduction across different feature sets and ECM treatment groups.

---

## What It Does

1. **Loads Silhouette Summary Data**
   - Reads from a CSV summary file containing silhouette scores from previously run clustering analyses.
   - File:  
     `/Volumes/SM/RP1B Coding Portfolio/pca_umap_validation_summary.csv`

2. **Filters Group Comparison Rows**
   - Only keeps rows that represent comparisons between experimental groups (i.e., filenames that include `_vs_`).

3. **Extracts Plot Labels**
   - Parses filenames to create meaningful labels in the format:  
     `Feature Set – Treatment Group`  
     Example:  
     `Shape And Size – SIS`

4. **Identifies ECM Treatment Type**
   - Tags each row based on which ECM treatment is involved: `SIS`, `UBM`, or `Cardiac`.

5. **Separates PCA and UMAP Data**
   - Splits the filtered data into two groups:
     - PCA-based clustering results
     - UMAP-based clustering results

6. **Plots Silhouette Scores**
   - Creates two horizontal bar plots:
     - Top: PCA scores by feature set and treatment
     - Bottom: UMAP scores by feature set and treatment
   - A red dashed line is drawn at 0.5 to indicate a common quality threshold for clustering.
   - Color-coded by ECM treatment group for comparison.

---

## Output

- One figure with two stacked bar plots:
  - **PCA Plot:** Silhouette scores for PCA-transformed feature sets
  - **UMAP Plot:** Silhouette scores for UMAP-transformed feature sets
- Each bar represents the quality of clustering for a specific feature set + treatment combo.
- X-axis labels are rotated for readability.

---

## Dependencies

This script uses the following Python libraries:

- `pandas`
- `matplotlib`
- `seaborn`

Install them via pip if needed:

```bash
pip install pandas matplotlib seaborn
