#!/usr/bin/env bash

subjectID=${1-$(pwd | grep -o "34P1[0-9][0-9][0-9]")}
subjectDir=${CENC_MRI_DATA}/$subjectID

freesurferDir=${subjectDir}/freesurfer/input

cd $freesurferDir

nohup recon-all -sd ${CENC_SUBJECTS_DIR} -subjid $subjectID -i t1w.nii.gz -T2 t2tse.nii.gz -FLAIR t2flair.nii.gz -autorecon1 > nohup.reconall.stage1.log &
