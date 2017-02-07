#!/usr/bin/env bash

cd ${1-$PWD}
nohup /aging1/software/matlab/bin/matlab -nodisplay -nodesktop -r "addpath('/cenc/software/imagewake2/beta/studies/cenc//matlab'); cenc_lst_lpa; exit" 1> std.out 2> err.out &