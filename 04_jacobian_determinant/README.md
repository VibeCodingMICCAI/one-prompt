# Jacobian determinant

```bash
python jacobian.py ddf.nii.gz jacobian.nii.gz
```

Input shape is `(X,Y,Z,3)`; the last axis is displacement in millimetres along world x, y and z. The affine converts voxel indices to world millimetres. The tool computes `det(I + grad(u))`. One means unchanged local volume; non-positive values indicate folding.
