#!/usr/bin/env python

import sys      
import os                                               # system functions
import shutil

import argparse
import iwUtilities     as util

import pandas as pd

#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #
     
     parser = argparse.ArgumentParser(prog='iwCtf_matrices')
               
     parser.add_argument("in_filename",         help="CSV input points" )
     parser.add_argument("out_filename",          help="CSV output points" )
     parser.add_argument("-t", "-transforms",   help="Transform", nargs="*" )

     parser.add_argument("-v","--verbose",    help="Verbose flag",      action="store_true", default=False )

     inArgs = parser.parse_args()

     #
     #
     #

     input_files = [ in_filename, iras_To_wras, wras_To_wlps ]

     util.verify_outputs( input_files )
     
     cmd = [ "antsApplyTransformsToPoints", "-d", "3", "-i", points, "-o", out_points , "-t"] + inArgs.transforms
     util.iw_subprocess(cmd, inArgs.verbose, inArgs.verbose)

     #
     #
     #

     if inArgs.verbose:
         in_points = pd.read_csv(in_filename,  names = ["x", "y", "z", "t", "label","comment"])
         print in_points

