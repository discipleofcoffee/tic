#!/usr/bin/env python

import sys      
import os                                               # system functions
import shutil

import argparse
import iwUtilities  as util
import iwCtf        as ctf

#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #
     
     parser = argparse.ArgumentParser(prog='iwCtf_icsa_to_wlps')
               
     parser.add_argument("in_filename",         help="CSV input points" )
     parser.add_argument("out_filename",        help="CSV output points" )
     parser.add_argument("-t", "--transform",   help="Transform")

     parser.add_argument("-v","--verbose",      help="Verbose flag",      action="store_true", default=False )
     parser.add_argument("--debug",             help="Debug   flag",      action="store_true", default=False )

     inArgs = parser.parse_args()

     input_files = [ inArgs.in_filename, inArgs.transform]

     util.verify_inputs(input_files, inArgs.debug)


     ctf.wlps_to_icsa(inArgs.in_filename, inArgs.out_filename, inArgs.transform, inArgs.verbose, inArgs.debug)

