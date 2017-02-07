#!/usr/bin/env python

import argparse
import iwUtilities     as util
import iwCtf           as ctf

import pandas as pd

#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #
     
     parser = argparse.ArgumentParser(prog='iwCtf_mri_to_meg')
               
     parser.add_argument("in_filename",          help="CSV input points" )
     parser.add_argument("out_filename",         help="CSV output points" )

     parser.add_argument("-v","--verbose",    help="Verbose flag",      action="store_true", default=False )

     inArgs = parser.parse_args()

     #
     #
     #

     input_files = [ inArgs.in_filename ]
     util.verify_inputs( input_files )

     ctf.mri_to_meg( inArgs.in_filename, inArgs.out_filename, inArgs.verbose )

