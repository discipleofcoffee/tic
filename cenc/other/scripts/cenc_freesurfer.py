#!/usr/bin/env python

"""

"""
import sys
import os                                               # system functions
import re

import argparse
import iwUtilities as util
import cenc
import imcollective_freesurfer  
import json 

import nipype.interfaces.fsl as fsl
import nipype.interfaces.freesurfer as fs 
from   nipype.pipeline.engine import Workflow, Node


#----------------------------------------------------------------------------------------------------------------------
#
#


def prepare( input_dir ):

     cenc_dirs = cenc.directories( input_dir )

     util.mkcd_dir( [ cenc_dirs['freesurfer']['input']  ])

     input_files = [ os.path.join( cenc_dirs['cenc']['reorient'], 't1w.nii.gz'),
                     os.path.join( cenc_dirs['cenc']['reorient'], 't2flair.nii.gz'),
                     os.path.join( cenc_dirs['cenc']['reorient'], 't2tse.nii.gz')
                     ]

     util.link_inputs( input_files, cenc_dirs['freesurfer']['input'] )

     return


#----------------------------------------------------------------------------------------------------------------------
# Deprecated function use imcollective_freesurfer.methods_recon_all()
#

def recon_all( input_dir ):

     cenc_dirs = cenc.directories( input_dir )

     freesurfer_command = [ 'recon-all', '-sd', cenc_dirs['cenc']['freesurfer_subjects_dir'],'-subjid', cenc_dirs['cenc']['id'],
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


def results( input_dir, verbose):

     cenc_dirs = cenc.directories( input_dir )
     cenc_freesurfer_dir = cenc_dirs['freesurfer']['mri']


     util.mkcd_dir( [ cenc_dirs['results']['dirs']['root'],
                      cenc_dirs['results']['dirs']['images'],
                      cenc_dirs['results']['dirs']['labels'] 
                      ],
                    True 
                    )

     files_to_convert = [ os.path.join( cenc_freesurfer_dir, 'nu.mgz'),
                          os.path.join( cenc_freesurfer_dir, 'aseg.mgz'),
                          os.path.join( cenc_freesurfer_dir, 'brainmask.mgz'),
                          os.path.join( cenc_freesurfer_dir, 'aparc.a2009s+aseg.mgz'),
                          os.path.join( cenc_freesurfer_dir, 'wmparc.mgz')
                          ]


     # Check if files exist

     if util.check_files(files_to_convert, True) == False:
          sys.exit()

     # Create link to directory

     if not os.path.exists(cenc_dirs['freesurfer']['results']):
          util.force_symbolic_link( cenc_dirs['freesurfer']['mri'], cenc_dirs['freesurfer']['results'])

     # TODO use input node to run this instead of a loop. The trick part is to have the files named correctly. 

     for ii in files_to_convert:
          mc = fs.MRIConvert( in_file  = ii,
                              out_file = os.path.join( cenc_dirs['results']['dirs']['labels'],
                                                       str.replace( os.path.basename(ii),'.mgz','.nii.gz')),
                              out_type = 'niigz'
                              )
          mc.run()

          
          reorient = fsl.Reorient2Std( in_file = mc.inputs.out_file, out_file = mc.inputs.out_file)
          reorient.run()

     # Link nu.nii.gz to results/native/images

     result_files = [ [ os.path.join( cenc_dirs['results']['dirs']['labels'], 'nu.nii.gz'), 
                        os.path.join( cenc_dirs['results']['dirs']['images'], 'nu.nii.gz') ]
                      ]
 
     for ii in result_files:
          util.force_hard_link( ii[0], ii[1])

     
     # Create final brain mask. 

     cenc.create_mask( os.path.join( cenc_dirs['results']['dirs']['labels'], 'brainmask.nii.gz'),         
                       os.path.join( cenc_dirs['results']['dirs']['labels'], 'aparc.a2009s+aseg.nii.gz'), 
                       os.path.join( cenc_dirs['results']['dirs']['labels'], 'mask.nii.gz')
                       )



     # Create macroscopic labels

     util.iw_subprocess( ['cenc_aseg_labels.sh'], True, True, False)


def status_run( input_dir, verbose ):

     cenc_dirs = cenc.directories( input_dir )

     result_files = [ os.path.join( cenc_dirs['freesurfer']['mri'], 'wmparc.mgz') ]
     freesurfer_status_run = util.check_files(result_files, False)

     if verbose:
          print( cenc_dirs['cenc']['id'] + ', cenc_freesurfer,     run, ' + str(freesurfer_status_run) )

     return freesurfer_status_run


def status_results( input_dir, verbose ):

     cenc_dirs = cenc.directories( input_dir )

     result_files = [ os.path.join( cenc_dirs['results']['dirs']['labels'], 'gm.left_subcortical.nii.gz' ),
                      os.path.join( cenc_dirs['results']['dirs']['labels'], 'gm.right_subcortical.nii.gz'),
                      os.path.join( cenc_dirs['results']['dirs']['labels'], 'gm.cerebral_cortex.nii.gz'  ),
                      os.path.join( cenc_dirs['results']['dirs']['labels'], 'gm.cerebellum_cortex.nii.gz'),
                      os.path.join( cenc_dirs['results']['dirs']['labels'], 'wm.cerebral.nii.gz'         ),
                      os.path.join( cenc_dirs['results']['dirs']['labels'], 'wm.cerebellum.nii.gz'       ),
                      os.path.join( cenc_dirs['results']['dirs']['labels'], 'nu.nii.gz'       ),
                      os.path.join( cenc_dirs['results']['dirs']['images'], 'nu.nii.gz'       ),
                      os.path.join( cenc_dirs['results']['dirs']['images'], 'nu_brain.nii.gz'       )
                      ]

     freesurfer_status_results = util.check_files(result_files, False)

     if verbose:
          print( cenc_dirs['cenc']['id'] + ', cenc_freesurfer, results, ' + str(freesurfer_status_results) )

     return freesurfer_status_results


def main():
    ## Parsing Arguments
    #
    #

    usage = "usage: %prog [options] arg1 arg2"

    parser = argparse.ArgumentParser(prog='cenc_freesurfer')

    parser.add_argument("--in_dir", help="Participant directory", default=os.getcwd())

    parser.add_argument("--prepare", help="Gather necessary inputs for Freesurfer analysis", action="store_true",
                        default=False)
    parser.add_argument("--methods", help="Freesurfer methods", nargs='*', choices=['recon-all', 'edit_pial'],
                        default=[None])
    parser.add_argument("--qa_methods", help="QA methods", nargs='*', choices=['recon-all', 'edit_pial'],
                        default=[None])
    parser.add_argument("--results", help="Gather Freesurfer results", action="store_true", default=False)
    parser.add_argument("--results_force", help="Gather Freesurfer results", action="store_true", default=False)
    parser.add_argument("--status", help="Status check. choices=['run', 'results']", nargs='*',
                        choices=['results', 'run', 'all'], default=[None])

    #     parser.add_argument("--status",           help="Check Freesurfer status",  action="store_true", default=False )
    #     parser.add_argument("--status_run",       help="Check Freesurfer run status",  action="store_true", default=False )
    #     parser.add_argument("--status_results",   help="Check Freesurfer results status",  action="store_true", default=False )

    parser.add_argument('-v', '--verbose', help="Verbose flag", action="store_true", default=False)

    inArgs = parser.parse_args()

    #

    cenc_dirs = cenc.directories(inArgs.in_dir)

    fs_info = imcollective_freesurfer.get_info(cenc_dirs['cenc']['id'],
                                               cenc_dirs['freesurfer']['subjects_dir'],
                                               cenc_dirs['freesurfer']['t1w'],
                                               cenc_dirs['freesurfer']['t2w'],
                                               cenc_dirs['freesurfer']['flair']
                                               )

    if inArgs.verbose:
        print(json.dumps(fs_info, indent=4, ensure_ascii=True, sort_keys=False))

    #
    # Prepare
    #

    if inArgs.prepare:
        prepare(inArgs.in_dir)

    #
    # Methods
    #

    if 'recon-all' in inArgs.methods:
        imcollective_freesurfer.methods_recon_all(fs_info, inArgs.verbose)

    if 'edit_pial' in inArgs.methods:
        imcollective_freesurfer.methods_recon_edit_pial(fs_info, inArgs.verbose)

    #
    # QA
    #

    if 'recon' in inArgs.qa_methods:
        imcollective_freesurfer.qa_methods_recon(fs_info, inArgs.verbose)

    if 'edit_pial' in inArgs.qa_methods:
        imcollective_freesurfer.qa_methods_edit_pial(fs_info, inArgs.verbose)

    #
    # Results
    #


    if inArgs.results:

        if status_run(inArgs.in_dir, False):

            if not status_results(inArgs.in_dir, False) or inArgs.results_force:
                results(inArgs.in_dir, inArgs.verbose)
            else:

                print(cenc_dirs['cenc']['id'] + ': cenc_freesurfer.py --results has already been run')
                sys.exit()
        else:
            print(cenc_dirs['cenc']['id'] + ': cenc_freesurfer.py --run has not completed or still needs to be run')
            sys.exit()

    #
    # Status
    #

    if 'run' in inArgs.status or 'all' in inArgs.status:
        status_run(inArgs.in_dir, True)

    if 'results' in inArgs.status or 'all' in inArgs.status:
        status_results(inArgs.in_dir, True)


#
# Main Function
#

if __name__ == "__main__":
    sys.exit(main())

