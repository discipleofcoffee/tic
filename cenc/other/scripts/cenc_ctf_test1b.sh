#!/bin/bash 

source $IMAGEWAKE2_PATH/imagewake_alias.sh
ixiTemplate="$IMAGEWAKE2_TEMPLATES/ixi/cerebellum/ixiTemplate2_e_T1wFullImage.nii.gz"

if false; then
mri_convert ../../freesurfer/results/mri/nu.mgz  nu.nii.gz
mri_convert ../../freesurfer/results/mri/aparc.a2009s+aseg.mgz  aparc.a2009s+aseg.nii.gz

cp ../../antsCT/01a-t1w_only/TemplateToSubject*Warp.nii.gz .
cp ../../antsCT/01a-t1w_only/SubjectToTemplate*Warp.nii.gz .

cp ../../antsCT/01a-t1w_only/TemplateToSubject*.mat .
cp ../../antsCT/01a-t1w_only/SubjectToTemplate*.mat .

fi

if false; then

echo;echo
cat fiducials_meg_csa_image.csv
echo;echo

echo
echo
csa_to_freeview_rsp fiducials_meg_csa_image.csv | sort -t, -nk5  | tee fiducials_meg_rsp_image.csv
echo
echo

iwCtf.py --image nu.nii.gz --affine_matrix --affine image_To_world.txt

antsApplyTransformsToPoints -d 3 -i fiducials_meg_rsp_image.csv  -o fiducials_meg_rsp_world.csv   -t image_To_world.txt

echo
echo "cat fiducials_meg_rsp_world.csv | tr "," " " | sed 's/nan//'"
cat fiducials_meg_rsp_world.csv | tr "," " " | sed 's/nan//'
echo
echo

ras_to_lps fiducials_meg_rsp_world.csv > fiducials_meg_lps_world.csv

echo
echo "cat fiducials_meg_lps_world.csv | tr "," " " | sed 's/nan//'"
cat fiducials_meg_lps_world.csv | tr "," " " | sed 's/nan//'
echo
echo


iwCreateRoi.py --image  nu.nii.gz --csv fiducials_meg_lps_world.csv --coordinates lps  --world -r 

fslmerge -t fiducials_meg_world_lps.nii.gz 00000*.gz
fslmaths fiducials_meg_world_lps.nii.gz -Tmean -mul 3 fiducials_meg_world_lps.nii.gz

echo;echo "labelstats native_To_ixi_fiducials.nii.gz"

labelstats fiducials_meg_lps_world.nii.gz

echo;echo

# frv nu.nii.gz fiducials_meg_ras_world.nii.gz

fi


#
# Transform to CTF space
#

# from fiducials_meg_lps_world.csv
# x y z t label comment
# -73.6339 -5.45763 -47.2203 0 1
# 4.36611 81.5424 -2.22034 0 2
#  77.3661 -12.4576 -38.2203 0 3

iwCtf.py --image nu.nii.gz                         \
          --lpa    73.6339   5.45763  -47.2203     \
          --nas    -4.36611 -81.5424   -2.22034    \
          --rpa   -77.3661   12.4576  -38.2203     \
          --ctf_scale .1 --ctf_matrix --ctf world_To_ctf.txt

antsApplyTransformsToPoints -d 3 -o fiducials_meg_ctf.csv -i fiducials_meg_lps_world.csv   -t world_To_ctf.txt

cat fiducials_meg_ctf.csv

echo;echo
echo "===================================================="
echo "Transform ROIs from Native Space to Template Space"
echo "===================================================="
echo
echo

antsApplyTransforms -d 3 -i fiducials_meg_lps_world.nii.gz \
                    -r $ixiTemplate \
                    -o native_To_ixi_fiducials.nii.gz  \
                    -t SubjectToTemplate1Warp.nii.gz -t SubjectToTemplate0GenericAffine.mat -v -n MultiLabel


echo;echo "labelstats native_To_ixi_fiducials.nii.gz"
labelstats native_To_ixi_fiducials.nii.gz


echo;echo
echo "===================================================="
echo "Transform Points From Native Space to Template Space"
echo "===================================================="

antsApplyTransformsToPoints -d 3 -i fiducials_meg_lps_world.csv  -o fiducials_meg_template.csv  -t TemplateToSubject1GenericAffine.mat -t TemplateToSubject0Warp.nii.gz

echo;echo "cat fiducials_meg_template.csv"
echo
cat fiducials_meg_template.csv | tr "," " " | sed 's/nan//'
echo
echo

echo "===================================================="
echo "Transform Points from Template Space to Native "
echo "===================================================="

antsApplyTransformsToPoints -d 3 -i fiducials_meg_template.csv -o fiducials_ixi_To_native_lps.csv  -t SubjectToTemplate1Warp.nii.gz -t SubjectToTemplate0GenericAffine.mat 


echo;echo "cat fiducials_ixi_To_native_lps.csv"
echo
cat fiducials_ixi_To_native_lps.csv  | tr "," " " | sed 's/nan//'
echo
echo

echo; echo "fiducials_meg_lps_world.csv"
echo
cat fiducials_meg_lps_world.csv | tr "," " " | sed 's/nan//'
echo
echo


echo "===================================================="
echo "Transform Points from Template Space to CTF Space "
echo "===================================================="

antsApplyTransformsToPoints -d 3 -i fiducials_meg_template.csv -o fiducials_ixi_To_ctf_lps.csv  \
     -t SubjectToTemplate1Warp.nii.gz -t SubjectToTemplate0GenericAffine.mat -t world_To_ctf.txt


echo;echo "cat fiducials_meg_template.csv"
echo
cat fiducials_ixi_To_ctf_lps.csv  | tr "," " " | sed 's/nan//'
echo
echo

echo; echo "cat fiducials_meg_ctf.csv"
echo
cat fiducials_meg_ctf.csv | tr "," " " | sed 's/nan//'
echo
echo
