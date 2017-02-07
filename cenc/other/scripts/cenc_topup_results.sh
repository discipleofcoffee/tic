#!/bin/bash


topup_input=${1-$PWD}
topup_dir=$(readlink -f ${topup_input}/.. )

topup_methods=${topup_dir}/methods/01-topup

topup_methods_results=${topup_dir}/methods/results
topup_results=${topup_dir}/results


echo
echo $RADCORE_MRI_DATA
echo $topup_input
echo $topup_results
echo


#
# Copy files to methods results
#

mkdir -p ${topup_methods_results}

ln ${topup_methods}/b0.nii.gz              $topup_methods_results
ln ${topup_methods}/b0_fmap_hz.nii.gz      $topup_methods_results
ln ${topup_methods}/b0_unwarped.nii.gz     $topup_methods_results
ln ${topup_methods}/topup_fieldcoef.nii.gz $topup_methods_results
ln ${topup_methods}/topup_movpar.txt       $topup_methods_results

#
# Copy files to final results
#

mkdir -p ${topup_results}

ln ${topup_methods}/b0.nii.gz              $topup_results
ln ${topup_methods}/b0_fmap_hz.nii.gz      $topup_results
ln ${topup_methods}/b0_unwarped.nii.gz     $topup_results
ln ${topup_methods}/topup_fieldcoef.nii.gz $topup_results
ln ${topup_methods}/topup_movpar.txt       $topup_results


