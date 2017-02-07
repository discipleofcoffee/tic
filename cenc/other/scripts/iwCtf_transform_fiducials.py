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
     
     parser = argparse.ArgumentParser(prog='iwCtf_transform_fiducials')
               
     parser.add_argument("in_image",       help="Native image" )
     parser.add_argument("in_fiducials",  help="Fiducials in CSA image space" )

     parser.add_argument("--in_dir",        help="Input directory", default=os.getcwd() )
     parser.add_argument("--out_dir",       help="Output directory", default='..' )
     parser.add_argument("--results_dir",   help="Results directory", default = '../results' )

     parser.add_argument("--reference_ctf",       help="Reference CTF Image", default=None )
     parser.add_argument("--reference_template",  help="Reference Template Image", default=None )

     parser.add_argument("--out_native_image",  help="Output Native Image", default='' )
     parser.add_argument("--out_template_image",  help="Output Template Image", default='' )
     parser.add_argument("--out_ctf_image",  help="Output CTF Image", default='' )

     parser.add_argument("--out_template",      help="Output filename of fiducials in Template World space", default='fiducials_template.csv' )
     parser.add_argument("--out_native",        help="Output filename of fiducials in LPS World space", default='fiducials_native.csv' )
     parser.add_argument("--out_ctf",           help="Output filename of fiducials in CTF World space", default='fiducials_ctf.csv' )

     parser.add_argument("--native_to_template", help="Native to Template transforms." 
                         + "default=[ SubjectToTemplate0GenericAffine.mat, SubjectToTemplate1Warp.nii.gz ] )",
                         nargs=2,
                         default=[ 'SubjectToTemplate0GenericAffine.mat', 'SubjectToTemplate1Warp.nii.gz' ] )

     parser.add_argument("--template_to_native", help="Template to Native transforms." 
                         + "default=[ TemplateToSubject1GenericAffine.mat, TemplateToSubject0Warp.nii.gz ] )",
                         nargs=2,
                         default=[ 'TemplateToSubject1GenericAffine.mat', 'TemplateToSubject0Warp.nii.gz' ] )


     parser.add_argument("--wlps_to_wctf",       help="Filename for affine matrix LPS world to CTF world coordinates",    default='affine_wlps_to_wctf.txt' )
     parser.add_argument("--iras_to_wras",       help="Filename for affine matrix RAS image to RAS world coordinates",    default='affine_iras_to_wras.txt' )
     parser.add_argument("--wras_to_wlps",       help="Filename for affine matrix RAS image to RAS world coordinates",    default='affine_wras_to_wlps.txt' )
     parser.add_argument("--iras_to_wlps",       help="Filename for affine matrix RAS image to RAS world coordinates",    default='affine_iras_to_wlps.txt' )

#     parser.add_argument("--ctf_scale",       help="CTF scale mm -> cm (default=0.1 [mm/cm]) ", type=float, default=1)
    
     parser.add_argument("-p", "--prepare",   help="Prepare data for processing by gathering necessary inputs.",      action="store_true", default=False )
     parser.add_argument("-r", "--run",       help="Run processing pipeline",      action="store_true", default=False )
     parser.add_argument("--run_stage",       help="Stages to run in the processing pipeline", type=int, nargs='*', default = [ 0,1,2,3,4 ] )

     parser.add_argument("--results",       help="Gather results after QC",   action="store_true", default=False )

     parser.add_argument("-v","--verbose",    help="Verbose flag", action="store_true", default=False )
     parser.add_argument("--debug",           help="Debug flag",  action="store_true", default=False )

     parser.add_argument("--qi",            help="QA inputs",      action="store_true", default=False )
     parser.add_argument("--qo",            help="QA outputs",      action="store_true", default=False )
     parser.add_argument("--qo_stage",      help="Stages to run in the processing pipeline (1)", type=int, nargs='*', default = [ 1 ])

     inArgs = parser.parse_args()
     
     #
     #
     #

     input_directory  = os.path.abspath(inArgs.in_dir)

     if os.path.isabs(inArgs.out_dir):
          output_directory = inArgs.out_dir
     else:
          output_directory = os.path.abspath(os.path.join(input_directory, inArgs.out_dir )) 

     if os.path.isabs(inArgs.results_dir):
          results_directory = inArgs.results_dir
     else:
          results_directory = os.path.abspath(os.path.join(input_directory, inArgs.results_dir )) 

     #
     #
     #

     if inArgs.prepare:
          input_directory = ctf_gather_and_prepare( inArgs.in_dir)
     else:
          input_directory = os.path.abspath(inArgs.in_dir)

     output_directory = util.path_relative_to( input_directory, inArgs.out_dir)

     image_native     = util.path_relative_to( input_directory, inArgs.in_image)
     fiducials_native = util.path_relative_to( input_directory, inArgs.in_fiducials)

     reference_ctf      = image_native
     reference_template = util.path_relative_to( input_directory, inArgs.reference_template )


     fiducials_native_icsa = 'fiducials_native_icsa.csv'

     stage_directory = [ os.path.abspath( os.path.join( output_directory,  '00-rename'                  )),
                         os.path.abspath( os.path.join( output_directory,  '01-transform_fiducials'     )),
                         os.path.abspath( os.path.join( output_directory,  '02-transform_images'        ))
                         ] 

     #
     #
     #

     util.print_stage("Displaying inputs to wbi_swi_rigid_to_inia.py", inArgs.verbose )

     if inArgs.verbose:
          print
          print "input_directory  = " +  input_directory
          print "output_directory = " +  output_directory
          print
          print "inArgs.image          = " +  str(inArgs.in_image)
          print "inArgs.in_icsa        = " +  str(inArgs.in_fiducials)
          print
          print "inArgs.iras_to_wras   = " + inArgs.iras_to_wras
          print "inArgs.wras_to_wlps   = " + inArgs.wras_to_wlps
          print "inArgs.wlps_to_wctf   = " + inArgs.wlps_to_wctf
          print
          print "inArgs.verbose        = " +  str(inArgs.verbose)

     #
     # Check input files
     #

     input_files = [ image_native, 
                     fiducials_native,  
                     util.path_relative_to( input_directory, inArgs.native_to_template[0]  ),
                     util.path_relative_to( input_directory, inArgs.native_to_template[1]  ),
                     util.path_relative_to( input_directory, inArgs.template_to_native[0]  ),
                     util.path_relative_to( input_directory, inArgs.template_to_native[1]  )
                     ]

     if os.path.exists(reference_template):
          input_files  = input_files + [ reference_template ]


     if inArgs.run or inArgs.qi:
          util.print_stage("Verifying inputs", inArgs.verbose )
          util.verify_inputs( input_files, inArgs.verbose)


     if inArgs.qi:

 
          util.fslview([image_native], inArgs.verbose)
          

     #
     # Stage 0 - Rename files to a common name by linking
     #
          
     stage0_directory     = stage_directory[0];     

     stage0_input_files   = input_files
     
     stage0_output_files   = [ os.path.abspath( os.path.join( stage0_directory, 'image_native.nii.gz'    )),
                               os.path.abspath( os.path.join( stage0_directory, 'fiducials_native_icsa.csv'   ))
                               ]

     native_to_template   =   [ util.path_relative_to( stage0_directory, 'native_to_template_affine.mat'   ),
                                util.path_relative_to( stage0_directory, 'native_to_template_warp.nii.gz'  )
                                ]

     template_to_native   =   [ util.path_relative_to( stage0_directory, 'template_to_native_affine.mat'   ),
                                util.path_relative_to( stage0_directory, 'template_to_native_warp.nii.gz'  )
                                ]


     stage0_output_files  = stage0_output_files + native_to_template + template_to_native


     if os.path.exists(reference_template):
          reference_template   = util.path_relative_to( stage0_directory, 'reference_template.nii.gz'  )
          stage0_output_files  = stage0_output_files + [ reference_template ] 

     if inArgs.run and (0 in inArgs.run_stage):
          
          util.print_stage('Entering Stage 0 - Renaming input files to common working names', inArgs.verbose) 

          util.verify_inputs(stage0_input_files, inArgs.verbose)
          util.mkcd_dir( stage0_directory )

          for ii in range(0,len(stage0_input_files)):

               if os.path.exists( stage0_output_files[ii] ):
                    os.unlink( stage0_output_files[ii] )

               os.link(stage0_input_files[ii], stage0_output_files[ii] )

          util.verify_outputs(stage0_output_files, inArgs.verbose)

     #
     # Stage 1
     #

     stage1_directory     = stage_directory[1];

     affine_iras_to_wras  = util.path_relative_to( stage1_directory, inArgs.iras_to_wras )
     affine_wras_to_wlps  = util.path_relative_to( stage1_directory, inArgs.wras_to_wlps )
     affine_iras_to_wlps  = util.path_relative_to( stage1_directory, inArgs.iras_to_wlps )
     affine_wlps_to_wctf  = util.path_relative_to( stage1_directory, inArgs.wlps_to_wctf )

     out_fiducials_ctf        = util.path_relative_to( stage1_directory, inArgs.out_ctf )
     out_fiducials_native     = util.path_relative_to( stage1_directory, inArgs.out_native )
     out_fiducials_template   = util.path_relative_to( stage1_directory, inArgs.out_template )
     
     stage1_input_files    = stage0_output_files
     stage1_output_files   = [ affine_iras_to_wlps, affine_iras_to_wlps, affine_wlps_to_wctf, 
                               out_fiducials_ctf, out_fiducials_native, out_fiducials_template  ] 

     if inArgs.run and (1 in inArgs.run_stage):
          
          util.print_stage('Entering Stage 1 - Calculating affine matrices', inArgs.verbose) 

          util.verify_inputs(stage1_input_files, inArgs.verbose)
          util.mkcd_dir( stage1_directory )

          util.link_inputs( stage1_input_files, stage1_directory)


          # iCSA to wLPS
          util.extract_affine(  image_native, affine_iras_to_wlps, True,  False, inArgs.verbose)
          
          ctf.icsa_to_wlps( fiducials_native_icsa, inArgs.out_native,  affine_iras_to_wlps, inArgs.verbose, inArgs.debug )

          # wLPS to wCTF
          # When transforming points use the inverse. I have no idea why. Ask ANTs.

          ctf.calc_matrix( inArgs.out_native, affine_wlps_to_wctf, 1.0, inArgs.verbose)
          ctf.wlps_to_wctf( inArgs.out_native, inArgs.out_ctf, affine_wlps_to_wctf, inArgs.verbose, inArgs.debug)

          # wLPS to wTemplate
          native_to_template_transform = [ template_to_native[1], template_to_native[0] ]

          ctf.transform_points( inArgs.out_native, inArgs.out_template, 
                                    native_to_template_transform, 1.0, inArgs.verbose, inArgs.debug)
          
          util.verify_outputs( stage1_output_files)

     #
     # Stage 2
     #

     stage2_directory     = stage_directory[2];

     out_image_ctf        = util.path_relative_to( stage2_directory, 'native_to_ctf.' + inArgs.in_image)
     out_image_template   = util.path_relative_to( stage2_directory, 'native_to_template.' + inArgs.in_image)

     affine_native_to_template = util.path_relative_to( stage0_directory, 'native_to_template_affine.mat')
     warp_native_to_template   = util.path_relative_to( stage0_directory, 'native_to_template_warp.nii.gz')

     affine_template_to_native = util.path_relative_to( stage0_directory, 'template_to_native_affine.mat')
     warp_template_to_native   = util.path_relative_to( stage0_directory, 'template_to_native_warp.nii.gz')

     stage2_input_files   = [ image_native, affine_native_to_template, warp_native_to_template ] 
                                                     
     stage2_input_files = stage2_input_files + [reference_template]
          
     stage2_input_files    = stage2_input_files + stage1_output_files 
     stage2_output_files   = [ out_image_ctf, out_image_template ] 

     if inArgs.run and (2 in inArgs.run_stage):
          
          util.print_stage('Entering Stage 2 - Transform points and images', inArgs.verbose) 

          util.verify_inputs(stage2_input_files, inArgs.verbose)
          util.mkcd_dir( stage2_directory )

          util.link_inputs( stage2_input_files, stage2_directory)

          command  =['antsApplyTransforms', '-d', '3', '-i', image_native, 
                     '-r', reference_ctf, '-o', out_image_ctf, '-t', affine_wlps_to_wctf ]

          subprocess.Popen( " ".join(command), shell=True )

          print reference_template, os.path.exists( reference_template )

          util.iw_subprocess( ['antsApplyTransforms', '-d', '3', '-i', image_native, 
                               '-r', reference_template, '-o', out_image_template, '-t', warp_native_to_template, affine_native_to_template, '-v'], 
                              inArgs.verbose, inArgs.debug)


          util.iw_subprocess( [ 'iwCreateRoi.py', '--image', image_native, '--csv', 'fiducials_native.csv', '-v', '-r', '--roi_prefix', 'fiducials.'],
                              inArgs.verbose, inArgs.debug)

          util.iw_subprocess( [ 'iwCreateRoi.py', '--image', out_image_template, '--csv', 'fiducials_template.csv', '-v', '-r', '--roi_prefix', 'fiducials.'],
                              inArgs.verbose, inArgs.debug)

          util.iw_subprocess( [ 'iwCreateRoi.py', '--image', out_image_ctf, '--csv', 'fiducials_ctf.csv', '-v', '-r', '--roi_prefix', 'fiducials.'],
                              inArgs.verbose, inArgs.debug)

          util.verify_outputs(stage2_output_files, inArgs.verbose)


     #
     # Gather Results
     # 

     result_inputs   = [ affine_wlps_to_wctf, 
                         out_fiducials_ctf, out_fiducials_native, out_fiducials_template,
                         affine_native_to_template, warp_native_to_template, 
                         affine_template_to_native, warp_template_to_native ] 

     if  inArgs.results:

          util.verify_inputs(result_inputs)
          util.mkcd_dir( results_directory  )
          util.link_inputs(  result_inputs,    results_directory)


     #
     # Quality Outputs
     #

     if inArgs.qo and 1 in inArgs.qo_stage:
          
          util.print_stage('Quality Outputs', True)

          ctf.print_points_from_file( out_fiducials_ctf,      True)
          ctf.print_points_from_file( out_fiducials_native,   True)
          ctf.print_points_from_file( out_fiducials_template, True)

     if inArgs.qo and 2 in inArgs.qo_stage:

          for ii in [ out_image_ctf, image_native, out_image_template]:
               
               util.freeview( [ [ ii, ':colormap=gray'], 
                                [ util.add_prefix_to_filename(ii, 'fiducials.'), ':colormap=jet' ]
                                ], inArgs.verbose, inArgs.debug )

