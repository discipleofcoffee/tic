#!/usr/bin/env python

"""

"""
import sys
import os                                               # system functions
import re

import argparse
import iwUtilities as util
import cenc
import cenc_freesurfer


def main():
     ## Parsing Arguments
     #
     #

     usage = "usage: %prog [options] arg1 arg2"

     parser = argparse.ArgumentParser(prog='cenc_freesurfer')

     parser.add_argument("--in_dir",       help="Participant directory", default = os.getcwd() )

     parser.add_argument("--cenc_data_dir",   help="CENC data directory", default = os.getenv('CENC_MRI_DATA')) 
     parser.add_argument("--cenc_freesurfer_dir",   help="CENC data directory", default = os.getenv('CENC_SUBJECTS_DIR')) 
     parser.add_argument("--cenc_results_dir",   help="CENC results directory", default = './results/native') 

     parser.add_argument("--prepare",    help="Gather necessary inputs for Freesurfer analysis", action="store_true", default=False )
     parser.add_argument("--run",        help="Freesurfer recon-all", action="store_true", default=False )
     parser.add_argument("--results",    help="Gather Freesurfer results",  action="store_true", default=False )


     inArgs = parser.parse_args()

     #
     #
     #

     if inArgs.prepare:
          prepare( inArgs.in_dir)

     if inArgs.run:
          pass

     if inArgs.results:
          pass


def prepare( in_dir ):

     cenc_participant_id, cenc_participant_dir = cenc.participant_id( in_dir )
     cenc_freesurfer_dir = os.path.abspath( inArgs.cenc_freesurfer_dir )

     cenc_freesurfer.prepare(cenc_participant_dir)
     recon_all( cenc_participant_id, cenc_freesurfer_dir)

     return



def results(cenc_participant_id, cenc_freesurfer_dir, cenc_results_dir):
     pass


#
# Main Function
#

if __name__ == "__main__":
    sys.exit(main())

