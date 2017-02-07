# !/usr/bin/env python

"""

"""

import sys      
import os                                               # system functions
import glob
import shutil
import distutils

import argparse
import subprocess
import iwQa
import iwUtilities

                    

#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #

     usage = "usage: %prog [options] arg1 arg2"

     class MyParser(argparse.ArgumentParser):
         def error(self, message):
             sys.stderr.write('error: %s\n' % message)
             self.print_help()
             sys.exit(2)

#fiducials_freeview_ras_image.csv
#fiducials_meg_csa_image.csv
#inia19_e_T1wFullImage.nii.gz
#pad.t1w.nii.gz
#rois_meg_ctf.csv
#SubjectToTemplate0GenericAffine.mat
#SubjectToTemplate1Warp.nii.gz
#t1w.nii.gz
#TemplateToSubject0Warp.nii.gz
#TemplateToSubject1GenericAffine.mat

     parser = argparse.ArgumentParser(prog='cenc_ctf')

     parser.add_argument("--image",             help="CTF reference image" )
     parser.add_argument("--mri_fiducials",     help="MRI fiducials (LPS space)" )
     parser.add_argument("--meg_fiducials",     help="MEG fiducials (LPS space)" )
     parser.add_argument("--ctf_rois",          help="MEG ROIs      (CTF space)" )

     parser.add_argument("--template",          help="Template Image" )

     parser.add_argument("--template_s2t_affine",    help="Template Image" )
     parser.add_argument("--template_s2t_warp",      help="Template Image" )
     parser.add_argument("--template_t2s_affine",    help="Template Image" )
     parser.add_argument("--template_t2s_warp",      help="Template Image" )


     parser.add_argument("--indir",           help="Input directory", default = os.getcwd() )
     parser.add_argument("--outdir",          help="Output directory", default = os.getcwd() )
     parser.add_argument("--outprefix",       help="Output prefix", default = "antsCT_" )
     parser.add_argument("-d","--display",    help="Display Results", action="store_true", default=False )
     parser.add_argument("-t","--template",   help="Template", default='inia19', choices=['inia19', 'ixi'])
     parser.add_argument("-v","--verbose",    help="Verbose flag",      action="store_true", default=False )
     parser.add_argument("--debug",           help="Debug flag",      action="store_true", default=False )
     parser.add_argument("--clean",           help="Clean directory by deleting intermediate files",      action="store_true", default=False )
     parser.add_argument("--qi",              help="QA inputs",      action="store_true", default=False )
     parser.add_argument("--qo",              help="QA outputs",      action="store_true", default=False )
     parser.add_argument("--nohup",           help="nohup",           action="store_true", default=False )
     parser.add_argument("-r", "--run",       help="Run processing pipeline",      action="store_true", default=False )

     inArgs = parser.parse_args()

     # Change director to input directory
     os.chdir( os.path.abspath(inArgs.indir) )

     input_files = [[ inArgs.t1full,":colormap=grayscale"]]

     optional_files = [[inArgs.t2flair, ":visible=0:colormap=grayscale"]]

     out_directory = os.path.abspath(inArgs.outdir)
     outFull       = os.path.join(out_directory, inArgs.outprefix)

     output1_files   = [[ inArgs.t1full,  ":visible=0:colormap=grayscale"],
                       [ outFull+"BrainSegmentationPosteriors1.nii.gz", ":visible=0:colormap=jet:colorscale=0.2,0.1:opacity=0.5"]]

     input_files = [[ inArgs.forward,":colormap=grayscale"],
                    [ inArgs.reverse,":colormap=jet"]]

     if inArgs.debug:
         print "inArgs.display  = " +  str(inArgs.display)
         print "inArgs.debug    = " +  str(inArgs.debug)
         print "inArgs.verbose  = " +  str(inArgs.verbose)



     # Quality Assurance input
     #
         
     if  inArgs.qi:
         iwQa.qa_input_files( input_files, True )

     
     # Run    
     # 
   
     if  inArgs.run or inArgs.nohup:          

          print "Runnning iwTopUp.py"

          if  iwQa.qa_input_files( input_files, False):

               if not os.path.exists( out_directory ):
                    os.makedirs( out_directory )

               command = ["antsCorticalThickness.sh", "-d", "3", "-a", inArgs.t1full, "-t", t_option, "-w", "0.25",
                          "-e", e_option, "-m", m_option, "-f", f_option, "-p", p_option, "-o", inArgs.outdir + "/" + inArgs.outprefix ]
               
               local_subprocess(command, inArgs.nohup )
             
          else:
               print "Unable to run iwAntsCT.py. Failed input QA."
               iwQa.qa_exist( input_files, True )
               print


     # Quality Assurance output
     #

     if  inArgs.qo:

          if iwQa.qa_exist(output1_files, False ):
               iwQa.freeview( output1_files ) 
          else:
               print "Unable to QO iwAntsCT.py. Failed output1 QA."
               iwQa.qa_exist( output1_files, True )
               print
