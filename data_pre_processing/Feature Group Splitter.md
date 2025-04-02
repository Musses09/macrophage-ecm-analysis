# Feature Group Splitter

This Python script processes a merged, normalized dataset of cellular features and **splits it into three separate CSV files** based on feature types.

## What It Does

The script:
1. **Loads** a single merged dataset from a CSV file.
2. **Organizes features** into three meaningful groups:
   - `shape_and_size`: Measures of cell and nucleus shape, size, elongation, and protrusions.
   - `intensity_and_texture`: Signal intensities and textural patterns from various cell regions.
   - `ser`: Structural pattern features (Spot, Ridge, Edge, etc.) across subcellular compartments.
3. **Exports** each group to its own CSV file.

These split datasets can be used for downstream analysis like PCA, UMAP, or training ML models.

## File Structure

- **Input**:  
  `processed_datasets/normalized_data/merged_dataset_normalized.csv`  
  (This file should already be preprocessed and normalized.)

- **Output**:  
  `UMAP and PCA/feature_groups_split/`  
  Contains:
  - `shape_and_size.csv`
  - `intensity_and_texture.csv`
  - `ser.csv`

##  How to Use It

Make sure the input file exists at the expected location. Then just run the script:

```bash
python split_features.py
