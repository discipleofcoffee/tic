#!/usr/bin/env python

import sys      
import os                                               # system functions
import shutil

import argparse
import iwCtf           as ctf
import iwUtilities     as util

import pandas as pd



#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #
     
     parser = argparse.ArgumentParser(prog='iwCtf_iras_to_wras')
               
     parser.add_argument("in_filename",         help="CSV input points" )
     parser.add_argument("out_filename",        help="CSV output points" )
     parser.add_argument("transform",           help="Affine transform" )

     parser.add_argument("-v","--verbose",    help="Verbose flag",      action="store_true", default=False )

     inArgs = parser.parse_args()

     #
     #
     #

     ctf.iras_to_wras(inArgs.in_filename, inArgs.out_filename, inArgs.transform, inArgs.verbose)


