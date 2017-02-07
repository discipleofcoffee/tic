#!/bin/bash


subject_id=${1-$PWD}
subject_dir=$(readlink -f ${subject_id} )

topup_results=${subject_dir}/diffusion/topup/results
dti_input=${subject_dir}/diffusion/dti/input
reorient_dir=${subject_dir}/reorient

echo
echo $RADCORE_MRI_DATA
echo $subject_id
echo $subject_dir
echo $dti_input
echo

mkdir -p ${dti_input}
cd ${dti_input}

#
# Copy files
#

# Topup and Eddy must have an even number of slices. Discard last slice.

fslroi ${reorient_dir}/dti.nii.gz ${dti_input}/dti.nii.gz 0 -1 0 -1 0 58 0 -1

cp ${reorient_dir}/dti.bval   $dti_input
cp ${reorient_dir}/dti.bvec   $dti_input

cp ${topup_results}/topup_movpar.txt         ${dti_input}
cp ${CENC_SCRIPTS}/cenc_topup_acqparams.txt  ${dti_input}/acqparams.txt

cp ${topup_results}/topup_fieldcoef.nii.gz  $dti_input

#
# Extract B0 image, calculate mean, and extract brain
#
# Since eddy will work in a non-distorted space we will base the mask on my_hifi_b0.nii.gz 
# (the secondary output from our topup command above). We generate this mask with the commands

fslmaths ${topup_results}/b0_unwarped.nii.gz -Tmean ${dti_input}/b0_unwarped.nii.gz
bet b0_unwarped.nii.gz bet.b0_unwarped -m

# Create index file

create_index.py dti.bval --index 8

#
# Remove unnecessary files
#


