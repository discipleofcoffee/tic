#!/usr/bin/env python

"""

"""

import sys      
import os                                               # system functions
import re
import glob

import argparse
import iwUtilities as util
import gzip

#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #

     usage = "usage: %prog [options] arg1 arg2"

     parser = argparse.ArgumentParser(prog='cenc_fmri_gather')
     parser.add_argument("in_dir",       help="Participant directory" )
     parser.add_argument("--cenc_dir",   help="CENC data directory", default = os.getenv('CENC_MRI_DATA')) 
     parser.add_argument("--out_dir",   help="CENC data directory", default = './structural/wmlesions/' ) 
     parser.add_argument("--reorient_dir",  help="NIFTI data directory", default = './reorient/')

     inArgs = parser.parse_args()

     #
     #
     #

     in_dir =  os.path.abspath(inArgs.in_dir)     

     id = util.extract_participant_id( in_dir,'34P1\d{3}')

     participant_dir = os.path.abspath( os.path.join(inArgs.cenc_dir, id))
     reorient_dir    = util.path_relative_to( participant_dir, inArgs.reorient_dir  )

     wm_lesions_dir       = util.path_relative_to( participant_dir, inArgs.out_dir  )
     wm_lesions_input_dir = os.path.join( wm_lesions_dir, 'input')
     wm_lesions_lpa_dir   = os.path.join( wm_lesions_dir, '01-lst_lpa')
     wm_lesions_lga_dir   = os.path.join( wm_lesions_dir, '02-lst_lga')

     # Create Output Directory if it doesn't exist

     files = [  os.path.abspath( os.path.join( reorient_dir, 't1w.nii.gz')), 
                os.path.abspath( os.path.join( reorient_dir, 't2flair.nii.gz')) 
                ]

     util.mkcd_dir( os.path.join(  wm_lesions_input_dir ) )
     util.link_inputs( files, wm_lesions_input_dir )

     #
     
     util.mkcd_dir( os.path.join(  wm_lesions_lpa_dir), False )

     util.mkcd_dir( os.path.join(  wm_lesions_lga_dir), True )
     util.copy_inputs( files, wm_lesions_lga_dir )

     for ii in glob.glob('*.gz'):
          os.system('gunzip ' + ii)

     util.link_inputs( glob.glob('*.nii'), wm_lesions_lpa_dir )

     
