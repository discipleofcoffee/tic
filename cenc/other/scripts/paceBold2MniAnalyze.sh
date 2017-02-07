#!/bin/bash

#
#  The following script was created following the ANTS example script explain at http://stnava.github.io/fMRIANTs/
#

#in=${1}             # Generic Input File Name
#nVolumes=${2}        # Number of Volumes to process

scriptName=$(basename $0);

fmri=norm.bold.nii.gz

inDir=$(readlink -f ${1-$PWD})
subjectID=$( echo ${inDir}  | grep -o 'inf0[12][0-9][0-9]' )

cp -f  $0 ${inDir}/${scriptName}.d$( date +"%m%d%y")  # Force the copy

# Create Output Directory
#

fmri_basename=norm.bold

outDir="${inDir}/../01-register_${fmri_basename}"

[ -d $outDir ] || mkdir -p ${outDir}

outDir=$(readlink -f ${outDir})

gmLabelThreshold=0.6;
wmLabelThreshold=0.6;
csfLabelThreshold=0.6;

echo
echo "IW>>> >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
echo
echo "funcName:"     $FUNCNAME
echo "date:"         $(date)
echo "user:"         $(whoami)
echo "subjectID:"    ${subjectID}
echo "pwd: "         $(pwd)
echo "inDir:"        ${inDir}
echo "outDir:"       ${outDir}
echo
echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> <<<IW "
echo


#
# Hard link input files to output directory. This allows easy access for additional processing
#

for ii in $( ls ${inDir}); do ln -sf ${inDir}/$ii ${outDir}/$ii; done

#
# Start Analysis
#

cd ${outDir}

echo "Analyzing bold2Mni for ${subjectID}"

ext='.nii.gz'

prefix=bold2Mni_native_To_mni
mean_fmri=${prefix}_mean.${fmri}


avgFmri=${prefix}_avg.nii.gz
fxd=${prefix}_fixed.nii.gz

##
#   T1 Files
#

t1wPrefix=t1w
t1Native=${t1wPrefix}_brain.nii.gz               # Native Brain Image 

t1Gm=${t1wPrefix}_brain_gm.nii.gz               # Native Brain Image 
t1GmCortical=${t1wPrefix}_brain_gm_cortical.nii.gz               # Native Brain Image 
t1GmSubcortical=${t1wPrefix}_brain_gm_subcortical.nii.gz               # Native Brain Image 

# Add Cortical and Subcortical GM structures together
fslmaths ${t1GmCortical} -add ${t1GmSubcortical} ${t1Gm}


t1Wm=${t1wPrefix}_brain_wm.nii.gz               # Native Brain Image 
t1Csf=${t1wPrefix}_brain_csf.nii.gz               # Native Brain Image 
t1Mask=${t1wPrefix}_brain_mask.nii.gz


t1GroupTemplate=${inPrefix}_groupTemplate.nii.gz                         # Group Template Image for Infinite Study
                    
native2GtGenericMat=${t1wPrefix}_native_To_ixi_0GenericAffine.mat 
native2GtWarp=${t1wPrefix}_native_To_ixi_1Warp.nii.gz 

#
# MNI Files
#
mniPrefix=mni
mniReference=${mniPrefix}_reference.nii.gz
gt2MniGenericMat=ixi_To_mni_0GenericAffine.mat
gt2MniWarp=ixi_To_mni_1Warp.nii.gz

echo
echo "#####################################################################################################"
echo ">>>>> Display Information about BOLD fMRI data file"
echo "#####################################################################################################"

echo

echo ${fmri}
echo

fslinfo ${fmri}
echo 


if [ ! -f ${avgFmri} ]; then
echo "#####################################################################################################"
echo ">>>>> Create a target (average) image"
echo "#####################################################################################################"
echo

 antsMotionCorr -d 3 -a ${fmri} -o ${avgFmri}

fi

t1masked_fmri=${prefix}_t1masked.${fmri}
mask_fmri=${prefix}_mask.${fmri}

if [ ! -f ${t1masked_fmri} ] ; then
echo "#####################################################################################################"
echo ">>>>> Mask Bold Image with T1w Mask"
echo "#####################################################################################################"
echo

antsApplyTransforms -d 3 -r ${avgFmri} -i ${t1Mask} -o ${prefix}_bold_${t1Mask} -t identity

fslmaths ${prefix}_bold_${t1Mask} -bin -mul ${fmri} ${t1masked_fmri}

fi




echo "####################################################################################################"
echo ">>>>> Read Header and dump out contents"
echo "####################################################################################################"
echo

#
#  Create a 4D target image for 4D deformable motion correction.    
#  First, parse the header info to find the number of time points.  

nVolumes=`PrintHeader ${t1masked_fmri} | grep Dimens | cut -d ',' -f 4 | cut -d ']' -f 1`
tr=`PrintHeader ${t1masked_fmri} | grep "Voxel Spac" | cut -d ',' -f 4 | cut -d ']' -f 1`

echo "Number of Volumes = " $nVolumes
echo "TR                = " $tr
echo 




if [ ! -f  ${prefix}_avg.nii.gz ]; then
echo "####################################################################################################"
echo ">>>>> Replicate the fixed 3D image nVolumes times to make a new 4D fixed image"
echo "####################################################################################################"
echo 


ImageMath 3 $fxd ReplicateImage ${prefix}_avg.nii.gz $nVolumes $tr 0


fi




if [ ! -f ${prefix}_mask.nii.gz ]; then
echo "####################################################################################################"
echo ">>>>> Collapse the transformations to a displacement field"
echo "####################################################################################################"
echo

#
# Use antsApplyTransforms to combine the displacement field and affine matrix into a single 
# concatenated transformation stored as a displacement field.
#

echo
echo "-- Combine Transform displacement fields from T1 Native space to MNI space ------"
echo

 antsApplyTransforms -d 3 -o [${prefix}_templateDiffCollapsedWarp.nii.gz,1] \
                     -t ${gt2MniWarp}                                  \
                     -t ${gt2MniGenericMat}                            \
                     -t ${native2GtWarp}                               \
                     -t ${native2GtGenericMat}                         \
                     -r $mniReference -v

antsApplyTransforms -d 3 -o ${prefix}_t1w.nii.gz       -r ${mniReference} -i ${t1Native} 	     -t ${prefix}_templateDiffCollapsedWarp.nii.gz
antsApplyTransforms -d 3 -o ${prefix}_gm.nii.gz        -r ${mniReference} -i ${t1Gm}     	     -t ${prefix}_templateDiffCollapsedWarp.nii.gz
antsApplyTransforms -d 3 -o ${prefix}_gmc.nii.gz       -r ${mniReference} -i ${t1GmCortical}     -t ${prefix}_templateDiffCollapsedWarp.nii.gz
antsApplyTransforms -d 3 -o ${prefix}_gmsc.nii.gz      -r ${mniReference} -i ${t1GmSubcortical}  -t ${prefix}_templateDiffCollapsedWarp.nii.gz
antsApplyTransforms -d 3 -o ${prefix}_wm.nii.gz        -r ${mniReference} -i ${t1Wm}     	     -t ${prefix}_templateDiffCollapsedWarp.nii.gz
antsApplyTransforms -d 3 -o ${prefix}_csf.nii.gz       -r ${mniReference} -i ${t1Csf}    	     -t ${prefix}_templateDiffCollapsedWarp.nii.gz
antsApplyTransforms -d 3 -o ${prefix}_mask.t1w.nii.gz  -r ${mniReference} -i ${t1Mask}   	     -t ${prefix}_templateDiffCollapsedWarp.nii.gz

fi


if [ ! -f  ${prefix}_templateDiffCollapsedWarp4D.nii.gz  ]; then
echo
echo "####################################################################################################"
echo ">>>>> Replicate the 3D template and 4D Displacement field"
echo "####################################################################################################"
echo 


cmd="ImageMath 3 ${mniPrefix}_reference4D.nii.gz  ReplicateImage $mniReference  $nVolumes $tr 0"
echo $cmd
$cmd


cmd="ImageMath 3 ${prefix}_templateDiffCollapsedWarp4D.nii.gz ReplicateDisplacement \
 ${prefix}_templateDiffCollapsedWarp.nii.gz $nVolumes $tr 0"

echo $cmd
$cmd

fi




if [ ! -f ${mask_fmri} ]; then
   echo
   echo "####################################################################################################"
   echo ">>>>> Apply all the transformations to the original BOLD data."
   echo "####################################################################################################"
   echo 

#     echo $(ls -l  ${mask_fmri})
#     echo $(ls -l  ${mniPrefix}_reference4D.nii.gz)
#     echo $(ls -l  ${prefix}_templateDiffCollapsedWarp4D.nii.gz)

   antsApplyTransforms -d 4 -o ${prefix}_${fmri}                              \
                       -t ${prefix}_templateDiffCollapsedWarp4D.nii.gz        \
                       -r ${mniPrefix}_reference4D.nii.gz -i ${t1masked_fmri}

   echo $(ls -l  ${prefix}_${fmri})

   fslmaths ${prefix}_${fmri}       -Tmean ${mean_fmri}
   fslmaths ${mean_fmri}            -bin   ${mask_fmri}
      
fi


if [ ! -f ${prefix}_native_To_mni_labels.nii.gz ]; then

   echo "####################################################################################################"
   echo ">>>> Applying transforms to brain labels"
   echo "####################################################################################################"
   echo 


   # Threshold each tissue type to create GM, WM, and CSF tissue mask

   gmLabelNumber=1;
   wmLabelNumber=2;
   csfLabelNumber=3;

   fslmaths ${prefix}_gm.nii.gz   -thr ${gmLabelThreshold}  -bin -mul $gmLabelNumber  ${prefix}_mask.gm.nii.gz 
   fslmaths ${prefix}_gmc.nii.gz  -thr ${gmLabelThreshold}  -bin -mul $gmLabelNumber  ${prefix}_mask.gmc.nii.gz 
   fslmaths ${prefix}_gmsc.nii.gz -thr ${gmLabelThreshold}  -bin -mul $gmLabelNumber  ${prefix}_mask.gmsc.nii.gz 
   fslmaths ${prefix}_wm.nii.gz   -thr ${wmLabelThreshold}  -bin -mul $wmLabelNumber  ${prefix}_mask.wm.nii.gz 
   fslmaths ${prefix}_csf.nii.gz  -thr ${csfLabelThreshold} -bin -mul $csfLabelNumber ${prefix}_mask.csf.nii.gz

   # Combine tissue masks to create a label image.
   fslmaths ${prefix}_mask.gm.nii.gz -add ${prefix}_mask.wm.nii.gz -add \
            ${prefix}_mask.csf.nii.gz -mas ${prefix}_mask.t1w.nii.gz        \
            ${prefix}_labels.nii.gz
      
fi
