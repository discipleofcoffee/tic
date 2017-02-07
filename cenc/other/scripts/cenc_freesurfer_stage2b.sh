#!/bin/bash

source ${IMAGEWAKE2_PATH}/imagewake_alias.sh

#
# Create directory for storing intermediate results
#
 subjectID=${1-$(pwd | grep -o "34P1[0-9][0-9][0-9]")}
 subjectDir=${CENC_MRI_DATA}/$subjectID

 echo
 echo $subjectDir
 echo


freesurferDir=${subjectDir}/freesurfer
cleanDir=${freesurferDir}/01-cleanBrainMask

           
cd $cleanDir


fslmaths nu.nii.gz -mas joint.mask.auto.nii.gz brainmask.nii.gz
mri_convert brainmask.nii.gz ../results/mri/brainmask.mgz

mkdir -p ../../antsCT/results
cp brainmask.nii.gz ../../antsCT/results/