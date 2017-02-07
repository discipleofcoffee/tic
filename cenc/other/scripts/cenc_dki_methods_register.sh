#!/bin/bash

#
# Topup Analysis
#

dtifit_input=${1-$PWD}
dtifit_input=$(readlink -f $dtifit_input)

dtifit_methods=$(readlink -f ${dtifit_input}/../methods/)
dtifit_eddy=$(readlink -f ${dtifit_methods}/01-eddy)
dtifit_dtifit=$(readlink -f ${dtifit_methods}/02-dtifit)
dtifit_register=$(readlink -f ${dtifit_methods}/03-register)

echo ${dtifit_register}
[ -d ${dtifit_register} ] || mkdir -p ${dtifit_register}
cd ${dtifit_register}


#
# Dtifit directory
#

ln ${dtifit_input}/nu_brain.nii.gz ${dtifit_register}

# antsRegistrationSyNQuick.sh -d 3 -m ${dtifit_dtifit}/dtifit_MD.nii.gz -f nu_brain.nii.gz -t s -o md_SyN_nu__

# dti_scalar_list  = [ FA, L1, L2, L3, MD, MO, S0 ]
# dti_vector_list  = [ V1, V2 ,V3 ]

for ii in MD FA; do
    echo
    antsApplyTransforms -v -d 3 -e 0 -i ${dtifit_dtifit}/dtifit_${ii}.nii.gz -r nu_brain.nii.gz -o md_SyN_nu__${ii}.nii.gz -t md_SyN_nu__1Warp.nii.gz -t md_SyN_nu__0GenericAffine.mat
    echo
    echo
done

for ii in V1 V2 V3; do
    echo
    echo $ii
    antsApplyTransforms -v -d 3 -e 1 -i ${dtifit_dtifit}/dtifit_${ii}.nii.gz -r nu_brain.nii.gz -o md_SyN_nu__${ii}.nii.gz -t md_SyN_nu__1Warp.nii.gz -t md_SyN_nu__0GenericAffine.mat
    echo
    echo
done



