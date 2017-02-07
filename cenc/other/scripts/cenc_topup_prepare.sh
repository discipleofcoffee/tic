#!/bin/bash


subject_id=${1-$PWD}
subject_dir=$(readlink -f ${subject_id} )
topup_input=${subject_dir}/diffusion/topup/input
reorient_dir=${subject_dir}/reorient

echo
echo $RADCORE_MRI_DATA
echo $subject_id
echo $subject_dir
echo $topup_input
echo

mkdir -p ${topup_input}

cd ${topup_input}

#
# Copy files
#

for ii in dki dti; do
    cp ${reorient_dir}/${ii}.nii.gz $topup_input
    cp ${reorient_dir}/${ii}.bval   $topup_input
    extract_b0.py ${ii}.nii.gz  ${ii}.bval
done

cp ${CENC_SCRIPTS}/cenc_topup_acqparams.txt  ${topup_input}/acqparams.txt
cp ${CENC_SCRIPTS}/cenc_topup_b02b0.cnf      ${topup_input}/b02b0.cnf

#
# Extract directory
#

fslmerge -t b0.nii.gz  b0.dki.nii.gz b0.dti.nii.gz

rm -rf  b0.dki.nii.gz  b0.dti.nii.gz dti* dki*


