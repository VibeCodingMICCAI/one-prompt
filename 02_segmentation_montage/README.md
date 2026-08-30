# Segmentation montage

```bash
python montage.py image.nii.gz mask.nii.gz montage.png --slices 16 --columns 4
```

Files must be 3D and on the same grid. Every non-zero label is overlaid; `--alpha` controls transparency.
