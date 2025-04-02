import pandas as pd
from pathlib import Path

# === CONFIG ===
input_path = Path("/Volumes/SM/RP1B Coding Portfolio/processed_datasets/normalized_data/merged_dataset_normalized.csv")
output_dir = Path("/Volumes/SM/RP1B Coding Portfolio/UMAP and PCA/feature_groups_split")
output_dir.mkdir(parents=True, exist_ok=True)

# === FEATURE GROUPS ===

shape_and_size = [
    "body_roundness", "CellArea", "cellbody_area", "Cell_Elongation", "cell_full_length",
    "cell_half_width", "Cell_length_by_area", "Cell_width_by_area", "cytoplasm_area",
    "NucleusArea", "Nuc_Elongation", "Nuc_full_length", "Nuc_half_width", "Nuc_Roundness",
    "number_protrusions", "percentProtrusion", "protrusion_extent", "mean_prlength",
    "mean_protrusionarea", "skeleton_area", "skeleton_node_count", "skeletonareapercent",
    "total_protrusionarea", "ringregion_area"
]

intensity_and_texture = [
    "cytointensityAct", "cytointensityTub", "CytoIntensityH", "CytoNonMembraneIntensityAct",
    "CytoNonMembraneIntensityTub", "GaborMax1_Actin", "GaborMin1_Actin", "HarConCellAct",
    "HarConCytoTub", "HarConMembAct", "HarCorrCellAct", "HarCorrCytoTub", "HarCorrMembAct",
    "HarHomCellAct", "HarHomCytoTub", "HarHomMembAct", "HarSVCellAct", "HarSVCytoTub",
    "HarSVMembAct", "logNucbyRingAct", "logNucbyRingTub", "MembranebyCytoOnlyAct",
    "MembranebyCytoOnlyTub", "MembraneIntensityAct", "MembraneIntensityTub", "NucbyCytoArea",
    "NucbyRingAct", "NucbyRingTub", "NucIntensityAct", "NucIntensityTub", "NucIntensityH",
    "NucPlusRingAct", "NucPlusRingTub", "ProtrusionIntensityAct", "ProtrusionIntensityTub",
    "RingbyCytoAct", "RingbyCytoTub", "ringIntensityAct", "ringIntensityTub", "RingIntensityH",
    "WholeCellIntensityAct", "WholeCellIntensityTub", "WholeCellIntensityH"
]

ser_features = [
    f"SER{pattern}{region}" for pattern in [
        "Bright", "Dark", "Edge", "Hole", "Ridge", "Saddle", "Spot", "Valley"
    ] for region in ["CellAct", "CytoTub", "MembAct", "Nuc"]
]

# === Load the merged dataset ===
df = pd.read_csv(input_path)

# Find sample column (handles naming variations)
sample_col = "Sample Type" if "Sample Type" in df.columns else "sample_type"

# Function to filter and export each group
def export_feature_group(name, feature_list):
    selected_cols = [sample_col] + [col for col in feature_list if col in df.columns]
    subset_df = df[selected_cols]
    out_path = output_dir / f"{name}.csv"
    subset_df.to_csv(out_path, index=False)
    print(f" Saved {name} to {out_path}")

# === Export all three feature groups ===
export_feature_group("shape_and_size", shape_and_size)
export_feature_group("intensity_and_texture", intensity_and_texture)
export_feature_group("ser", ser_features)
