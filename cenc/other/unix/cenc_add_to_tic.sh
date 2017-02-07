#!/usr/bin/env bash

# These commands should be added to your tic.sh script if you are planning to use the
# CENC analysis scripts and modules. An easy way to do this is
#
#   >> tail -7 /cenc/tic/studies/cenc/other/unix/cenc_add_to_tic.sh
#
# You will need to change the location of the CENC_PATH and CENC_DISKS.
#


# CENC Study initialization ==================================================

export CENC_PATH=/cenc/tic/studies/cenc  # where CENC project is located

export CENC_DISK=/cenc/          # The directory CENC_DISK directory is the parent directory of the CENC study.
                                 # On aging1a it is /cenc/. This changes depending upon the mount point for
                                 # each computer.

source ${CENC_PATH}/cenc_bash_setup.sh
