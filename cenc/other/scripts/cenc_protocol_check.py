#!/usr/bin/env python

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
from nibabel.nicom import csareader as csar               
import dicom


#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #

     usage = "usage: %prog [options] arg1 arg2"

     parser = argparse.ArgumentParser(prog='cenc_protocol_check')

     parser.add_argument("in_dcm",            help="DICOM file" )
     parser.add_argument("in_dcm_protocol",   help="CSV DICOM Protocol check" )

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

     if inArgs.debug:
         print "inArgs.display  = " +  str(inArgs.display)
         print "inArgs.debug    = " +  str(inArgs.debug)
         print "inArgs.verbose  = " +  str(inArgs.verbose)

     ds = dicom.read_file(inArgs.in_dcm)
     print ds
     print dir(ds)
     print ds.PatientsName

     csa = csar.get_csa_header(ds, 'b_matrix')
     print csa
#     ascii_header = csa['tags']['MrPhoenixProtocol']['items'][0] 



"""
Patient's Name                      PN: 'CENC_WL_WFU_111315'
Patient ID                          LO: 'CENC_WL_WFU_111315'
Issuer of Patient ID                LO: ''
Patient's Birth Date                DA: '19720101'
Patient's Sex                       CS: 'F'
Patient's Age                       AS: '043Y'
Patient's Size                      DS: '1.5748031516667'
Patient's Weight                    DS: '58.967015601'
Body Part Examined                  CS: 'HEAD'
Scanning Sequence                   CS: ['GR', 'IR']
Sequence Variant                    CS: ['SK', 'SP', 'MP']
Scan Options                        CS: 'IR'
MR Acquisition Type                 CS: '3D'
Sequence Name                       SH: '*tfl3d1_16ns'
Angio Flag                          CS: 'N'
Slice Thickness                     DS: '1.1999999284744'
Repetition Time                     DS: '2300'
Echo Time                           DS: '2.98'
Inversion Time                      DS: '900'
Number of Averages                  DS: '1'
Imaging Frequency                   DS: '123.224884'
Imaged Nucleus                      SH: '1H'
Echo Number(s)                      IS: '1'
Magnetic Field Strength             DS: '3'
Number of Phase Encoding Steps      IS: '240'
Echo Train Length                   IS: '1'
Percent Sampling                    DS: '100'
Percent Phase Field of View         DS: '93.75'
Pixel Bandwidth                     DS: '240'
Device Serial Number                LO: '45255'
Software Version(s)                 LO: 'syngo MR D13'
Protocol Name                       LO: 'SAG MPRAGE'
Transmit Coil Name                  SH: 'Body'
Acquisition Matrix                  US: [0, 256, 240, 0]
In-plane Phase Encoding Direction   CS: 'ROW'
Flip Angle                          DS: '9'
Variable Flip Angle Flag            CS: 'N'
"""



     
