#!/usr/bin/env bash
## Python Aliases
#

export CENC_PYTHON_PATH=${CENC_PATH}/cenc

#alias cenc_aseg_labels.sh

alias cenc_dcm_parse='${CENC_PYTHON_PATH}/cenc_dcm_parse.sh'

alias cenc_dcm_clean_draft='grep -v rs02 dcmConvert_cenc.cfg.draft | dcm_remove_rs |
                            sort -n | tee dcmConvert_cenc.cfg'

alias cenc_freesurfer='${CENC_PYTHON_PATH}/cenc_freesurfer.py'
alias cenc_id='${CENC_PYTHON_PATH}/cenc_id.py'
alias cenc_mt='${CENC_PYTHON_PATH}/cenc_mt.py'
alias cenc_mv_incoming='${CENC_PYTHON_PATH}/cenc_mv_incoming.sh'
alias cenc_swi='${CENC_PYTHON_PATH}/cenc_swi.py'
alias cenc_wmlesions='${CENC_PYTHON_PATH}/cenc_wmlesions.py'
alias cenc_fmri_gather='${CENC_PYTHON_PATH}/fmri_gather.py'

alias cenc_update_participant_list='ls -1d ${CENC_MRI_DATA}/34P1[0-9][0-9][0-9] | tee ${CENC_MRI_DATA}/participant.list'

alias cenc_lrt_participants='ls -1drt ${CENC_MRI_DATA}/34P1[0-9][0-9][0-9]'
alias cenc_llrt_participants='ls -ldrt ${CENC_MRI_DATA}/34P1[0-9][0-9][0-9]'

# Aliases
alias rec='source $CENC_PATH/other/unix/cenc_aliases.sh'
alias recenc='source $CENC_PATH/other/unix/cenc_aliases.sh'

alias cenc_redcap='python3 ${TIC_REDCAP_LINK_PATH}/redcap_link/redcap_upload.py cenc'

alias cdcencp='cd $CENC_PATH;    echo; ls;  echo'
alias cdcencs='cd $CENC_SCRIPTS; echo; ls;  echo'
alias cdcencm='cd $CENC_MATLAB;  echo; ls;  echo'

alias cdcp='cd $CENC_PATH;    echo; ls;  echo'
alias cdcs='cd $CENC_SCRIPTS; echo; ls;  echo'
alias cdcm='cd $CENC_MATLAB;  echo; ls;  echo'

alias cfs='echo; echo $SUBJECTS_DIR; SUBJECTS_DIR=$CENC_SUBJECTS_DIR; echo $SUBJECTS_DIR; echo'

ctf_sed() {
    # I had trouble getting the conversion to lower case working properly

    in_file=$1
    cat $in_file | sed -r -e 's/[[:blank:]]+/,/g' -e '$s/$/\n/' | tr '[:upper:]' '[:lower:]' | tee junk.csv
    mv junk.csv $in_file

#    -e '1 s/X/x/' -e '1 s/Y/y/'   -e '1 s/Z/z/' \
#    -e '1 s/C/c/' -e '1 s/A/a/'   -e '1 s/S/s/' 
#    echo "sed -r -e 's/[[:blank:]]+/,/g' -e '$s/$/\\\n/' $1"

}

## Functions
#
cdcencd() { 
    cdcd $1
}

cdc() { 
    cdcd $1
}

cdcd() { 
  if [ $# -eq 1 ]; then
      subjectID=$(printf "34P1%03d\n" $1)
      subjectDir=${CENC_MRI_DATA}/${subjectID}/;
      
      if [ -d $subjectDir ]; then
	  title ${subjectID}
      else
	  subjectDir=$CENC_MRI_DATA
	  title "CENC"
      fi

  else
      subjectDir=${CENC_MRI_DATA};
      title "CENC"
  fi

 cd $subjectDir
 echo; echo $PWD; echo; ls;  echo
}

cdcds() { 
  if [ $# -eq 1 ]; then
      subjectID=$(printf "34P1%03d\n" $1)
      subjectDir=${CENC_SUBJECTS_DIR}/${subjectID}/;
      
      if [ -d $subjectDir ]; then
	  title ${subjectID}
      else
	  subjectDir=$CENC_SUBJECTS_DIR
	  title "CENC"
      fi

  else
      subjectDir=${CENC_SUBJECTS_DIR};
      title "CENC"
  fi

 cd $subjectDir
 echo; echo $PWD; echo; ls;  echo
}



#cdcp() { 
#  if [ $# -eq 1 ]; then
#         cd /cenc/mri/pilot/cenc${1}/; echo; echo $PWD; echo; ls;  echo
#	 title cenc${1}
#  else
#         cd /cenc/mri/pilot/; echo; echo $PWD; echo ls;  echo
#	 title cencData
#  fi
#}