#!/usr/bin/env python

import argparse
import iwCtf           as ctf
import iwUtilities     as util


#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #
     
     parser = argparse.ArgumentParser(prog='iwCtf_iras_to_wlps')
               
     parser.add_argument("in_filename",         help="CSV input points"   )
     parser.add_argument("out_filename",        help="CSV output points"  )
     parser.add_argument("-t", "--transform",   help="Affine image transform", nargs=1 )

     parser.add_argument("-v","--verbose",    help="Verbose flag",      action="store_true", default=False )
     parser.add_argument("--debug",           help="Debug flag",      action="store_true", default=False )

     inArgs = parser.parse_args()

     util.verify_inputs([ inArgs.in_filename ] +  inArgs.transform, inArgs.debug)

     ctf.wlps_to_iras( inArgs.in_filename, inArgs.out_filename, inArgs.transform, inArgs.verbose, inArgs.debug)
