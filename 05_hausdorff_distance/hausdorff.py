#!/usr/bin/env python3
"""Compute symmetric surface Hausdorff distances between two masks."""

import argparse
import sys

import nibabel as nib
import numpy as np
from scipy.ndimage import binary_erosion, distance_transform_edt


def surface(mask):
    return mask & ~binary_erosion(mask, structure=np.ones((3, 3, 3)), border_value=0)


def hausdorff(mask_a_path, mask_b_path):
    nii_a, nii_b = nib.load(mask_a_path), nib.load(mask_b_path)
    a, b = nii_a.get_fdata() != 0, nii_b.get_fdata() != 0
    if a.ndim != 3 or b.ndim != 3:
        raise ValueError("both masks must be 3D")
    if a.shape != b.shape or not np.allclose(nii_a.affine, nii_b.affine, atol=1e-4):
        raise ValueError("masks must have the same shape and affine")
    if not a.any() or not b.any():
        raise ValueError("both masks must contain foreground voxels")
    spacing = nii_a.header.get_zooms()[:3]
    sa, sb = surface(a), surface(b)
    a_to_b = distance_transform_edt(~sb, sampling=spacing)[sa]
    b_to_a = distance_transform_edt(~sa, sampling=spacing)[sb]
    distances = np.concatenate([a_to_b, b_to_a])
    return max(a_to_b.max(), b_to_a.max()), np.percentile(distances, 95)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("mask_a")
    p.add_argument("mask_b")
    a = p.parse_args()
    try:
        hd, hd95 = hausdorff(a.mask_a, a.mask_b)
        print(f"Hausdorff distance: {hd:.6g} mm")
        print(f"95% Hausdorff:      {hd95:.6g} mm")
    except Exception as exc:
        sys.exit(f"error: {exc}")


if __name__ == "__main__":
    main()
