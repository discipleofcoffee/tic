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

     parser.add_argument("--a_max",           help="Maximum index along A direction of RAS", default=255)
     parser.add_argument("--s_max",           help="Maximum index along S direction of RAS", default=255)

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

     coordinates_iras = np.asarray(df.values)
     
     coordinates_ilps = coordinates_iras

     for ii, jj in enumerate(coordinates_iras):          

          coordinates_ilps[ii,0:2] = [ coordinates_iras[1],  inArgs.p_max-coordinates_iras[0], inArgs.s_max-coordinates_iras[2] ]
          print ii, jj
     

     print coordinates_ilps

     exit()
     #
     # Convert MEG fiducials from icsa to wlps
     #

     lpa_iras = 
     nas_iras = [ nas_icsa[1],  255-nas_icsa[0], 255-nas_icsa[2] ]
     rpa_iras = [ rpa_icsa[1],  255-rpa_icsa[0], 255-rpa_icsa[2] ]

     wlps_list  = [
                 reduce(lambda x, y: x+y, [ lpa_iras,  df.values[0,3:6].tolist()  ]),
                 reduce(lambda x, y: x+y, [ nas_iras,  df.values[1,3:6].tolist()  ]),
                 reduce(lambda x, y: x+y, [ rpa_iras,  df.values[2,3:6].tolist()  ]) ]

     df_iras = pd.DataFrame(wlps_list, columns=[ 'x','y','z','t','label', 'comment'])

     if inArgs.verbose:
          print "MEG fiducials in RAS image coordinates"
          print df_iras
          print

     df_iras.to_csv(inArgs.meg_iras, sep=',',header=1, index=False)

     #
     # Calculate RAS Image to LPS Worls matrix 
     #


     img_affine_matrix_lps = np.multiply( affine_wras_to_wlps,  img_affine_matrix_ras)
     
     lpa_wras = np.dot(img_affine_matrix_ras, np.concatenate( (lpa_iras, [1]) ))
     nas_wras = np.dot(img_affine_matrix_ras, np.concatenate( (nas_iras, [1]) ))
     rpa_wras = np.dot(img_affine_matrix_ras, np.concatenate( (rpa_iras, [1]) ))

     lpa_wlps = np.dot(affine_wras_to_wlps, lpa_wras )
     nas_wlps = np.dot(affine_wras_to_wlps, nas_wras )
     rpa_wlps = np.dot(affine_wras_to_wlps, rpa_wras )

     [ rotate_ctf, translate_ctf, origin_ctf ] = ctf_calc_rotate_translate_origin( nas_wlps, lpa_wlps, rpa_wlps, ctf_scale)
          
     affine_ctf = ctf_calc_affine( rotate_ctf, translate_ctf, 0*origin_ctf)

     if inArgs.verbose:
         print
         print "Image LPS World to CTF matrix"
         print affine_ctf
         print

     iwUtilities.save_itk_affine_matrix( affine_ctf, inArgs.wlps_to_wctf )


     #
     # Save MEG Fiducials in LPS World space. 
     #

     iwUtilities.verify_that_file_exists(inArgs.meg_iras)
     iwUtilities.verify_that_file_exists(inArgs.iras_to_wras)
     iwUtilities.verify_that_file_exists(inArgs.wras_to_wlps)

     cmd = [ "antsApplyTransformsToPoints", "-d", "3", "-i", inArgs.meg_iras, "-o", inArgs.meg_wlps, "-t", inArgs.iras_to_wras, inArgs.wras_to_wlps ]
     iwUtilities.iw_subprocess(cmd, inArgs.verbose, True )

