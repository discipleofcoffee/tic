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

from nipype.interfaces.ants import Registration
import nipype.interfaces.fsl as fsl

from   nipype.pipeline.engine import Workflow, Node


def extract_participant_id(in_dir, pattern):
     match = re.findall(pattern, in_dir)

     if not len(match) == 1:
          sys.exit('Participant ID not found')

     return match[0]

def main():
     ## Parsing Arguments
     #
     #

     usage = "usage: %prog"
     parser = argparse.ArgumentParser(prog='cenc_id')
     parser.add_argument("--in_cenc", help="CENC integer, acrostic, or directory", default = os.getcwd() )
     parser.add_argument("--cenc_dir", help="CENC integer, acrostic, or directory", default = os.getenv('CENC_MRI_DATA') )
     parser.add_argument("-m", "--method", help="Methods for ID. (list, update)", choices=['list','update','get'], default='get')
     parser.add_argument("--filter", help="Filter IDs", choices=['test','study','all'], default='study')
     parser.add_argument("-v", "--verbose", help="verbose flag", action="store_true", default=False )
     parser.add_argument("-o", "--output",  help="Return IDs as output", action="store_true", default=False )
     inArgs = parser.parse_args()

     output_flag = inArgs.output

     if inArgs.method in 'list':
          results = cenc.participants(inArgs.cenc_dir, inArgs.method, inArgs.filter, inArgs.verbose)

     if inArgs.method in 'update':
          results = cenc.participants(inArgs.cenc_dir, inArgs.method, inArgs.filter, inArgs.verbose)

     if inArgs.method in 'get':
          results = cenc.participant_id(inArgs.in_cenc)
          output_flag = True

     if output_flag:
          return results
     else:
          return
 
#
# Main Function
#

if __name__ == "__main__":
    sys.exit(main())

