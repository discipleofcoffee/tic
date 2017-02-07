#!/usr/bin/env python

import argparse

import iwCtf       as ctf
import iwUtilities as util

#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #
     
     parser = argparse.ArgumentParser(prog='iwCtf_extract_affine')
               
     parser.add_argument("in_image",           help="Input image" )
     parser.add_argument("out_affine",      help="Filename of affine matrix" )

     parser.add_argument("--ras",           help="Multiply affine by lps affine matrix before saving",      action="store_true", default=False )

     parser.add_argument("-v","--verbose",  help="Verbose flag",                       action="store_true", default=False )

     inArgs = parser.parse_args()

     util.verify_inputs( [inArgs.in_image], inArgs.verbose)



     ctf.extract_affine( inArgs.in_image, inArgs.out_affine, not inArgs.ras, inArgs.verbose)
               
 
