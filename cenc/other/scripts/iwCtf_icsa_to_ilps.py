#!/usr/bin/env python

import sys      
import os                                               # system functions
import shutil

import argparse
import iwUtilities     as util

import pandas as pd

def print_points( in_filename, in_pdframe, verbose_flag=False):

     if verbose_flag:
         print 
         print in_filename
         print '----------------------------------------'
         print in_pdframe
         print


def icsa_to_ilps(in_filename, out_filename, verbose_flag=False):

     
     in_points = pd.read_csv(in_filename, names=['c','s','a','t','label', 'comment'], skiprows=[0])
     
     print_points( in_filename, in_points, verbose_flag)

     out_points = in_points.copy()
     out_points.columns = ['l','p','s','t','label','comment']

     out_points['l'] =     in_points['s']
     out_points['p'] =     in_points['c']
     out_points['s'] = 256-in_points['a']

     print_points( out_filename, out_points, verbose_flag)

     return out_points




#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #
     
     parser = argparse.ArgumentParser(prog='iwCtf_icsa_to_iras')
               
     parser.add_argument("in_filename",         help="CSV input points" )
     parser.add_argument("out_filename",        help="CSV output points" )

     parser.add_argument("-v","--verbose",    help="Verbose flag",      action="store_true", default=False )

     inArgs = parser.parse_args()

     #
     #
     #

     out_points = icsa_to_ilps(inArgs.in_filename, inArgs.out_filename, inArgs.verbose)
     
     out_points.to_csv(inArgs.out_filename, index=False)



     
