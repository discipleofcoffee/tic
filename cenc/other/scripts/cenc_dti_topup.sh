#!/bin/bash


subject_id=${1-$PWD}
subject_dir=$(readlink -f ${CENC_MRI_DATA}/$subject_id)

echo $subject_id
echo $subject_dir


mkdir -p ${subject_dir}/diffusion/{topup,dki,dti}/input
mkdir -p ${subject_dir}/diffusion/topup/01-topup/; 


cd ${subject_dir}/diffusion/topup/input
for ii in bval bvec; do 
    ln ../../../reorient/dki.${ii} .
    ln ../../../reorient/dti.${ii} .
done

fslroi ../../../reorient/dki.nii.gz dki.nii.gz 0 -1 0 -1 0 58 0 -1 
fslroi ../../../reorient/dti.nii.gz dti.nii.gz 0 -1 0 -1 0 58 0 -1 


cd ${subject_dir}/diffusion/dki/input
for ii in nii.gz bval bvec; do 
    ln ../../topup/input/dki.${ii} .
done

cd ${subject_dir}/diffusion/dti/input
for ii in nii.gz bval bvec; do 
    ln ../../topup/input/dti.${ii} .
done



cd ${subject_dir}/diffusion/topup/input
ls

extract_b0.py dki.nii.gz dki.bval
extract_b0.py dti.nii.gz dti.bval

fslmerge -t b0.nii.gz  b0.dki.nii.gz b0.dti.nii.gz
cp ${CENC_SCRIPTS}/topup_acqparams.txt topup_acqparams.txt


nohup topup --config=b02b0.cnf --datain=topup_acqparams.txt --imain=b0.nii.gz --out=topup --iout=../01-topup/b0_unwarped.nii.gz --fout=b0_fmap_hz.nii.gz -v > nohup.toup.log &

