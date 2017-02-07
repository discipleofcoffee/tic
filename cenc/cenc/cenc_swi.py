#!/usr/bin/env python2

"""

"""
import sys
import os                                               # system functions
import re
import pandas
import json
import argparse
import _utilities as util
import cenc
import labels
import datetime
from collections import OrderedDict
import getpass
import subprocess
import shutil

def swi_config(in_dir, verbose=False):

     config = {'dirs': { 'input': os.path.abspath(in_dir), 
                         'working': os.path.abspath( os.path.join( in_dir, '..','methods') )
                         },

               'inputs': { 't1w': os.path.abspath(os.path.join(in_dir, 'nu.nii.gz')), 
                           't1w_brain': os.path.abspath(os.path.join(in_dir, 'nu_brain.nii.gz')), 
                           'swi': os.path.abspath(os.path.join(in_dir, 'swi.nii.gz')), 
                           'swi_magnitude': os.path.abspath(os.path.join(in_dir, 'swi_magnitude.nii.gz')), 
                           'swi_phase': os.path.abspath(os.path.join(in_dir, 'swi_phase.nii.gz'))
                           } 


               }

     dirs =  { 'input':   config['dirs']['input'],
               'working': config['dirs']['working'],
               'methods': { 'input'   : os.path.join( config['dirs']['working'], 'input'), 
                            '01-register': os.path.join( config['dirs']['working'], '01-register'), 
                            'results'   : os.path.join( config['dirs']['working'], 'results') 
                            } 
               }

     methods_00_input = { 'dir':os.path.join( config['dirs']['working'], 'input'), 

                           'inputs': [  config['inputs']['t1w'],
                                        config['inputs']['t1w_brain'],
                                        config['inputs']['swi'],
                                        config['inputs']['swi_magnitude'],
                                        config['inputs']['swi_phase']
                                        ],

                           'outputs': [ os.path.join( dirs['methods']['input'], 'nu.nii.gz'), 
                                        os.path.join( dirs['methods']['input'], 'nu_brain.nii.gz'),
                                        os.path.join( dirs['methods']['input'], 'swi.nii.gz'),
                                        os.path.join( dirs['methods']['input'], 'swi_magnitude.nii.gz'),
                                        os.path.join( dirs['methods']['input'], 'swi_phase.nii.gz')
                                        ]
                           }


     methods_01_register = { 'dir': dirs['methods']['01-register'],

                             'inputs': methods_00_input['outputs'],
                                                                                         
                             'outputs': [ os.path.join( dirs['methods']['01-register'], 'swi_Affine_nu__swi_magnitude_0GenericAffine.mat'),
                                          os.path.join( dirs['methods']['01-register'], 'swi_Affine_nu__swi_magnitude.nii.gz'),
                                          os.path.join( dirs['methods']['01-register'], 'swi_Affine_nu__swi_phase.nii.gz'),
                                          os.path.join( dirs['methods']['01-register'], 'swi_Affine_nu__swi.nii.gz')
                                          ]
                           }

     methods_results = { 'dir': dirs['methods']['02-stats'],

                          'inputs': methods_00_input['outputs'],
                          
                          'outputs': [ os.path.join( dirs['methods']['01-register'], 't2flair_Affine_nu__t2flair_Warped.nii.gz')
                                       ]
                           }

 
     methods= {'input': methods_00_input, 
               '01-register': methods_01_register,
               'results':methods_results,
                }

     dict  = { 'config': config, 'dirs':dirs, 'methods':methods}
               
     return dict



#=======================================================================================================================
# Prepare

def swi_link_inputs( input_dir, link_to_dir, change_to_dir = True ):

     cenc_dirs = cenc.directories( input_dir )

     util.mkcd_dir( [ link_to_dir ], change_to_dir )

     input_files = cenc_dirs['swi']['inputs']
     label_files = cenc_dirs['swi']['labels']

     util.link_inputs( input_files + label_files, link_to_dir )



def prepare( input_dir, verbose=False ):

     if verbose:
          print('Entering cenc_swi.py prepare')

     cenc_dirs = cenc.directories( input_dir )

     input_files = cenc_dirs['swi']['inputs']
     label_files = cenc_dirs['swi']['labels']

     swi_link_inputs( input_dir, cenc_dirs['swi']['dirs']['input'] )
     swi_link_inputs( input_dir, cenc_dirs['swi']['dirs']['input'] )

     return


#=======================================================================================================================
# Methods

def methods( in_methods, config, verbose=False):

     if '00_input' in in_methods or 'all' in in_methods:
          methods_00_input( config, verbose )
          
     if '01_register' in in_methods or 'all' in in_methods:
          methods_01_register( config, verbose )
               
     if '02_stats' in in_methods or 'all' in in_methods:
          methods_02_stats( config, verbose)



def ants_register(input_file):

     # This simple command appears to work. 
     command = ['antsRegistrationSyNQuick.sh', '-d', '3', '-m', input_file + '.nii.gz', '-r', 'nu.nii.gz',
                '-f', 'nu.nii.gz', '-t', 'a', '-o', 'swi_Affine_nu__' + input_file + '_' 
                ]

     util.iw_subprocess( command, True, True, False)


def ants_apply_transform(input_file):

     # This simple command appears to work. 
     command = ['antsApplyTransforms', '-d', '3', '-i', input_file + '.nii.gz', '-r', 'nu.nii.gz',
                '-o', 'swi_Affine_nu__' + input_file + '.nii.gz', '-t', 'swi_Affine_nu__swi_magnitude_0GenericAffine.mat' 
                ]

     util.iw_subprocess( command, True, True, False)



def methods_00_input( config, verbose ):
     """ Renames inputs from configureation file to standard naming convention"""
    
     if verbose:
          print
          print( config['config']['dirs'] )
          print
          print(config['methods']['input'])
          print

     util.mkcd_dir( [ config['methods']['input']['dir'] ], True)

     input_output_pairs = zip( config['methods']['input']['inputs'],  config['methods']['input']['outputs'] )

     for ii in input_output_pairs:
          os.link( ii[0], ii[1] )


def methods_01_register( input_dir, verbose=False):

     # Register SWI images to nu.nii.gz
     cenc_dirs = cenc.directories( input_dir )
     swi_link_inputs( input_dir, cenc_dirs['swi']['dirs']['register'] )
 
     ants_register('swi_magnitude')

     util.force_hard_link('swi_Affine_nu__swi_magnitude_Warped.nii.gz', 'swi_Affine_nu__swi_magnitude.nii.gz')

     ants_apply_transform('swi')
     ants_apply_transform('swi_phase')

     return


def methods_02_stats(config, verbose=False):

     input_dir = config['dirs']['input']

     util.mkcd_dir( [ config['methods']['results']['dir'] ], True)
     
     command = ['fslmaths', os.path.join( config['dirs']['methods']['01-register'], 'nu_brain.nii.gz'), '-bin',
                os.path.join(config['dirs']['methods']['results'], 'brain_mask.nii.gz')]

     util.iw_subprocess(command, verbose, verbose, False)
     
     for ii in [ 'swi', 'swi_magnitude', 'swi_phase'] :

          command  = ['fslmaths', os.path.join( config['dirs']['methods']['01-register'], 'swi_Affine_nu__' + ii + '.nii.gz'),
                      '-mas', 'brain_mask.nii.gz', ii + '.nii.gz']
          
          util.iw_subprocess(command, verbose, verbose, False)

     util.force_hard_link( os.path.join(config['methods']['input']['dir'], 'nu.nii.gz'), 'nu.nii.gz')
     util.force_hard_link( os.path.join(config['methods']['input']['dir'], 'nu_brain.nii.gz'), 'nu_brain.nii.gz')

#=======================================================================================================================
# Results

def results( input_dir ):
    """ Gather results and write the MagTran JSON output file"""

    cenc_dirs = cenc.directories( input_dir )

    swi_input_dir       = cenc_dirs['swi']['dirs']['input']
    swi_01_register_dir = cenc_dirs['swi']['dirs']['register']
    swi_results_dir     = cenc_dirs['swi']['dirs']['results']

    util.mkcd_dir( [ swi_results_dir ], True)

    result_files = [ [  os.path.join( cenc_dirs['swi']['dirs']['register'], 'swi_Affine_nu__swi_m0_Warped.nii.gz'),
    os.path.join( cenc_dirs['swi']['dirs']['results'],  'swi_Affine_nu__swi_m0.nii.gz')],

    [ os.path.join( cenc_dirs['swi']['dirs']['register'], 'swi_Affine_nu__swi_m1_Warped.nii.gz'),
    os.path.join( cenc_dirs['swi']['dirs']['results'],  'swi_Affine_nu__swi_m1.nii.gz')],

    [ os.path.join( cenc_dirs['swi']['dirs']['results'], 'magtrans.json'),
    os.path.join( cenc_dirs['swi']['dirs']['results'],  'magtrans.json') ],

    [ os.path.join( cenc_dirs['swi']['dirs']['register'], 'swir.nii.gz'),
    os.path.join( cenc_dirs['swi']['dirs']['results'],  'swir.nii.gz') ],

    [ os.path.join( cenc_dirs['swi']['dirs']['input'],    'nu.nii.gz'),
    os.path.join( cenc_dirs['swi']['dirs']['results'],  'nu.nii.gz') ],

    [ os.path.join( cenc_dirs['swi']['dirs']['register'], 'swir.nii.gz'),
    os.path.join( cenc_dirs['results']['dirs']['images'],  'swir.nii.gz') ]
    ]

    for ii in result_files:
        util.force_hard_link( ii[0], ii[1])

    return


def methods_write_json_redcap_swi_instrument(input_dir, verbose):
    """ Write MagTrans Instrument to JSON output file"""

    cenc_dirs = cenc.directories(input_dir)

    swir = os.path.join(cenc_dirs['swi']['dirs']['register'], 'swir.nii.gz')

    labels = [os.path.join(cenc_dirs['swi']['dirs']['input'], 'gm.cerebral_cortex.nii.gz'),
    os.path.join(cenc_dirs['swi']['dirs']['input'], 'gm.subcortical.nii.gz'),
    os.path.join(cenc_dirs['swi']['dirs']['input'], 'wm.cerebral.nii.gz'),
    os.path.join(cenc_dirs['swi']['dirs']['input'], 'wmlesions_lpa_mask.nii.gz')
    ]

    pandas.set_option('expand_frame_repr', False)

    df_stats_gm_cortical = iw_labels.measure_image_stats(labels[0], swir)
    df_stats_gm_subcortical = iw_labels.measure_image_stats(labels[1], swir)
    df_stats_wm_cerebral = iw_labels.measure_image_stats(labels[2], swir)
    df_stats_wm_lesions = iw_labels.measure_image_stats(labels[3], swir)

    dict_redcap = OrderedDict((('subject_id', cenc_dirs['cenc']['id']),
                               ('swi_analyst', getpass.getuser()),
                               ('swi_datetime', '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())),
                               ('swi_gm_cortical_mean', '{0:4.3f}'.format(df_stats_gm_cortical['mean'].values[0])),
                               ('swi_gm_cortical_std', '{0:4.3f}'.format(df_stats_gm_cortical['std'].values[0])),
                               ('swi_gm_subcortical_mean', '{0:4.3f}'.format(df_stats_gm_subcortical['mean'].values[0])),
                               ('swi_gm_subcortical_std','{0:4.3f}'.format(df_stats_gm_subcortical['std'].values[0])),
                               ('swi_wm_cortical_mean', '{0:4.3f}'.format(df_stats_wm_cerebral['mean'].values[0])),
                               ('swi_wm_cortical_std', '{0:4.3f}'.format(df_stats_wm_cerebral['std'].values[0])),
                               ('swi_wmlesions_mean', '{0:4.3f}'.format(df_stats_wm_lesions['mean'].values[0])),
                               ('swi_wmlesions_std', '{0:4.3f}'.format(df_stats_wm_lesions['std'].values[0]))
                               )
                              )

    magtrans_json_filename =  os.path.join(cenc_dirs['swi']['dirs']['results'], 'magtrans.json')

    with open(magtrans_json_filename, 'w') as outfile:
        json.dump(dict_redcap, outfile, indent=4, ensure_ascii=True, sort_keys=False)

    if verbose:
        cenc.print_json_redcap_instrument(magtrans_json_filename)

    return

def redcap(input_dir, verbose=False):
    pass

def qa_results(in_dir, verbose=False):
    cenc_dirs = cenc.directories(in_dir)

    cenc.print_json_redcap_instrument( os.path.join(cenc_dirs['swi']['dirs']['results'],'magtrans.json'))

    result_files = [os.path.join(cenc_dirs['swi']['dirs']['results'], 'nu.nii.gz') + ':colormap=grayscale',
                    os.path.join(cenc_dirs['swi']['dirs']['results'],
                                 'swi_Affine_nu__swi_m0.nii.gz') + ':colormap=grayscale:visible=0',
                    os.path.join(cenc_dirs['swi']['dirs']['results'],
                                 'swi_Affine_nu__swi_m1.nii.gz') + ':colormap=grayscale:visible=0',
                    os.path.join(cenc_dirs['swi']['dirs']['results'],
                                 'swir.nii.gz') + ':colormap=jet:colorscale=0,0.6:opacity=0.5'
                    ]

    qa_command = ['freeview', '-v'] + result_files



    if verbose:
        print
        print(' '.join(qa_command))
        print

    DEVNULL = open(os.devnull, 'wb')
    pipe = subprocess.Popen([' '.join(qa_command)], shell=True,
                            stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL, close_fds=True)

#=======================================================================================================================
# Status

def status_methods_01_register(config, verbose=False):

     input_dir = config['dirs']['input']

     cenc_dirs = cenc.directories(input_dir)

     result_files = [os.path.join(cenc_dirs['swi']['dirs']['register'], 'swi_Affine_nu__swi_magnitude.nii.gz'),
                     os.path.join(cenc_dirs['swi']['dirs']['register'], 'swi_Affine_nu__swi_phase.nii.gz'),
                     os.path.join(cenc_dirs['swi']['dirs']['register'], 'swi_Affine_nu__swi.nii.gz')
                     ]

     swi_status = util.check_files(result_files, False)

     if verbose:
          print(cenc_dirs['cenc']['id'] + ', cenc_swi, ' + 'methods_01_register' + ', ' + str(swi_status))
          
     return swi_status


def status_methods_02_stats( input_dir, verbose=False ):

     cenc_dirs = cenc.directories( input_dir )
     
     result_files = [ os.path.join( cenc_dirs['swi']['dirs']['results'], 'magtrans.json') ]
 
     swi_status = util.check_files(result_files, False)

     if verbose:
          print( cenc_dirs['cenc']['id'] + ', cenc_swi, ' + 'methods_02_stats' + ', ' + str(swi_status) )

     return swi_status

def status_methods( input_dir, verbose=False ):

    methods_01_register = status_methods_01_register(input_dir, verbose)
    methods_02_stats = status_methods_02_stats(input_dir, verbose)

    return methods_01_register and methods_02_stats

def status_results( input_dir, verbose=False ):

     cenc_dirs = cenc.directories( input_dir )

     result_files = [ os.path.join( cenc_dirs['swi']['dirs']['results'],  'swi_Affine_nu__swi_m0.nii.gz'),
                      os.path.join( cenc_dirs['swi']['dirs']['results'],  'swi_Affine_nu__swi_m1.nii.gz'), 
                      os.path.join( cenc_dirs['swi']['dirs']['results'],  'swir.nii.gz'),
                      os.path.join( cenc_dirs['swi']['dirs']['results'],  'nu.nii.gz'),
                      os.path.join( cenc_dirs['results']['dirs']['images'],  'swir.nii.gz')
                      ]

     swi_status = util.check_files(result_files, False)

     if verbose:
          print( cenc_dirs['cenc']['id'] + ', cenc_swi, ' + 'results' + ', ' + str(swi_status) )

     return swi_status


def status_inputs( input_dir, verbose=False ):

     cenc_dirs = cenc.directories( input_dir )

     input_files = cenc_dirs['swi']['inputs']
     label_files = cenc_dirs['swi']['labels']

     swi_status = util.check_files(input_files + label_files, False)

     if verbose:
          print( cenc_dirs['cenc']['id'] + ', cenc_swi, ' + 'input' + ', ' + str(swi_status) )

     return swi_status


def status_prepare( input_dir, verbose=False ):

     cenc_dirs = cenc.directories( input_dir )

     input_files = cenc_dirs['swi']['inputs']
     label_files = cenc_dirs['swi']['labels']

     swi_status = util.check_files(input_files + label_files, False)

     if verbose:
          print( cenc_dirs['cenc']['id'] + ', cenc_swi, ' + 'prepare' + ', ' + str(swi_status) )

     return swi_status

# ======================================================================================================================
#  Main
def main():
    ## Parsing Arguments

    usage = "usage: %prog [options] arg1 arg2"

    parser = argparse.ArgumentParser(prog='cenc_swi')

    parser.add_argument("--in_dir", help="Participant directory", default=os.getcwd())

    parser.add_argument("--cenc_data_dir", help="CENC data directory", default=os.getenv('CENC_MRI_DATA'))
    parser.add_argument("--cenc_freesurfer_dir", help="CENC data directory", default=os.getenv('CENC_SUBJECTS_DIR'))
    parser.add_argument("--cenc_results_dir", help="CENC results directory", default='./results/native')

    parser.add_argument("--methods", help="Methods [all, 01_register, 02_stats]", nargs='*', choices=['all', '00_input', '01_register', '02_stats'], default=[None])

    parser.add_argument("--prepare", help="Gather necessary inputs for SWI analysis", action="store_true", default=False)
    parser.add_argument("--results", help="Gather results", action="store_true", default=False)
    parser.add_argument("--redcap", help="Calculate RedCap results", action="store_true", default=False)

    parser.add_argument("--status", help="Status check. choices=[all, input, methods, results]", nargs='*',
                        choices=['all', 'input','methods','results', '01_register', '02_stats'], default=[None])


    parser.add_argument("--force", help="Force processing action to run", action="store_true", default=False)

    parser.add_argument("--qa", help="Check if SWI has been run on this participant",
                        choices=['prepare', 'results', 'methods'])
    parser.add_argument('-v', '--verbose', help="Verbose flag", action="store_true", default=False)

    inArgs = parser.parse_args()

    # Prepare

    cenc_dirs = cenc.directories(inArgs.in_dir)

    if inArgs.prepare:

        if status_inputs(inArgs.in_dir, False):
            prepare(inArgs.in_dir)

        else:
            if inArgs.verbose:
                print('cenc_swi.py: Inputs for prepare are not found')
                status_inputs(inArgs.in_dir, True)
                exit()

    # Methods
            
    config = swi_config( inArgs.in_dir, inArgs.verbose)

    if inArgs.methods is not None:
         methods( inArgs.methods, config, inArgs.verbose )


    # Results
    if inArgs.results and ((not status_results(inArgs.in_dir, False)) or inArgs.force):

        if status_methods(inArgs.in_dir, False):

            if (not status_results(inArgs.in_dir, False)) or inArgs.force:
                results(inArgs.in_dir)
            else:
                if inArgs.verbose:
                    print('cenc_swi.py: run has already been run')
        else:
            print( cenc_dirs['cenc']['id'] + ': cenc_swi.py run must be executed before results')


    if inArgs.redcap:
        redcap(inArgs.in_dir, inArgs.verbose)

    # Status

    if 'input' in inArgs.status or 'all' in inArgs.status:
        status_inputs(inArgs.in_dir, True)

    if '01_register' in inArgs.status or 'all' in inArgs.status:
        status_methods_01_register(inArgs.in_dir, True)

    if '02_stats' in inArgs.status or 'all' in inArgs.status:
        status_methods_01_register(inArgs.in_dir, True)

    if 'methods' in inArgs.status or 'all' in inArgs.status:
        status_methods(inArgs.in_dir, True)

    if 'results' in inArgs.status  or 'all' in inArgs.status:
        status_results(inArgs.in_dir, True)


    # QA
    if inArgs.qa in ['results']:
        qa_results(inArgs.in_dir)


# Main Function

if __name__ == "__main__":
    sys.exit(main())

