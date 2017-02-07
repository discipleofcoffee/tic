#!/usr/bin/env python

import nibabel as nib

import pandas as pd
import argparse
import iwUtilities
import numpy as np

def clean_nan(in_filename):
    
  with open(in_filename) as f:
    newText=f.read().replace(',nan', '')

  with open(in_filename, "w") as f:
    f.write(newText)

#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #
     
     parser = argparse.ArgumentParser(prog='iwCtf_transform')
               
     parser.add_argument("in_template",      help="CSV labels in CTF space in LPS world coordinates" )

     parser.add_argument("out_native",     help="Output filename of CSV Labels in Native space LPS world coordinates") 
     parser.add_argument("out_ctf",     help="Output filename of CSV Labels in Template space LPS world coordinates") 

     parser.add_argument("--ants_affine",     help="ANTS Affine tranformation Template To Subject", default='SubjectToTemplate0GenericAffine.mat')
     parser.add_argument("--ants_warp",       help="ANTS Affine tranformation Template To Subject", default='SubjectToTemplate1Warp.nii.gz')

     parser.add_argument("--wlps_to_wctf",    help="Filename for affine matrix LPS world to CTF world coordinates",    default='affine_wlps_to_wctf.txt' )

     parser.add_argument("-v","--verbose",    help="Verbose flag",      action="store_true", default=False )

     inArgs = parser.parse_args()
     
     if inArgs.verbose:
          print "inArgs.in_template       = " +  str(inArgs.in_template)
          print "inArgs.out_native        = " +  str(inArgs.out_native)
          print "inArgs.out_ctf           = " +  str(inArgs.out_ctf)

          print "inArgs.ants_affine       = " +  str(inArgs.ants_affine)
          print "inArgs.ants_warp         = " +  str(inArgs.ants_warp)
          print "inArgs.wlps_to_wctf      = " +  str(inArgs.wlps_to_wctf)
          print "inArgs.verbose           = " +  str(inArgs.verbose)

    
     #
     # Check inputs
     #     

     input_files = [inArgs.in_template, inArgs.ants_affine, inArgs.ants_warp, inArgs.wlps_to_wctf];
          
     for ii in input_files:
          iwUtilities.verify_that_file_exists(ii)

     #
     # Transform Template Points to Native Space
     #

     cmd = [ "antsApplyTransformsToPoints", "-d", "3", "-i", inArgs.in_template, "-o", inArgs.out_native, "-t", inArgs.ants_warp, inArgs.ants_affine ]
     iwUtilities.iw_subprocess(cmd, inArgs.verbose)

     clean_nan(inArgs.out_native)

     #
     # Transform CTF point to Template Space
     #

     cmd = [ "antsApplyTransformsToPoints", "-d", "3", "-i", inArgs.in_template, "-o", inArgs.out_ctf, "-t", inArgs.ants_warp, inArgs.ants_affine, inArgs.wlps_to_wctf ]
     iwUtilities.iw_subprocess(cmd, inArgs.verbose)

     clean_nan(inArgs.out_ctf)
