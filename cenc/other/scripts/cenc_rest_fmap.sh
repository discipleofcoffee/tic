#!/bin/bash

subjectID=${1-$(pwd | grep -o "34P[19][0-9][0-9][0-9]")}
subjectDir=$CENC_MRI_DATA/$subjectID

#
# Rest
#
reorientDir=${subjectDir}/reorient
restDir=${subjectDir}/rest/
antsCtDir=${subjectDir}/antsCT/01a-t1w_only

fmapInDir=$restDir/01-fmap/input
fmapOutDir=$(readlink -f  ${fmapInDir}/../01-prepare_fieldmap/ )



if [ ! -f $fmapInDir ]; then
    
    mkdir -p ${fmapInDir}
    cd ${fmapInDir}

    cp -f ${antsCtDir}/BrainExtractionMask.nii.gz     ${fmapInDir}
    cp -f ${reorientDir}/t1w.nii.gz          	      ${fmapInDir}

    fslmaths t1w.nii.gz -mas BrainExtractionMask.nii.gz  t1w_brain.nii.gz

    cp -f ${reorientDir}/fmap_magnitude.nii.gz                 ${fmapInDir}
    cp -f ${reorientDir}/fmap_phase.nii.gz                     ${fmapInDir}

    antsApplyTransforms -d 3 -i BrainExtractionMask.nii.gz -o fmap_magnitude_mask.nii.gz -r fmap_magnitude.nii.gz -t identity

fi

 iwFmap.py  --mask fmap_magnitude_mask.nii.gz --magnitude fmap_magnitude.nii.gz --phase fmap_phase.nii.gz --outdir $fmapOutDir \
            --indir ${fmapInDir} --run

    