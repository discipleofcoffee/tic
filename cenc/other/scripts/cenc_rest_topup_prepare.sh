#!/bin/bash


subject_id=${1-$PWD}
subject_dir=$(readlink -f ${subject_id} )
rest_input=${subject_dir}/functional/rest/input
reorient_dir=${subject_dir}/reorient

echo
echo $RADCORE_MRI_DATA
echo $subject_id
echo $subject_dir
echo $rest_input
echo

mkdir -p ${rest_input}

cd ${rest_input}

#
# Copy files
#

cp ${reorient_dir}/rest.nii.gz          $rest_input
cp ${reorient_dir}/rest_topup_ap.nii.gz $rest_input
cp ${reorient_dir}/rest_topup_pa.nii.gz $rest_input

#
# Extract directory
#

fslmerge -t rest_topup.nii.gz  rest_topup_ap.nii.gz rest_topup_pa.nii.gz

