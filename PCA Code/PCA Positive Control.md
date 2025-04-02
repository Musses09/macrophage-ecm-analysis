# PCA Analysis of Positive Controls

This script extracts positive control samples (`M0`, `M1`, `M2`) from multiple feature group datasets and performs Principal Component Analysis (PCA) to visualize variance within the controls.

## Overview

The pipeline runs in two main steps:
1. **Filtering**: Extracts only the positive control samples from larger datasets.
2. **PCA**: Runs PCA on each filtered dataset, saves component scores and explained variance, and generates visualizations of the top 3 principal components.

## Directory Structure

- **Input feature data**:  
  `/Volumes/SM/RP1B Coding Portfolio/UMAP and PCA/feature_groups_split/`

- **Filtered controls output**:  
  `/Volumes/SM/RP1B Coding Portfolio/UMAP and PCA/positive_controls_only/`

- **PCA results and plots**:  
  `/Volumes/SM/RP1B Coding Portfolio/UMAP and PCA/pca_positive_controls/`

## Feature Groups Analyzed

- `shape_and_size`
- `intensity_and_texture`
- `ser`

## Sample Types Used

Only positive controls:
- `M0`
- `M1`
- `M2`

## Step-by-Step Breakdown

### 1. Filter Positive Controls

For each feature group:
- Load the corresponding CSV.
- Identify and standardize the sample label column (`Sample Type` or `sample_type`).
- Filter rows where sample type is one of the positive controls.
- Save the filtered dataset to a new file.

### 2. Perform PCA

For each filtered dataset:
- Drop the label column and apply PCA to the remaining features.
- Keep the first 10 principal components.
- Save:
  - PCA component scores to `{group}_pca_data.csv`
  - Explained variance per component to `{group}_explained_variance.csv`
- Identify the top 3 components that explain the most variance.
- Generate 2D scatter plots for each pair of the top 3 PCs (`PC1 vs PC2`, `PC1 vs PC3`, `PC2 vs PC3`).
- Save all plots to a single PDF: `{group}_top3_pca_plots.pdf`

### Plot Styling

- Color scheme:
  - `M0`: Blue
  - `M1`: Red
  - `M2`: Green
- Legends and axes include variance percentages for interpretability.

## Output Files

For each feature group, the following files are generated:
- `*_pca_data.csv`: PCA-transformed component values
- `*_explained_variance.csv`: Variance explained by each principal component
- `*_top3_pca_plots.pdf`: Visualization of top PCs (3 plots per file)

## Dependencies

- `pandas`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `pathlib`

## Notes

- The script handles both possible label column names (`Sample Type` or `sample_type`).
- Missing values are not explicitly handled—ensure input data is pre-cleaned.
- All results are saved in organized subdirectories by feature group.
