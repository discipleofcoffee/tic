#!/usr/bin/env python

import sys      
import os                                               # system functions
import shutil

import subprocess
import argparse
import iwUtilities     as util

import nibabel as nb
import pandas  as pd
import numpy   as np

import iwCtf         as ctf


#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #
     
     parser = argparse.ArgumentParser(prog='iwCtf_transform_image')
               
     parser.add_argument("in_image",              help="Filename of input image CTF, Native, or Template space", nargs=1 )
     parser.add_argument("in_coordinate_system",  help="In coordinate system", choices=['ctf', 'native', 'template'], nargs=1)
     parser.add_argument("out_coordinate_system", help="Out coordinate system", choices=['ctf', 'native', 'template'], nargs=1)
     parser.add_argument("out_image",             help="Filename of output image", nargs=1 )
     parser.add_argument("reference_image",       help="Filename of reference image", nargs=1 )

     parser.add_argument("-n", "--interpolation",  help="Interpolation method. If you need finer control over interpolation use antsApplyTransforms directory",
                         default = 'HammingWindowedSinc', 
                         choices=[ 'Linear','NearestNeighbor','MultiLabel',
                                   'Gaussian','BSpline',
                                   'CosineWindowedSinc','WelchWindowedSinc','HammingWindowedSinc','LanczosWindowedSinc' 
                                   ]
                         )

     parser.add_argument("--native_to_template", help="Native to Template transforms." 
                         + "default=[ native_to_template_affine.mat, native_to_template_warp.nii.gz )",
                         nargs=2,
                         default=[ 'native_to_template_affine.mat', 'native_to_template_warp.nii.gz' ] )

     parser.add_argument("--template_to_native", help="Template to Native transforms." 
                         + "default=[ template_to_native_affine.mat, template_to_native_warp.nii.gz ] )",
                         nargs=2,
                         default=[ 'template_to_native_affine.mat', 'template_to_native_warp.nii.gz' ] )

     parser.add_argument("--native_to_ctf",       help="Filename for affine matrix LPS world to CTF world coordinates",    default='affine_wlps_to_wctf.txt' )

     parser.add_argument("-v","--verbose",    help="Verbose flag",      action="store_true", default=False )
     parser.add_argument("--debug",           help="Debug flag",      action="store_true", default=False )

     inArgs = parser.parse_args()
     
     #
     #
     #

     util.print_stage("Displaying inputs to iwCtf_transform_image", inArgs.debug )

     if inArgs.debug:
          print
          print "inArgs.in_image   = " +  str(inArgs.in_image)
          print "inArgs.out_image  = " +  str(inArgs.out_image)
          print
          print "inArgs.native_to_ctf  = " + inArgs.native_to_ctf
          print
          print "inArgs.verbose        = " +  str(inArgs.verbose)

     exit()

     in_coordinate_system  = inArgs.in_coordinate_system[0].lower()
     out_coordinate_system = inArgs.out_coordinate_system[0].lower()

     template_to_native    = inArgs.template_to_native
     native_to_template    = inArgs.native_to_template

     # antsApplyTransformToPoints use the inverse transforms of that used by antsApplyTransformToPoints


     native_to_ctf_transforms     = [ inArgs.native_to_ctf ]

     ctf_to_native_transforms     =  [ "[", inArgs.native_to_ctf, ",", "1", "]" ]

     native_to_template_transforms = [ native_to_template[1], native_to_template[0] ]

     ctf_to_template_transforms    =  native_to_template_transforms + ctf_to_native_transforms

     template_to_native_transforms = [ template_to_native[0], template_to_native[1] ]

     template_to_ctf_transforms    = native_to_ctf_transforms + template_to_native_transforms 

     if inArgs.debug:
          ctf_to_native_transforms
          native_to_ctf_transforms


     if  in_coordinate_system == 'ctf':

          if out_coordinate_system == 'ctf':
               sys.exit('CTF to CTF not allowed.')

          elif out_coordinate_system == 'native':

               ctf.transform_image( inArgs.in_image, inArgs.out_image, inArgs.reference_image, ctf_to_native_transforms,    inArgs.interpolation, inArgs.verbose, inArgs.debug)

          elif out_coordinate_system == 'template':

               ctf.transform_image( inArgs.in_image, inArgs.out_image, inArgs.reference_image, ctf_to_template_transforms,    inArgs.interpolation, inArgs.verbose, inArgs.debug)

          else:
               sys.exit('Unknown transform')


     if  in_coordinate_system == 'native':

          if out_coordinate_system == 'ctf':

               ctf.transform_image( inArgs.in_image, inArgs.out_image, inArgs.reference_image, 
                                    native_to_ctf_transforms,  inArgs.interpolation, inArgs.verbose, inArgs.debug)

          elif out_coordinate_system == 'native':
               sys.exit('Native to Native not allowed.')

          elif out_coordinate_system == 'template':

               ctf.transform_image( inArgs.in_image, inArgs.out_image, inArgs.reference_image,
                                     native_to_template_transforms,    inArgs.interpolation, inArgs.verbose, inArgs.debug)

          else:               
               sys.exit('Unknown transform')
          


     if  in_coordinate_system == 'template':

          if out_coordinate_system == 'ctf':
               ctf.transform_image( inArgs.in_image, inArgs.out_image, inArgs.reference_image, 
                                     template_to_ctf_transforms, inArgs.interpolation, inArgs.verbose, inArgs.debug)
          
          elif out_coordinate_system == 'native':

               ctf.transform_image( inArgs.in_image, inArgs.out_image, inArgs.reference_image, 
                                     template_to_native_transforms,  inArgs.interpolation, inArgs.verbose, inArgs.debug)

          elif out_coordinate_system == 'template':
               sys.exit('Template to Template not allowed.')
               
          else:
               sys.exit('Unknown transform')
