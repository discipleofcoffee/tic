#!/usr/bin/env python

import sys      
import os                                               # system functions
import shutil

import argparse
import iwUtilities     as util
import iwCtf        as ctf

import nibabel as nb
import pandas as pd
import numpy as np



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


def ctf_matrix( in_fiducials, out_ctf_matrix, ctf_scale=0.1 ):

     df=pd.read_csv( in_fiducials, sep=',',header=0)

     lpa = np.asarray(df.values[0,0:3])
     nas = np.asarray(df.values[1,0:3])
     rpa = np.asarray(df.values[2,0:3])

     [ rotate_ctf, translate_ctf, origin_ctf ] = ctf_calc_rotate_translate_origin( nas, lpa, rpa, ctf_scale)
                    
     affine_wlps_to_wctf = ctf_calc_affine( rotate_ctf, translate_ctf, 0*origin_ctf)
     
     util.write_itk_affine_matrix( affine_wlps_to_wctf, [0,0,0], out_ctf_matrix, inArgs.verbose )




#
# Main Function
#

if __name__ == "__main__":


     ## Parsing Arguments
     #
     #
     
     parser = argparse.ArgumentParser(prog='iwCtf_icsa_to_wlps')
               
     parser.add_argument("in_fiducials",        help="CSV input points" )
     parser.add_argument("out_ctf_matrix",      help="CSV output points" )

     parser.add_argument("--ctf_scale",    help="CTF scale factor",    type=float, default=1)

     parser.add_argument("-v","--verbose",      help="Verbose flag",      action="store_true", default=False )
     parser.add_argument("--debug",             help="Debug   flag",      action="store_true", default=False )

     inArgs = parser.parse_args()

     util.verify_inputs( [ inArgs.in_fiducials ], inArgs.debug)

     #
     # Display initial points if asked
     #

     if inArgs.verbose:
          ctf.print_points_from_file(inArgs.in_fiducials, inArgs.verbose)


     df=pd.read_csv(inArgs.in_fiducials, sep=',',header=0)

     lpa = np.asarray(df.values[0,0:3])
     nas = np.asarray(df.values[1,0:3])
     rpa = np.asarray(df.values[2,0:3])

     [ rotate_ctf, translate_ctf, origin_ctf ] = ctf_calc_rotate_translate_origin( nas, lpa, rpa, inArgs.ctf_scale)
                    
     affine_wlps_to_wctf = ctf_calc_affine( rotate_ctf, translate_ctf, 0*origin_ctf)
     
     util.write_itk_affine_matrix( affine_wlps_to_wctf, [0,0,0], inArgs.out_ctf_matrix, inArgs.verbose )
