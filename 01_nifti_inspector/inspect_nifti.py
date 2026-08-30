#!/usr/bin/env python3
"""Print a compact summary of a NIfTI image."""

import argparse
import sys

import nibabel as nib
import numpy as np


def inspect(path):
    image = nib.load(path)
    data = np.asanyarray(image.dataobj)
    finite = data[np.isfinite(data)]
    zooms = image.header.get_zooms()[: data.ndim]
    print(f"File:         {path}")
    print(f"Shape:        {data.shape}")
    print(f"Data type:    {data.dtype}")
    print(f"Spacing:      {tuple(round(float(x), 6) for x in zooms)}")
    print(f"Orientation:  {''.join(nib.aff2axcodes(image.affine))}")
    print("Affine:")
    print(np.array2string(image.affine, precision=5, suppress_small=True))
    print(f"Finite:       {finite.size}/{data.size}")
    if finite.size:
        p = np.percentile(finite, [1, 25, 50, 75, 99])
        print(f"Range:        {finite.min():.6g} to {finite.max():.6g}")
        print(f"Mean / SD:    {finite.mean():.6g} / {finite.std():.6g}")
        print(f"P1/25/50/75/99: {'  '.join(f'{x:.6g}' for x in p)}")
    else:
        print("Statistics:   no finite values")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="input .nii or .nii.gz")
    args = parser.parse_args()
    try:
        inspect(args.input)
    except Exception as exc:
        sys.exit(f"error: {exc}")


if __name__ == "__main__":
    main()
