# Dataset Preprocessing Pipeline

This Python script performs preprocessing of raw imaging-derived feature datasets. It automates the workflow of cleaning, transforming, detecting outliers, and normalizing numeric features for further analysis.

---

## What the Script Does

The script processes all `.csv` files found in the raw data folder and performs the following:

1. **Adds Sample Type Metadata**  
   - Detects sample type from filename (e.g., "M1", "UBM", "Cardiac").
   - Adds a `Sample Type` column if it's not already in the file.

2. **Cleans Column Names**  
   - Strips leading/trailing spaces from column headers.

3. **Identifies Metadata Columns**  
   - Columns like `Well`, `Row`, `Field`, etc., are separated out so they aren't transformed or normalized.

4. **Handles Skewed Distributions**  
   - Applies log1p or square root transformations to numeric features based on their skewness.

5. **Detects and Handles Outliers**  
   - Uses IQR (Interquartile Range) and Grubbs' Test to detect outliers.
   - Outliers are either dropped or log-transformed depending on the skew.

6. **Normalizes the Dataset**  
   - Applies `StandardScaler` to numeric features (excluding metadata and constant columns).

7. **Saves Results**  
   - Merged dataset with sample type: `merged_dataset_with_sample_type.csv`
   - Normalized dataset: `merged_dataset_normalized.csv`
   - Boxplots of raw feature distributions before outlier removal.

---

## Input and Output Structure

### Input Directory
