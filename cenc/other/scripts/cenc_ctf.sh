#!/bin/bash

source $IMAGEWAKE2_PATH/imagewake_alias.sh

inputDir="$PWD/"
fiducialsDir="${inputDir}/../01b-fiducials"
ctfDir="${inputDir}/../02b-ctf"
registerDir="${inputDir}/../03b-template"


padT1w=pad.t1w.nii.gz

rois_meg_ctf="rois_meg_ctf.csv"
rois_meg_lps="rois_meg_lps.csv"

rois_ctf="rois_ctf.csv"
rois_lps_world="rois_lps_world.csv"
rois_template="rois_template.csv"

fiducials_meg_csa_image=fiducials_meg_csa_image
fiducials_meg_ras_image=fiducials_meg_ras_image
fiducials_meg_lps_world=fiducials_meg_lps_world

fiducials_lps_world="fiducials_lps_world.csv"

fiducials_freeview_ras_image=fiducials_freeview_ras_image
fiducials_freeview_ras_world=fiducials_freeview_ras_world
fiducials_freeview_lps_world=fiducials_freeview_lps_world

affineMatrix_ras_image_to_world=affine_ras_image_to_world.txt
affineMatrix_ras_to_lps=affine_ras_to_lps_world.txt
ctfMatrix=affine_lps_world_to_ctf.txt



if [ ! -d $fiducialsDir ]; then

     mkdir $fiducialsDir
     cd    $fiducialsDir

     cp ${inputDir}${padT1w}                          .
     cp ${inputDir}${fiducials_meg_csa_image}.csv       .
     cp ${inputDir}${fiducials_freeview_ras_image}.csv  .

     #
     #
     #

     echo
     echo "${fiducials_meg_csa_image}.csv"
     echo
      
     cat "${fiducials_meg_csa_image}.csv"

     #
     # Create Affine Transform. This goes from RAS index to RAS World. The matrix affine_ras_to_lps.txt is created.  
     # These should be combined but  I still have questions about this. 
     #

     iwCtf.py --image ${padT1w}  --affine_matrix --affine ${affineMatrix_ras_image_to_world}

     #echo "#"
     #echo "# Transform CSA and Image Coordinates to RAS World Coordinates"
     #echo "#"
     #echo

     csa_to_ras_image ${fiducials_meg_csa_image}.csv | sort -t, -nk5  > ${fiducials_meg_ras_image}.csv

     antsApplyTransformsToPoints -d 3 -i ${fiducials_meg_ras_image}.csv -o ${fiducials_meg_lps_world}.csv   -t ${affineMatrix_ras_image_to_world}  ${affineMatrix_ras_to_lps}
     sed 's/,nan//g' ${fiducials_meg_lps_world}.csv -i

     echo
     echo "${fiducials_meg_lps_world}.csv"
     echo 

     cat ${fiducials_meg_lps_world}.csv 

     #
     # Transform FreeView RAS Image Coordinates to LPS World Coordinates
     #
     
     echo
     echo
     echo 
     echo "${fiducials_freeview_ras_image}.csv"
     echo

     cat "${fiducials_freeview_ras_image}.csv"

     antsApplyTransformsToPoints -d 3 -i "${fiducials_freeview_ras_image}.csv" -o "${fiducials_freeview_lps_world}.csv"   \
	 -t ${affineMatrix_ras_image_to_world}  ${affineMatrix_ras_to_lps}

     sed 's/,nan//g'  "${fiducials_freeview_lps_world}.csv" -i

     echo
     echo "${fiducials_freeview_lps_world}.csv"
     echo 

     cat "${fiducials_freeview_lps_world}.csv"

     #
     #
     #

     iwCreateRoi.py --image $padT1w --csv "${fiducials_meg_lps_world}.csv" --world -r
     iwLabelMerge.sh "${fiducials_meg_lps_world}.nii.gz"  000*.nii.gz
     rm -rf 000*.gz

     iwCreateRoi.py --image $padT1w --csv "${fiducials_freeview_lps_world}.csv" --world -r
     iwLabelMerge.sh "${fiducials_freeview_lps_world}.nii.gz"  000*.nii.gz
     rm -rf 000*.gz

fi

#
#
#

if [ ! -d $ctfDir ]; then 

     mkdir $ctfDir
     cd    $ctfDir
     pwd
     
     cut -d "," -f 1-5 ${inputDir}/${rois_meg_ctf}             >  ${rois_meg_ctf}
     cp ${fiducialsDir}/*.gz                                   .
     cp ${fiducialsDir}/affine*.txt                            .
     cp ${fiducialsDir}/"${fiducials_meg_lps_world}.csv"       .
     cp ${fiducialsDir}/"${fiducials_freeview_lps_world}.csv"  .
     
     #
     # Create Single Tranform List
     #

     cut -d "," -f 1-5 "${fiducials_meg_lps_world}.csv"   >  ${fiducials_lps_world}
     cat "${fiducials_freeview_lps_world}.csv" | sed 1d   >> ${fiducials_lps_world}
     sed -i -e '$a\' ${fiducials_lps_world}

     
     echo
     echo ${fiducials_lps_world}
     echo

     cat ${fiducials_lps_world}
     echo
     echo
     #
     # Create CTF Transform to LPS World coordinates
     #

     iwCtf.py --image ${padT1w} --in_csv "${fiducials_meg_lps_world}.csv" --ctf_matrix --ctf ${ctfMatrix} --ctf_scale 0.1
             
     antsApplyTransformsToPoints -d 3 -i "${fiducials_lps_world}" -o "${rois_ctf}" -t ${ctfMatrix}

     cut -d "," -f 1-5 ${rois_meg_ctf} | sed 1d   >> ${rois_ctf}

     echo
     echo "${rois_ctf}"
     echo

     cat "${rois_ctf}"


     antsApplyTransformsToPoints -d 3 -o "${rois_lps_world}" -i "${rois_ctf}" -t [ ${ctfMatrix}, 1 ]

     echo
     echo "${rois_lps_world}"
     echo

     cat "${rois_lps_world}"


     antsApplyTransformsToPoints -d 3 -i "${rois_meg_ctf}" -o "${rois_meg_lps}" -t [ ${ctfMatrix}, 1 ]

     #
     # Create 
     #

     echo; echo; echo

     iwCreateRoi.py --image $padT1w --csv "${rois_lps_world}" --world -r --verbose
     iwLabelMerge.sh "${rois_lps_world//.csv/.nii.gz}"  000*.nii.gz
     rm -rf 000*.gz
    

 fi



if [ ! -d $templateDir ]; then 

     mkdir $templateDir
     cd    $templateDir
     
     cp ${ctfDir}/*.gz                                         .
     cp ${ctfDir}/affine*.txt                                  .
     cp ${ctfDir}/*.csv                                        .

fi

#
#
# ImageMath 3 inia19_e_T1wFullImage.nii.gz PadImage inia19_e_T1wFullImage.nii.gz 64
#
# antsApplyTransforms -d 3 -i t1w.nii.gz -o native_To_inia_t1w.nii.gz -r inia19_e_T1wFullImage.nii.gz -t  SubjectToTemplate1Warp.nii.gz SubjectToTemplate0GenericAffine.mat -v
#
# antsApplyTransforms -d 3 -i fiducials_freeview_lps_world.nii.gz -o native_To_inia_fiducials_freeview_lps_world.nii.gz -r inia19_e_T1wFullImage.nii.gz 
#                     -t  SubjectToTemplate1Warp.nii.gz Subjecfrv native_To_inia_fiducials_freeview_lps_world.nii.gz native_To_inia_t1w.nii.gz -n MultiLabel
#
#


#antsApplyTransformsToPoints -d 3 -i fiducials_freeview_lps_world.csv -o fiducials_freeview_template_v1a.csv -t  SubjectToTemplate0GenericAffine.mat SubjectToTemplate1Warp.nii.gz;
#antsApplyTransformsToPoints -d 3 -i fiducials_freeview_lps_world.csv -o fiducials_freeview_template_v1b.csv -t  SubjectToTemplate1Warp.nii.gz       SubjectToTemplate0GenericAffine.mat;

#
# 2A is the winner
#

antsApplyTransformsToPoints -d 3 -i fiducials_freeview_lps_world.csv -o fiducials_freeview_template_v2a.csv -t  TemplateToSubject1GenericAffine.mat TemplateToSubject0Warp.nii.gz;

#antsApplyTransformsToPoints -d 3 -i fiducials_freeview_lps_world.csv -o fiducials_freeview_template_v2b.csv -t  TemplateToSubject0Warp.nii.gz       TemplateToSubject1GenericAffine.mat;
#
