# Hausdorff distance

```bash
python hausdorff.py mask-a.nii.gz mask-b.nii.gz
```

Any non-zero voxel is foreground. Masks must be non-empty, 3D and on the same grid. Distances are between boundary voxels in millimetres; HD95 pools both directed surface distances.
