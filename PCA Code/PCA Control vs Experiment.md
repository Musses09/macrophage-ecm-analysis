# PCA Analysis: Positive Controls vs Experimental Samples

This script performs Principal Component Analysis (PCA) to compare positive control samples against experimental samples across several biological feature groups.

## Inputs

- **Control data path:** `/Volumes/SM/RP1B Coding Portfolio/UMAP and PCA/positive_controls_only`
- **Experimental data path:** `/Volumes/SM/RP1B Coding Portfolio/UMAP and PCA/experimental_samples`

Each CSV file is named using the format: `{feature_group}_{sample}.csv`

### Feature Groups

- `shape_and_size`
- `intensity_and_texture`
- `ser`

### Sample Groups

- **Positive Controls:** `M0`, `M1`, `M2`
- **Experimental Samples:** `SIS`, `UBM`, `Cardiac`

### Color Palettes

Used for plotting:
- Controls: `M0` (blue), `M1` (red), `M2` (green)
- Experimentals: `SIS` (orange), `UBM` (purple), `Cardiac` (brown)

## Output

Results are saved under:
