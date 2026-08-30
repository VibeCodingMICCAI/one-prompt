"""Create tiny synthetic, non-clinical NIfTI inputs for all five demos."""

from pathlib import Path

import nibabel as nib
import numpy as np


OUT = Path(__file__).resolve().parent
SHAPE = (48, 56, 40)
SPACING = np.array([1.5, 1.2, 2.0])


def main():
    grid = np.indices(SHAPE, dtype=float)
    centre = (np.array(SHAPE) - 1)[:, None, None, None] / 2
    xyz = (grid - centre) * SPACING[:, None, None, None]
    radius = np.sqrt((xyz**2).sum(axis=0))

    rng = np.random.default_rng(7)
    image = 20 + 90 * np.exp(-(radius / 20) ** 2) + rng.normal(0, 2, SHAPE)
    mask = (radius < 15).astype(np.uint8)
    shifted = (np.sqrt(((xyz - np.array([3, 0, 0])[:, None, None, None]) ** 2).sum(0)) < 15).astype(np.uint8)
    ddf = np.moveaxis(0.05 * xyz, 0, -1).astype(np.float32)
    affine = np.eye(4)
    affine[:3, :3] = np.diag(SPACING)
    affine[:3, 3] = -centre[:, 0, 0, 0] * SPACING

    for name, data in [("image.nii.gz", image.astype(np.float32)), ("mask.nii.gz", mask),
                       ("mask_shifted.nii.gz", shifted), ("ddf.nii.gz", ddf)]:
        nib.save(nib.Nifti1Image(data, affine), OUT / name)
        print(f"wrote {OUT / name}")


if __name__ == "__main__":
    main()
