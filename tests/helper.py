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

def opus_products_test(input_path, expected):
    target_pdsfile = instantiate_target_pdsfile(input_path)
    res = target_pdsfile.opus_products()
    msg = (f'Total number of products ({len(res)}) does not match the expected'+
           f' results ({len(expected)})')
    assert len(res) == len(expected), msg
    for key in res:
        assert key in expected
        all_files = []
        all_files_abspath = []
        for files in res[key]:
            all_files += files
        msg = f'Total number of files does not match under {key}'
        assert len(all_files) == len(expected[key]), msg
        for pdsf in all_files:
            assert pdsf.abspath in expected[key]
            all_files_abspath.append(pdsf.abspath)
        msg = f'Files does not match under {key}'
        assert all_files_abspath.sort() == expected[key].sort(), msg
