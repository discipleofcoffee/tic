#!/usr/bin/env python

import sys      
import os                                               # system functions
import shutil

import argparse
import iwUtilities     as util
import iwCtf        as ctf


import pandas as pd

def run(in_filename, out_filename, in_transforms, scale, verbose_flag, debug_flag):

     if type(in_filename) is list:
          filename = in_filename
     else:
          filename = [ in_filename ]

     if type(in_transforms) is list:
          transforms = in_transforms
     else:
          transforms = [ in_transforms ]

     input_files = filename + transforms 

     if debug_flag:
          print input_files
          print

     util.verify_inputs( input_files )

     in_points = ctf.print_points_from_file(in_filename, verbose_flag)

     cmd = [ "antsApplyTransformsToPoints", "-d", "3", "-i", in_filename, "-o", out_filename , "-t"] + transforms
     util.iw_subprocess(cmd, debug_flag, debug_flag)

     # Perform scaling

     out_points = pd.read_csv(out_filename, sep=',',header=0)
     out_points = ctf.scale_points( out_points, scale, debug_flag )
     
     # Fix Comment Column
     out_points['comment'] = in_points['comment']

     #
     ctf.write_points( out_filename, out_points, verbose_flag)


#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #
     
     parser = argparse.ArgumentParser(prog='iwCtf_matrices')
               
     parser.add_argument("in_filename",         help="CSV input points" )
     parser.add_argument("out_filename",        help="CSV output points" )
     parser.add_argument("-t", "--transforms",  help="Transform", nargs="*" )
     parser.add_argument("-s", "--scale",       help="Scale (LPS is in mm, CTF in cm)", type=float, default=1.0 )

     parser.add_argument("-v","--verbose",    help="Verbose flag",      action="store_true", default=False )
     parser.add_argument("--debug",             help="Debug   flag",      action="store_true", default=False )

     inArgs = parser.parse_args()

     #
     #
     #

     run( inArgs.in_filename, inArgs.out_filename, inArgs.transform, inArgs.verbose, inArgs.debug)
     


