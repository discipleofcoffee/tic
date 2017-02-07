#!/usr/bin/env python2

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


def cenc_stats(input_dir, in_image, out_json, instrument_prefix='', verbose=False):
    """ Write MagTrans Instrument to JSON output file"""

    cenc_dirs = cenc.directories( input_dir )

    if verbose:
         print(cenc_dirs['results']['dirs']['labels'])

    labels = {'gm_cerebral':    os.path.join( cenc_dirs['results']['dirs']['labels'], 'gm.cerebral_cortex.nii.gz'),
              'gm_subcortical': os.path.join( cenc_dirs['results']['dirs']['labels'], 'gm.subcortical.nii.gz'),
              'wm_cerebral':    os.path.join( cenc_dirs['results']['dirs']['labels'], 'wm.cerebral.nii.gz'),
              'wm_lesions':     os.path.join( cenc_dirs['results']['dirs']['labels'], 'wmlesions_lpa_mask.nii.gz')
              }
    
    pandas.set_option('expand_frame_repr', False)

    df_stats_gm_cortical    = iw_labels.measure_image_stats(labels['gm_cerebral'], in_image)
    df_stats_gm_subcortical = iw_labels.measure_image_stats(labels['gm_subcortical'], in_image)
    df_stats_wm_cerebral    = iw_labels.measure_image_stats(labels['wm_cerebral'], in_image)
    df_stats_wm_lesions     = iw_labels.measure_image_stats(labels['wm_lesions'], in_image)

    dict_stats = OrderedDict(( ('subject_id', cenc_dirs['cenc']['id']),
                               ( instrument_prefix + 'analyst', getpass.getuser()),
                               ( instrument_prefix + 'datetime', '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())),
                               ( instrument_prefix + 'image', in_image),
                               ( instrument_prefix + 'gm_cortical_mean', '{0:4.3f}'.format(df_stats_gm_cortical['mean'].values[0])),
                               ( instrument_prefix + 'gm_cortical_std', '{0:4.3f}'.format(df_stats_gm_cortical['std'].values[0])),
                               ( instrument_prefix + 'gm_subcortical_mean', '{0:4.3f}'.format(df_stats_gm_subcortical['mean'].values[0])),
                               ( instrument_prefix + 'gm_subcortical_std','{0:4.3f}'.format(df_stats_gm_subcortical['std'].values[0])),
                               ( instrument_prefix + 'wm_cortical_mean', '{0:4.3f}'.format(df_stats_wm_cerebral['mean'].values[0])),
                               ( instrument_prefix + 'wm_cortical_std', '{0:4.3f}'.format(df_stats_wm_cerebral['std'].values[0])),
                               ( instrument_prefix + 'wmlesions_mean', '{0:4.3f}'.format(df_stats_wm_lesions['mean'].values[0])),
                               ( instrument_prefix + 'wmlesions_std', '{0:4.3f}'.format(df_stats_wm_lesions['std'].values[0]))
                               )
                              )

    if out_json==None:
         json_stats_filename =  in_image.replace( 'nii.gz', 'json')
    else:
         json_stats_filename = out_json
         
    if verbose:
         print( json_stats_filename )

    with open(json_stats_filename, 'w') as outfile:
         json.dump(dict_stats, outfile, indent=4, ensure_ascii=True, sort_keys=False)

    if verbose:
        util.print_json_redcap_instrument(json_stats_filename)

    return

# ======================================================================================================================
#  Main
def main():
    ## Parsing Arguments

    usage = "usage: %prog [options] arg1 arg2"

    parser = argparse.ArgumentParser(prog='cenc_mt')

    parser.add_argument("in_image", help="Input image", default=None )
    parser.add_argument("--in_dir", help="Participant directory", default=os.getcwd())
    parser.add_argument("--out_json", help="Output JSON filename", default=None )
    parser.add_argument("--prefix", help="Instrument Prefix", default='' )

    parser.add_argument('-v', '--verbose', help="Verbose flag", action="store_true", default=False)

    inArgs = parser.parse_args()

    cenc_stats(inArgs.in_dir, inArgs.in_image, inArgs.out_json, inArgs.prefix, inArgs.verbose)


# Main Function

if __name__ == "__main__":
    sys.exit(main())

    
