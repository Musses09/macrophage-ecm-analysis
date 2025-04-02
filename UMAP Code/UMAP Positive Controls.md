# UMAP Analysis on Positive Controls

This script performs 2D UMAP (Uniform Manifold Approximation and Projection) on positive control samples (`M0`, `M1`, `M2`) from different biological feature groups. It generates low-dimensional visualizations to highlight patterns or group separation within the controls.

---

## What the Script Does

1. **Loops through a list of feature groups**:  
   - `shape_and_size`  
   - `intensity_and_texture`  
   - `ser`

2. **For each group**:
   - Loads a CSV containing only positive control data
   - Cleans the sample type labels
   - Drops missing values
   - Applies UMAP to reduce the data to 2D
   - Saves the 2D coordinates and sample labels to a CSV
   - Plots the UMAP result as a color-coded scatterplot and saves it to a PDF

---

## File Paths

### Input Directory

Each input file must be named like:
- `shape_and_size_positive_controls.csv`
- `intensity_and_texture_positive_controls.csv`
- `ser_positive_controls.csv`

### Output Directory

For each feature group, the script will output:
- `{group}_umap_2d.csv`: 2D coordinates of samples
- `{group}_umap_2d_plot.pdf`: UMAP scatterplot

---

## Sample Types

Only positive controls are included:
- `M0`
- `M1`
- `M2`

These are colored consistently in plots:
- `M0`: blue  
- `M1`: red  
- `M2`: green

---

## UMAP Parameters

The script uses the following UMAP settings:
- `n_components=2`: 2D projection
- `n_neighbors=10`: local neighborhood size
- `min_dist=0.6`: controls how tightly points are packed
- `random_state=42`: for reproducibility

These parameters balance separation and structure in the resulting 2D space.

---

## Plotting

- UMAP results are plotted using `seaborn.scatterplot`.
- Each sample type is shown in a different color.
- Plot includes a legend and title.
- Output is saved as a high-resolution PDF.

---

## Dependencies

Install the following Python libraries before running:

```bash
pip install pandas matplotlib seaborn umap-learn

