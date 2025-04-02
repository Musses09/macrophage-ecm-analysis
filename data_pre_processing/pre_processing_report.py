import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from pathlib import Path
from matplotlib.backends.backend_pdf import PdfPages

# === File Paths ===
# Load and merge all raw CSV files
raw_folder = Path("/Volumes/SM/RP1B Coding Portfolio/raw datasets")
file_pattern = "MacsExpt1_10k_*.csv"
raw_files = list(raw_folder.glob(file_pattern))
print("Found raw files:")
for f in raw_files:
    print(f.name)
raw_df = pd.concat([pd.read_csv(f) for f in raw_files], ignore_index=True)

processed_data_path = Path("/Volumes/SM/RP1B Coding Portfolio/processed_datasets/Final Datasets/merged_dataset_normalized.csv")
processed_df = pd.read_csv(processed_data_path)

feature_group_dir = Path("/Volumes/SM/RP1B Coding Portfolio/UMAP and PCA/feature_groups_split")
output_pdf_path = Path("/Volumes/SM/RP1B Coding Portfolio/Results/preprocessing summary/feature_summary.pdf")

# === Sample Group Definitions ===
positive_controls = ["M0", "M1", "M2"]
experimental = ["Cardiac", "SIS", "UBM"]
all_sample_types = positive_controls + experimental

# === Feature Group Files ===
feature_group_files = {
    "Shape/Size": feature_group_dir / "shape_and_size.csv",
    "Intensity/Texture": feature_group_dir / "intensity_and_texture.csv",
    "SER": feature_group_dir / "ser.csv",
}

# === Count Samples by Group ===
def count_samples(df):
    counts = df["Sample Type"].value_counts().reindex(all_sample_types, fill_value=0)
    return counts.to_frame(name="Sample Count")

raw_counts = count_samples(raw_df)
processed_counts = count_samples(processed_df)

# === Set Up PDF Output ===
pdf = PdfPages(output_pdf_path)

# === Page 1: Sample Count Comparison ===
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(all_sample_types))
width = 0.35
ax.bar(x - width / 2, raw_counts["Sample Count"], width, label="Raw")
ax.bar(x + width / 2, processed_counts["Sample Count"], width, label="Processed")
ax.set_ylabel("Sample Count")
ax.set_title("Sample Size Comparison: Raw vs Processed")
ax.set_xticks(x)
ax.set_xticklabels(all_sample_types, rotation=45)
ax.legend()
plt.tight_layout()
pdf.savefig()
plt.close()

# === Store Top Features ===
top_features_all = {sample_type: [] for sample_type in all_sample_types}

# === PCA and Feature Ranking ===
for group_name, file_path in feature_group_files.items():
    print(f"🔍 Processing feature group: {group_name}")
    group_df = pd.read_csv(file_path)

    for sample_type in all_sample_types:
        subset = group_df[group_df["Sample Type"] == sample_type].copy()
        features = subset.drop(columns=["Sample Type", "Unique ID"], errors='ignore')

        if features.shape[0] < 1:
            print(f" Skipping {sample_type} for {group_name} — no data.")
            continue

        try:
            pca = PCA(n_components=min(len(features.columns), len(features)))
            pca.fit(features)
            loadings = pd.DataFrame(
                pca.components_.T,
                index=features.columns,
                columns=[f"PC{i + 1}" for i in range(pca.n_components_)]
            )
            top10_pc1 = loadings["PC1"].abs().sort_values(ascending=False).head(10)

            for feat in top10_pc1.index:
                top_features_all[sample_type].append((feat, top10_pc1[feat], group_name))

        except Exception as e:
            print(f" PCA failed for {sample_type} in {group_name}: {e}")

# === Create Stacked Bar Charts ===
for sample_type in all_sample_types:
    top_feats = sorted(top_features_all[sample_type], key=lambda x: -x[1])[:10]

    if not top_feats:
        continue

    features, loadings, groups = zip(*top_feats)
    colors = {"Shape/Size": "tab:blue", "Intensity/Texture": "tab:orange", "SER": "tab:green"}
    color_vals = [colors[g] for g in groups]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(features, loadings, color=color_vals)
    ax.set_title(f"Top 10 Features by PCA (PC1) — {sample_type}")
    ax.set_ylabel("Absolute Loading (PC1)")
    ax.set_xticks(np.arange(len(features)))
    ax.set_xticklabels(features, rotation=45, ha='right')
    ax.set_ylim(0, max(loadings) * 1.2)
    legend_labels = [plt.Line2D([0], [0], color=val, lw=4) for val in colors.values()]
    ax.legend(legend_labels, colors.keys(), title="Feature Group")
    plt.tight_layout()
    pdf.savefig()
    plt.close()

# === Create Summary Tables ===
for sample_type in all_sample_types:
    top_feats = sorted(top_features_all[sample_type], key=lambda x: -x[1])[:10]
    if not top_feats:
        continue

    df_table = pd.DataFrame(top_feats, columns=["Feature", "PC1 Loading", "Feature Group"])
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.axis('off')
    table = ax.table(cellText=df_table.values,
                     colLabels=df_table.columns,
                     loc='center',
                     cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    plt.title(f"Top 10 Features — {sample_type}")
    pdf.savefig()
    plt.close()

# === Finish PDF ===
pdf.close()
print(f"\n PDF saved to: {output_pdf_path}")
