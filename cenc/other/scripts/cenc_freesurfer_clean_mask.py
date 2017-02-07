#!/usr/bin/env python

"""

"""
import sys
import os                                               # system functions
import re

import argparse
import iwUtilities as util

import nipype.interfaces.fsl as fsl
import nipype.interfaces.freesurfer as fs 


def main():
     ## Parsing Arguments
     #
     #

     usage = "usage: %prog [options] arg1 arg2"

     parser = argparse.ArgumentParser(prog='cenc_freesurfer')

     parser.add_argument("--brainmask",  help="Freesurfer brainmask.nii.gz", default = 'brainmask.nii.gz')
     parser.add_argument("--aseg",       help="Aseg", default = 'aseg.nii.gz')
     parser.add_argument("--out",       help="Aseg", default = 'mask.nii.gz' )

     inArgs = parser.parse_args()

     # Create final brain mask

     brainmask = inArgs.brainmask
     aseg      = inArgs.aseg
     mask      = inArgs.out

     maths = fsl.ImageMaths(in_file=brainmask,
                            op_string= '-bin -kernel box 12 -ero -add ' + aseg + ' -bin -kernel box 9 -dilM -kernel box 7 -ero',
                            out_file=mask)
     print maths.cmdline

     maths.run()


#
# Main Function
#

if __name__ == "__main__":
    sys.exit(main())

