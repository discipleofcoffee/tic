#!/usr/bin/env bash

cd ${1-$PWD}
/aging1/software/matlab/bin/matlab -nodisplay -nodesktop \
-r "addpath('/cenc/software/imagewake2/beta/studies/cenc//matlab'); cenc_lst_lpa('./t2flair_Affine_nu__t2flair_Warped.nii', '', false); exit" 
