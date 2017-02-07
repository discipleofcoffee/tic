#!/bin/bash

source ${IMAGEWAKE2_PATH}/imagewake_alias.sh

#
# Create directory for storing intermediate results
#
 subjectID=${1-$(pwd | grep -o "34P1[0-9][0-9][0-9]")}
 subjectDir=${CENC_MRI_DATA}/$subjectID

 echo
 echo $subjectDir
 echo


 freesurferDir=${subjectDir}/freesurfer
 cleanDir=01-cleanBrainMask

           
 cd $freesurferDir

 [ -L results ] || ln -s  ${CENC_SUBJECTS_DIR}/${subjectID}/ results


 [ -d $cleanDir ] || mkdir $cleanDir

 cd $cleanDir
 cp ${subjectDir}/antsCT/01a-t1w_only/BrainExtractionMask.nii.gz antsCT.mask.auto.nii.gz


#       
#        Copy results from FreeSurfer Stage 1.  This assumes that a link was created to the output directory of freesurfer.
#        

 mri_convert ../results/mri/brainmask.auto.mgz brainmask.auto.nii.gz
 mri_convert ../results/mri/nu.mgz nu.nii.gz

#        
#        Resample antsCT Mask into nu.nii.gz space (i.e. 256x256x256)
#        

 antsApplyTransforms -d 3 -i antsCT.mask.auto.nii.gz -r nu.nii.gz \
    -o resampled.antsCT.mask.auto.nii.gz   -n MultiLabel -t identity
        
#
#        Create FreeSurfer Mask from auto extraction brainmask.auto.nii.gz
#        

fslmaths brainmask.auto.nii.gz -bin freesurfer.mask.auto.nii.gz

#        
#        Create a difference mask
#        

fslmaths resampled.antsCT.mask.auto.nii.gz -mul 2 -sub freesurfer.mask.auto.nii.gz diff.mask.auto.nii.gz

#            
#        If you are interested you can measure the difference of the masks
#        

 labelstats diff.mask.auto.nii.gz
                       
#           -1 = Tissue included in FreeSurfer but not antsCT
#            1 =  Tissue included in both FreeSurfer and antsCT
#            2 =  Tissue excluded by FreeSurfer included antsCT
#                
#        You can display just the mask and the volume with the following cut command
        
cut -d , -f 5,7 diff.mask.auto.csv | tr "," "\t"
            
#                label    volume
#                -1    130752
#                1    1.32227e+06
#                2    3318
 
#       
#        Display mask on original FreeSurfer normalized intensity T1w image.
#        

freeview nu.nii.gz diff.mask.auto.nii.gz:colormap=heat:opacity=0.5 &   