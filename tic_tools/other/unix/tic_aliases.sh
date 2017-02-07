#!/usr/bin/env bash

alias cdtic='cd $TIC_PATH; lsreport_function'
alias cdstudies='cd $STUDIES_PATH; lsreport_function'
alias cdtemplates='cd $TEMPLATES_PATH; lsreport_function'

alias cdsd='cd $SUBJECTS_DIR; lsreport_function'

alias  fsvinia='fslview $IMAGEWAKE2_PATH/templates/inia19_rhesus_macaque/inia19_e_T1wFullImage.nii.gz &'
alias  fsvfsl='fslview $FSL_DIR/data/standard/MNI152_T1_1mm_brain.nii.gz &'
alias  fsvixi='fslview $IMAGEWAKE2_PATH/templates/ixi/cerebellum/ixiTemplate2_e_T1wFullImage.nii.gz &'

alias cda='echo; echo $PWD; cd $(pwd -P); echo $PWD; echo; ls; echo'

alias redcm='source $IMAGEWAKE2_SCRIPTS/dcm_functions.sh'


alias ag='alias | grep'
alias hg='history | grep '
alias eg='env | grep '
alias lg='ls | grep '

alias lsp='echo; echo $PATH | tr ":" "\n" | cat -n | sort -n -r; echo'          # Enumerates path
alias lspp='echo; echo $PYTHONPATH | tr ":" "\n" | cat -n | sort -n -r; echo'   # Enumerates Python Path


alias frv='freeview'
alias fsv='fslview'
alias fsvall='fslview_all_function'

alias lsreport='lsreport_function'

alias lnflatten='${TIC_TOOLS_PATH}/other/unix/lnflatten.sh'
alias cpflatten='${TIC_TOOLS_PATH}/other/unix/cpflatten.sh'

alias tic_reorient2std='${TIC_TOOLS_PATH}/other/unix/tic_reorient2std.sh ../../reorient *.gz'
alias tic_path='echo; echo $TIC_PATH; echo'

# Aliases to TIC Python functions

alias tic_plot_overlay='$TIC_TOOLS_PYTHONPATH/plot_overlay.py'
alias tic_ants_ct='$TIC_TOOLS_PYTHONPATH/ants_ct.py'

