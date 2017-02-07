#!/usr/bin/env python

"""

"""
import sys
import os                                               # system functions
import re
import pandas
import json
import argparse
import iwUtilities as util
import cenc
import iw_labels
import datetime
from collections import OrderedDict
import getpass
import subprocess



#=======================================================================================================================
# Prepare

def mt_link_inputs( input_dir, link_to_dir, change_to_dir = True ):

     cenc_dirs = cenc.directories( input_dir )

     util.mkcd_dir( [ link_to_dir ], change_to_dir )

     input_files = cenc_dirs['mt']['inputs']
     label_files = cenc_dirs['mt']['labels']

     util.link_inputs( input_files + label_files, link_to_dir )



def prepare( input_dir, verbose=False ):

     if verbose:
          print('Entering cenc_mt.py prepare')

     cenc_dirs = cenc.directories( input_dir )

     input_files = cenc_dirs['mt']['inputs']
     label_files = cenc_dirs['mt']['labels']

     mt_link_inputs( input_dir, cenc_dirs['mt']['dirs']['input'] )
     mt_link_inputs( input_dir, cenc_dirs['mt']['dirs']['input'] )

     return


#=======================================================================================================================
# Methods

def ants_register(input_file):

     # antsRegistration call:
     #--------------------------------------------------------------------------------------
     if False:

          # I am having problems callling the interface.  Same problem of bad interface.

          command = ['antsRegistration', '--dimensionality', 3, '--float', 0, 
                     '--output', '[', 'mt_Affine_nu__' + input_file +'_,', 
                     'mt_Affine_nu__' + input_file + '_Warped.nii.gz,', 
                     'mt_Affine_nu__' + input_file + '_InverseWarped.nii.gz', ']', 
                     '--interpolation', 'Linear', 
                     '--use-histogram-matching', 0,
                     '--winsorize-image-intensities', [0.005,0.995],
                     '--initial-moving-transform', '[', 'nu.nii.gz,' + input_file + '.nii.gz,', 1, ']',
                     '--transform', 'Rigid[0.1]',
                     '--metric', 'MI[nu.nii.gz,mt_m1.nii.gz,1,32,Regular,0.25]', 
                     '--convergence', '[1000x500x250x0,1e-6,10]',
                     '--shrink-factors', '8x4x2x1',
                     '--smoothing-sigmas', '3x2x1x0vox', 
                     '--transform', 'Affine[0.1]',
                     '--metric', 'MI[nu.nii.gz,' + input_file + '.nii.gz,1,32,Regular,0.25]',
                     '--convergence', '[1000x500x250x0,1e-6,10]', 
                     '--shrink-factors', '8x4x2x1', 
                     '--smoothing-sigmas', '3x2x1x0vox'
                    ]
     #--------------------------------------------------------------------------------------

      # I am having problems callling the interface.  Same problem of bad interface.
     if False:
          reg = Registration()
          reg.inputs.fixed_image = 'nu.nii.gz'
          reg.inputs.moving_image = input_file + '.nii.gz'
          reg.inputs.output_transform_prefix = "mt_Affine_nu__" + input_file + "_"
          reg.inputs.transforms = ['Affine']
          reg.inputs.transform_parameters = [(2.0,), (0.25, 3.0, 0.0)]
          reg.inputs.number_of_iterations = [[1000,500,200,100]]
          reg.inputs.dimension = 3
          reg.inputs.write_composite_transform = False
          reg.inputs.collapse_output_transforms = False
          reg.inputs.initialize_transforms_per_stage = False
          reg.inputs.metric = ['MI']
          reg.inputs.metric_weight = [1]
          reg.inputs.radius_or_number_of_bins = [32]
          reg.inputs.sampling_strategy = ['Random']
          reg.inputs.sampling_percentage = [0.05]
          reg.inputs.convergence_threshold = [1.e-10]
          reg.inputs.convergence_window_size = [10]
          reg.inputs.smoothing_sigmas = [[3,2,1,0]]
          reg.inputs.sigma_units = ['vox']
          reg.inputs.shrink_factors = [[8,4,2,1]]
          reg.inputs.use_estimate_learning_rate_once = [True]
          reg.inputs.use_histogram_matching = [True] # This is the default
          reg.inputs.output_warped_image = 'mt_Affine_nu__' + input_file + '.nii.gz'
          reg.inputs.terminal_output='stream'
          print reg.cmdline
          # reg.run()


     # This simple command appears to work. 
     command = ['antsRegistrationSyNQuick.sh', '-d', '3', '-m', input_file + '.nii.gz', '-r', 'nu.nii.gz',
                '-f', 'nu.nii.gz', '-t', 'a', '-o', 'mt_Affine_nu__' + input_file + '_' 
                ]

     util.iw_subprocess( command, True, True, False)


def methods_01_register( input_dir, verbose=False):

     # Register MT images to nu.nii.gz
     cenc_dirs = cenc.directories( input_dir )
     mt_link_inputs( input_dir, cenc_dirs['mt']['dirs']['register'] )
 
     ants_register('mt_m0')
     ants_register('mt_m1')

     # Calculate MTR image
     command = ['ImageMath', 3, 'mtr.nii.gz', 'MTR', 'mt_Affine_nu__mt_m0_Warped.nii.gz', 
                'mt_Affine_nu__mt_m1_Warped.nii.gz', 'nu_brain.nii.gz']

     util.iw_subprocess( command, verbose, verbose, False)

     return


def methods_02_stats(input_dir, verbose=False):

    # Register MT images to nu.nii.gz
    cenc_dirs = cenc.directories(input_dir)

    util.mkcd_dir( [ cenc_dirs['mt']['dirs']['02-stats'] ], True)

    methods_write_json_redcap_mt_instrument(input_dir, verbose)


    return

#=======================================================================================================================
# Results

def results( input_dir ):
    """ Gather results and write the MagTran JSON output file"""

    cenc_dirs = cenc.directories( input_dir )

    mt_input_dir       = cenc_dirs['mt']['dirs']['input']
    mt_01_register_dir = cenc_dirs['mt']['dirs']['register']
    mt_results_dir     = cenc_dirs['mt']['dirs']['results']

    util.mkcd_dir( [ mt_results_dir ], True)

    result_files = [ [  os.path.join( cenc_dirs['mt']['dirs']['register'], 'mt_Affine_nu__mt_m0_Warped.nii.gz'),
    os.path.join( cenc_dirs['mt']['dirs']['results'],  'mt_Affine_nu__mt_m0.nii.gz')],

    [ os.path.join( cenc_dirs['mt']['dirs']['register'], 'mt_Affine_nu__mt_m1_Warped.nii.gz'),
    os.path.join( cenc_dirs['mt']['dirs']['results'],  'mt_Affine_nu__mt_m1.nii.gz')],

    [ os.path.join( cenc_dirs['mt']['dirs']['02-stats'], 'magtrans.json'),
    os.path.join( cenc_dirs['mt']['dirs']['results'],  'magtrans.json') ],

    [ os.path.join( cenc_dirs['mt']['dirs']['register'], 'mtr.nii.gz'),
    os.path.join( cenc_dirs['mt']['dirs']['results'],  'mtr.nii.gz') ],

    [ os.path.join( cenc_dirs['mt']['dirs']['input'],    'nu.nii.gz'),
    os.path.join( cenc_dirs['mt']['dirs']['results'],  'nu.nii.gz') ],

    [ os.path.join( cenc_dirs['mt']['dirs']['register'], 'mtr.nii.gz'),
    os.path.join( cenc_dirs['results']['dirs']['images'],  'mtr.nii.gz') ]
    ]

    for ii in result_files:
        util.force_hard_link( ii[0], ii[1])

    return


def methods_write_json_redcap_mt_instrument(input_dir, verbose):
    """ Write MagTrans Instrument to JSON output file"""

    cenc_dirs = cenc.directories(input_dir)

    mtr = os.path.join(cenc_dirs['mt']['dirs']['register'], 'mtr.nii.gz')

    labels = [os.path.join(cenc_dirs['mt']['dirs']['input'], 'gm.cerebral_cortex.nii.gz'),
    os.path.join(cenc_dirs['mt']['dirs']['input'], 'gm.subcortical.nii.gz'),
    os.path.join(cenc_dirs['mt']['dirs']['input'], 'wm.cerebral.nii.gz'),
    os.path.join(cenc_dirs['mt']['dirs']['input'], 'wmlesions_lpa_mask.nii.gz')
    ]

    pandas.set_option('expand_frame_repr', False)

    df_stats_gm_cortical = iw_labels.measure_image_stats(labels[0], mtr)
    df_stats_gm_subcortical = iw_labels.measure_image_stats(labels[1], mtr)
    df_stats_wm_cerebral = iw_labels.measure_image_stats(labels[2], mtr)
    df_stats_wm_lesions = iw_labels.measure_image_stats(labels[3], mtr)

    dict_redcap = OrderedDict((('subject_id', cenc_dirs['cenc']['id']),
                               ('mt_analyst', getpass.getuser()),
                               ('mt_datetime', '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())),
                               ('mt_gm_cortical_mean', '{0:4.3f}'.format(df_stats_gm_cortical['mean'].values[0])),
                               ('mt_gm_cortical_std', '{0:4.3f}'.format(df_stats_gm_cortical['std'].values[0])),
                               ('mt_gm_subcortical_mean', '{0:4.3f}'.format(df_stats_gm_subcortical['mean'].values[0])),
                               ('mt_gm_subcortical_std','{0:4.3f}'.format(df_stats_gm_subcortical['std'].values[0])),
                               ('mt_wm_cortical_mean', '{0:4.3f}'.format(df_stats_wm_cerebral['mean'].values[0])),
                               ('mt_wm_cortical_std', '{0:4.3f}'.format(df_stats_wm_cerebral['std'].values[0])),
                               ('mt_wmlesions_mean', '{0:4.3f}'.format(df_stats_wm_lesions['mean'].values[0])),
                               ('mt_wmlesions_std', '{0:4.3f}'.format(df_stats_wm_lesions['std'].values[0]))
                               )
                              )

    magtrans_json_filename =  os.path.join(cenc_dirs['mt']['dirs']['02-stats'], 'magtrans.json')

    with open(magtrans_json_filename, 'w') as outfile:
        json.dump(dict_redcap, outfile, indent=4, ensure_ascii=True, sort_keys=False)

    if verbose:
        cenc.print_json_redcap_instrument(magtrans_json_filename)

    return

def redcap(input_dir, verbose=False):
    pass

def qa_results(in_dir, verbose=False):
    cenc_dirs = cenc.directories(in_dir)

    cenc.print_json_redcap_instrument( os.path.join(cenc_dirs['mt']['dirs']['results'],'magtrans.json'))

    result_files = [os.path.join(cenc_dirs['mt']['dirs']['results'], 'nu.nii.gz') + ':colormap=grayscale',
                    os.path.join(cenc_dirs['mt']['dirs']['results'],
                                 'mt_Affine_nu__mt_m0.nii.gz') + ':colormap=grayscale:visible=0',
                    os.path.join(cenc_dirs['mt']['dirs']['results'],
                                 'mt_Affine_nu__mt_m1.nii.gz') + ':colormap=grayscale:visible=0',
                    os.path.join(cenc_dirs['mt']['dirs']['results'],
                                 'mtr.nii.gz') + ':colormap=jet:colorscale=0,0.6:opacity=0.5'
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

def status_methods_01_register(input_dir, verbose=False):
    cenc_dirs = cenc.directories(input_dir)

    result_files = [os.path.join(cenc_dirs['mt']['dirs']['register'], 'mt_Affine_nu__mt_m0_Warped.nii.gz'),
                    os.path.join(cenc_dirs['mt']['dirs']['register'], 'mt_Affine_nu__mt_m1_Warped.nii.gz'),
                    os.path.join(cenc_dirs['mt']['dirs']['register'], 'mtr.nii.gz')
                    ]

    mt_status = util.check_files(result_files, False)

    if verbose:
        print(cenc_dirs['cenc']['id'] + ', cenc_mt, ' + 'methods_01_register' + ', ' + str(mt_status))

    return mt_status


def status_methods_02_stats( input_dir, verbose=False ):

     cenc_dirs = cenc.directories( input_dir )
     
     result_files = [ os.path.join( cenc_dirs['mt']['dirs']['02-stats'], 'magtrans.json') ]
 
     mt_status = util.check_files(result_files, False)

     if verbose:
          print( cenc_dirs['cenc']['id'] + ', cenc_mt, ' + 'methods_02_stats' + ', ' + str(mt_status) )

     return mt_status


def status_methods( input_dir, verbose=False ):

    methods_01_register = status_methods_01_register(input_dir, verbose)
    methods_02_stats = status_methods_02_stats(input_dir, verbose)

    return methods_01_register and methods_02_stats

def status_results( input_dir, verbose=False ):

     cenc_dirs = cenc.directories( input_dir )

     result_files = [ os.path.join( cenc_dirs['mt']['dirs']['results'],  'mt_Affine_nu__mt_m0.nii.gz'),
                      os.path.join( cenc_dirs['mt']['dirs']['results'],  'mt_Affine_nu__mt_m1.nii.gz'), 
                      os.path.join( cenc_dirs['mt']['dirs']['results'],  'mtr.nii.gz'),
                      os.path.join( cenc_dirs['mt']['dirs']['results'],  'nu.nii.gz'),
                      os.path.join( cenc_dirs['results']['dirs']['images'],  'mtr.nii.gz')
                      ]

     mt_status = util.check_files(result_files, False)

     if verbose:
          print( cenc_dirs['cenc']['id'] + ', cenc_mt, ' + 'results' + ', ' + str(mt_status) )

     return mt_status


def status_inputs( input_dir, verbose=False ):

     cenc_dirs = cenc.directories( input_dir )

     input_files = cenc_dirs['mt']['inputs']
     label_files = cenc_dirs['mt']['labels']

     mt_status = util.check_files(input_files + label_files, False)

     if verbose:
          print( cenc_dirs['cenc']['id'] + ', cenc_mt, ' + 'input' + ', ' + str(mt_status) )

     return mt_status


def status_prepare( input_dir, verbose=False ):

     cenc_dirs = cenc.directories( input_dir )

     input_files = cenc_dirs['mt']['inputs']
     label_files = cenc_dirs['mt']['labels']

     mt_status = util.check_files(input_files + label_files, False)

     if verbose:
          print( cenc_dirs['cenc']['id'] + ', cenc_mt, ' + 'prepare' + ', ' + str(mt_status) )

     return mt_status

# ======================================================================================================================
#  Main
def main():
    ## Parsing Arguments

    usage = "usage: %prog [options] arg1 arg2"

    parser = argparse.ArgumentParser(prog='cenc_mt')

    parser.add_argument("--in_dir", help="Participant directory", default=os.getcwd())

    parser.add_argument("--cenc_data_dir", help="CENC data directory", default=os.getenv('CENC_MRI_DATA'))
    parser.add_argument("--cenc_freesurfer_dir", help="CENC data directory", default=os.getenv('CENC_SUBJECTS_DIR'))
    parser.add_argument("--cenc_results_dir", help="CENC results directory", default='./results/native')

    parser.add_argument("--methods", help="Methods [all, 01_register, 02_stats]", nargs='*', choices=['all', '01_register', '02_stats'], default=[None])

    parser.add_argument("--prepare", help="Gather necessary inputs for MT analysis", action="store_true", default=False)
    parser.add_argument("--results", help="Gather results", action="store_true", default=False)
    parser.add_argument("--redcap", help="Calculate RedCap results", action="store_true", default=False)

    parser.add_argument("--status", help="Status check. choices=[all, input, methods, results]", nargs='*',
                        choices=['all', 'input','methods','results', '01_register', '02_stats'], default=[None])


    parser.add_argument("--force", help="Force processing action to run", action="store_true", default=False)

    parser.add_argument("--qa", help="Check if MT has been run on this participant",
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
                print('cenc_mt.py: Inputs for prepare are not found')
                status_inputs(inArgs.in_dir, True)
                exit()

    # Methods

    if '01_register' in inArgs.methods or 'all' in inArgs.methods:

        if (not status_methods_01_register(inArgs.in_dir, False)) or inArgs.force:
            methods_01_register(inArgs.in_dir, inArgs.verbose)
        else:
            print( cenc_dirs['cenc']['id'] + ': cenc_mt.py: run has already been run')

    if '02_stats' in inArgs.methods or 'all' in inArgs.methods:

        if status_methods_01_register(inArgs.in_dir):
            if (not status_methods_02_stats(inArgs.in_dir)) or inArgs.force:
                methods_02_stats(inArgs.in_dir, inArgs.verbose)
            else:
                print(cenc_dirs['cenc']['id'] + ': cenc_mt.py: methods_02_stats has already been run')
        else:
            print(cenc_dirs['cenc']['id'] + ':  cenc_mt.py methods_01_register must be run first')


    # Results
    if inArgs.results and ((not status_results(inArgs.in_dir, False)) or inArgs.force):

        if status_methods(inArgs.in_dir, False):

            if (not status_results(inArgs.in_dir, False)) or inArgs.force:
                results(inArgs.in_dir)
            else:
                if inArgs.verbose:
                    print('cenc_mt.py: run has already been run')
        else:
            print( cenc_dirs['cenc']['id'] + ': cenc_mt.py run must be executed before results')


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

