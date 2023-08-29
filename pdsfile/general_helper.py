##########################################################################################
# pdsfile/general_helper.py
# Helper functions being used in tests, the parent class & both pds3 & pds4 subclasses
##########################################################################################

import pdsgroup
import os

# For tests
# try:
#     PDS_HOLDINGS_DIR = os.environ['PDS_HOLDINGS_DIR']
# except KeyError: # pragma: no cover
#     PDS_HOLDINGS_DIR = os.path.realpath('/Library/WebServer/Documents/holdings')

# try:
#     PDS4_HOLDINGS_DIR = os.environ['PDS4_HOLDINGS_DIR']
# except KeyError: # pragma: no cover
#     # TODO: update this when we know the actual path of pds4 holdings on the webserver
#     PDS4_HOLDINGS_DIR = os.path.realpath('/Library/WebServer/Documents/holdings')

# PDS4_BUNDLES_DIR = f'{PDS4_HOLDINGS_DIR}/bundles'

DEFAULT_FILE_CACHE_LIFETIME =  12 * 60 * 60      # 12 hours
LONG_FILE_CACHE_LIFETIME = 7 * 24 * 60 * 60      # 7 days
SHORT_FILE_CACHE_LIFETIME = 2 * 24 * 60 * 60     # 2 days
FOEVER_FILE_CACHE_LIFETIME = 0                   # forever

def cache_lifetime_for_class(arg, cls):
    """Return the default cache lifetime in seconds with a given object. A returned
    lifetime of zero means keep forever.

    Keyword arguments:
        arg -- an object
        cls -- the class calling the method
    """

    # Keep Viewmaster HTML for 12 hours
    if isinstance(arg, str):
        return DEFAULT_FILE_CACHE_LIFETIME

    # Keep RANKS, VOLS, etc. forever
    elif not isinstance(arg, cls):
        return FOEVER_FILE_CACHE_LIFETIME

    # Cache PdsFile bundlesets/bundles for a long time, but not necessarily forever
    elif not arg.interior:
        return LONG_FILE_CACHE_LIFETIME

    elif arg.isdir and arg.interior.lower().endswith('data'):
        return LONG_FILE_CACHE_LIFETIME     # .../bundlename/*data for a long time
    elif arg.isdir:
        return SHORT_FILE_CACHE_LIFETIME            # Other directories for two days
    else:
        return DEFAULT_FILE_CACHE_LIFETIME

# For tests under /tests
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
    results = target_pdsfile.opus_products()
    # Note that messages are more useful if extra values are identified before
    # missing values. That's because extra items are generally more diagnostic
    # of the issue at hand.
    for key in results:
        assert key in expected, f'Extra key: {key}'
    for key in expected:
        assert key in results, f'Missing key: {key}'
    for key in results:
        result_paths = []       # flattened list of logical paths
        for pdsfiles in results[key]:
            result_paths += cls.logicals_for_pdsfiles(pdsfiles)
        for path in result_paths:
            assert path in expected[key], f'Extra file under key {key}: {path}'
        for path in expected[key]:
            assert path in result_paths, f'Missing file under key {key}: {path}'

def versions_test_for_class(input_path, cls, holdings_dir, expected, is_abspath=True):
    target_pdsfile = instantiate_target_pdsfile_for_class(input_path, cls,
                                                          holdings_dir, is_abspath)
    res = target_pdsfile.all_versions()
    keys = list(res.keys())
    keys.sort(reverse=True)
    for key in keys:
        assert key in expected, f'"{key}" not expected'
        assert res[key].logical_path == expected[key], \
               f'value mismatch at "{key}": {expected[key]}'
    keys = list(expected.keys())
    keys.sort(reverse=True)
    for key in keys:
        assert key in res, f'"{key}" missing'

# For tests under rules
def translate_first_for_class(trans, path, cls):
    """Return the logical paths of "first" files found using given translator on path.

    Keyword arguments:
        trans -- a translator instance
        path  -- a file path
        cls   -- the class calling the method
    """

    patterns = trans.first(path)
    if not patterns:
        return []

    if isinstance(patterns, str):
        patterns = [patterns]

    patterns = [p for p in patterns if p]       # skip empty translations
    patterns = cls.abspaths_for_logicals(patterns)

    abspaths = []
    for pattern in patterns:
        abspaths += cls.glob_glob(pattern)

    return abspaths

def translate_all_for_class(trans, path, cls):
    """Return logical paths of all files found using given translator on path.

    Keyword arguments:
        trans -- a translator instance
        path  -- a file path
        cls   -- the class calling the method
    """

    patterns = trans.all(path)
    if not patterns:
        return []

    if isinstance(patterns, str):
        patterns = [patterns]

    patterns = [p for p in patterns if p]       # skip empty translations
    patterns = cls.abspaths_for_logicals(patterns)

    abspaths = []
    for pattern in patterns:
        abspaths += cls.glob_glob(pattern)

    return abspaths

def unmatched_patterns_for_class(trans, path, cls):
    """Return a list of all translated patterns that did not find a matching path in the
    file system.

    Keyword arguments:
        trans -- a translator instance
        path  -- a file path
        cls   -- the class calling the method
    """

    patterns = trans.all(path)
    patterns = [p for p in patterns if p]       # skip empty translations
    patterns = cls.abspaths_for_logicals(patterns)

    unmatched = []
    for pattern in patterns:
        abspaths = cls.glob_glob(pattern)
        if not abspaths:
            unmatched.append(pattern)

    return unmatched

def logical_path_from_abspath(abspath, cls):
    """Return the logical path derived from an absolute path.

    Keyword arguments:
        abspath -- the abosulte path of a file
        cls     -- the class calling the method
    """
    parts = abspath.partition('/'+cls.PDS_HOLDINGS+'/')
    print('########')
    print(cls.PDS_HOLDINGS)
    print(cls)
    if parts[1]:
        return parts[2]

    raise ValueError('Not compatible with a logical path: ', abspath)
