#!/usr/bin/env python

import sys      
import os                                               # system functions
import shutil

import argparse
import iwUtilities     as util

import nibabel as nb
import pandas as pd
import numpy as np



def ctf_calc_affine(in_rotate, in_translate, in_origin):

     affine_ctf          = np.zeros((4,4))
     affine_ctf[3,3]     = 1 
     affine_ctf[0:3,0:3] = rotate_ctf
     affine_ctf[0:3,3]   = translate_ctf

     return affine_ctf


def ctf_calc_rotate_translate_origin( in_nas,  in_lpa, in_rpa, in_scale=1 ):

    nas = np.array( [ in_nas[0], in_nas[1], in_nas[2] ] )
    rpa = np.array( [ in_rpa[0], in_rpa[1], in_rpa[2] ] )
    lpa = np.array( [ in_lpa[0], in_lpa[1], in_lpa[2] ] )
    
    origin_ctf = 0.5 * (rpa+lpa)
    x_ctf = norm(nas - origin_ctf)
    z_ctf = norm( np.cross( x_ctf, lpa-rpa))
    y_ctf = norm( np.cross( z_ctf, x_ctf))
    
    rotate_ctf    = in_scale * np.matrix( [x_ctf, y_ctf, z_ctf ]).getT().getI()
    translate_ctf = -np.dot(rotate_ctf, origin_ctf)

    return [rotate_ctf, translate_ctf, origin_ctf ]


def norm(x):

     x_norm = np.linalg.norm(x)

     if not x_norm == 0:
          return x/x_norm
     else:
          print "Error: norm of vector is 0"
          quit()

#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #
     
     parser = argparse.ArgumentParser(prog='iwCtf_matrices')
               
     parser.add_argument("image",           help="CTF reference image" )
     parser.add_argument("in_icsa",         help="Fiducials in CSA image space" )

     parser.add_argument("--in_dir",        help="Input directory", default=os.getcwd() )
     parser.add_argument("--out_dir",       help="Output directory", default='..' )

     parser.add_argument("--out_iras",      help="Output filename of fiducials in RAS image space", default='fiducials_iras.csv' )
     parser.add_argument("--out_wlps",      help="Output filename of fiducials in LPS World space", default='fiducials_wlps.csv' )
     parser.add_argument("--out_wctf",      help="Output filename of fiducials in CTF World space", default='fiducials_wctf.csv' )

     parser.add_argument("--wlps_to_wctf",       help="Filename for affine matrix LPS world to CTF world coordinates",    default='affine_wlps_to_wctf.txt' )
     parser.add_argument("--iras_to_wras",       help="Filename for affine matrix RAS image to RAS world coordinates",    default='affine_iras_to_wras.txt' )

     parser.add_argument("--wras_to_wlps",         help="Filename for affine matrix RAS world to LPS world coordinates", default='affine_wras_to_wlps.txt' )

     parser.add_argument("--ctf_scale",    help="CTF scale from index to physical units [cm^3]. Assume isotropic. (default=0.1 [cm^3]) ",
                                           type=float, default=.1)
    
     parser.add_argument("-r", "--run",               help="Run processing pipeline",      action="store_true", default=False )
     parser.add_argument("--run_stage",       help="Stages to run in the processing pipeline", type=int, nargs='*', default = [ 0,1,2,3,4 ] )

     parser.add_argument("-v","--verbose",    help="Verbose flag",      action="store_true", default=False )

     inArgs = parser.parse_args()
     
     #
     #
     #


     input_directory  = os.path.abspath(inArgs.in_dir)
     output_directory = util.path_relative_to( input_directory, inArgs.out_dir)

     #
     #
     #

     util.print_stage("Displaying inputs to wbi_swi_rigid_to_inia.py", inArgs.verbose )

     if inArgs.verbose:
          print
          print "input_directory  = " +  input_directory
          print "output_directory = " +  output_directory
          print
          print "inArgs.image          = " +  str(inArgs.image)
          print "inArgs.in_icsa        = "  +  str(inArgs.in_icsa)
          print "inArgs.out_iras       = "  +  str(inArgs.out_iras)
          print "inArgs.out_wlps       = "  +  str(inArgs.out_wlps)
          print "inArgs.iras_to_wras   = " +  str(inArgs.iras_to_wras)
          print "inArgs.wras_to_wlps   = " +  str(inArgs.wras_to_wlps)
          print "inArgs.wlps_to_wctf   = " +  str(inArgs.wlps_to_wctf)
          print "inArgs.verbose        = " +  str(inArgs.verbose)

     #
     #
     #

     stage_directory = [ os.path.abspath( os.path.join( output_directory,  '00-rename'      )),
                         os.path.abspath( os.path.join( output_directory,  '01-matrices'    )),
                         os.path.abspath( os.path.join( output_directory,  '02-transformed' ))
                         ] 
    
     print
     print output_directory
     print stage_directory
     print

     #
     # Check input files
     #
     util.print_stage("Verifying inputs", inArgs.verbose )

     input_files =      [ os.path.abspath( os.path.join( input_directory, inArgs.image       )),
                          os.path.abspath( os.path.join( input_directory, inArgs.in_icsa     ))
                          ]

     util.verify_inputs( input_files, inArgs.verbose)

     image_filename = input_files[0]
     icsa_fiducials = input_files[1]

     #
     # Check inputs
     #     

     if inArgs.in_icsa.count('.') > 1:
         print
         print inArgs.in_icsa + " must contain only one \".\" "
         print
         exit()


     img           = nb.load(image_filename)
     header        = img.get_header()

     img_affine_matrix_ras = np.asarray(img.get_affine())
     data_shape        = np.asarray( header.get_data_shape() )
     data_pixel_size   = np.asarray( header.get_zooms()      )

     if not np.all( data_shape ==  256 ):
         print
         print inArgs.image + "\'s data shape is " + str(data_shape)
         print "It must be [ 256 256 256 ]. Zero pad image accordingly before continuing."
         print
         exit()

     if not np.all(data_pixel_size == data_pixel_size[0]):
         print
         print inArgs.img + "pixel dimensions must be isotropic."
         print data_pixel_size
         print
         exit()


     ctf_scale = inArgs.ctf_scale


     #
     # Stage 0 - Rename files to a common name by linking
     #
     
     
#     stage0_directory     = stage_directory[0];
     
#     stage0_input_files   = [   swi, swi_mag, swi_phase,  t1w, template ]

     
#     stage0_output_files   = [ os.path.abspath( os.path.join( stage0_directory, 'swi.nii.gz'       )),
#                               os.path.abspath( os.path.join( stage0_directory, 'swi_mag.nii.gz'   )),
#                               os.path.abspath( os.path.join( stage0_directory, 'swi_phase.nii.gz' )),
#                               os.path.abspath( os.path.join( stage0_directory, 't1w.nii.gz'       )), 
#                               os.path.abspath( os.path.join( stage0_directory, 'template.nii.gz'  )) 
#                               ] 


#     if inArgs.run and (0 in inArgs.run_stage):
#          
#          util.print_stage('Entering Stage 0 - Renaming input files to common working names', inArgs.verbose) 

#          util.verify_inputs(stage0_input_files, inArgs.verbose)
#          util.mkcd_dir( stage0_directory )

#          for ii in range(0,len(stage0_input_files)):

#               if os.path.exists( stage0_output_files[ii] ):
#                    os.unlink( stage0_output_files[ii] )

#               os.link(stage0_input_files[ii], stage0_output_files[ii] )

#          util.verify_outputs(stage0_output_files, inArgs.verbose)
     
     #
     # Stage 1
     #

     stage1_directory      = stage_directory[1];
     print stage1_directory

     stage1_input_files    = input_files
     
     stage1_output_files   = [ os.path.abspath( os.path.join( stage1_directory, inArgs.iras_to_wras  )),
                               os.path.abspath( os.path.join( stage1_directory, inArgs.wras_to_wlps  )),
                               os.path.abspath( os.path.join( stage1_directory, inArgs.out_iras      )),
                               os.path.abspath( os.path.join( stage1_directory, inArgs.wlps_to_wctf  )),
                               os.path.abspath( os.path.join( stage1_directory, inArgs.out_wlps      )),
                               os.path.abspath( os.path.join( stage1_directory, inArgs.out_wctf      ))
                               ] 

     affine_out_iras_to_wras  = stage1_output_files[0] 
     affine_out_wras_to_wlps  = stage1_output_files[1] 
     affine_out_wlps_to_wctf  = stage1_output_files[3] 

     fiducials_out_iras = stage1_output_files[2]
     fiducials_out_wlps = stage1_output_files[4]
     fiducials_out_wctf = stage1_output_files[5]

     print stage1_output_files

     if inArgs.run and (1 in inArgs.run_stage):
          
          util.print_stage("Entering Stage 1 - Creating matrices", inArgs.verbose)
               
          util.verify_inputs(stage1_input_files, inArgs.verbose)
          util.mkcd_dir( stage1_directory )
          util.link_inputs( stage1_input_files,  stage1_directory)


          #
          # Save ITK affine matrix
          #
          

          if inArgs.verbose:
               print
               print "Image affine RAS image to RAS world  matrix"
               print img_affine_matrix_ras
               print
               
               util.save_itk_affine_matrix( img_affine_matrix_ras, affine_out_iras_to_wras, inArgs.verbose )
               
               #          
               #
               #
               
               affine_wras_to_wlps = np.asarray([[ -1, 0, 0, 0], [0, -1, 0, 0], [0,0,1,0], [0,0,0,1]])
               
               util.save_itk_affine_matrix( affine_wras_to_wlps, affine_out_wras_to_wlps, inArgs.verbose )
               
               #
               # Save CSA to LPS affine matrix
               #
               
               df=pd.read_csv(inArgs.in_icsa, sep=',',header=0)
               
               if inArgs.verbose:
                    print "OUT fiducials as defined in " + inArgs.in_icsa 
                    print df
                    print
                    
                    lpa_icsa = np.asarray(df.values[0,0:3])
                    nas_icsa = np.asarray(df.values[1,0:3])
                    rpa_icsa = np.asarray(df.values[2,0:3])
                    
                    if not ( (lpa_icsa[1] < nas_icsa[1]) and (nas_icsa[1] < rpa_icsa[1])  ):
                         print
                         print 'Fiducials must be listed left to right in OUT fiducial file'
                         print
                         print df.values
                         print
                         exit()
                         
                    if not ( (nas_icsa[0] < lpa_icsa[0]) and (nas_icsa[0] < rpa_icsa[0])  ):
                        print
                        print 'Nasion point coronal index must be less than LPA and RPA coronal index'
                        print
                        print df.values
                        print
                        exit()
                              
                    if not np.all( np.less( lpa_icsa, 256*np.ones(3) ) ):
                         print
                         print 'All image indices for LPA fiducial must be less than 255'
                         print df.values[0]
                         print
                         exit()
                                   
                    if not np.all( np.less( nas_icsa, 256*np.ones(3) ) ):
                         print
                         print 'All image indices for Nasion fiducial must be less than 255'
                         print df.values[1]
                         print
                         exit()

                    if not np.all( np.less( rpa_icsa, 256*np.ones(3) ) ):
                         print
                         print 'All image indices for RPA fiducial must be less than 255'
                         print df.values[2]
                         print
                         exit()

                    #
                    # Convert OUT fiducials from CSA image  to RAS image
                    #
                         
                    lpa_iras = [ lpa_icsa[1],  255-lpa_icsa[0], 255-lpa_icsa[2] ]
                    nas_iras = [ nas_icsa[1],  255-nas_icsa[0], 255-nas_icsa[2] ]
                    rpa_iras = [ rpa_icsa[1],  255-rpa_icsa[0], 255-rpa_icsa[2] ]
                    
                    wlps_list  = [
                         reduce(lambda x, y: x+y, [ lpa_iras,  df.values[0,3:6].tolist()  ]),
                         reduce(lambda x, y: x+y, [ nas_iras,  df.values[1,3:6].tolist()  ]),
                         reduce(lambda x, y: x+y, [ rpa_iras,  df.values[2,3:6].tolist()  ]) ]
                    
                    df_iras = pd.DataFrame(wlps_list, columns=[ 'x','y','z','t','label', 'comment'])

                    if inArgs.verbose:
                         print "OUT fiducials in RAS image coordinates"
                         print df_iras
                         print
                         
                    df_iras.to_csv(stage1_output_files[2], sep=',',header=1, index=False)
 
                    #
                    # Calculate RAS Image to LPS World matrix 
                    #


                    img_affine_matrix_lps = np.multiply( affine_wras_to_wlps,  img_affine_matrix_ras)
                    
                    lpa_wras = np.dot(img_affine_matrix_ras, np.concatenate( (lpa_iras, [1]) ))
                    nas_wras = np.dot(img_affine_matrix_ras, np.concatenate( (nas_iras, [1]) ))
                    rpa_wras = np.dot(img_affine_matrix_ras, np.concatenate( (rpa_iras, [1]) ))
                    
                    lpa_wlps = np.dot(affine_wras_to_wlps, lpa_wras )
                    nas_wlps = np.dot(affine_wras_to_wlps, nas_wras )
                    rpa_wlps = np.dot(affine_wras_to_wlps, rpa_wras )
                    
                    [ rotate_ctf, translate_ctf, origin_ctf ] = ctf_calc_rotate_translate_origin( nas_wlps, lpa_wlps, rpa_wlps, ctf_scale)
                    
                    affine_ctf = ctf_calc_affine( rotate_ctf, translate_ctf, 0*origin_ctf)
                    
                    if inArgs.verbose:
                         print
                         print "Image LPS World to CTF matrix"
                         print affine_ctf
                         print

                    util.save_itk_affine_matrix( affine_ctf, affine_out_wlps_to_wctf, inArgs.verbose )


                    #
                    # Save OUT Fiducials in LPS World space. 
                    #
                    
                    util.verify_outputs( stage1_output_files[0:3] )
                    
                    cmd = [ "antsApplyTransformsToPoints", "-d", "3", "-i", fiducials_out_iras, "-o",  fiducials_out_wlps, "-t", inArgs.iras_to_wras, inArgs.wras_to_wlps ]
                    util.iw_subprocess(cmd, inArgs.verbose, inArgs.verbose)


                    #
                    # Save OUT Fiducials in CTF World space. 
                    #
                    
                    util.verify_that_file_exists(fiducials_out_wlps)

                    cmd = [ "antsApplyTransformsToPoints", "-d", "3", "-i", fiducials_out_iras, "-o",  fiducials_out_wctf, "-t", inArgs.iras_to_wras, inArgs.wras_to_wlps, inArgs.wlps_to_wctf ]
                    util.iw_subprocess(cmd, inArgs.verbose, inArgs.verbose)
                    
                    
                    util.verify_outputs( stage1_output_files )
