#!/bin/bash

#
# Topup Analysis
#

topup_input=${1-$PWD}
topup_methods=$(readlink -f ${topup_input}/../methods/)
echo ${topup_methods}

[ -d ${topup_methods} ] || mkdir -p ${topup_methods}

cd ${topup_methods}

#
# Topup directory
#
topup_topup=${topup_methods}/01-topup

if [ ! -f ${topup_topup}/b02b0.cnf ]; then

    echo $topup_topup

    [ -d ${topup_topup} ] || mkdir -p ${topup_topup}
    
    ln ${topup_input}/b0.nii.gz       ${topup_topup}
    ln ${topup_input}/acqparams.txt   ${topup_topup}
    ln ${topup_input}/b02b0.cnf       ${topup_topup}
fi

cd ${topup_topup}

nohup topup --config=b02b0.cnf --datain=acqparams.txt --imain=b0.nii.gz --out=topup --iout=b0_unwarped.nii.gz --fout=b0_fmap_hz.nii.gz -v > nohup.topup.log &

