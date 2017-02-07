#!/usr/bin/env python

"""

"""

import sys      
import os                                               # system functions
import re
import tarfile
import glob

import argparse
import iwUtilities as util

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
     parser.add_argument("--nifti_dir",  help="NIFTI data directory", default = './data/nifti')
     parser.add_argument("--dicom_dir",  help="NIFTI data directory", default = './data/dicom')
     parser.add_argument("--out_dir",    help="NIFTI data directory", default = './data/fmri')
     parser.add_argument("--tarball",    help="tarball name", default = None)

     inArgs = parser.parse_args()

     #
     #
     #

     in_dir =  os.path.abspath(inArgs.in_dir)     

     id = util.extract_participant_id( in_dir,'34P1\d{3}')

     participant_dir = os.path.abspath( os.path.join(inArgs.cenc_dir, id))

     nifti_dir = util.path_relative_to( participant_dir, inArgs.nifti_dir  )
     dicom_dir = util.path_relative_to( participant_dir, inArgs.dicom_dir  )
     out_dir   = util.path_relative_to( participant_dir, inArgs.out_dir    )

     if  not inArgs.tarball == None:
          tarball_filename = inArgs.tarball
     else:
          tarball_filename =  id + '_fmri.tar.gz'

     if os.path.isfile( os.path.join( out_dir, tarball_filename )):
          sys.exit('fMRI tarball already exists for ' + id + '.');
          

     # Create Output Directory if it doesn't exist

     files = [  os.path.abspath( os.path.join( dicom_dir, 'dcmConvertAll.cfg')), 
                os.path.abspath( os.path.join( dicom_dir, 'dcmConvert_cenc.cfg')), 
                os.path.abspath( os.path.join( nifti_dir, 'rest.nii.gz'))
                ]

     util.mkcd_dir( out_dir )
     util.link_inputs( files, out_dir )

     files_to_be_tarred = glob.glob('*')

     # Create TarBall

     tarball = tarfile.open( tarball_filename, 'w:gz')
     
     for f in files_to_be_tarred: 
          tarball.add(f)

     tarball.close()

     # Clean Directory

     for ii in files_to_be_tarred:
          os.remove( ii )
     
