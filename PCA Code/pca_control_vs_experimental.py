import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path

# === CONFIG ===
input_controls = Path("/Volumes/SM/RP1B Coding Portfolio/UMAP and PCA/positive_controls_only")
input_experimentals = Path("/Volumes/SM/RP1B Coding Portfolio/UMAP and PCA/experimental_samples")
output_base = Path("/Volumes/SM/RP1B Coding Portfolio/UMAP and PCA/pca_controls_vs_experimentals")
output_base.mkdir(parents=True, exist_ok=True)

feature_groups = ["shape_and_size", "intensity_and_texture", "ser"]
positive_controls = ["M0", "M1", "M2"]
experimental_samples = ["SIS", "UBM", "Cardiac"]

control_palette = {"M0": "blue", "M1": "red", "M2": "green"}
experimental_colors = {"SIS": "orange", "UBM": "purple", "Cardiac": "brown"}

# === PCA COMPARISON LOOP ===
for group in feature_groups:
    controls_file = input_controls / f"{group}_positive_controls.csv"
    controls_df = pd.read_csv(controls_file)
    label_col = "Sample Type" if "Sample Type" in controls_df.columns else "sample_type"
    controls_df[label_col] = controls_df[label_col].astype(str).str.strip()

    for exp in experimental_samples:
        exp_file = input_experimentals / f"{group}_{exp}.csv"
        if not exp_file.exists():
            print(f" Skipping missing file: {exp_file}")
            continue

        # Load and clean experimental data
        experimental_df = pd.read_csv(exp_file)
        experimental_df[label_col] = experimental_df[label_col].astype(str).str.strip()

        # Combine controls + one experimental group
        combined_df = pd.concat([controls_df, experimental_df], ignore_index=True)
        sample_types = combined_df[label_col].unique()
        print(f"🔍 Running PCA for {group} | Controls vs {exp} | Sample Types: {sample_types}")

        # Prepare input for PCA
        X = combined_df.drop(columns=[label_col]).dropna()
        y = combined_df.loc[X.index, label_col]

        # Run PCA
        pca = PCA(n_components=10)
        components = pca.fit_transform(X)
        pc_cols = [f"PC{i+1}" for i in range(10)]
        pca_df = pd.DataFrame(components, columns=pc_cols)
        pca_df[label_col] = y
        explained_var = pca.explained_variance_ratio_

        # Output paths
        output_dir = output_base / exp
        output_dir.mkdir(parents=True, exist_ok=True)
        base_filename = f"{group}_controls_vs_{exp}"

        # Save PCA data
        pca_df.to_csv(output_dir / f"{base_filename}_pca_components.csv", index=False)
        pd.DataFrame({
            "Principal Component": pc_cols,
            "Explained Variance Ratio": explained_var
        }).to_csv(output_dir / f"{base_filename}_explained_variance.csv", index=False)

        # Top 3 PCs for plotting
        top3_idx = sorted(range(10), key=lambda i: explained_var[i], reverse=True)[:3]
        top3_pcs = [pc_cols[i] for i in top3_idx]

        # Plotting
        pdf_path = output_dir / f"{base_filename}_pca_plots.pdf"
        with PdfPages(pdf_path) as pdf:
            for i in range(3):
                for j in range(i + 1, 3):
                    x_pc, y_pc = top3_pcs[i], top3_pcs[j]
                    plt.figure(figsize=(12, 9))

                    # Plot controls
                    for ctrl in positive_controls:
                        sns.scatterplot(
                            data=pca_df[pca_df[label_col] == ctrl],
                            x=x_pc, y=y_pc,
                            label=ctrl,
                            color=control_palette[ctrl],
                            alpha=0.6
                        )

                    # Plot experimental group
                    sns.scatterplot(
                        data=pca_df[pca_df[label_col] == exp],
                        x=x_pc, y=y_pc,
                        label=exp,
                        color=experimental_colors[exp],
                        alpha=0.9,
                        edgecolor="black",
                        linewidth=0.5
                    )

                    plt.xlabel(f"{x_pc} ({explained_var[pc_cols.index(x_pc)] * 100:.2f}%)")
                    plt.ylabel(f"{y_pc} ({explained_var[pc_cols.index(y_pc)] * 100:.2f}%)")
                    plt.title(f"PCA: {x_pc} vs {y_pc} — {group.replace('_', ' ').title()} | Controls vs {exp}")
                    plt.legend(title="Sample Type", bbox_to_anchor=(1.05, 1), loc="upper left")
                    plt.tight_layout()
                    pdf.savefig()
                    plt.close()

        print(f" Saved PCA results → {pdf_path}")
