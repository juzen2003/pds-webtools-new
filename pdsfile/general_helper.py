##########################################################################################
# pdsfile/general_helper.py
# Helper functions being used in tests, the parent class & both pds3 & pds4 subclasses
##########################################################################################

import pdslogger
import pdsgroup

import fnmatch
import functools
import glob
import math
import os


##########################################################################################
# Configurations
##########################################################################################
_GLOB_CACHE_SIZE = 200
PATH_EXISTS_CACHE_SIZE = 200
FILE_BYTE_UNITS = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

try:
    PDS_HOLDINGS_DIR = os.environ['PDS_HOLDINGS_DIR']
except KeyError: # pragma: no cover
    PDS_HOLDINGS_DIR = os.path.realpath('/Library/WebServer/Documents/holdings')

try:
    PDS4_HOLDINGS_DIR = os.environ['PDS4_HOLDINGS_DIR']
except KeyError: # pragma: no cover
    # TODO: update this when we know the actual path of pds4 holdings on the webserver
    PDS4_HOLDINGS_DIR = os.path.realpath('/Library/WebServer/Documents/holdings')

PDS4_BUNDLES_DIR = f'{PDS4_HOLDINGS_DIR}/bundles'

##########################################################################################
# For tests under /tests
##########################################################################################
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

##########################################################################################
# For tests under rules
##########################################################################################
def translate_first_for_class(trans, path, cls):
    """Return the logical paths of "first" files found using given translator on path.

    Keyword arguments:
        trans -- a translator instance
        path  -- a file path
        cls   -- the class calling the other methods inside the function
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
        cls   -- the class calling the other methods inside the function
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

##########################################################################################
# Support functions for pdsfile/__init__.py
##########################################################################################
def unmatched_patterns_for_class(trans, path, cls):
    """Return a list of all translated patterns that did not find a matching path in the
    file system.

    Keyword arguments:
        trans -- a translator instance
        path  -- a file path
        cls   -- the class calling the other methods inside the function
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
        cls     -- the class calling the other methods inside the function
    """
    parts = abspath.partition('/'+cls.PDS_HOLDINGS+'/')
    if parts[1]:
        return parts[2]

    raise ValueError('Not compatible with a logical path: ', abspath)

def construct_category_list(voltypes):
    category_list = []
    for checksums in ('', 'checksums-'):
        for archives in ('', 'archives-'):
            for voltype in voltypes:
                category_list.append(checksums + archives + voltype)

    category_list.remove('checksums-documents')
    category_list.remove('archives-documents')
    category_list.remove('checksums-archives-documents')

    return category_list

def clean_join(a, b):
#     joined = os.path.join(a,b).replace('\\', '/')
    if a:
        return a + '/' + b
    else:
        return b

def clean_abspath(path):
    abspath = os.path.abspath(path)
    if os.sep == '\\':
        abspath = abspath.replace('\\', '/')
    return abspath

@functools.lru_cache(maxsize=_GLOB_CACHE_SIZE)
def clean_glob(cls, pattern, force_case_sensitive=False):
    results = glob.glob(pattern)
    if os.sep == '\\':
        results = [x.replace('\\', '/') for x in results]

    if force_case_sensitive and cls.FS_IS_CASE_INSENSITIVE:
        filtered_results = []
        for result in results:
            result = repair_case(result, cls)
            if fnmatch.fnmatchcase(result, pattern):
                filtered_results.append(result)

        return filtered_results

    else:
        return results

def needs_glob(pattern):
    """Return True if the given expression contains wildcards

    Keyword arguments:
        pattern -- expression pattern
    """
    return '*' in pattern or '?' in pattern or '[' in pattern

def repair_case(abspath, cls):
    """Return a file's absolute path with capitalization exactly as it appears
    in the file system. Raises IOError if the file is not found.

    Keyword arguments:
        abspath -- an absolute path of a file
        cls     -- the class calling the other methods inside the function
    """

    trailing_slash = abspath.endswith('/')  # must preserve a trailing slash!
    abspath = clean_abspath(abspath)

    # Fields are separated by slashes
    parts = abspath.split('/')
    if parts[-1] == '':
        parts = parts[:-1]      # Remove trailing slash

    # On Unix, parts[0] is always '' so no need to check case
    # On Windows, this skips over the name of the drive

    # For each subsequent field (between slashes)...
    for k in range(1, len(parts)):

        # Convert it to lower case for matching
        part_lower = parts[k].lower()

        # Construct the name of the parent directory and list its contents.
        # This will raise an IOError if the file does not exist or is not a
        # directory.
        if k == 1:
            basenames = os.listdir('/')
        else:
            basenames = cls.os_listdir('/'.join(parts[:k]))

        # Find the first name that matches when ignoring case
        found = False
        for name in basenames:
            if name.lower() == part_lower:

                # Replace the field with the properly capitalized name
                parts[k] = name
                found = True
                break

    # Reconstruct the full path
    if trailing_slash: parts.append('')
    abspath = '/'.join(parts)

    # Raise an IOError if last field was not found
    if not found:
        with open(abspath, 'rb') as f:
            pass

    return abspath

def formatted_file_size(size):
    order = int(math.log10(size) // 3) if size else 0
    return '{:.3g} {}'.format(size / 1000.**order, FILE_BYTE_UNITS[order])

def is_logical_path(path):
    """Return True if the given path appears to be a logical path; False
    otherwise.

    Keyword arguments:
        path -- the path of a file
    """

    return ('/holdings/' not in path)

def abspath_for_logical_path(path, cls):
    """Return the absolute path derived from the given logical path.

    The logical path starts at the category, below the holdings/ directory. To
    get the absolute path, we need to figure out where the holdings directory is
    located. Note that there can be multiple drives hosting multiple holdings
    directories.

    Keyword arguments:
        path -- the path of a file
        cls  -- the class calling the other methods inside the function
    """

    # Check for a valid logical path
    parts = path.split('/')
    if parts[0] not in cls.CATEGORIES:
        raise ValueError('Not a logical path: ' + path)

    # Use the list of preloaded holdings directories if it is not empty
    if cls.LOCAL_PRELOADED:
        holdings_list = cls.LOCAL_PRELOADED

    elif cls.LOCAL_HOLDINGS_DIRS:
        holdings_list = cls.LOCAL_HOLDINGS_DIRS

    elif 'PDS_HOLDINGS_DIR' in os.environ:
        holdings_list = [os.environ['PDS_HOLDINGS_DIR']]
        cls.LOCAL_HOLDINGS_DIRS = holdings_list

    # Without a preload or an environment variable, check the
    # /Library/WebSever/Documents directory for a symlink. This only works for
    # MacOS with the website installed, but that's OK.
    else:
        holdings_dirs = glob.glob('/Library/WebServer/Documents/holdings*')
        holdings_dirs.sort()
        holdings_list = [os.path.realpath(h) for h in holdings_dirs]
        cls.LOCAL_HOLDINGS_DIRS = holdings_list

    # With exactly one holdings/ directory, the answer is easy
    if len(holdings_list) == 1:
        return os.path.join(holdings_list[0], path)

    # Otherwise search among the available holdings directories in order
    for root in holdings_list:
        abspath = os.path.join(root, path)
        matches = cls.glob_glob(abspath)
        if matches: return matches[0]

    # File doesn't exist. Just pick one.
    if holdings_list:
        return os.path.join(holdings_list[0], path)

    raise ValueError('No holdings directory for logical path ' + path)

def selected_path_from_path(path, cls, abspaths=True):
    """Return the logical path or absolute path derived from a logical or
    an absolute path.

    Keyword arguments:
        path     -- the path of a file
        cls      -- the class calling the other methods inside the function
        abspaths -- the flag to determine if the return value is an absolute path (default
                    True)
    """

    if is_logical_path(path):
        if abspaths:
            return abspath_for_logical_path(path, cls)
        else:
            return path

    else:
        if abspaths:
            return path
        else:
            return logical_path_from_abspath(path, cls)

##########################################################################################
# PdsLogger support
##########################################################################################
def set_logger(cls, logger=None):
    """Set the PdsLogger.

    Keyword arguments:
        logger -- the pdslogger (default None)
        cls    -- the class with its attribute being updated
    """
    if not logger:
        logger = pdslogger.NullLogger()

    cls.LOGGER = logger

def set_easylogger(cls):
    """Log all messages directly to stdout.

    Keyword arguments:
        cls -- the class calling the other methods inside the function
    """
    set_logger(cls, pdslogger.EasyLogger())
