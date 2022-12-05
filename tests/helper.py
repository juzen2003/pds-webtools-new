import os
import pdsfile
import pdsgroup
import pdsgrouptable

try:
    PDS_HOLDINGS_DIR = os.environ['PDS_HOLDINGS_DIR']
except KeyError: # pragma: no cover
    PDS_HOLDINGS_DIR = os.path.realpath('/Library/WebServer/Documents/holdings')

def instantiate_target_pdsfile(path, is_abspath=True):
    if is_abspath:
        TESTFILE_PATH = PDS_HOLDINGS_DIR + '/' + path
        target_pdsfile = pdsfile.PdsFile.from_abspath(TESTFILE_PATH)
    else:
        TESTFILE_PATH = path
        target_pdsfile = pdsfile.PdsFile.from_logical_path(TESTFILE_PATH)
    return target_pdsfile

def get_pdsfiles(paths, is_abspath=True):
    pdsfiles_arr = []
    if is_abspath:
        for path in paths:
            TESTFILE_PATH = PDS_HOLDINGS_DIR + '/' +  path
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
        target_pdsgroup = pdsgroup.PdsGroup(pdsfiles=pdsfiles)
        pdsgroups_arr.append(target_pdsgroup)
    return pdsgroups_arr

def opus_products_test(input_path, expected):
    target_pdsfile = instantiate_target_pdsfile(input_path)
    res = target_pdsfile.opus_products()
    msg = (f'Total number of products ({len(res)}) does not match the expected'+
           f' results ({len(expected)})')
    assert len(res) == len(expected), msg
    for key in res:
        assert key in expected, f'"{key}" does not exist'
        all_files = []
        all_files_abspath = []
        for files in res[key]:
            all_files += files
        msg = f'Total number of files does not match under {key}'
        if len(all_files) != len(expected[key]):
            print(len(all_files))
            print(len(expected[key]))
        assert len(all_files) == len(expected[key]), msg
        for pdsf in all_files:
            if pdsf.abspath not in expected[key]:
                print(pdsf.abspath)
                print(key)
            msg = f'{pdsf.logical_path} does not exist under {key}'
            assert pdsf.abspath in expected[key], msg
            all_files_abspath.append(pdsf.abspath)
        msg = f'File does not match under {key}'
        assert all_files_abspath.sort() == expected[key].sort(), msg
