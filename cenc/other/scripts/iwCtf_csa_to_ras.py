#!/usr/bin/env python

import sys      
import os                                               # system functions
import glob
import shutil
import distutils
import nibabel as nib

import pandas as pd
import argparse
import subprocess
import iwUtilities
import csv
import numpy as np


#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #
     
     parser = argparse.ArgumentParser(prog='iwCtf_matrices')
     parser.add_argument("csv_filename",      help="CTF reference image" )

     parser.add_argument("--c_max",           help="Maximum index along C direction of CSA", default=255)
     parser.add_argument("--a_max",           help="Maximum index along A direction of CSA", default=255)

     parser.add_argument("-v","--verbose",    help="Verbose flag",      action="store_true", default=False )

     inArgs = parser.parse_args()
     #
     # Read in CSV coordinates file
     #

     df=pd.read_csv(inArgs.csv_filename, sep=',',header=0)

     if inArgs.verbose:
          print "Coordinates as defined in " + inArgs.csv_filename 
          print df
          print

     coordinates_icsa = np.asarray(df.values)
     
     coordinates_ilps = coordinates_icsa

     for ii, jj in enumerate(coordinates_icsa):          

          coordinates_ilps[ii,0:2] = [ coordinates_icsa[1],  inArgs.c_max-coordinates_icsa[0], inArgs.a_max-coordinates_icsa[2] ]
          print ii, jj
     

     print coordinates_ilps

     exit()

     df_iras = pd.DataFrame(wlps_list, columns=[ 'x','y','z','t','label', 'comment'])

     if inArgs.verbose:
          print "MEG fiducials in RAS image coordinates"
          print df_iras
          print

     df_iras.to_csv(inArgs.meg_iras, sep=',',header=1, index=False)

