#!/bin/bash

subjectID=${1-$(pwd | grep -o "34P[19][0-9][0-9][0-9]")}
subjectDir=$CENC_MRI_DATA/$subjectID

#
# Rest
#

reorientDir=${subjectDir}/reorient
boldDir=${subjectDir}/bold/
fmapDir=$boldDir/01-fmap/results
epiregDir=$boldDir/02-epireg/input
antsCtDir=${subjectDir}/antsCT/01a-t1w_only

if [ ! -f $epiregDir ]; then
    
    mkdir -p ${epiregDir}
    cd ${epiregDir}

    cp -f ${fmapDir}/fmap_magnitude.nii.gz       ${epiregDir}
    cp -f ${fmapDir}/fmap_magnitude_brain.nii.gz ${epiregDir}
    cp -f ${fmapDir}/fmap_radians.nii.gz         ${epiregDir}

    cp -f ${reorientDir}/t1w.nii.gz          	 ${epiregDir}
    N4B -f ${reorientDir}/bold.nii.gz          	 ${epiregDir}

    N4BiasFieldCorrection -d 4 -v -i ${reorientDir}/bold.nii.gz  -o n4.bold.nii.gz 

    cp -f ${antsCtDir}/BrainExtractionMask.nii.gz     ${epiregDir}
    cp -f ${reorientDir}/t1w.nii.gz          	      ${epiregDir}

    fslmaths t1w.nii.gz -mas BrainExtractionMask.nii.gz  t1w_brain.nii.gz

fi  

echo

iwFeatEpiReg.py  --fmap_magnitude fmap_magnitude.nii.gz   \
    		 --fmap_magnitude fmap_magnitude.nii.gz   \
    		 --fmap_radians fmap_radians.nii.gz       \
    		 --t1brain t1w_brain.nii.gz               \
    		 --epi     n4.bold.nii.gz                 \
    		 --indir   ${epiregDir}                   \
    		 --out_dir ${epiregDir}/../01-bbr/        \
    		 --tr 2 --nvolumes 200 --esp 0.51 --fsf_prepare --fsf_diff --qi --display

echo
echo "After you QI Feat inputs for iwFeatEpiReg.py you may" 
echo "run iwFeatEpiReg.py by executing the command "
echo "  "
echo "   iwFeatEpiReg.py --nohup "  
echo





#>> iwFeatEpiReg.py -h
#
#usage: iwEpiReg [-h] [-d] [-v] [--debug] [--no_clean] [--prepare] [--qi]
#                [--qo] [--report] [-r] [--indir INDIR] [--epi EPI]
#                [--t1brain T1BRAIN] [--fmap_radians FMAP_RADIANS]
#                [--fmap_magnitude FMAP_MAGNITUDE]
#                [--fmap_magnitude_brain FMAP_MAGNITUDE_BRAIN]
#                [--out_prefix OUT_PREFIX] [--esp ESP] [--te TE] [--tr TR]
#                [--nvolumes NVOLUMES] [--fsf FSF] [--nohup]
#                [--ignore_exception] [--pedir PEDIR] [--out_dir OUT_DIR]
#
#optional arguments:
#  -h, --help            show this help message and exit
#  -d, --display         Display Results
#  -v, --verbose         Verbose flag
#  --debug               Debug flag
#  --no_clean            Clean directory by deleting intermediate files
#  --prepare             Prepare design FSF file
#  --qi                  QA inputs
#  --qo                  QA outputs
#  --report              Report
#  -r, --run             Run processing pipeline
#  --indir INDIR         Input directory
#  --epi EPI             4D EPI data
#  --t1brain T1BRAIN     Skull Stripped T1w image (brain only)

#  --fmap_radians FMAP_RADIANS
#                        Fieldmap in radians (see iwFmap.py)

#  --fmap_magnitude FMAP_MAGNITUDE
#                        Fieldmap magnitude full brain image

#  --fmap_magnitude_brain FMAP_MAGNITUDE_BRAIN
#                        Fieldmap magnitude brain (skull stripped)

#  --out_prefix OUT_PREFIX
#                        Output prefix
#  --esp ESP             Echo spacing [ms]. Divide by acceleration factor if
#                        necessary
#  --te TE               Echo Time [ms].
#  --tr TR               Repitition Time [s]
#  --nvolumes NVOLUMES   Number of Volumes in EPI data
#  --fsf FSF             FEAT Design file (default = epireg.fsf)
#  --nohup               Run FEAT in background. Log files are created
#  --ignore_exception    Echo spacing in milliseconds. Divide by acceleration
#                        factor if necessary
#  --pedir PEDIR         Phase encode direction (x,-x,y,-y,z,-z)
#  --out_dir OUT_DIR     Output directory
    