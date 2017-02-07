#!/usr/bin/env bash

subjectID=${1-$(pwd | grep -o "34P1[0-9][0-9][0-9]")}
subjectDir=${CENC_MRI_DATA}/$subjectID

freesurferInputDir=${subjectDir}/freesurfer/input


cd $freesurferInputDir

nohup recon-all -sd ${CENC_SUBJECTS_DIR} -subjid $subjectID -all \
    -qcache \
    -measure thickness \
    -measure curv \
    -measure sulc \
    -measure area \
    -measure jacobian_white > nohup.reconall.stage3.log  &