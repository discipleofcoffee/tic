#!/usr/bin/env python

import sys      
import os                                               # system functions
import shutil

import argparse
import iwUtilities   as util
import iwCtf         as ctf

import nibabel as nb
import pandas as pd
import numpy as np


#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #
     
     parser = argparse.ArgumentParser(prog='iwCtf_matrices')
               
     parser.add_argument("image",           help="CTF reference image" )
     parser.add_argument("in_fiducials",    help="Fiducials in CSA image space" )

     parser.add_argument("--in_dir",        help="Input directory", default=os.getcwd() )
     parser.add_argument("--out_dir",       help="Output directory", default='..' )

     parser.add_argument("--out_fiducials",  help="Filename for affine matrix LPS world to CTF world coordinates",  default='affine_iras_to_wras.txt' )

     parser.add_argument("--out_affine_matrix",  help="Filename for affine matrix LPS world to CTF world coordinates",  default='affine_iras_to_wras.txt' )
     parser.add_argument("--out_ctf_matrix",     help="Filename for affine matrix RAS image to RAS world coordinates",  default='affine_wlps_to_wctf.txt' )

     parser.add_argument("--ctf_scale",    help="CTF scale from index to physical units [cm^3]. Assume isotropic. (default=0.1 [cm^3]) ",
                                           type=float, default=.1)
    
     parser.add_argument("-r", "--run",               help="Run processing pipeline",      action="store_true", default=False )
     parser.add_argument("--run_stage",       help="Stages to run in the processing pipeline", type=int, nargs='*', default = [ 0,1,2,3,4 ] )

     parser.add_argument("-v","--verbose",    help="Verbose flag",      action="store_true", default=False )

     inArgs = parser.parse_args()
     
     #
     #
     #


     input_directory  = os.path.abspath(inArgs.in_dir)
     output_directory = util.path_relative_to( input_directory, inArgs.out_dir)

     #
     #
     #

     util.print_stage("Displaying inputs to wbi_swi_rigid_to_inia.py", inArgs.verbose )

     if inArgs.verbose:
          print
          print "input_directory  = " +  input_directory
          print "output_directory = " +  output_directory
          print
          print "inArgs.image          = " +  str(inArgs.image)
          print "inArgs.in_fiducials        = "  +  str(inArgs.in_fiducials)
          print
          print "inArgs.verbose        = " +  str(inArgs.verbose)

     #
     #
     #

     stage_directory = [ os.path.abspath( os.path.join( output_directory,  '00-rename'      )),
                         os.path.abspath( os.path.join( output_directory,  '01-matrices'    )),
                         os.path.abspath( os.path.join( output_directory,  '02-transformed' ))
                         ] 
    
     print
     print output_directory
     print stage_directory
     print

     #
     # Check input files
     #
     util.print_stage("Verifying inputs", inArgs.verbose )

     input_files =      [ os.path.abspath( os.path.join( input_directory, inArgs.image       )),
                          os.path.abspath( os.path.join( input_directory, inArgs.in_fiducials     ))
                          ]

     util.verify_inputs( input_files, inArgs.verbose)

     image_filename = input_files[0]
     fiducials      = input_files[1]

     #
     # Save image affine matrix
     #
     
     util.save_image_affine_matrix( image_filename, inArgs.out_affine_matrix )

     #
     # Calculate and Save CTF matrix (wLPS to wCTF)
     #

#     ctf_matrix = ctf.calc_ctf_matrix( in_fiducials, inArgs.ctf_scale, inArgs.verbose)

#     util.write_itk_affine_matrix(ctf_matrix, inArgs.ctf_matrix, verbose_flag=False):






