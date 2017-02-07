#!/usr/bin/env python

"""

"""
import sys
import os                                               # system functions
import re

import argparse
import iwUtilities as util
import cenc

import nipype.interfaces.fsl as fsl
import nipype.interfaces.freesurfer as fs 
from   nipype.pipeline.engine import Workflow, Node


def main():
     ## Parsing Arguments
     #
     #

     usage = "usage: %prog [options] arg1 arg2"

     parser = argparse.ArgumentParser(prog='cenc_freesurfer')

     parser.add_argument("--in_dir",       help="Participant directory", default = os.getcwd() )

     parser.add_argument("--cenc_data_dir",   help="CENC data directory", default = os.getenv('CENC_MRI_DATA')) 
     parser.add_argument("--cenc_freesurfer_dir",   help="CENC data directory", default = os.getenv('CENC_SUBJECTS_DIR')) 
     parser.add_argument("--cenc_results_dir",   help="CENC results directory", default = './results/native') 

     parser.add_argument("--prepare",    help="Gather necessary inputs for Freesurfer analysis", action="store_true", default=False )
     parser.add_argument("--run",        help="Freesurfer recon-all", action="store_true", default=False )
     parser.add_argument("--results",    help="Gather Freesurfer results",  action="store_true", default=False )

     parser.add_argument('-v','--verbose', help="Verbose flag",  action="store_true", default=False )


     inArgs = parser.parse_args()

     #
     #
     #
     
     cenc_participant_id, cenc_participant_dir = cenc.participant_id( inArgs.in_dir )

     cenc_freesurfer_dir = os.path.abspath( inArgs.cenc_freesurfer_dir )
     cenc_results_dir = os.path.abspath( os.path.join( cenc_participant_dir, inArgs.cenc_results_dir) )

     if inArgs.prepare:
          prepare( cenc_participant_dir )

     if inArgs.run:
          recon_all( cenc_participant_id, cenc_freesurfer_dir)

     if inArgs.results:
          results(cenc_participant_id, cenc_participant_dir,  cenc_freesurfer_dir, cenc_results_dir, 
                  inArgs.verbose)


def prepare( cenc_participant_dir ):

     freesurfer_input_dir = os.path.join( cenc_participant_dir, 'freesurfer', 'input' )

     util.mkcd_dir( [ freesurfer_input_dir ])

     input_files = [ os.path.join( cenc_participant_dir, 'reorient', 't1w.nii.gz'),
                     os.path.join( cenc_participant_dir, 'reorient', 't2flair.nii.gz'),
                     os.path.join( cenc_participant_dir, 'reorient', 't2tse.nii.gz')
                     ]

     util.link_inputs( input_files, freesurfer_input_dir)

     return



def recon_all( cenc_participant_id, cenc_freesurfer_dir ):

     freesurfer_command = [ 'recon-all', '-sd', cenc_freesurfer_dir,'-subjid', cenc_participant_id, 
                            '-all', '-i', 't1w.nii.gz',
                            '-T2', 't2tse.nii.gz',
                            '-FLAIR', 't2flair.nii.gz',
                            '-qcache',
                            '-measure', 'thickness',
                            '-measure', 'curv',
                            '-measure', 'sulc',
                            '-measure', 'area',
                            '-measure', 'jacobian_white'
                            ]

     util.iw_subprocess( freesurfer_command, True, True, True)

     return


def results(cenc_participant_id,  cenc_participant_dir, cenc_freesurfer_dir,cenc_results_dir, verbose):

     util.mkcd_dir( [ cenc_results_dir ], True)

     files_to_convert = [ os.path.join( cenc_freesurfer_dir, cenc_participant_id, 'mri', 'nu.mgz'),
                          os.path.join( cenc_freesurfer_dir, cenc_participant_id, 'mri', 'aseg.mgz'),
                          os.path.join( cenc_freesurfer_dir, cenc_participant_id, 'mri', 'brainmask.mgz'),
                          os.path.join( cenc_freesurfer_dir, cenc_participant_id, 'mri', 'aparc.a2009s+aseg.mgz'),
                          os.path.join( cenc_freesurfer_dir, cenc_participant_id, 'mri', 'wmparc.mgz')
                          ]

     # Check if files exist

     print files_to_convert

     if util.check_files(files_to_convert, True) == False:
          sys.exit()

     # Create link to directory

     freesurfer_results_dir =  os.path.abspath(os.path.join( cenc_participant_dir, 'freesurfer','results'))

     if not os.path.exists(freesurfer_results_dir):
          util.force_symbolic_link( os.path.join( cenc_freesurfer_dir,  cenc_participant_id ), freesurfer_results_dir)

     # TODO use input node to run this instead of a loop

     mc = Node( fs.MRIConvert( out_type = 'niigz'
                               ),
                name="mri_convert"
                )  
       
     mc.iterables = ( "in_file", files_to_convert )

     reorient = Node( fsl.Reorient2Std(), name="reorient" )

     workflow_convert = Workflow(name='cenc_freesurfer_nipype_workflow')
     workflow_convert.base_dir = cenc_results_dir
     
     workflow_convert.connect( [ (mc,       reorient, [('out_file', 'in_file')] )]
                               )    
     workflow_convert.run()
     
     # Create final brain mask. This takes forever. Speeding it up would be helpful. 

     cenc.create_mask( os.path.join( cenc_results_dir, 'brainmask.nii.gz'),         
                       os.path.join( cenc_results_dir, 'aparc.a2009s+aseg.nii.gz'), 
                       os.path.join( cenc_results_dir, 'mask.nii.gz')
                       )

#
# Main Function
#

if __name__ == "__main__":
    sys.exit(main())

