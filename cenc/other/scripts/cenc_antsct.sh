#!/usr/bin/env bash

subjectID=${1-$(pwd | grep -o "34P[19][0-9][0-9][0-9]")}
subjectDir=${CENC_MRI_DATA}/$subjectID

echo
echo "cenc_antsct.sh " $subjectID
echo

antsctInputDir=${subjectDir}/antsCT/input

cd $antsctInputDir
ls -l 
echo


iwAntsCT.py --t1full t1w.nii.gz --outdir ../01a-t1w_only --outprefix "" -t ixi --nohup
#iwAntsCT.py --t1full t1w.nii.gz --t2full t2tse.nii.gz --t2flair t2flair.nii.gz --outdir ../01b-t1_t2_flair --outprefix "" -t ixi --nohup
