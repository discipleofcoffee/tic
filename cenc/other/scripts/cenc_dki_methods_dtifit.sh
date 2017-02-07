#!/bin/bash

#
# Topup Analysis
#

dtifit_input=${1-$PWD}

dtifit_methods=$(readlink -f ${dtifit_input}/../methods/)
eddy_methods=$(readlink -f ${dtifit_input}/../methods/01-eddy)

echo ${dtifit_methods}

[ -d ${dtifit_methods} ] || mkdir -p ${dtifit_methods}

cd ${dtifit_methods}


#
# Dtifit directory
#
dtifit_dtifit=${dtifit_methods}/02-dtifit

if [ ! -f ${dtifit_dtifit}/b02b0.cnf ]; then

    echo $dtifit_dtifit

    [ -d ${dtifit_dtifit} ] || mkdir -p ${dtifit_dtifit}

    ln ${eddy_methods}/eddy.nii.gz                   ${dtifit_dtifit}    
    ln ${eddy_methods}/bet.b0_unwarped_mask.nii.gz   ${dtifit_dtifit}
    ln ${dtifit_input}/dki.bvec                      ${dtifit_dtifit}
    ln ${dtifit_input}/dki.bval                      ${dtifit_dtifit}

fi

cd ${dtifit_dtifit}

dtifit --data=eddy.nii.gz --out=dtifit --mask=bet.b0_unwarped_mask.nii.gz --bvecs=dki.bvec --bvals=dki.bval -V


