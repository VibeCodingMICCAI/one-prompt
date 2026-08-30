# Centre-preserving resampler

```bash
python resample.py image.nii.gz isotropic.nii.gz --spacing 1 1 1
python resample.py mask.nii.gz small-mask.nii.gz --size 32 32 32 --labels
```

Choose output spacing or output size. `--labels` selects nearest-neighbour interpolation. The world-space centre is unchanged.
