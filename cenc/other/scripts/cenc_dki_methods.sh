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
    
    ln ${eddy_input}/b0.nii.gz       ${eddy_eddy}
    ln ${eddy_input}/acqparams.txt   ${eddy_eddy}
    ln ${eddy_input}/b02b0.cnf       ${eddy_eddy}
fi

cd ${eddy_eddy}

eddy --imain=dki.nii.gz --mask=bet.mean.b0.dki_mask.nii.gz --index=index.txt --acqp=dki_acqparams.txt --bvecs=dki.bvec --bvals=dki.bval --out=../02-eddy/eddy --niter=1 --topup=topup -v --repol

