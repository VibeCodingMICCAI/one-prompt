#!/usr/bin/env python3
"""Resample a 3D NIfTI while keeping its world-space centre fixed."""

import argparse
import sys

import nibabel as nib
import numpy as np
from scipy.ndimage import affine_transform


def resample(input_path, output_path, spacing=None, size=None, labels=False):
    source = nib.load(input_path)
    data = np.asanyarray(source.dataobj)
    if data.ndim != 3:
        raise ValueError("input must be 3D")
    old_size = np.array(data.shape)
    old_spacing = np.array(source.header.get_zooms()[:3])
    if spacing is None and size is None:
        raise ValueError("provide --spacing or --size")
    new_spacing = np.array(spacing, float) if spacing else old_spacing * old_size / np.array(size)
    new_size = np.array(size, int) if size else np.maximum(1, np.rint(old_size * old_spacing / new_spacing)).astype(int)
    if np.any(new_spacing <= 0) or np.any(new_size <= 0):
        raise ValueError("spacing and size values must be positive")

    direction = source.affine[:3, :3] / old_spacing
    new_affine = np.eye(4)
    new_affine[:3, :3] = direction * new_spacing
    old_centre = source.affine @ np.r_[((old_size - 1) / 2), 1]
    new_affine[:3, 3] = old_centre[:3] - new_affine[:3, :3] @ ((new_size - 1) / 2)
    output_to_input = np.linalg.inv(source.affine) @ new_affine
    result = affine_transform(
        data, output_to_input[:3, :3], output_to_input[:3, 3],
        output_shape=tuple(new_size), order=0 if labels else 1, mode="constant", cval=0,
    )
    if labels:
        result = result.astype(data.dtype)
    nib.save(nib.Nifti1Image(result, new_affine, source.header), output_path)
    print(f"saved {output_path}: shape {tuple(new_size)}, spacing {tuple(new_spacing)}")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input")
    p.add_argument("output")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--spacing", nargs=3, type=float, metavar=("SX", "SY", "SZ"))
    group.add_argument("--size", nargs=3, type=int, metavar=("NX", "NY", "NZ"))
    p.add_argument("--labels", action="store_true", help="nearest-neighbour interpolation")
    a = p.parse_args()
    try:
        resample(a.input, a.output, a.spacing, a.size, a.labels)
    except Exception as exc:
        sys.exit(f"error: {exc}")


if __name__ == "__main__":
    main()
