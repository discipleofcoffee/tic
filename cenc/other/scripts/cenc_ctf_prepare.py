# !/usr/bin/env python

"""

"""

import sys      
import os                                               # system functions
import glob
import shutil
import distutils
import regexp    as re

import argparse
import subprocess
import iwQa
import iwUtilities

def extract_participant( in_dir ):

     match = re.search( '34P1[0-9][0-9][0-9]', in_dir )

     return match.string
                    

#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #

     usage = "usage: %prog [options] arg1 arg2"

     parser = argparse.ArgumentParser(prog='iwAntsCT')
     parser.add_argument("in_dir",      help="Participant directory", default = os.getcwd() )
     parser.add_argument("cenc_dir",    help="CENC data directory", default = os.getenv('CENC_MRI_DATA')) 

     #
     #
     #

     # Change director to input directory
     in_dir os.chdir( os.path.abspath(inArgs.indir) )

     
     id = extract_participant_id( in_dir ) 

     print id
