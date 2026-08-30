# 🧠 One Prompt, One Tool

Five deliberately small command-line programs for the **Vibe Coding in Medical Imaging: Responsible LLM-Assisted Programming** tutorial at MICCAI 2026. Each is simple enough to request in one prompt, read in a few minutes, and run immediately.

> **Prompt it. Run it. Understand it.**

## 🚀 Quick start

```bash
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

Then create the example data (about 382 KB) without storing it in Git:

```bash
python examples/generate_examples.py
```

💡 This command creates a small synthetic, non-clinical image, two masks and a displacement field in `examples/`. They work with all five tools and can be deleted and recreated at any time.

## 🧰 Five one-prompt applications

### 1. 🔍 NIfTI inspector

> Write a minimal standalone Python CLI using nibabel and NumPy. Given a NIfTI file, print its shape, data type, voxel spacing, axis orientation, affine, finite-value count, intensity range, mean, standard deviation and percentiles. Handle NaN/Inf and 3D/4D files. Use argparse and clear errors.

```bash
python 01_nifti_inspector/inspect_nifti.py examples/image.nii.gz
```

### 2. 🎨 Image and segmentation montage

> Write a minimal standalone Python CLI using nibabel, NumPy and matplotlib. Given a 3D NIfTI image and same-grid segmentation, save a PNG montage of evenly spaced axial slices with a transparent coloured segmentation overlay and contours. Use robust intensity windowing, argparse and clear validation.

```bash
python 02_segmentation_montage/montage.py examples/image.nii.gz examples/mask.nii.gz montage.png
```

### 3. 📐 Centre-preserving image resampler

> Write a minimal standalone Python CLI using nibabel, NumPy and scipy. Resample a 3D NIfTI to requested voxel spacing and/or image size while preserving the world-space centre. Use linear interpolation for images, nearest-neighbour with a flag for labels, update the affine correctly, and expose a clear argparse interface.

```bash
python 03_image_resampler/resample.py examples/image.nii.gz resampled.nii.gz --spacing 1 1 1
```

### 4. 🌀 Jacobian determinant map

> Write a minimal standalone Python CLI using nibabel and NumPy. Given a 3D displacement field NIfTI shaped (X,Y,Z,3), whose vector components are world-axis displacements in millimetres, compute det(I + grad(u)) with physical voxel spacing and save a NIfTI map. Use argparse, document the convention, and print min/max and the percentage of non-positive determinants.

```bash
python 04_jacobian_determinant/jacobian.py examples/ddf.nii.gz jacobian.nii.gz
```

### 5. 📏 Hausdorff distance

> Write a minimal standalone Python CLI using nibabel, NumPy and scipy. Given two binary 3D NIfTI masks on the same grid, compute the symmetric Hausdorff distance and 95th-percentile Hausdorff distance between their surfaces in millimetres. Use distance transforms, validate grids and non-empty masks, and provide argparse output.

```bash
python 05_hausdorff_distance/hausdorff.py examples/mask.nii.gz examples/mask_shifted.nii.gz
```

Each folder has a short README with additional options and assumptions.

> ⚠️ These are teaching tools, not validated clinical software.
