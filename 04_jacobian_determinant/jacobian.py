#!/usr/bin/env python3
"""Compute det(I + grad(u)) from a displacement field."""

import argparse
import sys

import nibabel as nib
import numpy as np


def jacobian(input_path, output_path):
    field_nii = nib.load(input_path)
    field = field_nii.get_fdata()
    if field.ndim != 4 or field.shape[-1] != 3:
        raise ValueError("field must have shape (X, Y, Z, 3)")
    # First differentiate by voxel index, then convert to world coordinates.
    du_by_index = np.empty(field.shape[:3] + (3, 3))
    for component in range(3):
        derivatives = np.gradient(field[..., component], edge_order=1)
        for axis in range(3):
            du_by_index[..., component, axis] = derivatives[axis]
    du_by_world = du_by_index @ np.linalg.inv(field_nii.affine[:3, :3])
    determinant = np.linalg.det(du_by_world + np.eye(3)).astype(np.float32)
    nib.save(nib.Nifti1Image(determinant, field_nii.affine, field_nii.header), output_path)
    print(f"saved {output_path}")
    print(f"range: {determinant.min():.6g} to {determinant.max():.6g}")
    print(f"non-positive: {100 * np.mean(determinant <= 0):.3f}%")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("field", help="(X,Y,Z,3) displacement field in mm")
    p.add_argument("output")
    a = p.parse_args()
    try:
        jacobian(a.field, a.output)
    except Exception as exc:
        sys.exit(f"error: {exc}")


if __name__ == "__main__":
    main()
