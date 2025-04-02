import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path

# === CONFIG ===
input_dir = Path("/Volumes/SM/RP1B Coding Portfolio/UMAP and PCA/feature_groups_split")
filtered_dir = Path("/Volumes/SM/RP1B Coding Portfolio/UMAP and PCA/positive_controls_only")
output_dir = Path("/Volumes/SM/RP1B Coding Portfolio/UMAP and PCA/pca_positive_controls")

filtered_dir.mkdir(parents=True, exist_ok=True)
output_dir.mkdir(parents=True, exist_ok=True)

feature_groups = ["shape_and_size", "intensity_and_texture", "ser"]
positive_controls = ["M0", "M1", "M2"]

# === STEP 1: Extract & Save Positive Controls ===
for group in feature_groups:
    df = pd.read_csv(input_dir / f"{group}.csv")
    sample_col = "Sample Type" if "Sample Type" in df.columns else "sample_type"

    df[sample_col] = df[sample_col].astype(str).str.strip()
    df_pos = df[df[sample_col].isin(positive_controls)].copy()
    out_file = filtered_dir / f"{group}_positive_controls.csv"
    df_pos.to_csv(out_file, index=False)
    print(f" Saved positive controls for {group} → {out_file}")

# === STEP 2: Run PCA on Filtered Files ===
for group in feature_groups:
    print(f"\n Running PCA for positive controls: {group}")

    df = pd.read_csv(filtered_dir / f"{group}_positive_controls.csv")
    sample_col = "Sample Type" if "Sample Type" in df.columns else "sample_type"

    # Separate features and labels
    X = df.drop(columns=[sample_col])
    y = df[sample_col].astype(str).str.strip()

    # Run PCA
    pca = PCA(n_components=10)
    components = pca.fit_transform(X)

    # PCA DataFrame
    pc_cols = [f"PC{i+1}" for i in range(10)]
    pca_df = pd.DataFrame(components, columns=pc_cols)
    pca_df[sample_col] = y

    # Save transformed data
    pca_df.to_csv(output_dir / f"{group}_pca_data.csv", index=False)

    # Save explained variance
    variance_df = pd.DataFrame({
        "Principal Component": pc_cols,
        "Explained Variance Ratio": pca.explained_variance_ratio_
    })
    variance_df.to_csv(output_dir / f"{group}_explained_variance.csv", index=False)

    # Plot top 3 PCs
    top3_idx = sorted(range(10), key=lambda i: pca.explained_variance_ratio_[i], reverse=True)[:3]
    top3_pcs = [pc_cols[i] for i in top3_idx]

    # Fixed color mapping for M0, M1, M2
    palette = {
        "M0": "blue",
        "M1": "red",
        "M2": "green"
    }

    pdf_path = output_dir / f"{group}_top3_pca_plots.pdf"
    with PdfPages(pdf_path) as pdf:
        for i in range(3):
            for j in range(i + 1, 3):
                x_pc, y_pc = top3_pcs[i], top3_pcs[j]

                plt.figure(figsize=(12, 9))
                sns.scatterplot(
                    x=x_pc, y=y_pc,
                    hue=sample_col,
                    palette=palette,
                    data=pca_df,
                    alpha=0.8
                )
                plt.xlabel(f"{x_pc} ({pca.explained_variance_ratio_[pc_cols.index(x_pc)] * 100:.2f}%)")
                plt.ylabel(f"{y_pc} ({pca.explained_variance_ratio_[pc_cols.index(y_pc)] * 100:.2f}%)")
                plt.title(f"PCA: {x_pc} vs {y_pc} ({group})")
                plt.legend(title="Sample Type", bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.tight_layout()
                pdf.savefig()
                plt.close()

    print(f" PCA for {group} done. Saved plots + data to {output_dir}")

