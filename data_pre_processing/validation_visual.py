import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your silhouette summary file
df = pd.read_csv("/Volumes/SM/RP1B Coding Portfolio/pca_umap_validation_summary.csv")

# Only keep rows that involve group comparisons
df_filtered = df[df['File Name'].str.contains('_vs_')].copy()

# Label for plot
def extract_feature_set_and_group(filename):
    parts = filename.replace("_pca_components.csv", "").replace("_umap_2d.csv", "").split("_vs_")
    feature = parts[0].replace("_", " ").title()
    group = parts[1].upper()
    return f"{feature} – {group}"

df_filtered['Label'] = df_filtered['File Name'].apply(extract_feature_set_and_group)

# Extract treatment
def get_treatment(group_str):
    for name in ['SIS', 'UBM', 'Cardiac']:
        if name.upper() in group_str.upper():
            return name
    return 'Unknown'

df_filtered['Treatment'] = df_filtered['Groups Compared'].apply(get_treatment)

# Split PCA and UMAP into two separate DataFrames
df_pca = df_filtered[df_filtered['File Name'].str.contains('pca')]
df_umap = df_filtered[df_filtered['File Name'].str.contains('umap')]

# --- Plot ---
fig, axes = plt.subplots(nrows=2, figsize=(14, 10), sharex=True)

# PCA plot
sns.barplot(data=df_pca, x='Label', y='Silhouette Score', hue='Treatment', palette='Set2', ax=axes[0])
axes[0].set_title("Silhouette Scores by Feature Set and ECM Treatment (PCA)")
axes[0].axhline(0.5, ls='--', color='red')
axes[0].set_ylabel("Silhouette Score")
axes[0].legend(title='ECM Treatment')

# UMAP plot
sns.barplot(data=df_umap, x='Label', y='Silhouette Score', hue='Treatment', palette='Set2', ax=axes[1])
axes[1].set_title("Silhouette Scores by Feature Set and ECM Treatment (UMAP)")
axes[1].axhline(0.5, ls='--', color='red')
axes[1].set_ylabel("Silhouette Score")
axes[1].set_xlabel("Feature Set – Treatment Group")
axes[1].legend(title='ECM Treatment')

# Rotate x-axis labels on the bottom plot only
plt.setp(axes[1].get_xticklabels(), rotation=45, ha='right')

plt.tight_layout()
plt.show()
