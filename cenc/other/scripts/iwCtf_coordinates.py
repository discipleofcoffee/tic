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


def save_affine_voxel_to_world(in_filename, out_affine_filename):
     
     import numpy as np
     import nibabel as nib

     try:
          with open(in_filename) as file:
              img           = nib.load(in_filename)
              print img.get_affine()

              iwUtilities.save_itk_affine_matrix( img.get_affine(), out_affine_filename)
          
     except IOError as e:
          print
          raise e

def ctf_calc_affine(in_rotate, in_translate, in_origin):

     affine_ctf          = np.zeros((4,4))
     affine_ctf[3,3]     = 1 
     affine_ctf[0:3,0:3] = rotate_ctf
     affine_ctf[0:3,3]   = translate_ctf

     return affine_ctf


def ctf_calc_rotate_translate_origin( in_nas,  in_lpa, in_rpa, in_scale=1 ):

    nas = np.array( [ in_nas[0], in_nas[1], in_nas[2] ] )
    rpa = np.array( [ in_rpa[0], in_rpa[1], in_rpa[2] ] )
    lpa = np.array( [ in_lpa[0], in_lpa[1], in_lpa[2] ] )
    
    origin_ctf = 0.5 * (rpa+lpa)
    x_ctf = norm(nas - origin_ctf)
    z_ctf = norm( np.cross( x_ctf, lpa-rpa))
    y_ctf = norm( np.cross( z_ctf, x_ctf))
    
    rotate_ctf    = in_scale * np.matrix( [x_ctf, y_ctf, z_ctf ]).getT().getI()
    translate_ctf = -np.dot(rotate_ctf, origin_ctf)

    return [rotate_ctf, translate_ctf, origin_ctf ]


def norm(x):

     x_norm = np.linalg.norm(x)

     if not x_norm == 0:
          return x/x_norm
     else:
          print "Error: norm of vector is 0"
          quit()

#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #
     
     parser = argparse.ArgumentParser(prog='iwCtf_matrices')
               
     parser.add_argument("image",           help="CTF reference image" )
     parser.add_argument("meg_icsa",        help="MEG fiducials (CSA image space)" )

     parser.add_argument("--meg_iras",      help="Output filename MEG fiducials in LPS World space", default='fiducials_meg_iras.csv' )
     parser.add_argument("--meg_wlps",      help="Output filename MEG fiducials in LPS World space", default='fiducials_meg_wlps.csv' )

     parser.add_argument("--wlps_to_wctf",       help="Filename for affine matrix LPS world to CTF world coordinates",    default='affine_wlps_to_ctf.txt' )
     parser.add_argument("--iras_to_wras",       help="Filename for affine matrix RAS image to RAS world coordinates",    default='affine_icsa_to_wras.txt' )

     parser.add_argument("--wras_to_wlps",         help="Filename for affine matrix RAS world to LPS world coordinates", default='affine_wras_to_wlps.txt' )

     parser.add_argument("--ctf_scale",    help="CTF scale from index to physical units [cm^3]. Assume isotropic. (default=0.1 [cm^3]) ",
                                           type=float, default=.1)
    
     parser.add_argument("-v","--verbose",    help="Verbose flag",      action="store_true", default=False )

     inArgs = parser.parse_args()
     
     if inArgs.verbose:
          print "inArgs.image          = " +  str(inArgs.image)
          print "inArgs.meg_icsa       = "  +  str(inArgs.meg_icsa)
          print "inArgs.meg_iras       = "  +  str(inArgs.meg_iras)
          print "inArgs.meg_wlps       = "  +  str(inArgs.meg_wlps)
          print "inArgs.iras_to_wras   = " +  str(inArgs.iras_to_wras)
          print "inArgs.wras_to_wlps   = " +  str(inArgs.wras_to_wlps)
          print "inArgs.wlps_to_wctf   = " +  str(inArgs.wlps_to_wctf)
          print "inArgs.verbose        = " +  str(inArgs.verbose)
    
     #
     # Check inputs
     #     

     iwUtilities.verify_that_file_exists(inArgs.image)
     iwUtilities.verify_that_file_exists(inArgs.meg_icsa)

     img           = nib.load(inArgs.image)
     header        = img.get_header()

     img_affine_matrix_ras = np.asarray(img.get_affine())
     data_shape        = np.asarray( header.get_data_shape() )
     data_pixel_size   = np.asarray( header.get_zooms()      )

     if not np.all( data_shape ==  256 ):
         print
         print inArgs.image + "\'s data shape is " + str(data_shape)
         print "It must be [ 256 256 256 ]. Zero pad image accordingly before continuing."
         print
         exit()

     if not np.all(data_pixel_size == data_pixel_size[0]):
         print
         print inArgs.img + "pixel dimensions must be isotropic."
         print data_pixel_size
         print
         exit()


     ctf_scale = inArgs.ctf_scale

     #
     # Save ITK affine matrix
     #

     if inArgs.verbose:
         print
         print "Image affine RAS image to RAS world  matrix"
         print img_affine_matrix_ras
         print

     iwUtilities.save_itk_affine_matrix( img_affine_matrix_ras, inArgs.iras_to_wras )

     #          
     #
     #

     affine_wras_to_wlps = np.asarray([[ -1, 0, 0, 0], [0, -1, 0, 0], [0,0,1,0], [0,0,0,1]])
     
     iwUtilities.save_itk_affine_matrix( affine_wras_to_wlps, inArgs.wras_to_wlps )

     #
     # Save CSA to LPS affine matrix
     #

     df=pd.read_csv(inArgs.meg_icsa, sep=',',header=0)

     if inArgs.verbose:
          print "MEG fiducials as defined in " + inArgs.meg_icsa 
          print df
          print
         
     lpa_icsa = np.asarray(df.values[0,0:3])
     nas_icsa = np.asarray(df.values[1,0:3])
     rpa_icsa = np.asarray(df.values[2,0:3])

     if not ( (lpa_icsa[1] < nas_icsa[1]) and (nas_icsa[1] < rpa_icsa[1])  ):
         print
         print 'Fiducials must be listed left to right in MEG fiducial file'
         print
         print df.values
         print
         exit()

     if not ( (nas_icsa[0] < lpa_icsa[0]) and (nas_icsa[0] < rpa_icsa[0])  ):
         print
         print 'Nasion point coronal index must be less than LPA and RPA coronal index'
         print
         print df.values
         print
         exit()

     if not np.all( np.less( lpa_icsa, 256*np.ones(3) ) ):
         print
         print 'All image indices for LPA fiducial must be less than 255'
         print df.values[0]
         print
         exit()

     if not np.all( np.less( nas_icsa, 256*np.ones(3) ) ):
         print
         print 'All image indices for Nasion fiducial must be less than 255'
         print df.values[1]
         print
         exit()

     if not np.all( np.less( rpa_icsa, 256*np.ones(3) ) ):
         print
         print 'All image indices for RPA fiducial must be less than 255'
         print df.values[2]
         print
         exit()

     #
     # Convert MEG fiducials from icsa to wlps
     #

     lpa_iras = [ lpa_icsa[1],  255-lpa_icsa[0], 255-lpa_icsa[2] ]
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

