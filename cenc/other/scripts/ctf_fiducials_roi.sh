#!/bin/bash

source $IMAGEWAKE2_PATH/imagewake_alias.sh

inputDir=$PWD
fiducialsDir="${inputDIr}/../01-fiducials"
ctfDir="${inputDIr}/../02-ctf"


if [ ! -d $fiducialsDir ]; then

     mkdir $fiducialsDir
     cd    $fiducialsDir

     cp ${inputDir}pad.t1w.nii.gz .
     cp ${inputDir}fiducials_meg_csa_image.csv .

     echo
     echo "fiducials_meg_csa_image.csv"
     echo
     cat fiducials_meg_csa_image.csv | tr "," " " | sed 's/nan//'

     #
     # Create Affine Transform. This goes from RAS index to RAS World. The matrix affine.ras_to_lps.txt is created.  
     # These should be combined but  I still have questions about this. 
     #

     iwCtf.py --image pad.t1w.nii.gz --affine_matrix --affine affine.image_To_world.txt

     #
     # Transform to RAS Image Coordinates
     #

     echo 
     echo "fiducials_meg_ras_image.csv"
     echo

     csa_to_ras_image fiducials_meg_csa_image.csv | sort -t, -nk5  | tee fiducials_meg_ras_image.csv

     antsApplyTransformsToPoints -d 3 -i fiducials_meg_ras_image.csv -o fiducials_meg_lps_world.csv   -t affine.image_To_world.txt -t affine.ras_to_las_world.txt
     sed 's/,nan//g' fiducials_meg_lps_world.csv

     echo
     echo "fiducials_meg_lps_world.csv"
     echo 
     cat fiducials_meg_lps_world.csv | tr "," " " | sed 's/nan//'

     #
     #
     #

     iwCreateRoi.py --image pad.t1w.nii.gz --csv fiducials_meg_lps_world.csv --world -r

     fslmerge -t fiducials_meg_lps_world.nii.gz  00000*.gz

     fslmaths    fiducials_meg_lps_world_nii.gz -Tmean -mul 3 fiducials_meg_lps_world.nii.gz

     freeview pad.t1w.nii.gz fiducials_meg_lps_world.nii.gz:colormap=jet:opacity=0.5

fi

#
#
#

ctfDir="../02-ctf"

if [ ! -d $ctfDir ]; then 

     mkdir $ctfDir
     cd    $ctfDir

     cut -d , -f 1-5 ../input/rois_meg_ctf.csv           > rois_meg_ctf.csv 
     chmod +w rois_meg_ctf.csv

     ln ../01-fiducials/fiducials_meg_lps_world.csv .
     ln ../input/pad.t1w.nii.gz .


     iwCtf.py --image pad.t1w.nii.gz --affine_matrix --affine affine.image_To_world.txt --in_csv fiducials_meg_lps_world.csv --ctf_matrix --ctf affine.world_to_ctf.txt --ctf_scale 0.1
             
     antsApplyTransformsToPoints -d 3 -i fiducials_meg_lps_world.csv -o fiducials_meg_lps_ctf.csv   -t affine.world_to_ctf.txt

     echo
     echo "fiducials_meg_lps_ctf.csv"
     echo

     cat fiducials_meg_lps_ctf.csv | tr "," " " | sed 's/,nan//g'

     #
     #
     #

     sed 's/,nan//g'  fiducials_meg_lps_ctf.csv >  fids_rois_meg_lps_ctf.csv
     cat rois_meg_ctf.csv | sed -n '1!p' >> fids_rois_meg_lps_ctf.csv
     
     ech
     echo 'fids_rois_meg_lps_ctf.csv'
     echo

     cat fids_rois_meg_lps_ctf.csv

     #
     # Transform from CTF to LPS World
     #


     antsApplyTransformsToPoints -d 3 -i fids_rois_meg_lps_ctf.csv -o fids_rois_meg_lps_world.csv   -t [ affine.world_to_ctf.txt, 1]
     sed -e 's/,nan//g' -e 's/nan//g' fids_rois_meg_lps_world.csv -i

     echo 
     echo 'fids_rois_meg_lps_world.csv'
     echo

     head -10 fids_rois_meg_lps_world.csv

     echo
     echo 'fiducials_meg_lps_world.csv'
     echo

     cat fiducials_meg_lps_world.csv

     #
     # Create ROI Image
     #

     roiImage=head_8_fids_rois_meg_lps_world

     head -8 fids_rois_meg_lps_world.csv > ${roiImage}.csv

     iwCreateRoi.py --image pad.t1w.nii.gz --csv ${roiImage}.csv --world -r

     fslmerge -t ${roiImage}.nii.gz 0*.gz
     fslmaths    ${roiImage}.nii.gz -mul $(fslval ${roiImage}.nii.gz dim4 )  ${roiImage}.nii.gz

 fi