################################################################################
# rules/pytest_support.py
################################################################################

import pdsfile
import translator
import re
import os

try:        # PDS_DATA_DIR overrides the default holdings directory location
    holdings_dir = os.environ['PDS_DATA_DIR']
    pdsfile.set_local_holdings_dirs([holdings_dir])
except KeyError:
    pass

def translate_first(trans, path):
    """Logical paths of "first" files found using given translator on path."""

    patterns = trans.first(path)
    if not patterns:
        return []

    if isinstance(patterns, str):
        patterns = [patterns]

    patterns = [p for p in patterns if p]       # skip empty translations
    patterns = pdsfile.PdsFile.abspaths_for_logicals(patterns)

    abspaths = []
    for pattern in patterns:
        abspaths += pdsfile.PdsFile.glob_glob(pattern)

    return abspaths

def translate_all(trans, path):
    """Logical paths of all files found using given translator on path."""

    patterns = trans.all(path)
    if not patterns:
        return []

    if isinstance(patterns, str):
        patterns = [patterns]

    patterns = [p for p in patterns if p]       # skip empty translations
    patterns = pdsfile.PdsFile.abspaths_for_logicals(patterns)

    abspaths = []
    for pattern in patterns:
        abspaths += pdsfile.PdsFile.glob_glob(pattern)

    return abspaths

def unmatched_patterns(trans, path):
    """List all translated patterns that did not find a matching path in the
    file system."""

    patterns = trans.all(path)
    patterns = [p for p in patterns if p]       # skip empty translations
    patterns = pdsfile.PdsFile.abspaths_for_logicals(patterns)

    unmatched = []
    for pattern in patterns:
        abspaths = pdsfile.PdsFile.glob_glob(pattern)
        if not abspaths:
            unmatched.append(pattern)

    return unmatched

################################################################################
# Dave's test suite helpers
################################################################################

def instantiate_target_pdsfile(path, is_abspath=True):
    if is_abspath:
        TESTFILE_PATH = pdsfile.abspath_for_logical_path(path)
        target_pdsfile = pdsfile.PdsFile.from_abspath(TESTFILE_PATH)
    else:
        TESTFILE_PATH = path
        target_pdsfile = pdsfile.PdsFile.from_logical_path(TESTFILE_PATH)
    return target_pdsfile

def get_pdsfiles(paths, is_abspath=True):
    pdsfiles_arr = []
    if is_abspath:
        for path in paths:
            TESTFILE_PATH = pdsfile.abspath_for_logical_path(path)
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
            result_paths += pdsfile.PdsFile.logicals_for_pdsfiles(pdsfiles)
        for path in result_paths:
            assert path in expected[key], f'Extra file under key {key}: {path}'
        for path in expected[key]:
            assert path in result_paths, f'Missing file under key {key}: {path}'
