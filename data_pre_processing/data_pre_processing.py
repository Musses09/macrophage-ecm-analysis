
import pandas as pd
import numpy as np
from pathlib import Path
import re
from scipy.stats import skew, t
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import shutil

# Define paths
RAW_DATA_DIR = Path("/Volumes/SM/RP1B Coding Portfolio/raw datasets")
PROCESSED_DIR = Path("/Volumes/SM/RP1B Coding Portfolio/processed_datasets")
NORMALIZED_DIR = PROCESSED_DIR / "normalized_data"
BOXPLOT_DIR = PROCESSED_DIR / "boxplots"

# Create directories if they don't exist
for dir_path in [PROCESSED_DIR, NORMALIZED_DIR, BOXPLOT_DIR]:
    dir_path.mkdir(exist_ok=True)

# Get all CSV files (exclude hidden macOS files)
data_files = [f for f in RAW_DATA_DIR.glob("*.csv") if not f.name.startswith('._')]
print(f"Found {len(data_files)} datasets to process")

# Metadata patterns
META_PATTERNS = [
    r'Experiment', r'Well', r'Unique', r'Row', r'Column',
    r'Field', r'Object', r'Plate'
]

# Sample types
SAMPLE_TYPE_MAPPING = {
    'SIS': ['SIS', 'sis'],
    'UBM': ['UBM', 'ubm'],
    'Cardiac': ['Cardiac', 'cardiac'],
    'M0': ['M0', 'm0'],
    'M1': ['M1', 'm1'],
    'M2': ['M2', 'm2']
}

EXCLUDE_NORM_COLS = ["Well ID", "Unique ID", "Row", "Column", "Field",
                     "Object Number (per well)", "Sample Type", "Experiment"]

def get_sample_type_from_filename(filename):
    filename = str(filename).lower()
    for sample_type, patterns in SAMPLE_TYPE_MAPPING.items():
        if any(pattern.lower() in filename for pattern in patterns):
            return sample_type
    return 'Unknown'

def add_sample_type_to_raw_files():
    backup_dir = RAW_DATA_DIR / "original_files_backup"
    backup_dir.mkdir(exist_ok=True)
    for file in data_files:
        backup_path = backup_dir / file.name
        if not backup_path.exists():
            shutil.copy2(file, backup_path)
        df = pd.read_csv(file)
        if 'Sample Type' in df.columns:
            continue
        sample_type = get_sample_type_from_filename(file.name)
        df.insert(0, 'Sample Type', sample_type)
        df.to_csv(file, index=False)
        print(f"Added Sample Type '{sample_type}' to {file.name}")

def clean_column_names(df):
    df.columns = [col.strip() for col in df.columns]
    return df

def get_meta_columns(df):
    meta_cols = [col for col in df.columns if any(re.search(patt, col, re.IGNORECASE) for patt in META_PATTERNS)]
    return meta_cols + ['Sample Type']

def transform_skewed_features(df, feature_cols):
    for col in feature_cols:
        col_data = df[col].replace(0, 1e-5)
        col_skew = skew(col_data.dropna())
        shift = abs(col_data.min()) + 1 if (col_data <= 0).any() else 0
        if abs(col_skew) > 1.0:
            df[col] = np.log1p(col_data + shift)
        elif 0.5 < abs(col_skew) <= 1.0:
            df[col] = np.sqrt(col_data + shift)
    return df

def grubbs_test(data, alpha=0.05):
    data = data.dropna()
    n = len(data)
    if n < 3:
        return [], None, None, None, None
    mean = data.mean()
    std_dev = data.std()
    max_value, min_value = data.max(), data.min()
    G_max = abs(max_value - mean) / std_dev
    G_min = abs(min_value - mean) / std_dev
    G_value = max(G_max, G_min)
    outlier = max_value if G_max > G_min else min_value
    t_value = t.ppf(1 - alpha / (2 * n), n - 2)
    critical_value = ((n - 1) * t_value) / (((n - 2 + t_value ** 2) ** 0.5))
    return [outlier] if G_value > critical_value else [], mean, std_dev, G_value, critical_value

def handle_outliers(df, feature_cols, dataset_name):
    samples_removed = 0
    plt.figure(figsize=(15, len(feature_cols) * 1.5))
    for idx, col in enumerate(feature_cols, 1):
        plt.subplot((len(feature_cols) // 3) + 1, 3, idx)
        sns.boxplot(y=df[col], flierprops=dict(markerfacecolor='red', marker='o'))
        plt.title(col)
    plt.tight_layout()
    boxplot_path = BOXPLOT_DIR / f"{dataset_name}_boxplots.png"
    plt.savefig(boxplot_path)
    plt.close()
    print(f"Boxplot saved at {boxplot_path}")
    df_reset = df.copy()
    for col in feature_cols:
        Q1, Q3 = df[col].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        iqr_outliers = df[(df[col] < lower) | (df[col] > upper)][col]
        grubbs_outliers, *_ = grubbs_test(df[col])
        all_outliers = set(iqr_outliers.tolist() + grubbs_outliers)
        for val in all_outliers:
            outlier_rows = df_reset[df_reset[col] == val]
            if not outlier_rows.empty:
                index = outlier_rows.index[0]
                if index in df_reset.index:
                    if abs(skew(df[col].dropna())) > 1:
                        df_reset.loc[index, col] = np.log1p(val)
                    else:
                        df_reset = df_reset.drop(index)
        samples_removed += len(all_outliers)
    return df_reset, samples_removed

def normalize_and_save(merged_df):
    final_processed_folder = NORMALIZED_DIR
    exclude_columns = EXCLUDE_NORM_COLS + ["sample_type"]
    existing_exclude_columns = [col for col in exclude_columns if col in merged_df.columns]

    numeric_columns = merged_df.select_dtypes(include=['number']).columns
    columns_to_normalize = [col for col in numeric_columns if col not in existing_exclude_columns]
    constant_columns = [col for col in columns_to_normalize if merged_df[col].var() == 0]

    if constant_columns:
        print(f"The following columns have no variance (constant values): {constant_columns}")
        columns_to_normalize = [col for col in columns_to_normalize if col not in constant_columns]

    scaler = StandardScaler()
    merged_df_normalized = merged_df.copy()
    merged_df_normalized[columns_to_normalize] = scaler.fit_transform(merged_df[columns_to_normalize])

    output_file = final_processed_folder / "merged_dataset_normalized.csv"
    merged_df_normalized.to_csv(output_file, index=False)
    print("Normalized dataset saved.")

    # Copy to final destination
    final_destination = Path("/Volumes/SM/RP1B Coding Portfolio/processed_datasets/Final Datasets/merged_dataset_normalized.csv")
    shutil.copy(output_file, final_destination)
    print(f"Copy saved to: {final_destination}")

def preprocess_all():
    add_sample_type_to_raw_files()
    cleaned_dataframes = []
    for file in data_files:
        df = pd.read_csv(file)
        df = clean_column_names(df)
        meta_cols = get_meta_columns(df)
        feature_cols = [col for col in df.columns if col not in meta_cols]

        print(f"Processing {file.name} (Sample Type: {df['Sample Type'].iloc[0]})")
        df[feature_cols] = df[feature_cols].fillna(1e-5).replace(0, 1e-5)
        df = transform_skewed_features(df, feature_cols)
        df_clean, _ = handle_outliers(df, feature_cols, file.stem)
        cleaned_dataframes.append(df_clean)

    merged_df = pd.concat(cleaned_dataframes, ignore_index=True)
    merged_df.to_csv(NORMALIZED_DIR / "merged_dataset_with_sample_type.csv", index=False)
    print(f"Merged dataset saved with {len(merged_df)} rows.")
    normalize_and_save(merged_df)

if __name__ == "__main__":
    preprocess_all()
