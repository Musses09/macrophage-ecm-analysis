# Import necessary packages
import os
import pandas as pd
import umap
import matplotlib.pyplot as plt
import seaborn as sns

# Define file paths
input_folder = "/Volumes/SM/RP1B Coding Portfolio/step_4_normalized_data"
file_path = os.path.join(input_folder, "merged_dataset_with_sample_type.csv")

# Read CSV and ensure proper encoding
df = pd.read_csv(file_path)

# Display basic info
print("First few rows of the dataset:")
print(df.head())
print("\nColumn names:", df.columns)

# Ensure "sample_type" exists
if "sample_type" not in df.columns:
    raise KeyError("The column 'sample_type' is missing from the dataset!")

# Define positive controls and experimental sample types
positive_controls = ["M0", "M1", "M2"]
experimental_types = ["SIS", "UBM", "Cardiac"]

# Columns to exclude from UMAP
exclude_columns = ["Well ID", "Unique ID", "Row", "Column", "Field", "Object Number (per well)", "sample_type"]
feature_columns = [col for col in df.columns if col not in exclude_columns]

# Create output folder if it doesn't exist
test_run_folder = "/Volumes/SM/RP1B Coding Portfolio/test run"
if not os.path.exists(test_run_folder):
    os.makedirs(test_run_folder)

# Loop through each experimental sample type and create a separate UMAP plot
for exp_type in experimental_types:
    # Filter dataset: Select only positive controls + current experimental type
    subset_df = df[df["sample_type"].isin(positive_controls + [exp_type])]

    # Extract features and labels
    features = subset_df[feature_columns].dropna()  # Handle missing values
    labels = subset_df["sample_type"].astype(str).loc[features.index]  # Keep labels aligned

    # Apply UMAP
    reducer = umap.UMAP(n_neighbors=5, min_dist=0.3, n_components=2, random_state=42)
    embedding = reducer.fit_transform(features)

    # Convert UMAP output to a DataFrame for plotting
    embedding_df = pd.DataFrame(embedding, columns=["UMAP1", "UMAP2"])
    embedding_df["sample_type"] = labels.values  # Assign labels for coloring

    # Plot UMAP results
    plt.figure(figsize=(6, 4))
    sns.scatterplot(
        x="UMAP1", y="UMAP2", hue="sample_type", palette="Set1", data=embedding_df, s=100
    )
    plt.title(f"UMAP Projection: {exp_type} vs. M0, M1, M2", fontsize=16)
    plt.legend(title="Sample Type", loc='center left', bbox_to_anchor=(1, 0.5))

    # Save plot
    png_path = os.path.join(test_run_folder, f"umap_projection_{exp_type}.png")
    plt.savefig(png_path, bbox_inches='tight', dpi=300)
    plt.show()

    print(f"UMAP plot for {exp_type} saved at: {png_path}")
