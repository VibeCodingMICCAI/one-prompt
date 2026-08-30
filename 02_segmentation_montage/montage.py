#!/usr/bin/env python3
"""Save axial image slices with a segmentation overlay."""

import argparse
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np


def make_montage(image_path, mask_path, output, slices=12, columns=4, alpha=0.35):
    image_nii, mask_nii = nib.load(image_path), nib.load(mask_path)
    image, mask = image_nii.get_fdata(), mask_nii.get_fdata()
    if image.ndim != 3 or mask.ndim != 3:
        raise ValueError("image and segmentation must both be 3D")
    if image.shape != mask.shape or not np.allclose(image_nii.affine, mask_nii.affine, atol=1e-4):
        raise ValueError("image and segmentation must have the same shape and affine")
    if slices < 1 or columns < 1:
        raise ValueError("--slices and --columns must be positive")
    finite = image[np.isfinite(image)]
    if not finite.size:
        raise ValueError("image contains no finite values")
    low, high = np.percentile(finite, [1, 99])
    indices = np.linspace(0, image.shape[2] - 1, min(slices, image.shape[2]), dtype=int)
    rows = int(np.ceil(len(indices) / columns))
    fig, axes = plt.subplots(rows, columns, figsize=(3 * columns, 3 * rows), squeeze=False)
    for ax, z in zip(axes.flat, indices):
        base, seg = np.rot90(image[:, :, z]), np.rot90(mask[:, :, z])
        ax.imshow(base, cmap="gray", vmin=low, vmax=high)
        ax.imshow(np.ma.masked_where(seg <= 0, seg), cmap="autumn", alpha=alpha, interpolation="none")
        if np.any(seg > 0) and np.any(seg <= 0):
            ax.contour(seg > 0, levels=[0.5], colors="cyan", linewidths=0.7)
        ax.set_title(f"z = {z}")
        ax.axis("off")
    for ax in axes.flat[len(indices):]:
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(output, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"saved {output}")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("image")
    p.add_argument("segmentation")
    p.add_argument("output", help="output .png or .jpg")
    p.add_argument("--slices", type=int, default=12)
    p.add_argument("--columns", type=int, default=4)
    p.add_argument("--alpha", type=float, default=0.35)
    a = p.parse_args()
    try:
        make_montage(a.image, a.segmentation, a.output, a.slices, a.columns, a.alpha)
    except Exception as exc:
        sys.exit(f"error: {exc}")


if __name__ == "__main__":
    main()
