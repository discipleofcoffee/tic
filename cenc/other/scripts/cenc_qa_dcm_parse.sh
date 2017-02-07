#!/usr/bin/env bash 

source ${IMAGEWAKE2_PATH}/scripts/dcm_functions.sh

basename=dcmConvert_cenc_qa.cfg

dcm_group dcmConvertAll.cfg > 01.${basename}


sed -i -e  "/localizer/d" 01.${basename}
sed -i -e  "/rs02/d" 01.${basename}

sed -i -e  "s/SAGMPRAGE_rs01/adni_qa_mprage/g"  01.${basename}
sed -i -e  "s/RestingStatefMRI/fmri_qa_fbirn/g" 01.${basename}

dcm_remove_rs 01.${basename} > 02.${basename}

sort  -k 4,4  -k 1,1n 02.${basename} | tee ${basename}.draft


rm 0{1,2}.${basename}

