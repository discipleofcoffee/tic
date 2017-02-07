#!/usr/bin/env bash

# CENC bash shell environment. These enviroment variables should be placed in your initial shell script.
#
# export CENC_PATH=/Users/bkraft/PycharmProjects/cenc
# export CENC_DISK=/Volumes/cenc/
#


export CENC_SUBJECTS_DIR=$CENC_DISK/mri/freesurfer
export CENC_MRI_DATA=$CENC_DISK/mri/subjects/

export CENC_MATLAB=${CENC_PATH}/other/matlab
export CENC_SCRIPTS=${CENC_PATH}/other/scripts

export CENC_CTF_TEMPLATE="$IMAGEWAKE2_TEMPLATES/ixi/cerebellum_isotropic/ixiIsotropic_t_T1wSkullStripped.nii.gz"

export PATH=${CENC_PATH}/cenc/:$PATH
export PYTHONPATH=${CENC_PATH}/cenc/:$PYTHONPATH

source ${CENC_PATH}/other/unix/cenc_aliases.sh


