#!/usr/bin/env python

import iwCtf       as ctf
import argparse

#
# Main Function
#

if __name__ == "__main__":

     ## Parsing Arguments
     #
     #
     
     parser = argparse.ArgumentParser(prog='iwCtf_print_points')
     parser.add_argument("in_points",           help="ANTs Label Point file" )
     inArgs = parser.parse_args()
     
     ctf.print_points_from_file( inArgs.in_points, True)
               
 
