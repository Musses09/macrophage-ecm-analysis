import os
import pandas as pd
import umap
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path

# === CONFIG ===
input_dir = Path("/Volumes/SM/RP1B Coding Portfolio/UMAP and PCA/positive_controls_only")
output_dir = Path("/Volumes/SM/RP1B Coding Portfolio/UMAP and PCA/umap_positive_controls")
output_dir.mkdir(parents=True, exist_ok=True)

feature_groups = ["shape_and_size", "intensity_and_texture", "ser"]
positive_controls = ["M0", "M1", "M2"]

# Color scheme
color_map = {"M0": "blue", "M1": "red", "M2": "green"}

# === RUN UMAP for each group ===
for group in feature_groups:
    print(f"\n Running UMAP for: {group}")

    df = pd.read_csv(input_dir / f"{group}_positive_controls.csv")
    sample_col = "Sample Type" if "Sample Type" in df.columns else "sample_type"
    df[sample_col] = df[sample_col].astype(str).str.strip()
    df = df[df[sample_col].isin(positive_controls)]

    # Split features and labels
    X = df.drop(columns=[sample_col]).dropna()
    y = df.loc[X.index, sample_col]

    # UMAP 2D with adjusted params to increase spacing
    reducer = umap.UMAP(n_components=2, n_neighbors=10, min_dist=0.6, random_state=42)
    embedding = reducer.fit_transform(X)

    # Combine with labels
    umap_df = pd.DataFrame(embedding, columns=["UMAP1", "UMAP2"])
    umap_df[sample_col] = y.values
    umap_df.to_csv(output_dir / f"{group}_umap_2d.csv", index=False)

    # Plot to PDF
    pdf_path = output_dir / f"{group}_umap_2d_plot.pdf"
    with PdfPages(pdf_path) as pdf:
        plt.figure(figsize=(12, 9))  #  Make plot smaller
        sns.scatterplot(
            data=umap_df,
            x="UMAP1", y="UMAP2",
            hue=sample_col,
            palette=color_map,
            s=50,
            alpha=0.85
        )
        plt.title(f"UMAP 2D - {group}")
        plt.legend(title="Sample Type", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        pdf.savefig()
        plt.close()

    print(f" Saved 2D UMAP plot for {group} → {pdf_path}")
