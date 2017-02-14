#!/bin/bash

FSLDIR=/aging1/software//fsl5.09/bin

python2 ${TIC_LABELS_PYTHONPATH}/extract.py aseg.nii.gz -x 10 11 12 13 17 18 --out gm.left_subcortical.nii.gz
python2 ${TIC_LABELS_PYTHONPATH}/extract.py aseg.nii.gz -x 49 50 51 52 53 54 --out gm.right_subcortical.nii.gz

python2 ${TIC_LABELS_PYTHONPATH}/extract.py aseg.nii.gz -x 8 47 --out gm.cerebral_cortex.nii.gz
python2 ${TIC_LABELS_PYTHONPATH}/extract.py aseg.nii.gz -x 3 42 --out gm.cerebellum_cortex.nii.gz

python2 ${TIC_LABELS_PYTHONPATH}/extract.py aseg.nii.gz -x 2 41 --out wm.cerebral.nii.gz
python2 ${TIC_LABELS_PYTHONPATH}/extract.py aseg.nii.gz -x 7 46 --out wm.cerebellum.nii.gz

for ii in gm.left_subcortical.nii.gz gm.right_subcortical.nii.gz \
          gm.cerebral_cortex.nii.gz gm.cerebellum_cortex.nii.gz  \
          wm.cerebral.nii.gz wm.cerebellum.nii.gz; do $FSLDIR/fslmaths $ii -bin $ii; done

$FSLDIR/fslmaths gm.left_subcortical.nii.gz -add gm.right_subcortical.nii.gz gm.subcortical.nii.gz

rm brainmask.nii.gz
fslmaths nu.nii.gz -mas mask.nii.gz  ../images/nu_brain.nii.gz
