#!/bin/bash


subject_id=${1-$PWD}
subject_dir=$(readlink -f ${subject_id} )

topup_results=${subject_dir}/diffusion/topup/results
dki_input=${subject_dir}/diffusion/dki/input
reorient_dir=${subject_dir}/reorient

echo
echo $RADCORE_MRI_DATA
echo $subject_id
echo $subject_dir
echo $dki_input
echo

mkdir -p ${dki_input}
cd ${dki_input}

#
# Copy files
#

# Topup and Eddy must have an even number of slices. Discard last slice.

fslroi ${reorient_dir}/dki.nii.gz ${dki_input}/dki.nii.gz 0 -1 0 -1 0 58 0 -1

cp ${reorient_dir}/dki.bval   $dki_input
cp ${reorient_dir}/dki.bvec   $dki_input

cp ${topup_results}/topup_movpar.txt         ${dki_input}
cp ${CENC_SCRIPTS}/cenc_topup_acqparams.txt  ${dki_input}/acqparams.txt

cp ${topup_results}/topup_fieldcoef.nii.gz  $dki_input

#
# Extract B0 image, calculate mean, and extract brain
#
# Since eddy will work in a non-distorted space we will base the mask on my_hifi_b0.nii.gz 
# (the secondary output from our topup command above). We generate this mask with the commands

fslmaths ${topup_results}/b0_unwarped.nii.gz -Tmean ${dki_input}/b0_unwarped.nii.gz
bet b0_unwarped.nii.gz bet.b0_unwarped -m

# Create index file

create_index.py dki.bval --index 8

#
# Remove unnecessary files
#


