#!/bin/bash

subjectID=${1-$(pwd | grep -o "34P[19][0-9][0-9][0-9]")}
subjectDir=$CENC_MRI_DATA/$subjectID

#
# Create fmri Tarball
#

cenc_fmri_gather.py $subjectDir

#
# antsCT
#

cd $subjectDir
antsCtDir=${subjectDir}/antsCT/input

if [ ! -f ${antsCtDir} ]; then

    mkdir -p ${antsCtDir}
    cd ${antsCtDir}

    ln -sf ../../reorient/t1w.nii.gz .

    cenc_antsct.sh $subjectID

fi

#
# FreeSurfer
#

freesurferDir=${subjectDir}/freesurfer/input

if [ ! -f ${freesurferDir} ]; then

    mkdir -p ${freesurferDir}
    cd ${freesurferDir}

    ln -sf ../../reorient/t1w.nii.gz     .
    ln -sf ../../reorient/t2tse.nii.gz   .
    ln -sf ../../reorient/t2flair.nii.gz .

    cenc_freesurfer.sh $subjectID
fi

#
# Register 
#

if false; then

    registerDir=${subjectDir}/register/


    if [ ! -f $registerDir ]; then
        
        mkdir -p ${registerDir}/{mt,swi,t1w,t2flair,t2tse}/input
        cd $registerDir

        ln -sf ../reorient/t1w.nii.gz     	     ${registerDir}/mt/input
        ln -sf ../reorient/mt0.nii.gz     	     ${registerDir}/mt/input
        ln -sf ../reorient/mt1.nii.gz     	     ${registerDir}/mt/input

        ln -sf ../reorient/t1w.nii.gz                ${registerDir}/swi/input
        ln -sf ../reorient/swi_magnitude.nii.gz      ${registerDir}/swi/input
        ln -sf ../reorient/swi_phase.nii.gz          ${registerDir}/swi/input
        ln -sf ../reorient/swi.nii.gz                ${registerDir}/swi/input

        ln -sf ../reorient/t1w.nii.gz     	     ${registerDir}/t1w/input

        ln -sf ../reorient/t1w.nii.gz     	     ${registerDir}/t2tse/input
        ln -sf ../reorient/t2tse.nii.gz   	     ${registerDir}/t2tse/input

        ln -sf ../reorient/t1w.nii.gz     	     ${registerDir}/t2flair/input
        ln -sf ../reorient/t2flair.nii.gz 	     ${registerDir}/t2flair/input    

    fi  

fi
