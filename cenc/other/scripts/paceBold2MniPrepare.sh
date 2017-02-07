#!/bin/bash

#
#  The following script was created following the ANTS example script explain at http://stnava.github.io/fMRIANTs/
#

scriptName=$(basename $0);

inSubjectDir=$(readlink -f ${1-$PWD})
inBoldMniDir=${2-bold2Mni} 

subjectID=$(basename ${inSubjectDir})

echo "Preparing bold2Mni analysis for ${subjectID}"


inputDir=${inSubjectDir}/${inBoldMniDir}/input/
echo $inputDir


antsCtResultsDir=${inSubjectDir}/antsCT/results
featResultsDir=${inSubjectDir}/epireg/results/
echo $featResultsDir

resultsDir=${inSubjectDir}/${inBoldMniDir}/results/


t1TemplateDir=${IMAGEWAKE2_TEMPLATES}/ixi/cerebellum/
mniTemplateDir=${INFINITE_MRI_TEMPLATES}/mni/


prefix=bold2Mni

[ -d ${inputDir} ]   || mkdir -p ${inputDir}

cp  $0 ${inputDir}/${scriptName}.d$( date +"%m%d%y")


#
# Copy fMRI data
#

cp  ${featResultsDir}/bold.nii.gz       ${inputDir}/bold.nii.gz
cp  ${featResultsDir}/norm.bold.nii.gz  ${inputDir}/norm.bold.nii.gz
cp  ${featResultsDir}/bold.par          ${inputDir}/bold.par

#
# Link Native Subject to MNI template
#

t1wPrefix=t1w
antsCT_prefix=antsCT_

cp  ${antsCtResultsDir}/${antsCT_prefix}ExtractedBrain0N4.nii.gz             ${inputDir}/${t1wPrefix}_brain.nii.gz
cp  ${antsCtResultsDir}/${antsCT_prefix}SubjectToTemplate0GenericAffine.mat  ${inputDir}/${t1wPrefix}_native_To_ixi_0GenericAffine.mat
cp  ${antsCtResultsDir}/${antsCT_prefix}SubjectToTemplate1Warp.nii.gz        ${inputDir}/${t1wPrefix}_native_To_ixi_1Warp.nii.gz

cp  ${antsCtResultsDir}/${antsCT_prefix}BrainSegmentationPosteriors2.nii.gz  ${inputDir}/${t1wPrefix}_brain_gm_cortical.nii.gz
cp  ${antsCtResultsDir}/${antsCT_prefix}BrainSegmentationPosteriors4.nii.gz  ${inputDir}/${t1wPrefix}_brain_gm_subcortical.nii.gz
cp  ${antsCtResultsDir}/${antsCT_prefix}BrainSegmentationPosteriors3.nii.gz  ${inputDir}/${t1wPrefix}_brain_wm.nii.gz
cp  ${antsCtResultsDir}/${antsCT_prefix}BrainSegmentationPosteriors1.nii.gz  ${inputDir}/${t1wPrefix}_brain_csf.nii.gz

cp  ${antsCtResultsDir}/${antsCT_prefix}BrainExtractionMask.nii.gz           ${inputDir}/${t1wPrefix}_brain_mask.nii.gz


#
# MNI Template
#

mniPrefix=mni

mniLowResTemplateSource=${mniTemplateDir}/mni_icbm152_t1_tal_nlin_sym_09a_brain_4x4x4.nii.gz
mniHighResTemplateSource=${mniTemplateDir}/mni_icbm152_t1_tal_nlin_sym_09a_brain.nii.gz

mniLowResTemplateLink=${mniPrefix}_LowResTemplate.nii.gz
mniHighResTemplateLink=${mniPrefix}_HighResTemplate.nii.gz

mniGenericAffineSource=${t1TemplateDir}/to_mni/ixi_To_mni_0GenericAffine.mat
mni1WarpSource=${t1TemplateDir}/to_mni/ixi_To_mni_1Warp.nii.gz

cp  ${mniLowResTemplateSource}  ${inputDir}/${mniPrefix}_reference.nii.gz
cp  ${mniGenericAffineSource}   ${inputDir}/
cp  ${mni1WarpSource}           ${inputDir}/






