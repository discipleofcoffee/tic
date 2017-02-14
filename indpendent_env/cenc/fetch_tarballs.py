#!/usr/bin/env python
"""
SCP copy of CENC partipant ID to local directory for FTP to CENC servers.
"""

import os
import argparse

cenc_local_directory = "/Users/bkraft/cenc/upload"
cenc_remote_directory = "/cenc/mri/subjects/"
cenc_prefix = "34P1"

usage = "usage: %prog [options] arg1 arg2"

parser = argparse.ArgumentParser(prog='cenc_scp')

parser.add_argument("cenc_id_number", help="CENC ID number", nargs='*', type=int)
parser.add_argument("--username", help="username", default='bkraft')
parser.add_argument("--machine", help="machine", default='aging1a.medeng.wfubmc.edu')

inArgs = parser.parse_args()

for ii in inArgs.cenc_id_number:
    cenc_acrostic = "%s%03d" % (cenc_prefix, ii)
    cenc_data_directory = os.path.join(cenc_remote_directory, cenc_acrostic, 'data')

    cenc_tarballs = (os.path.join(cenc_data_directory, 'dicom', cenc_acrostic + '.tar.gz'),
                     os.path.join(cenc_data_directory, 'fmri',  cenc_acrostic + '_fmri.tar.gz')
                     )

    for jj in cenc_tarballs:
        command = "scp {user}@{machine}:{tarball} {local_directory}".format(user=inArgs.username,
                                                                            machine=inArgs.machine,
                                                                            tarball=jj,
                                                                            local_directory=cenc_local_directory)

        os.system(command)