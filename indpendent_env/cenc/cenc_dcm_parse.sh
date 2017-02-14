#!/usr/bin/env bash 

source ${TIC_TOOLS_PATH}/other/unix/dcm_functions.sh

basename=dcmConvert_cenc.cfg

dcm_group dcmConvertAll.cfg > 01.${basename}

sed -i -e  "/localizer_rs01/d" 01.${basename}

sed -i -e  "s/sag_mprage_rs01/t1w/g" 01.${basename}

sed -i -e  "s/sag_swi_rs01/swi_magnitude/g" 01.${basename}
sed -i -e  "s/sag_swi_rs02/swi_phase/g"     01.${basename}
sed -i -e  "/sag_swi_rs03/d"                01.${basename}
sed -i -e  "s/sag_swi_rs04/swi/g"           01.${basename}

sed -i -e  "s/sag_t2tse_rs01/t2tse/g" 01.${basename}

sed -i -e  "s/sag_t2flair_rs01/t2flair/g" 01.${basename}

sed -i -e  "s/sag_mt_rs01/mt_m0/g" 01.${basename}
sed -i -e  "s/sag_mt_rs02/mt_m1/g" 01.${basename}

sed -i -e  "s/ax_dki_P>>A_rs01/dki/g"                01.${basename}
sed -i -e  "/ax_dki_P>>A_rs02/d" 		     01.${basename}
sed -i -e  "/ax_dki_P>>A_rs03/d" 		     01.${basename}
sed -i -e  "/ax_dki_P>>A_rs04/d" 		     01.${basename}
sed -i -e  "/ax_dki_P>>A_rs05/d" 		     01.${basename}   
sed -i -e  "s/dki_topup_A>>P_rs01/dki_topup_ap/g"    01.${basename}
sed -i -e  "s/dki_topup_P>>A_rs01/dki_topup_pa/g"    01.${basename}

sed -i -e  "s/restA>>P_rs01/rest/g"                  01.${basename}
sed -i -e  "/restA>>P_rs02/d"                        01.${basename}
sed -i -e  "s/rest_topup_A>>P_rs01/rest_topup_ap/g"  01.${basename}
sed -i -e  "s/rest_topup_P>>A_rs01/rest_topup_pa/g"  01.${basename}

sed -i -e  "s/pcaslA>>P_rs01/pcasl_raw/g" 01.${basename}
sed -i -e  "s/pcaslA>>P_rs02/pcasl_mc/g" 01.${basename}
sed -i -e  "s/pcaslA>>P_rs03/pcasl_pwi/g" 01.${basename}
sed -i -e  "s/pcaslA>>P_rs04/pcasl_cbf/g" 01.${basename}
sed -i -e  "s/pcasl_topup_P>>A_rs01/pcasl_topup_pa/g" 01.${basename}
sed -i -e  "s/pcasl_topup_A>>P_rs01/pcasl_topup_ap/g" 01.${basename}

sed -i -e  "s/ax_dti_A>>P_rs01/dti/g" 01.${basename}
sed -i -e  "/ax_dti_A>>P_rs02/d" 01.${basename}
sed -i -e  "/ax_dti_A>>P_rs03/d" 01.${basename}
sed -i -e  "/ax_dti_A>>P_rs04/d" 01.${basename}
sed -i -e  "/ax_dti_A>>P_rs05/d" 01.${basename}

sed -i -e  "s/dti_topup_A>>P_rs01/dti_topup_ap/g" 01.${basename}
sed -i -e  "s/dti_topup_P>>A_rs01/dti_topup_pa/g" 01.${basename}

sed -i -e  "s/ax_grass_64_rs01/fmap_magnitude/" 01.${basename}
sed -i -e  "s/ax_grass_64_rs02/fmap_phase/" 01.${basename}

sed -i -e  "/sag_t2tse_rs01/d" 01.${basename}
sed -i -e  "/sag_t2flair_rs01/d" 01.${basename}
sed -i -e  "/sag_mt_rs01/d" 01.${basename}


sort  -k 4,4  -k 1,1n 01.${basename} > 02.${basename}

dcm_group  02.${basename} > ${basename}.draft


rm 0{1,2}.${basename}

