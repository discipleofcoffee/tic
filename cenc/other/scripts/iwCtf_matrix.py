#!/usr/bin/env python

import sys      
import os                                               # system functions
import shutil

import argparse
import iwUtilities     as util
import iwCtf        as ctf

#
# Main Function
#

if __name__ == "__main__":


     ## Parsing Arguments
     #
     #
     
     parser = argparse.ArgumentParser(prog='iwCtf_icsa_to_wlps')
               
     parser.add_argument("in_fiducials",        help="CSV input points" )
     parser.add_argument("out_ctf_matrix",      help="CSV output points" )

     parser.add_argument("--ctf_scale",    help="CTF scale factor",    type=float, default=1)

     parser.add_argument("-v","--verbose",      help="Verbose flag",      action="store_true", default=False )
     parser.add_argument("--debug",             help="Debug   flag",      action="store_true", default=False )

     inArgs = parser.parse_args()

     util.verify_inputs( [ inArgs.in_fiducials ], inArgs.debug)

     ctf.calc_matrix( inArgs.in_fiducials, inArgs.out_ctf_matrix, inArgs.ctf_scale,  inArgs.verbose)
     
