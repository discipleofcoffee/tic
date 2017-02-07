#!/usr/bin/env bash
### Cenc bash shell environment
#
#

# CENC Data directories

export CENC_SUBJECTS_DIR=/cenc/mri/freesurfer
export CENC_MRI_DATA=/cenc/mri/subjects/


# CENC workflows

export CENC_PATH=/Users/bkraft/PycharmProjects/cenc

export CENC_MATLAB=${CENC_PATH}/other/matlab
export CENC_SCRIPTS=${CENC_PATH}/other/scripts

export CENC_CTF_TEMPLATE="$IMAGEWAKE2_TEMPLATES/ixi/cerebellum_isotropic/ixiIsotropic_t_T1wSkullStripped.nii.gz"

export PYTHONPATH=${CENC_PATH}/cenc/:$PYTHONPATH

# CENC Aliases
source ${CENC_PATH}/other/unix/cenc_alias.sh


