#!/bin/bash

#
# Topup Analysis
#

eddy_input=${1-$PWD}
eddy_methods=$(readlink -f ${eddy_input}/../methods/)
echo ${eddy_methods}

[ -d ${eddy_methods} ] || mkdir -p ${eddy_methods}

cd ${eddy_methods}


#
# Eddy directory
#
eddy_eddy=${eddy_methods}/01-eddy

if [ ! -f ${eddy_eddy}/b02b0.cnf ]; then

    echo $eddy_eddy

    [ -d ${eddy_eddy} ] || mkdir -p ${eddy_eddy}


    ln ${eddy_input}/dki.nii.gz                    ${eddy_eddy}    
    ln ${eddy_input}/bet.b0_unwarped_mask.nii.gz   ${eddy_eddy}
    ln ${eddy_input}/index.txt                     ${eddy_eddy}

    ln ${eddy_input}/acqparams.txt                 ${eddy_eddy}

    ln ${eddy_input}/dki.bvec                      ${eddy_eddy}
    ln ${eddy_input}/dki.bval                      ${eddy_eddy}

    ln ${eddy_input}/topup_movpar.txt              ${eddy_eddy}
    ln ${eddy_input}/topup_fieldcoef.nii.gz        ${eddy_eddy}

fi

cd ${eddy_eddy}

cmd="nohup eddy --imain=dki.nii.gz --mask=bet.b0_unwarped_mask.nii.gz --index=index.txt --acqp=acqparams.txt --bvecs=dki.bvec --bvals=dki.bval --out=eddy --niter=5 --topup=topup -v --repol > nohup.eddy.log &"
echo $cmd

nohup eddy --imain=dki.nii.gz --mask=bet.b0_unwarped_mask.nii.gz --index=index.txt --acqp=acqparams.txt --bvecs=dki.bvec --bvals=dki.bval --out=eddy --niter=5 --topup=topup -v --repol > nohup.eddy.log &


