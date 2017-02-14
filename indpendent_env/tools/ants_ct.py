#!/usr/bin/env python
"""
   Call antsCorticalThickness.sh in stages. This was a misguided attempt to understand antsCorticalThickness.sh.
   Users should just use ants_ct.py instead.
"""

import sys      
import os                                               # system functions
import glob
import shutil
# import distutils

import argparse
# import subprocess
import _qa_utilities as qa
import _utilities as util

from collections import OrderedDict
import getpass

QA_CHOICES=['input', 'results', 'methods', 'segment', 'thickness', 'extract', 'normalize']

def qa_methods_extract(output_files):
     qa_display(output_files, 'extract')

def qa_methods_segment(output_files):
     qa_display(output_files, 'segment')

def qa_methods_thickness(output_files):
     qa_display(output_files, 'thickness')

def qa_methods_normalize(output_files):
     qa_display(output_files, 'normalize')

def qa_results(output_files):
     qa_display(output_files, 'results')


def qa_display(output_files, method):

     if qa.qa_exist(output_files, False):
          qa.freeview( output_files, True, inArgs.verbose )
          
     else:
          print('Unable to QA ' + method + 'ants_ct.py')
          qa.qa_exist( output_files, True )
          print()
          
          

brain_segmentation_files = ( 'BrainSegmentation0N4.nii.gz',
                       'BrainSegmentationConvergence.txt',
                       'BrainSegmentation.nii.gz',
                       'BrainSegmentationPosteriors1.nii.gz',
                       'BrainSegmentationPosteriors2.nii.gz',
                       'BrainSegmentationPosteriors3.nii.gz',
                       'BrainSegmentationPosteriors4.nii.gz',
                       'BrainSegmentationPosteriors5.nii.gz',
                       'BrainSegmentationPosteriors6.nii.gz'
                       )

registration_files = ( 'BrainNormalizedToTemplate.nii.gz',
                 'BrainSegmentationTiledMosaic.png',
                 'brainvols.csv',
                 'CorticalThickness.nii.gz',
                 'CorticalThicknessNormalizedToTemplate.nii.gz',
                 'CorticalThicknessTiledMosaic.png',
                 'BrainExtractionBrain.nii.gz',
                 'ExtractedBrain0N4.nii.gz',
                 'ExtractedTemplateBrain.nii.gz',
                 'RegistrationTemplateBrainMask.nii.gz',
                 'SubjectToTemplate0GenericAffine.mat',
                 'SubjectToTemplate1Warp.nii.gz',
                 'SubjectToTemplateLogJacobian.nii.gz',
                 'TemplateToSubject0Warp.nii.gz',
                 'TemplateToSubject1GenericAffine.mat'
                 )

def get_info(input_dir, subject_id=None, methods_dir='../methods', results_dir='../results',
             t1=None, t2=None, flair=None, verbose=False):


    base = OrderedDict((('subject_id', subject_id),
                        ('input', input_dir),
                        ('methods', util.path_relative_to(input_dir, methods_dir)),
                        ('results', util.path_relative_to(input_dir, results_dir))
                        )
                       )

    input_files = OrderedDict((('t1', os.path.abspath(t1) if t1 else None),
                               ('t2', os.path.abspath(t2) if t2 else None),
                               ('flair', os.path.abspath(flair) if flair else None)
                               )
                              )


    extract_files = OrderedDict(( ('mask', os.path.join(base['methods'],'BrainExtractionMask.nii.gz'))
                            ))

    segment_files = OrderedDict(( ('n4', os.path.join(base['methods'],'BrainSegmentation0N4.nii.gz')),
                                 ('convergence',os.path.join(base['methods'],'BrainSegmentationConvergence.txt')),
                                 ('segment',os.path.join(base['methods'],'BrainSegmentation.nii.gz')),
                                 ('p_csf',os.path.join(base['methods'],'BrainSegmentationPosteriors1.nii.gz')),
                                 ('p_gm_cortical',os.path.join(base['methods'],'BrainSegmentationPosteriors2.nii.gz')),
                                 ('p_wm',os.path.join(base['methods'],'BrainSegmentationPosteriors3.nii.gz')),
                                 ('p_gm_subcortical',os.path.join(base['methods'],'BrainSegmentationPosteriors4.nii.gz')),
                                 ('p_brainstem',os.path.join(base['methods'],'BrainSegmentationPosteriors5.nii.gz')),
                                 ('p_cerebellum',os.path.join(base['methods'],'BrainSegmentationPosteriors6.nii.gz'))
                               ))

    register_files = OrderedDict(( ('brain_to_template',os.path.join(base['methods'],'BrainNormalizedToTemplate.nii.gz')),
                                 ('brainseg_mosaic',os.path.join(base['methods'],'BrainSegmentationTiledMosaic.png')),
                                 ('brainvols',os.path.join(base['methods'],'brainvols.csv')),
                                 ('ct',os.path.join(base['methods'],'CorticalThickness.nii.gz')),
                                 ('ct_to_template',os.path.join(base['methods'],'CorticalThicknessNormalizedToTemplate.nii.gz')),
                                 ('ct_mosaic',os.path.join(base['methods'],'CorticalThicknessTiledMosaic.png')),
                                 ('brain_extraction_brain',os.path.join(base['methods'],'BrainExtractionBrain.nii.gz')),
                                 ('extracted_brain_n4',os.path.join(base['methods'],'ExtractedBrain0N4.nii.gz',)),
                                 ('extracted_template_brain',os.path.join(base['methods'],'ExtractedTemplateBrain.nii.gz')),
                                 ('template_brain_mask',os.path.join(base['methods'],'RegistrationTemplateBrainMask.nii.gz',)),
                                 ('subject_to_template_affine',os.path.join(base['methods'],'SubjectToTemplate0GenericAffine.mat',)),
                                 ('subject_to_template_warp',os.path.join(base['methods'],'SubjectToTemplate1Warp.nii.gz',)),
                                 ('subject_to_template_jacobian',os.path.join(base['methods'],'SubjectToTemplateLogJacobian.nii.gz',)),
                                 ('template_to_subject_warp',os.path.join(base['methods'],'TemplateToSubject0Warp.nii.gz',)),
                                 ('template_to_subject_affine',os.path.join(base['methods'],'TemplateToSubject1GenericAffine.mat'))
                                 ))

    # output_result_files = [[inArgs.t1full, ':visible=1:colormap=grayscale'],
    #                        [outFull + 'BrainSegmentationPosteriors2.nii.gz',
    #                         ':visible=0:colormap=heat:heatscale=0.1,0.5,1:opacity=0.5'],
    #                        [outFull + 'BrainSegmentationPosteriors3.nii.gz',
    #                         ':visible=0:colormap=heat:heatscale=0.1,0.5,1:opacity=0.5'],
    #                        [outFull + 'CorticalThickness.nii.gz', ':visible=0:colormap=heat:opacity=0.75'],
    #                        [outFull + 'BrainSegmentation.nii.gz',
    #                         ':visible=1:colormap=lut:colorscale=0,6:opacity=0.75:lut=' +
    #                         brain_segmentation_lut],
    #                        ]

    results_files = OrderedDict(( ('segment', os.path.join(base['results'], 'BrainSegmentation.nii.gz')),
                                  ('p_gm', os.path.join(base['results'], 'gm_posterior.nii.gz')),
                                  ('p_wm', os.path.join(base['results'], 'wm_posterior.nii.gz')),
                                  ('subject_to_template_affine',os.path.join(base['results'],'SubjectToTemplate0GenericAffine.mat',)),
                                  ('subject_to_template_warp',os.path.join(base['results'],'SubjectToTemplate1Warp.nii.gz',)),
                                  ('subject_to_template_jacobian',os.path.join(base['results'],'SubjectToTemplateLogJacobian.nii.gz',)),
                                  ('template_to_subject_warp',os.path.join(base['results'],'TemplateToSubject0Warp.nii.gz',)),
                                  ('template_to_subject_affine',os.path.join(base['results'],'TemplateToSubject1GenericAffine.mat'))
                                  ))

    ants_ct_info = {'base': base, 'input': input_files, 'extract': extract_files,
            'segment':segment_files, 'register':register_files, 'results':results_files}

    if verbose:
        print(ants_ct_info)


    return ants_ct_info

#endregion

def ants_ct_status( out_directory, out_prefix):

     check_files =  [os.path.abspath( os.path.join(out_directory, out_prefix + f)) for f in brain_segmentation_files ]
     check_files += [os.path.abspath( os.path.join(out_directory, out_prefix + f)) for f in registration_files ]

     ants_ct_status = False

     for ii in check_files:
          if os.path.isfile(ii): 
               return True

     return ants_ct_status



def clean( out_dir ):

     os.chdir(out_dir)

     for ii in registration_files + brain_segmentation_files:
          delete_files = glob.glob('*' + ii )     # Delete files regardless of prefix

          for jj in delete_files:
               os.remove( jj )


def results():
    pass
    # BrainExtractionMask.nii.gz
    # BrainSegmentation.nii.gz
    # BrainSegmentationTiledMosaic.png
    # CorticalThickness.nii.gz
    # CorticalThicknessNormalizedToTemplate.nii.gz
    # CorticalThicknessTiledMosaic.png
    # SubjectToTemplate0GenericAffine.mat
    # SubjectToTemplate1Warp.nii.gz
    # SubjectToTemplateLogJacobian.nii.gz
    # TemplateToSubject0Warp.nii.gz
    # TemplateToSubject1GenericAffine.mat

def methods_write_json_redcap_mt_instrument(input_dir, verbose):
    """ Write MagTrans Instrument to JSON output file"""

    cenc_dirs = cenc.directories(input_dir)

    mtr = os.path.join(cenc_dirs['mt']['dirs']['register'], 'mtr.nii.gz')

    label_list = [os.path.join(cenc_dirs['mt']['dirs']['input'], 'gm.cerebral_cortex.nii.gz'),
    os.path.join(cenc_dirs['mt']['dirs']['input'], 'gm.subcortical.nii.gz'),
    os.path.join(cenc_dirs['mt']['dirs']['input'], 'wm.cerebral.nii.gz'),
    os.path.join(cenc_dirs['mt']['dirs']['input'], 'wmlesions_lpa_mask.nii.gz')
    ]

    pandas.set_option('expand_frame_repr', False)

    df_stats_gm_cortical = labels.measure(label_list[0], mtr)
    df_stats_gm_subcortical = labels.measure(label_list[1], mtr)
    df_stats_wm_cerebral = labels.measure(label_list[2], mtr)
    df_stats_wm_lesions = labels.measure(label_list[3], mtr)

    dict_redcap = OrderedDict((('subject_id', cenc_dirs['cenc']['id']),
                               ('antsct_analyst', getpass.getuser()),
                               ('antsct_datetime', '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())),
                               ('antsct_csf_volume_mm3', '{0:4.3f}'.format(df_stats['mean'].values[0])),
                               ('antsct_gm_cortical_volume_mm3', '{0:4.3f}'.format(df_stats['std'].values[0])),
                               ('antsct_wm_volume_mm3', '{0:4.3f}'.format(df_stats['mean'].values[0])),
                               ('antsct_gm_subcortical_mm3','{0:4.3f}'.format(df_stats['std'].values[0])),
                               ('antsct_brainstem', '{0:4.3f}'.format(df_stats['mean'].values[0])),
                               ('antsct_cerebellum', '{0:4.3f}'.format(df_stats['std'].values[0]))
                               )
                              )



    return

def methods_write_json_redcap_ants_ct_instrument(input_file, output_directory, subject_id, output_dir, verbose):

    dict_ants_ct = OrderedDict((('subject_id', cenc_dirs['cenc']['id']),
                               ('act_analyst', getpass.getuser()),
                               ('act_datetime', '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())),
                               ('act_gm_cortical_mean', '{0:4.3f}'.format(df_stats_gm_cortical['mean'].values[0])),
                               ('act_gm_cortical_std', '{0:4.3f}'.format(df_stats_gm_cortical['std'].values[0])),
                               ('act_gm_subcortical_mean',
                                '{0:4.3f}'.format(df_stats_gm_subcortical['mean'].values[0])),
                               ('act_gm_subcortical_std',
                                '{0:4.3f}'.format(df_stats_gm_subcortical['std'].values[0])),
                               ('act_wm_cortical_mean', '{0:4.3f}'.format(df_stats_wm_cerebral['mean'].values[0])),
                               ('act_wm_cortical_std', '{0:4.3f}'.format(df_stats_wm_cerebral['std'].values[0])),
                               ('act_wmlesions_mean', '{0:4.3f}'.format(df_stats_wm_lesions['mean'].values[0])),
                               ('act_wmlesions_std', '{0:4.3f}'.format(df_stats_wm_lesions['std'].values[0]))
                               )
                              )

    magtrans_json_filename = os.path.join(cenc_dirs['mt']['dirs']['02-stats'], 'ants_ct.json')

    with open(magtrans_json_filename, 'w') as outfile:
        json.dump(dict_redcap, outfile, indent=4, ensure_ascii=True, sort_keys=False)


    return

def methods( t1full, t2full, t2flair, options, verbose=False, debug=False, nohup=False):

     print('\nRunnning ants_ct.py\n')
          

     if  qa.qa_input_files( input_files, False):
          
          if not os.path.exists( out_directory ):
               os.makedirs( out_directory )
               
          callCommand = ['antsCorticalThickness.sh', '-d', '3', '-t', options['t_option'], '-w', '0.25',
                         '-e', options['e_option'], '-m', options['m_option'], '-f', options['f_option'], '-p', options['p_option'], 
                         '-o', options['o_option'] 
                         ]
               
          callCommand = callCommand + [ '-a', t1full ] 
          
          if not t2full == None:
               callCommand = callCommand + [ '-a', t2full ] 
               
          if not inArgs.t2flair == None:
               callCommand = callCommand + [ '-a', t2flair ] 
               
          util.iw_subprocess( callCommand, verbose, debug,  nohup )
                    
     else:
          print('Unable to run iwAntsCT.py. Failed input QA.')
          qa.qa_exist( input_files, True )
          print()



#
# Main Function
#

if __name__ == '__main__':

     ## Parsing Arguments
     #
     #

     usage = 'usage: %prog [options] arg1 arg2'

     parser = argparse.ArgumentParser(prog='ants_ct')
     parser.add_argument('--t1full',          help='Full T1w image (default = t1w.nii.gz )', default = 't1w.nii.gz' )
     parser.add_argument('--t2full',          help='T2 TSE used in QI and QO (default = None )', default = None )
     parser.add_argument('--t2flair',         help='T2 Flair used in QI and QO (default = None )', default = None )

     parser.add_argument('--indir',           help='Input directory', default = os.getcwd() )
     parser.add_argument('--outdir',          help='Output directory', default = '../methods/' )

     parser.add_argument('--outprefix',       help='Output prefix', default = '' )

     parser.add_argument('--mask',            help='Mask to use for antsCorticalThickness.sh.', default = None)

     parser.add_argument('-d','--display',    help='Display Results', action='store_true', default=False )
     parser.add_argument('-t','--template',   help='Template', default='inia19', choices=['inia19', 'ixi'])
     parser.add_argument('-v','--verbose',    help='Verbose flag',      action='store_true', default=False )
     parser.add_argument('--debug',           help='Debug flag',      action='store_true', default=False )
     parser.add_argument('--clean',           help=('Clean --outdir by removing files created during'
                                                    'antsCorticalThickness.sh Segmentation and Registration stages. '
                                                    'This will allow you to rerun antsCorticalThickness.sh after you '
                                                    'have edited BrainExtractionMask.nii.gz '),
                         action='store_true', default=False )

     parser.add_argument('--methods',         help='Run processing pipeline',      action='store_true', default=False )
     parser.add_argument('--nohup',           help='nohup',           action='store_true', default=False )

     parser.add_argument('--qa', help='QA methods (input, results, methods)', nargs='*', choices=QA_CHOICES, default=[None])

     parser.add_argument('--results',         help='Create JSON file', action='store_true', default=False)
     parser.add_argument('--results_dir',     help='Results directory', default = '../results/' )

     parser.add_argument('--subject_id',      help='Subject ID. Only used for dumping JSON file.  If not defined then '
                                                   'and empyt Subject ID is used.', action='store_true', default=False)

     inArgs = parser.parse_args()

     # Change director to input directory
     os.chdir( os.path.abspath(inArgs.indir) )

     input_files = [[ inArgs.t1full,':colormap=grayscale']]

     optional_files = [[inArgs.t2flair, ':visible=0:colormap=grayscale']]

     if inArgs.template == 'ixi':
          
          template_dir    =  os.getenv('TEMPLATE_IXI')
          template_prefix = 'ixiTemplate2'

          e_option = template_dir +  template_prefix + '_e_T1wFullImage.nii.gz'
          t_option = template_dir +  template_prefix + '_t_T1wSkullStripped.nii.gz'
          m_option = template_dir +  template_prefix + '_m_BrainCerebellumProbabilityMask.nii.gz'
          f_option = template_dir +  template_prefix + '_f_BrainCerebellumExtractionMask.nii.gz'
          p_option = template_dir + 'priors%d.nii.gz'
          
          p1_option = template_dir + 'priors1.nii.gz'
          p2_option = template_dir + 'priors2.nii.gz'
          p3_option = template_dir + 'priors3.nii.gz'
          p4_option = template_dir + 'priors4.nii.gz'
          p5_option = template_dir + 'priors5.nii.gz'
          p6_option = template_dir + 'priors6.nii.gz'

     elif inArgs.template == 'inia19':

          template_dir    =  os.getenv('TEMPLATE_INIA19')
          template_prefix = 'inia19'

          e_option = os.path.join( template_dir, template_prefix + '_e_T1wFullImage.nii.gz')
          t_option = os.path.join( template_dir, template_prefix + '_t_T1wSkullStripped.nii.gz')
          m_option = os.path.join( template_dir, template_prefix + '_m_BrainProbabilityMask.nii.gz')
          f_option = os.path.join( template_dir, template_prefix + '_f_BrainExtractionMask.nii.gz')
          p_option = os.path.join( template_dir, template_prefix + '_priors0%d.nii.gz')
          
          p1_option = os.path.join( template_dir, template_prefix + '_priors01.nii.gz')
          p2_option = os.path.join( template_dir, template_prefix + '_priors02.nii.gz')
          p3_option = os.path.join( template_dir, template_prefix + '_priors03.nii.gz')
          p4_option = os.path.join( template_dir, template_prefix + '_priors04.nii.gz')
          p5_option = os.path.join( template_dir, template_prefix + '_priors05.nii.gz')
          p6_option = os.path.join( template_dir, template_prefix + '_priors06.nii.gz')
          
     else:
          print('Unknown template')
          quit()


     brain_segmentation_lut = os.path.abspath( os.path.join( os.path.dirname(os.path.abspath(__file__)), 'AntsCorticalThicknessColorLUT.txt'))

     out_directory = os.path.abspath(inArgs.outdir)


     outFull       = os.path.join(out_directory, inArgs.outprefix)

     output_extract_files =  [[ inArgs.t1full, ':visible=1:colormap=grayscale'],
                              [ outFull+'BrainExtractionMask.nii.gz', ':visible=1:colormap=jet:opacity=0.5']
                              ]

     output_segment_files   = [[ inArgs.t1full,                                ':visible=1:colormap=grayscale'],
                               [ outFull+'BrainSegmentationPosteriors3.nii.gz', ':visible=0:colormap=heat:heatscale=0.1,0.5,1:opacity=0.5'],
                               [ outFull+'BrainSegmentationPosteriors2.nii.gz', ':visible=0:colormap=heat:heatscale=0.1,0.5,1:opacity=0.5'],
                               [ outFull+'BrainSegmentationPosteriors1.nii.gz', ':visible=0:colormap=jet:colorscale=0.2,0.1:opacity=0.5'],
                               [ outFull+'BrainSegmentation.nii.gz', ':visible=1:colormap=lut:colorscale=0,6:opacity=0.75:lut='+ 
                                 brain_segmentation_lut]
                               ]

     output_thickness_files =   [[ outFull+'ExtractedBrain0N4.nii.gz',':visible=1:colormap=grayscale'], 
                                 [ outFull+'CorticalThickness.nii.gz',':visible=1:colormap=heat:opacity=0.75']
                                 ]

     output_normalize_files =   [[ t_option,                                    ':visible=0:colormap=grayscale'],
                                 [ outFull+'BrainNormalizedToTemplate.nii.gz',  ':visible=1:colormap=grayscale'],
                                 [ outFull+'CorticalThicknessNormalizedToTemplate.nii.gz', ':visible=1:colormap=heat:opacity=0.75']
                                 ]
     

     output_result_files   = [[ inArgs.t1full,                                ':visible=1:colormap=grayscale'],
                              [ outFull+'BrainSegmentationPosteriors2.nii.gz', ':visible=0:colormap=heat:heatscale=0.1,0.5,1:opacity=0.5'],
                              [ outFull+'BrainSegmentationPosteriors3.nii.gz', ':visible=0:colormap=heat:heatscale=0.1,0.5,1:opacity=0.5'],
                              [ outFull+'CorticalThickness.nii.gz',':visible=0:colormap=heat:opacity=0.75'],        
                              [ outFull+'BrainSegmentation.nii.gz', ':visible=1:colormap=lut:colorscale=0,6:opacity=0.75:lut='+ 
                                brain_segmentation_lut],                             
                               ]



     input_files = [[ inArgs.t1full,':visible=1:colormap=grayscale'],
                    [ inArgs.t2full,':visible=1:colormap=jet:opacity=0.5'],
                    [ e_option, ':visible=0:colormap=grayscale'],
                    [ t_option, ':visible=0:colormap=grayscale'],
                    [ m_option, ':visible=0:colormap=grayscale'],
                    [ f_option, ':visible=0:colormap=grayscale'],
                    [ p1_option, ':visible=0:colormap=jet'],
                    [ p2_option, ':visible=0:colormap=jet'],
                    [ p3_option, ':visible=0:colormap=jet'],
                    [ p4_option, ':visible=0:colormap=jet'],
                    [ p5_option, ':visible=0:colormap=jet'],
                    [ p6_option, ':visible=0:colormap=jet']]
     

     options = { 'e_option': e_option, 't_option':t_option, 'm_option':m_option, 'f_option':f_option,
                 'p_option': p_option, 'p_options':[p1_option, p2_option, p3_option, p4_option, p5_option, p6_option],
                 'o_option': inArgs.outdir + '/' + inArgs.outprefix }


     # Grab info
     ants_ct_info = get_info(inArgs.indir, subject_id=inArgs.subject_id, methods_dir=output_dir,
                             results_dir=inArgs.results, t1=inArgs.t1full, t2=inArgs.t2full, flair=inArgs.t2flair,
                             verbose=inArgs.verbose)

     # QA inputs
     #
         
     if 'input' in inArgs.qa:
          qa.qa_input_files( input_files, True, False )
          qa.freeview( input_files[:2], True, inArgs.verbose )
          qa.freeview( input_files[2:], True, inArgs.verbose )
          
     # Clean Directory

     if inArgs.clean:
          clean( out_directory )

     # Replace Mask

     if inArgs.mask is not None:
          
          if not os.path.exists(out_directory):
               os.makedirs(out_directory)

               shutil.copy2( os.path.abspath( os.path.join(inArgs.indir, inArgs.mask )),
                             os.path.abspath( os.path.join(out_directory, inArgs.outprefix + 'BrainExtractionMask.nii.gz' )))
          else:

               if ants_ct_status( out_directory, inArgs.outprefix):
                    print('\nOutput directory should be cleaned before proceeding.\n')
                    exit()

               
               
     # Methods
     # 
   
     if  inArgs.methods or inArgs.nohup:
          methods(inArgs.t1full, inArgs.t2full, inArgs.t2flair, options, inArgs.verbose, inArgs.debug, inArgs.nohup)

     if 'extract' in inArgs.qa or 'methods' in inArgs.qa:
          qa_methods_extract(output_extract_files)

     if 'segment' in inArgs.qa or 'methods' in inArgs.qa:
          qa_methods_segment(output_segment_files)

     if 'thickness' in inArgs.qa or 'methods' in inArgs.qa:
          qa_methods_normalize(output_thickness_files)

     if 'normalize' in inArgs.qa or 'methods' in inArgs.qa:
          qa_methods_normalize(output_normalize_files)

     # QA Results
     #

     if 'results' in inArgs.qa:
          qa_results(output_result_files)

