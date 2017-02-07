#!/usr/bin/env python

import pandas as pd
import argparse
import subprocess
import iwUtilities
import numpy as np

def convert_array(iras_coordinates, r_max, a_max):

     coordinates_ilps = coordinates_iras

     for ii, jj in enumerate(coordinates_iras):          
          coordinates_ilps[ii,0:3] = [ r_max-jj[0], a_max - jj[1],  jj[2] ]

     return coordinates_ilps


#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #
     
     parser = argparse.ArgumentParser(prog='iwCtf_matrices')
     parser.add_argument("iras_filename",      help="CSV filename in RAS image coordinates")
     parser.add_argument("ilps_filename",      help="CSV filename in LPS image coordinates")

     parser.add_argument("--r_max",           help="Maximum index along R direction of RAS", type=int, default=255)
     parser.add_argument("--a_max",           help="Maximum index along A direction of RAS", type=int, default=255)

     parser.add_argument("-v","--verbose",    help="Verbose flag",      action="store_true", default=False )

     inArgs = parser.parse_args()

     #
     # Read in CSV coordinates file
     #

     iwUtilities.verify_that_file_exists(inArgs.iras_filename)

     df_iras = pd.read_csv(inArgs.iras_filename, sep=',',header=0)

     if inArgs.verbose:
          print "Coordinates as defined in " + inArgs.iras_filename 
          print df_iras
          print

     coordinates_iras = np.asarray(df_iras.values)
     coordinates_ilps = convert_array(coordinates_iras, inArgs.r_max, inArgs.a_max)

     
     df_ilps = pd.DataFrame(coordinates_ilps, columns=[ 'x','y','z','t','label', 'comment'])

     if inArgs.verbose:
          print "MEG fiducials in RAS image coordinates"
          print df_ilps
          print

     df_ilps.to_csv(inArgs.ilps_filename, sep=',',header=1, index=False)

