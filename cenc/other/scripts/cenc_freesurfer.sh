#!/usr/bin/env bash

subjectID=${1-$(pwd | grep -o "34P[19][0-9][0-9][0-9]")}
subjectDir=${CENC_MRI_DATA}/$subjectID

echo
echo "cenc_freesurfer.sh " $subjectID
echo

freesurferInputDir=${subjectDir}/freesurfer/input

cd $freesurferInputDir
ls -l 
echo

nohup recon-all -sd ${CENC_SUBJECTS_DIR} -subjid $subjectID -all \
    -i  t1w.nii.gz        \
    -T2 t2tse.nii.gz      \
    -FLAIR t2flair.nii.gz \
    -qcache               \
    -measure thickness    \
    -measure curv         \
    -measure sulc         \
    -measure area         \
    -measure jacobian_white > nohup.reconall.log  &