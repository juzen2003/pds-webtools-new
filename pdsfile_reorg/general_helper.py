################################################################################
# Helper functions being used in the parent class & both pds3 & pds4 subclasses
################################################################################

import pdsgroup

DEFAULT_FILE_CACHE_LIFETIME =  12 * 60 * 60      # 12 hours
LONG_FILE_CACHE_LIFETIME = 7 * 24 * 60 * 60      # 7 days

def cache_lifetime_for_class(arg, cls):
    """Used by caches. Given any object, it returns the default lifetime in
    seconds. A returned lifetime of zero means keep forever.
    """

    # Keep Viewmaster HTML for 12 hours
    if isinstance(arg, str):
        return 12 * 60 * 60

    # Keep RANKS, VOLS, etc. forever
    elif not isinstance(arg, cls):
        return 0

    # Cache PdsFile bundlesets/bundles for a long time, but not necessarily forever
    elif not arg.interior:
        return LONG_FILE_CACHE_LIFETIME

    elif arg.isdir and arg.interior.lower().endswith('data'):
        return LONG_FILE_CACHE_LIFETIME     # .../bundlename/*data for a long time
    elif arg.isdir:
        return 2 * 24 * 60 * 60             # Other directories for two days
    else:
        return DEFAULT_FILE_CACHE_LIFETIME

# For tests
def instantiate_target_pdsfile_for_class(path, cls, holdings_dir, is_abspath=True):
    if is_abspath:
        TESTFILE_PATH = holdings_dir + '/' + path
        target_pdsfile = cls.from_abspath(TESTFILE_PATH)
    else:
        TESTFILE_PATH = path
        target_pdsfile = cls.from_logical_path(TESTFILE_PATH)
    return target_pdsfile

def get_pdsfiles_for_class(paths, cls, holdings_dir, is_abspath=True):
    pdsfiles_arr = []
    if is_abspath:
        for path in paths:
            TESTFILE_PATH = holdings_dir + '/' +  path
            target_pdsfile = cls.from_abspath(TESTFILE_PATH)
            pdsfiles_arr.append(target_pdsfile)
    else:
        for path in paths:
            TESTFILE_PATH = path
            target_pdsfile = cls.from_logical_path(TESTFILE_PATH)
            pdsfiles_arr.append(target_pdsfile)
    return pdsfiles_arr

def get_pdsgroups_for_class(paths_group, cls, holdings_dir, is_abspath=True):
    pdsgroups_arr = []
    for paths in paths_group:
        pdsfiles = get_pdsfiles_for_class(paths, cls, holdings_dir, is_abspath)
        target_pdsgroup = pdsgroup.PdsGroup(pdsfiles=pdsfiles)
        pdsgroups_arr.append(target_pdsgroup)
    return pdsgroups_arr

def opus_products_test_for_class(
    input_path, cls, holdings_dir, expected, is_abspath=True
):
    target_pdsfile = instantiate_target_pdsfile_for_class(input_path, cls,
                                                          holdings_dir, is_abspath)
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
