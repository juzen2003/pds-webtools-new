##########################################################################################
# pdsfile/preload_and_cache.py
# Store the code for preload management and cache
##########################################################################################

import os
from .general_helper import clean_join
# from . import PdsFile
# from .pds3file import Pds3File
# from .pds4file import Pds4File

##########################################################################################
# Filesystem vs. shelf files
##########################################################################################

# The above just a guess until preload. Certain unexpected behavior can arise
# when the file system is case-insensitive, such as glob.glob matching files
# that it really shouldn't. We only do the extra work to fix this if we know,
# or believe, that the file system is case-insensitive. Note also that when
# SHELVES_ONLY is True, the file system is effectively case-sensitive because
# we only use file names and paths found in the shelf files.

def use_shelves_only(cls, status=True):
    """Call before preload(). Status=True to identify files based on their
    presence in the infoshelf files first. Search the file system only if a
    shelf is missing."""

    cls.SHELVES_ONLY = status

##########################################################################################
# How to handle missing shelf files
##########################################################################################

def require_shelves(cls, status=True):
    """Call before preload(). Status=True to raise exceptions when shelf files
    are missing or incomplete. Otherwise, missing shelf info is only logged as a
    warning instead.
    """

    cls.SHELVES_REQUIRED = status

##########################################################################################
# Memcached and other cache support
##########################################################################################

# Cache of PdsFile objects:
#
# These entries in the cache are permanent:
#
# CACHE['$RANKS-<category>/']
#       This is a dictionary keyed by [bundleset] or [bundlename], which returns a
#       sorted list of ranks. Ranks are the PdsFile way of tracking versions of
#       objects. A higher rank (an integer) means a later version. All keys are
#       lower case. Replace "<category>" above by one of the names of the
#       holdings/ subdirectories.
#
# CACHE['$VOLS-<category>/']
#       This is a dictionary of dictionaries, keyed by [bundleset][rank] or
#       [bundlename][rank]. It returns the directory path of the bundleset or bundlename.
#       Keys are lower case.
#
# CACHE['$PRELOADED']
#       This is a list of holdings abspaths that have been preloaded.
#
# CACHE['$VOLINFO-<bundleset>']
# CACHE['$VOLINFO-<bundleset/bundlename>']
#       Returns (description, icon_type, version, publication date, list of
#                data set IDs)
#       for bundlenames and bundlesets. Keys are lower case.
#
# In addition...
#
# CACHE[<logical-path-in-lower-case>]
#       Returns the PdsFile object associated with the given path, if it has
#       been cached.

DEFAULT_FILE_CACHE_LIFETIME =  12 * 60 * 60      # 12 hours
LONG_FILE_CACHE_LIFETIME = 7 * 24 * 60 * 60      # 7 days
SHORT_FILE_CACHE_LIFETIME = 2 * 24 * 60 * 60     # 2 days
FOEVER_FILE_CACHE_LIFETIME = 0                   # forever
DICTIONARY_CACHE_LIMIT = 200000

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

def is_preloading(cls):
    return cls.CACHE.get_now('$PRELOADING')

def pause_caching(cls):
    cls.CACHE.pause()

def resume_caching(cls):
    cls.CACHE.resume()

def get_permanent_values(holdings_list, port, cls):
    """Load the most obvious set of permanent values from the cache to ensure
    we have current local copies."""

    try:
        pause_caching(cls)

        # For each category...
        for category in cls.CATEGORY_LIST:

            # Get the cached values
            _ = cls.CACHE['$RANKS-' + category + '/']
            _ = cls.CACHE['$VOLS-'  + category + '/']
            pdsf0 = cls.CACHE[category]

            # Also get the bundleset-level PdsFile inside each category
            for bundleset in pdsf0.childnames:
                if bundleset.endswith('.txt') or bundleset.endswith('.tar.gz'):
                    continue

                # Get the entry keyed by the logical path
                pdsf1 = cls.CACHE[category + '/' + bundleset.lower()]

                # Also get its bundle-level children
                for bundlename in pdsf1.childnames:
                    if bundlename.endswith('.txt') or bundlename.endswith('.tar.gz'):
                        continue

                    key = (pdsf1.logical_path + '/' + bundlename).lower()
                    pdsf2 = cls.CACHE[key]

    except KeyError as e:
        cls.LOGGER.warn('Permanent value %s missing from Memcache; '
                    'preloading again' % str(e))
        cls.preload(holdings_list, port, force_reload=True)

    else:
        cls.LOGGER.info('Permanent values retrieved from Memcache',
                    str(len(cls.CACHE.permanent_values)))

    finally:
        resume_caching()

def load_volume_info(holdings, cls):
    """Load bundle info associated with this holdings directory.

    Each record contains a sequence of values separated by "|":
        key: bundleset, bundleset/bundlename, category/bundleset, or category/bundleset/bundlename
        description
        icon_type or blank for default
        version ID or a string of dashes "-" if not applicable
        publication date or a string of dashes "-" if not applicable
        data set ID (if any) or MD5 checksum if this is in the documents/ tree
        additional data set IDs (if any)

    This creates and caches a dictionary based on the key identified above. Each
    entry is a tuple with five elements:
        description,
        icon_type or blank for default,
        version ID or None,
        publication date or None,
        list of data set IDs,
        MD5 checksum or ''

    A value only containing a string of dashes "-" is replaced by None.
    Blank records and those beginning with "#" are ignored.
    """

    volinfo_path = clean_join(holdings, '_volinfo')

    volinfo_dict = {}           # the master dictionary of high-level paths vs.
                                # (description, icon_type, version ID,
                                #  publication date, optional list of data set
                                #  IDs, optional checksum)

    keys_without_dsids = []     # internal list of entries without data set IDs
    dsids_vs_key = {}           # global dictionary of data set IDs for entries
                                # that have them

    # For each file in the volinfo subdirectory...
    children = os.listdir(volinfo_path)
    for child in children:

        # Ignore these
        if child.startswith('.'): continue
        if not child.endswith('.txt'):
            continue

        # Read the file
        table_path = clean_join(volinfo_path, child)
        with open(table_path, 'r', encoding='utf-8') as f:
            recs = f.readlines()

        # Interpret each record...
        for rec in recs:
            if rec[0] == '#':
                continue                        # ignore comments

            parts = rec.split('|')              # split by "|"
            parts = [p.strip() for p in parts]  # remove extraneous blanks
            if parts == ['']:
                continue                        # ignore blank lines

            # Identify missing info
            while len(parts) <= 5:
                parts.append('')

            if parts[2] == '' or set(parts[2]) == {'-'}:
                parts[2] = None
            if set(parts[3]) == {'-'}:
                parts[3] = None
            if set(parts[4]) == {'-'}:
                parts[4] = None

            if (parts[0].startswith('documents/') or
                parts[0].rpartition('/')[2] in cls.EXTRA_README_BASENAMES):
                    md5 = parts[5]
                    dsids = []
            else:
                    md5 = ''
                    dsids = list(parts[5:])

            # Update either keys_without_dsids or dsids_vs_key. This is used
            # to fill in data set IDs for voltypes other than "volumes/".
            if dsids == ['']:
                dsids = []

            if dsids:
                dsids_vs_key[parts[0]] = dsids
            else:
                keys_without_dsids.append(parts[0])

            # Fill in the master dictionary
            volinfo = (parts[1], parts[2], parts[3], parts[4], dsids, md5)
            volinfo_dict[parts[0]] = volinfo

    # Update the list of data set IDs wherever it's missing
    for key in keys_without_dsids:
        (category, _, remainder) = key.partition('/')
        if category in cls.VOLTYPES:
            (volset_with_suffix, _, remainder) = remainder.partition('/')
            bundleset = '_'.join(volset_with_suffix.split('_')[:2])
            alt_keys = (bundleset + '/' + remainder,
                        'volumes/' + bundleset + '/' + remainder)
            for alt_key in alt_keys:
                if alt_key in dsids_vs_key:
                    volinfo_dict[key] = (volinfo_dict[key][:4] +
                                         (dsids_vs_key[alt_key],
                                          volinfo_dict[key][5]))
                    break

    # Save the master dictionary in the cache now
    for key,volinfo in volinfo_dict.items():
        cls.CACHE.set('$VOLINFO-' + key.lower(), volinfo, lifetime=0)

    cls.LOGGER.info('Volume info loaded', volinfo_path)

def cache_categoriey_merged_dirs(cls):
    for category in cls.CATEGORY_LIST:
        if category not in cls.CACHE:
            cls.CACHE.set(category, cls.new_merged_dir(category), lifetime=0)

# def init_cache(cls):
#     return pdscache.DictionaryCache(lifetime=cls.cache_lifetime,
#                                     limit=cls.DICTIONARY_CACHE_LIMIT,
#                                     logger=cls.LOGGER)

# def cache_lifetime_for_pdsfile(arg):
#     return cache_lifetime_for_class(arg, PdsFile)
# def cache_lifetime_for_pds3file(arg):
#     return cache_lifetime_for_class(arg, Pds3File)
# def cache_lifetime_for_pds4file(arg):
#     return cache_lifetime_for_class(arg, Pds4File)
