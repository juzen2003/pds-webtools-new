import os
import pdsfile

PDS_DATA_DIR = os.environ['PDS_DATA_DIR']

def instantiate_target_pdsfile(path, is_abspath=True):
    if is_abspath:
        TESTFILE_PATH = PDS_DATA_DIR + '/' + path
        target_pdsfile = pdsfile.PdsFile.from_abspath(TESTFILE_PATH)
    else:
        TESTFILE_PATH = path
        target_pdsfile = pdsfile.PdsFile.from_logical_path(TESTFILE_PATH)
    return target_pdsfile

def get_pdsfiles(paths, is_abspath=True):
    pdsfiles_arr = []
    if is_abspath:
        for path in paths:
            TESTFILE_PATH = PDS_DATA_DIR + '/' +  path
            target_pdsfile = pdsfile.PdsFile.from_abspath(TESTFILE_PATH)
            pdsfiles_arr.append(target_pdsfile)
    else:
        for path in paths:
            TESTFILE_PATH = path
            target_pdsfile = pdsfile.PdsFile.from_logical_path(TESTFILE_PATH)
            pdsfiles_arr.append(target_pdsfile)
    return pdsfiles_arr

def get_pdsgroups(paths_group, is_abspath=True):
    pdsgroups_arr = []
    for paths in paths_group:
        pdsfiles = get_pdsfiles(paths, is_abspath)
        pdsgroup = pdsfile.PdsGroup(pdsfiles=pdsfiles)
        pdsgroups_arr.append(pdsgroup)
    return pdsgroups_arr
