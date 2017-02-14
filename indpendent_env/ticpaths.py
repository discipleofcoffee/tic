# coding: utf-8
# a script to query the location of site-packages and write a pth file with the paths to tic project directories.
import sys
from pprint import pprint

paths = sys.path
# pprint.pprint(paths)

if paths[0][0] == '/': # if the first path starts with / then it's a *nix system, else windows.
    dir_sep = '/'
else:
    dir_sep = '\\'
site_dir = "site-packages"
site_dir_loc = list()
not_site_loc = list()
for path in paths:
    if site_dir in (path.rpartition(dir_sep)[2]):
        site_dir_loc.append(path)
    else:
        not_site_loc.append(path)
pprint(site_dir_loc)
print()
pprint(not_site_loc)

"""
tic paths-


"""