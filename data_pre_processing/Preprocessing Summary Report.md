# Preprocessing Summary Report

This script generates a detailed PDF summary of the data preprocessing pipeline. It compares raw vs processed sample counts and ranks the top contributing features from each group using PCA (Principal Component Analysis).

The report helps validate preprocessing steps and highlight the most important features by sample type.

---

## What It Does

1. **Loads Raw and Processed Data**
   - Merges multiple raw `.csv` files (matching pattern: `MacsExpt1_10k_*.csv`)
   - Loads the fully processed and normalized dataset
   - Loads each feature group dataset (Shape/Size, Intensity/Texture, SER)

2. **Counts Samples per Sample Type**
   - Compares sample counts across raw and processed datasets
   - Visualized as a grouped bar chart

3. **Performs PCA on Each Feature Group**
   - Runs PCA separately for each feature group and each sample type
   - Identifies top 10 features contributing to the first principal component (PC1)
   - Tracks feature importance using absolute loadings

4. **Visualizes Top Features**
   - Creates stacked bar charts of the top 10 PC1 features for each sample type
   - Groups features by type (color-coded)

5. **Generates Summary Tables**
   - Outputs a clean table of top 10 PC1 features and loadings for each sample type

6. **Exports Everything to a PDF**
   - PDF is saved to:
     ```
     /Volumes/SM/RP1B Coding Portfolio/Results/preprocessing summary/feature_summary.pdf
     ```

---

## Input Files and Structure

### Raw Data
- Location:  
  `/Volumes/SM/RP1B Coding Portfolio/raw datasets/`
- Pattern matched:  
  `MacsExpt1_10k_*.csv`

### Processed Data
- Location:  
  `/Volumes/SM/RP1B Coding Portfolio/processed_datasets/Final Datasets/merged_dataset_normalized.csv`

### Feature Group Files
- Location:  
  `/Volumes/SM/RP1B Coding Portfolio/UMAP and PCA/feature_groups_split/`
- Files used:
  - `shape_and_size.csv`
  - `intensity_and_texture.csv`
  - `ser.csv`

---

## Sample Types Tracked

- Positive controls:  
  `M0`, `M1`, `M2`

- Experimental groups:  
  `Cardiac`, `SIS`, `UBM`

All sample types are processed and visualized individually.

---

## Output

### PDF Report Includes:
- Sample count comparison: Raw vs Processed
- Bar plots showing top PC1 features for each sample type
- Summary tables of top 10 feature loadings per group

Location:  
`/Volumes/SM/RP1B Coding Portfolio/Results/preprocessing summary/feature_summary.pdf`

---

## Dependencies

Required Python libraries:
- `pandas`
- `numpy`
- `matplotlib`
- `sklearn`
- `pathlib`

Install any missing packages with pip:

```bash
pip install pandas numpy matplotlib scikit-learn
