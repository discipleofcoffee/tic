#!/usr/bin/env bash
### Cenc bash shell environment
#
#

echo

case $HOST in
  flip.medctr.ad.wfubmc.edu)
    export CENC_PATH=/Users/bkraft/PycharmProjects/cenc
    export CENC_DISK=/Volumes/cenc/
    ;;

  aging1a | aging2a)
    export CENC_PATH=/cenc/tic/studies/cenc
    export CENC_DISK=/cenc/
    ;;

  *)
     echo "Unknown HOSTNAME"
esac

#


export CENC_SUBJECTS_DIR=$CENC_DISK/mri/freesurfer
export CENC_MRI_DATA=$CENC_DISK/mri/subjects/

export CENC_MATLAB=${CENC_PATH}/other/matlab
export CENC_SCRIPTS=${CENC_PATH}/other/scripts

export CENC_CTF_TEMPLATE="$IMAGEWAKE2_TEMPLATES/ixi/cerebellum_isotropic/ixiIsotropic_t_T1wSkullStripped.nii.gz"

export PYTHONPATH=${CENC_PATH}/cenc/:$PYTHONPATH

source ${CENC_PATH}/other/unix/cenc_alias.sh


