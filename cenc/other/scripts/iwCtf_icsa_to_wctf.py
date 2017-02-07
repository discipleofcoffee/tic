#!/usr/bin/env python

import sys      
import os                                               # system functions
import shutil

import argparse
import iwUtilities  as util
import iwCtf        as ctf

import pandas as pd

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
     parser.add_argument("-t", "--transforms",  help="Transform", nargs=3)

     parser.add_argument("-v","--verbose",    help="Verbose flag",      action="store_true", default=False )

     inArgs = parser.parse_args()

     #
     #
     #


     _pd_00 = ctf.icsa_to_iras(inArgs.in_filename, '00_iwCtf_iras.csv', inArgs.verbose)

     ctf.write_points( '00_iwCtf_iras.csv', _pd_00 )

     _pd_01 = ctf.apply_affine_transform('00_iwCtf_iras.csv', '01_iwCtf_wras.csv', inArgs.transforms[0] )

     ctf.write_points( '01_iwCtf_wras.csv', _pd_01, inArgs.verbose )

     _pd_02 = ctf.apply_affine_transform('01_iwCtf_wras.csv', '02_iwCtf_wlps.csv', inArgs.transforms[1] )

     ctf.write_points( '02_iwCtf_wlps.csv',  _pd_02, inArgs.verbose )

     _pd_03 = ctf.apply_affine_transform('02_iwCtf_wlps.csv', inArgs.out_filename, inArgs.transforms[2] )

     ctf.write_points( inArgs.out_filename,  _pd_03, inArgs.verbose )


     # Clean up temporary files

#     for ii in ['00_iwCtf_icsa_to_wctf.csv', '01_iwCtf_icsa_to_wctf.csv','02_iwCtf_icsa_to_wctf.csv']:
#          os.remove(ii)


     
