#!/usr/bin/env python
"""
"""

import sys      
import os                                               # system functions
import errno
import glob
import shutil
import distutils
import re
import argparse
import subprocess
import nibabel
import numpy
import scipy.ndimage
import json

from collections import OrderedDict

import iwUtilities     as util


def participants(in_cenc_dir, in_method, in_filter='study', verbose=False):
     
     if in_filter in 'study':
          cenc_id_pattern = '34P1[0-9][0-9][0-9]'
     elif in_filter in 'test':
          cenc_id_pattern = '34P9[0-9][0-9][0-9]'
     else:
          bcenc_id_pattern = '34P[19][0-9][0-9][0-9]'
     
     cenc_dir = os.path.abspath(in_cenc_dir)     

     os.chdir(cenc_dir)
     cenc_participants = sorted(glob.glob(cenc_id_pattern))
                    
     if in_method in 'update':
          with open(os.path.join(cenc_dir, 'participants.list'), 'w') as file_handler:
               for item in cenc_participants:
                    file_handler.write("{}\n".format(item))

     if verbose:
          print
          for ii in cenc_participants:
               print ii
          print

     return cenc_participants


def participant_id(in_dir, cenc_dir=os.getenv('CENC_MRI_DATA'), acrostic_flag=True, directory_flag=True, exist_flag=True):
     
     pattern = re.compile('34P[19]\d{3}')

     if in_dir.isdigit():
#          print(['Is digit', in_dir])
          in_dir = '34P1' + '{0:03d}'.format(int(in_dir))
#          print(['Is digit transformed', in_dir])

     if pattern.match(in_dir) and not os.path.isdir(in_dir):
#          print(['Is Acrostic', in_dir])
          in_dir = os.path.join(cenc_dir, in_dir)

#     print(['Is directory', in_dir])

     in_abs_dir = os.path.abspath(in_dir)     
     cenc_participant_id     = util.extract_participant_id( in_abs_dir,'34P[19]\d{3}')
     cenc_participant_dir    = os.path.abspath( os.path.join( cenc_dir, cenc_participant_id))
     cenc_participant_exists = os.path.isdir(cenc_participant_dir)

     cenc_results = []

     if acrostic_flag:
          cenc_results += [cenc_participant_id]

     if directory_flag:
          cenc_results += [cenc_participant_dir]

     if exist_flag:
          cenc_results += [cenc_participant_exists]


     return cenc_results


def directories( input_dir ):
     
     cenc_participant_id, cenc_participant_dir, cenc_participant_exists = participant_id( input_dir )

     if not cenc_participant_exists:
          print
          print('CENC Participant ' + cenc_participant_id + ' does not exist')
          print
          sys.exit()

     cenc_freesurfer_subjects_dir =  os.getenv('CENC_SUBJECTS_DIR')
     cenc_results_native_dir = os.path.abspath( os.path.join( cenc_participant_dir, 'results', 'native')) 


     cenc_dict = { 'id': cenc_participant_id, 
                   'root': cenc_participant_dir, 'results': cenc_results_native_dir,
                   'freesurfer_subjects_dir': cenc_freesurfer_subjects_dir, 
                   'reorient': util.path_relative_to( cenc_participant_dir, 'reorient'), 
                   'functional': util.path_relative_to( cenc_participant_dir, 'functional'), 
                   'structural': util.path_relative_to( cenc_participant_dir, 'structural'),
                   } 


     # CENC Final Results

     results_dict = { 'dirs': {'root':  cenc_dict['results'],
                               'labels': os.path.join( cenc_dict['results'], 'labels'),
                               'images': os.path.join( cenc_dict['results'], 'images')
                               }
                      }


     # Freesurfer Analysis

     freesurfer_dir =  util.path_relative_to( cenc_participant_dir, 'freesurfer')

     freesurfer_dict = { 'base': freesurfer_dir,
                         'subjects_dir': cenc_freesurfer_subjects_dir, 
                         'input': os.path.join(freesurfer_dir, 'input'),
                         't1w': os.path.join(freesurfer_dir, 'input','t1w.nii.gz'),
                         't2w': os.path.join(freesurfer_dir, 'input', 't2tse.nii.gz'),
                         'flair': os.path.join(freesurfer_dir, 'input', 't2flair.nii.gz'),
                         'results': os.path.join( freesurfer_dir, 'results'),
                         'mri': os.path.join( cenc_dict['freesurfer_subjects_dir'], cenc_dict['id'], 'mri')
                         }

     
     # White Matter Lesions Segmentation Toolbox

     wmlesions_dir = util.path_relative_to( cenc_dict['structural'], 'wmlesions' )
     wmlesions_methods_dir =  util.path_relative_to( wmlesions_dir, 'methods')

     wmlesions_dict = { 'dirs': {'root': wmlesions_dir, 
                                 'input': util.path_relative_to( wmlesions_dir, 'input'),
                                 'methods': util.path_relative_to( wmlesions_dir, 'methods'),
                                 'rename': util.path_relative_to( wmlesions_methods_dir, '00-rename'),
                                 'register': util.path_relative_to( wmlesions_methods_dir, '01-register'),
                                 'lpa': util.path_relative_to( wmlesions_methods_dir, '02-lpa'),
                                 'stats': util.path_relative_to(wmlesions_methods_dir, '03-stats'),
                                 'results': util.path_relative_to( wmlesions_dir, 'results')
                                 }
                        }

     # Magnetization Transfer

     mt_dir = util.path_relative_to( cenc_dict['structural'], 'mt' )

     mt_labels = [ os.path.join( results_dict['dirs']['labels'],  'gm.cerebral_cortex.nii.gz'),
                   os.path.join( results_dict['dirs']['labels'],  'gm.subcortical.nii.gz'),
                   os.path.join( results_dict['dirs']['labels'],  'wm.cerebral.nii.gz'),
                   os.path.join( results_dict['dirs']['labels'],  'wmlesions_lpa_mask.nii.gz')
                   ]

     mt_inputs = [ os.path.join( cenc_dict['reorient'], 'mt_m0.nii.gz'),
                   os.path.join( cenc_dict['reorient'], 'mt_m1.nii.gz'),
                   os.path.join( results_dict['dirs']['images'], 'nu.nii.gz'),
                   os.path.join( results_dict['dirs']['images'], 'nu_brain.nii.gz')
                   ]

     mt_dict = { 'dirs' : {'root': mt_dir, 
                           'input': util.path_relative_to( mt_dir, 'input'),
                           'register': util.path_relative_to( os.path.join( mt_dir, 'methods'), '01-register'),
                           '02-stats': util.path_relative_to( os.path.join( mt_dir, 'methods'), '02-stats'),
                           'results': util.path_relative_to( mt_dir, 'results') 
                          },

                 'inputs' : mt_inputs,
                 'labels' : mt_labels
                 }


     # SWI Transfer

     swi_dir = util.path_relative_to( cenc_dict['structural'], 'swi' )

     swi_labels = [ os.path.join( results_dict['dirs']['labels'],  'gm.cerebral_cortex.nii.gz'),
                   os.path.join( results_dict['dirs']['labels'],  'gm.subcortical.nii.gz'),
                   os.path.join( results_dict['dirs']['labels'],  'wm.cerebral.nii.gz'),
                   os.path.join( results_dict['dirs']['labels'],  'wmlesions_lpa_mask.nii.gz')
                   ]

     swi_inputs = [ os.path.join( cenc_dict['reorient'], 'swi_magnitude.nii.gz'),
                    os.path.join( cenc_dict['reorient'], 'swi_phase.nii.gz'),
                    os.path.join( cenc_dict['reorient'], 'swi.nii.gz'),
                    os.path.join( results_dict['dirs']['images'], 'nu.nii.gz'),
                    os.path.join( results_dict['dirs']['images'], 'nu_brain.nii.gz')
                   ]

     swi_dict = { 'dirs' : {'root': swi_dir, 
                           'input': util.path_relative_to( swi_dir, 'input'),
                           'register': util.path_relative_to( os.path.join( swi_dir, 'methods'), '01-register'),
                           '02-stats': util.path_relative_to( os.path.join( swi_dir, 'methods'), '02-stats'),
                           'results': util.path_relative_to( swi_dir, 'results') 
                          },

                 'inputs' : swi_inputs,
                 'labels' : swi_labels
                 }


     # Return

     return { 'cenc':cenc_dict, 'results':results_dict, 'freesurfer':freesurfer_dict, 'wmlesions':wmlesions_dict, 
              'mt':mt_dict, 'swi':swi_dict }

                                               



def create_mask(in_brainmask, in_aseg, mask ):

     nii_brainmask   = nibabel.load(in_brainmask)
     array_brainmask = 1. * (nii_brainmask.get_data()>0)

     if False:
          nii_aseg      = nibabel.load(in_aseg)


          array_aseg      = nii_aseg.get_data()
          
          array_mask_01     = scipy.ndimage.morphology.binary_erosion( 1.*(array_brainmask>0), numpy.ones( [15,15,15] ) )
          array_mask_02      = 1.* ((array_mask_01 + array_aseg) > 0)
          
          #     out_nifti = nibabel.Nifti1Image( 1.*array_mask_02,  None, nii_brainmask.get_header() )
          #     nibabel.save( out_nifti,  '02.mask.nii.gz' )
          
          array_mask_03     = scipy.ndimage.morphology.binary_fill_holes( 1.*(array_mask_02) )
          #     out_nifti = nibabel.Nifti1Image( 1.*array_mask_03,  None, nii_brainmask.get_header() )
          #     nibabel.save( out_nifti,  '03.mask.nii.gz' )
          
          array_mask_04     = scipy.ndimage.morphology.binary_closing( array_mask_03, numpy.ones( [5,5,5] ))
          array_mask_05     = scipy.ndimage.morphology.binary_fill_holes( 1.*(array_mask_04) )
          array_mask_06     = scipy.ndimage.morphology.binary_opening( array_mask_05, numpy.ones( [5,5,5] ))
          
 
     out_nifti = nibabel.Nifti1Image( array_brainmask,  None, nii_brainmask.get_header() )
     nibabel.save( out_nifti,  mask )

def print_json_redcap_instrument(json_filename):
    """ Print REdCap instrument measures to a JSON file"""


    with open(json_filename, 'r') as infile:
        print('')
        print(json.dumps(json.load(infile, object_pairs_hook=OrderedDict), indent=4, ensure_ascii=True,
        sort_keys=False))
        print(' ')
