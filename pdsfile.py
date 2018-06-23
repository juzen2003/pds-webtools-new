import datetime
import glob
import math
import os
import pickle
import random
import re
import shelve
import sys
import time

try:
    import pylibmc
    HAS_PYLIBMC = True
except ImportError:
    HAS_PYLIBMC = False

import pdsfile_rules        # Default rules
import rules                # Rules unique to each volume set
import pdscache
import pdsviewable
import translator
import pdstable

################################################################################
# Configuration
################################################################################

VOLTYPES = ['volumes', 'calibrated', 'diagrams', 'metadata', 'previews']
VIEWABLE_VOLTYPES = ['previews', 'diagrams']

VIEWABLE_EXTS = set(['jpg', 'png', 'gif', 'tif', 'tiff', 'jpeg', 'jpeg_small'])
DATAFILE_EXTS = set(['dat', 'img', 'cub', 'qub', 'fit', 'fits'])

VOLSET_REGEX        = re.compile(r'^([A-Z][A-Z0-9x]{1,5}_[0-9x]{3}x)$')
VOLSET_REGEX_I      = re.compile(VOLSET_REGEX.pattern, re.I)
VOLSET_PLUS_REGEX   = re.compile(VOLSET_REGEX.pattern[:-1] +
                        r'(|_\w+?|_v[0-9.]+)' +
                        r'((?:|_calibrated|_diagrams|_metadata|_previews)' +
                        r'(?:|_md5.txt|.tar.gz))$')
VOLSET_PLUS_REGEX_I = re.compile(VOLSET_PLUS_REGEX.pattern, re.I)

CATEGORY_REGEX      = re.compile(r'^(|checksums\-)(|archives\-)(\w+)$')
CATEGORY_REGEX_I    = re.compile(CATEGORY_REGEX.pattern, re.I)

VOLNAME_REGEX       = re.compile(r'^([A-Z][A-Z0-9]{1,5}_(?:[0-9]{4}|UNKS))$')
VOLNAME_REGEX_I     = re.compile(VOLNAME_REGEX.pattern, re.I)
VOLNAME_PLUS_REGEX  = re.compile(VOLNAME_REGEX.pattern[:-1] +
                                  r'(|_\w+)(|_md5.txt|.tar.gz)$')
VOLNAME_PLUS_REGEX_I = re.compile(VOLNAME_PLUS_REGEX.pattern, re.I)

LOGFILE_TIME_FMT = '%Y-%m-%dT%H-%M-%S'

PLAIN_TEXT_EXTS = set(['lbl', 'txt', 'asc', 'tab', 'cat', 'fmt', 'f', 'c',
                       'cpp', 'pro', 'for', 'f77', 'py', 'inc', 'h', 'sh',
                       'idl', 'csh', 'tf', 'ti', 'tls', 'lsk', 'tsc'])

MIME_TYPES_VS_EXT = {
    'fit'       : 'image/fits',
    'fits'      : 'image/fits',
    'jpg'       : 'image/jpg',
    'jpeg'      : 'image/jpg',
    'jpeg_small': 'image/jpg',
    'tif'       : 'image/tiff',
    'tiff'      : 'image/tiff',
    'png'       : 'image/png',
    'bmp'       : 'image/bmp',
    'gif'       : 'image/*',
    'csv'       : 'text/csv',
    'pdf'       : 'application/pdf',
    'xml'       : 'text/xml',
    'rtf'       : 'text/rtf',
    'htm'       : 'text/html',
    'html'      : 'text/html',
}

# DESC_AND_ICON_FIXES updates descriptions and icons for virtual directories
# Value returned is [suffix, new_icon_type]
DESC_AND_ICON_FIXES = {
  ('calibrated/', 'VOLUME'): (' (<b>calibrated</b>)', 'VOLUME'  ),
  ('calibrated/', 'VOLDIR'): (' (<b>calibrated</b>)', 'VOLDIR'  ),
  ('metadata/',   'VOLUME'): (' (<b>metadata</b>)',   'INDEXDIR'),
  ('metadata/',   'VOLDIR'): (' (<b>metadata</b>)',   'INDEXDIR'),
  ('previews/',   'VOLUME'): (' (<b>previews</b>)',   'IMAGEDIR'),
  ('previews/',   'VOLDIR'): (' (<b>previews</b>)',   'IMAGEDIR'),
  ('diagrams/',   'VOLUME'): (' (<b>diagrams</b>)',   'DIAGDIR' ),
  ('diagrams/',   'VOLDIR'): (' (<b>diagrams</b>)',   'DIAGDIR' ),

  ('archives-volumes/',    'VOLUME'): (' (<b>tar.gz</b>)',           'TARBALL'),
  ('archives-volumes/',    'VOLDIR'): (' (<b>tar.gz</b>)',           'TARDIR' ),
  ('archives-calibrated/', 'VOLUME'): (' (<b>calibrated tar.gz</b>)','TARBALL'),
  ('archives-calibrated/', 'VOLDIR'): (' (<b>calibrated tar.gz</b>)','TARDIR' ),
  ('archives-metadata/',   'VOLUME'): (' (<b>metadata tar.gz</b>)',  'TARBALL'),
  ('archives-metadata/',   'VOLDIR'): (' (<b>metadata tar.gz</b>)',  'TARDIR' ),
  ('archives-previews/',   'VOLUME'): (' (<b>previews tar.gz</b>)',  'TARBALL'),
  ('archives-previews/',   'VOLDIR'): (' (<b>previews tar.gz</b>)',  'TARDIR' ),
  ('archives-diagrams/',   'VOLUME'): (' (<b>diagrams tar.gz</b>)',  'TARBALL'),
  ('archives-diagrams/',   'VOLDIR'): (' (<b>diagrams tar.gz</b>)',  'TARDIR' ),
}

CATEGORIES = set()
for checksums in ('', 'checksums-'):
    for archives in ('', 'archives-'):
        for voltype in VOLTYPES:
            CATEGORIES.add(checksums + archives + voltype)

################################################################################
# PdsLogger support
################################################################################

LOGGER = None       # Optional logger
DEBUGGING = False   # True for extra-detailed debugging logs

def set_logger(logger, debugging=False):

    global LOGGER, DEBUGGING

    LOGGER = logger
    DEBUGGING = debugging

################################################################################
# Pickle files vs. shelf files
################################################################################

USE_PICKLES = False

def use_pickles(status=True):
    """Call before preload(). Status=True to read ancillary information from
    pickle files; False to read from shelf files instead. Shelf files are a bit
    faster but do not work across platforms."""

    global USE_PICKLES

    USE_PICKLES = status

################################################################################
# Memcached support
################################################################################

# Cache of PdsFile objects:
#
# CACHE['$RANKS-category/']
#       Dictionary keyed by [volset or volname] returns a sorted list of ranks.
#       Keys are lower case.
#
# CACHE['$VOLS-category/']
#       Dictionary keyed by [volset or volname][rank] returns the CACHE key
#       of the volset or name. Keys are lower case.
#
# CACHE['$PRELOADED']
#       List of preloaded holdings abspaths
#
# CACHE['$VOLINFO-<volset or volset/volname>']
#       Returns (description, icon_type, version, publication date, list of
#                data set IDs)
#       for volnames and volsets. Keys are lower case.

def cache_lifetime(arg):
    """Used by caches. Returns the default lifetime based on what is being
    cached."""

    if type(arg) == str:                    # Keep HTML for 12 hours
        return 12 * 60 * 60
    elif not isinstance(arg, PdsFile):      # RANKS, VOLS, etc. forever
        return 0
    elif not arg.interior:                  # Tree down to volname level forever
        return 0
    elif arg.interior.lower() == 'data':    # .../volname/data forever
        return 0
    elif arg.isdir:
        return 3 * 24 * 60 * 60             # Other directories for three days
    else:
        return 12 * 60 * 60                 # Files for 12 hours

# Initialize the cache
LOCAL_PRELOADED = []        # local copy of CACHE['$PRELOADED']
MEMCACHE_PORT = 0           # default is to use a DictionaryCache instead
DICTIONARY_CACHE_LIMIT = 200000

# This cache is used if preload() is never called. No filesystem is required.
CACHE = pdscache.DictionaryCache(lifetime=cache_lifetime,
                                 limit=DICTIONARY_CACHE_LIMIT,
                                 logger=LOGGER)

FILESYSTEM = False
DEFAULT_CACHING = 'all'     # 'dir', 'all' or 'none';
                            # use 'dir' for Viewmaster without MemCache;
                            # use 'all' for Viewmaster with MemCache;
                            # use 'all' in the absence of a filesystem.

def preload_required(holdings_list, port=0, clear=False):
    """Returns True if a preload is required; False if the needed information is
    already cached and available.
    """

    global LOCAL_PRELOADED

    if clear: return True
    if port != MEMCACHE_PORT: return True

    try:
        if CACHE.get_now('$PRELOADING'): return True
    except KeyError:
        pass

    # Convert holdings to a list of strings
    if type(holdings_list) == str:
        holdings_list = [holdings_list]

    if set(holdings_list) != set(LOCAL_PRELOADED):
        try:
            preloaded = CACHE['$PRELOADED']
        except KeyError:
            return True

    LOCAL_PRELOADED = preloaded
    return set(holdings_list) != set(LOCAL_PRELOADED)

def preload(holdings_list, port=0, clear=False):
    """Cache the top-level directories, starting from the given holdings
    directories.

    Input:
        holdings_list       a single abslute path to a holdings directory, or
                            else a list of absolute paths.
        port                port to use for memcached; zero to prevent use of
                            memcached.
        clear               True to clear the cache before preloading.
    """

    global CACHE, MEMCACHE_PORT, DEFAULT_CACHING, LOCAL_PRELOADED, FILESYSTEM
    FILESYSTEM = True

    # Convert holdings to a list of strings
    if type(holdings_list) == str:
        holdings_list = [holdings_list]

    cleared_already = False

    # Use cache as requested
    if (port == 0 and MEMCACHE_PORT == 0) or not HAS_PYLIBMC:
        default_paths = CACHE
        CACHE = pdscache.DictionaryCache(lifetime=cache_lifetime,
                                         limit=DICTIONARY_CACHE_LIMIT,
                                         logger=LOGGER)

        if LOGGER:
            LOGGER.info('Caching PdsFile objects in local dictionary')

    else:
        MEMCACHE_PORT = MEMCACHE_PORT or port
        try:
            CACHE = pdscache.MemcachedCache(MEMCACHE_PORT,
                                            lifetime=cache_lifetime,
                                            logger=LOGGER)
            if LOGGER:
                LOGGER.info('Connecting to PdsFile Memcache [%s]' %
                            MEMCACHE_PORT)

            # Clear if necessary
            if clear and not CACHE.is_blocked():
                CACHE.clear(block=True)
                cleared_already = True

        except pylibmc.Error:
            if LOGGER:
                LOGGER.error(('Failed to connect PdsFile Memcache [%s]; '+
                               'using dictionary instead') %
                              MEMCACHE_PORT)

            MEMCACHE_PORT = 0
            CACHE = pdscache.DictionaryCache(lifetime=cache_lifetime,
                                             limit=DICTIONARY_CACHE_LIMIT,
                                             logger=LOGGER)

    # Define default caching based on whether MemCache is active
    if MEMCACHE_PORT == 0:
        DEFAULT_CACHING = 'dir'
    else:
        DEFAULT_CACHING = 'all'

    ############################################################################
    # Recursive interior function
    ############################################################################

    def _preload_dir(pdsdir):
        if not pdsdir.isdir: return
        if LOGGER: LOGGER.debug('Pre-loading', pdsdir.abspath)

        if LOGGER and not pdsdir.volset:
            LOGGER.info('Caching', pdsdir.logical_path)

        pdsdir.permanent = True
        if pdsdir.logical_path.startswith('volumes/'):
            key = pdsdir.logical_path[8:]   # Skip over 'volumes/'
            try:
                (description, icon_type, version, pubdate,
                              dsids) = CACHE['$VOLINFO-' + key.lower()]
            except KeyError:
                if LOGGER:
                    LOGGER.warn('Volume info not found', pdsdir.logical_path)

            else:
                pdsdir._description_and_icon_filled = (description, icon_type)
                pdsdir._volume_version_id_filled = version
                pdsdir._volume_publication_date_filled = pubdate
                pdsdir._volume_data_set_ids_filled = dsids

        if pdsdir.volname: return           # don't go deeper than volume name

        for basename in pdsdir.childnames:
            try:
                child = pdsdir.child(basename, fix_case=False,
                                               caching='all', lifetime=0)
                _preload_dir(child)

            except ValueError:              # Skip out-of-place files
                pdsdir._childnames_filled.remove(basename)

    ############################################################################
    # Begin active code
    ############################################################################

    if LOGGER:
        LOGGER.add_root(holdings_list)

    # Initialize the list of preloaded holdings directories
    try:
        preloaded = CACHE['$PRELOADED']
    except KeyError:
        preloaded = []

    already_loaded = True
    for holdings in holdings_list:
        if holdings in preloaded:
            if LOGGER:
                LOGGER.info('Holdings are already cached', str(holdings))
        else:
            already_loaded = False

    if already_loaded:
        LOCAL_PRELOADED = preloaded
        if MEMCACHE_PORT: get_permanent_values()
        return

    # Clear and block the cache before proceeding
    if not cleared_already:
        CACHE.clear(block=True) # Blocked means every other thread is waiting

    # Indicate that the cache is preloading
    CACHE.set('$PRELOADING', True)
    CACHE.flush()

    # Pause the cache before proceeding--saves I/O
    CACHE.pause()       # Paused means no local changes will be flushed to the
                        # external cache until resume() is called.

    ############################################################################
    # Always create and cache permanent, category-level virtual directories.
    # These are roots of the cache tree and they are also virtual directories,
    # meaning that their childen can be assembled from multiple physical
    # directories.
    ############################################################################

    for category in CATEGORIES:
        CACHE.set(category, PdsFile.new_virtual(category), lifetime=0)

    try:    # undo the pause and block in the finally clause below

        # Initialize RANKS, VOLS and category list
        categories = []     # order counts below!
        for checksums_ in ('', 'checksums-'):
          for archives_ in ('', 'archives-'):
            for voltype in VOLTYPES:
                category = checksums_ + archives_ + voltype
                categories.append(category)

                category_ = category + '/'
                key = '$RANKS-' + category_
                try:
                    _ = CACHE[key]
                except KeyError:
                    CACHE.set(key, {}, lifetime=0)

                key = '$VOLS-'  + category_
                try:
                    _ = CACHE[key]
                except KeyError:
                    CACHE.set(key, {}, lifetime=0)

        # Prepare dictionary of top-level PdsFiles
        for holdings in holdings_list:

            holdings = os.path.abspath(holdings)
            if os.sep == '\\':
                holdings = holdings.replace('\\', '/')

            if holdings in preloaded:
                continue

            if LOGGER: LOGGER.info('Pre-loading ' + holdings)

            # Load volume info
            load_volume_info(holdings)

            # Load directories starting from here
            holdings_ = holdings.rstrip('/') + '/'

            for c in categories:
                category_abspath = holdings_ + c
                if not os.path.exists(category_abspath): continue
                if not os.path.isdir(category_abspath):
                  if LOGGER:
                    LOGGER.warn('Not a directory, ignored', category_abspath)

                # This is the physical PdsFile, but from_abspath also adds this
                # object to the list of childnames of the virtual directory.
                pdsdir = PdsFile.from_abspath(category_abspath, fix_case=False,
                                              caching='all', lifetime=0)
                _preload_dir(pdsdir)

            preloaded.append(holdings)

    finally:
        CACHE.set('$PRELOADED', preloaded, lifetime=0)
        CACHE.set('$PRELOADING', False)
        CACHE.resume()
        CACHE.unblock(flush=True)
        LOCAL_PRELOADED = preloaded

    if LOGGER:
        LOGGER.info('PdsFile preloading completed')

def is_preloading():
    return CACHE.get_now('$PRELOADING')

def pause_caching():
    CACHE.pause()

def resume_caching():
    CACHE.resume()

def clear_cache(block=True):
    CACHE.clear(block)

def block_cache():
    CACHE.block()

def unblock_cache():
    CACHE.unblock()

def load_volume_info(holdings):
    """Load volume info associated with this holdings directory.

    Each record contains a sequence of values separated by "|":
        key: volset, volset/volname, category/volset, or category/volset/volname
        description
        icon_type or blank for default
        version ID
        publication date
        data set ID (if any)
        additional data set IDs (if any)

    Blank records and those beginning with "#" are ignored.
    """

    volinfo_path = _clean_join(os.path.split(holdings)[0], 'volinfo')

    children = os.listdir(volinfo_path)
    for child in children:
        if not child.endswith('.tab'): continue

        table_path = _clean_join(volinfo_path, child)
        with open(table_path) as f:
            recs = f.readlines()

        for rec in recs:
            if rec[0] == '#': continue

            parts = rec.split('|')
            parts = [p.strip() for p in parts]
            if parts == ['']: continue  # ignore blank lines

            # Fill in icon type if missing
            if parts[2] == '':
                parts[2] = 'VOLUME' if '/' in parts[0] else 'VOLDIR'

            volinfo = (parts[1], parts[2], parts[3], parts[4], list(parts[5:]))
            CACHE.set('$VOLINFO-' + parts[0].lower(), volinfo, lifetime=0)

    if LOGGER:
        LOGGER.info('Volume info loaded', volinfo_path)

def get_permanent_values():
    """Load the most obvious set of permanent values from the cache to ensure
    we have local copies."""

    for category in CATEGORIES:
        _ = CACHE.get('$RANKS-' + category + '/')
        _ = CACHE.get('$VOLS-'  + category + '/')
        pdsf0 = CACHE.get(category)

        for volset in pdsf0.childnames:
            pdsf1 = CACHE.get(category + '/' + volset)
            pdsf1a = CACHE.get(pdsf1.abspath)

            for volname in pdsf1.childnames:
                pdsf2 = CACHE.get(pdsf1.logical_path + '/' + volname)
                pdsf2a = CACHE.get(pdsf2.abspath)

################################################################################
# PdsFile class
################################################################################

class PdsFile(object):

    # Global registry of subclasses
    SUBCLASSES = {}

    # Translator from volume set ID to key in global registry
    VOLSET_TRANSLATOR = translator.TranslatorByRegex([('.*', 0, 'default')])

    # Default translators, can be overridden by volset-specific subclasses
    DESCRIPTION_AND_ICON = pdsfile_rules.DESCRIPTION_AND_ICON
    VOLUMES_TO_ASSOCIATIONS = pdsfile_rules.VOLUMES_TO_ASSOCIATIONS
    ASSOCIATIONS_TO_VOLUMES = pdsfile_rules.ASSOCIATIONS_TO_VOLUMES
    INFO_FILE_BASENAMES = pdsfile_rules.INFO_FILE_BASENAMES
    NEIGHBORS = pdsfile_rules.NEIGHBORS
    SORT_KEY = pdsfile_rules.SORT_KEY
    SPLIT_RULES = pdsfile_rules.SPLIT_RULES
    VIEW_OPTIONS = pdsfile_rules.VIEW_OPTIONS
    VIEWABLES = pdsfile_rules.VIEWABLES

    OPUS_TYPE = pdsfile_rules.OPUS_TYPE
    OPUS_FORMAT = pdsfile_rules.OPUS_FORMAT
    OPUS_PRODUCTS = pdsfile_rules.OPUS_PRODUCTS
    OPUS_ID_TO_FILESPEC = pdsfile_rules.OPUS_ID_TO_FILESPEC
    FILESPEC_TO_OPUS_ID = pdsfile_rules.FILESPEC_TO_OPUS_ID
    FILESPEC_TO_LOGICAL_PATH = pdsfile_rules.FILESPEC_TO_LOGICAL_PATH

    FILENAME_KEYLEN = 0

    # Used to help with debugging
    LAST_EXC_INFO = (None, None, None)

    ############################################################################
    # Constructor
    ############################################################################

    def __init__(self):
        """Constructor returns a blank PdsFile object. Not for external use."""

        self.basename     = ''
        self.abspath      = ''
        self.logical_path = ''      # Logical path starting after 'holdings/'

        self.disk_        = ''      # Disk name alone
        self.root_        = ''      # Disk path + '/holdings/'
        self.html_root_   = ''      # 'holdings/', 'holdings2/', etc.

        self.category_    = ''      # Always checksums_ + archives_ + voltype_
        self.checksums_   = ''
        self.archives_    = ''
        self.voltype_     = ''

        self.volset_      = ''
        self.volset       = ''
        self.suffix       = ''
        self.version_message = ''
        self.version_rank = 0
        self.version_id   = ''

        self.volname_     = ''
        self.volname      = ''

        self.interior     = ''
        self.row_dicts    = []
        self.column_names = []

        self.permanent    = False
        self.is_virtual   = False

        self._exists_filled         = None
        self._islabel_filled        = None
        self._isdir_filled          = None
        self._split_filled          = None
        self._global_anchor_filled  = None
        self._childnames_filled     = None
        self._info_filled           = None  # bytes, child_count, modtime,
                                            # checksum, size)
        self._date_filled           = None
        self._formatted_size_filled = None
        self._is_viewable_filled    = None
        self._info_basename_filled  = None
        self._label_basename_filled = None
        self._viewset_filled        = None
        self._local_viewset_filled  = None
        self._iconset_filled        = None
        self._internal_links_filled = None
        self._mime_type_filled      = None
        self._opus_id_filled        = None
        self._opus_type_filled      = None
        self._opus_format_filled    = None
        self._view_options_filled   = None  # (grid, multipage, continuous)
        self._volume_info_filled    = None  # (desc, icon type, version ID,
                                            #  pub date, list of dataset IDs)
        self._description_and_icon_filled    = None
        self._volume_publication_date_filled = None
        self._volume_version_id_filled       = None
        self._volume_data_set_ids_filled     = None
        self._version_ranks_filled           = None
        self._exact_archive_url_filled       = None
        self._exact_checksum_url_filled      = None
        self._associated_parallels_filled    = None

    @staticmethod
    def new_virtual(basename):
        """A virtual directory with the given basename. Virtual directories
        contain children from multiple physical directories. Examples are
        volumes/, archives-volumes/, etc."""

        if basename not in CATEGORIES:
            raise ValueError('Invalid category: ' + basename)

        this = PdsFile()

        this.basename     = basename
        this.abspath      = None
        this.logical_path = basename

        this.disk_        = None
        this.root_        = None
        this.html_root_   = None

        this.category_    = basename.rstrip('/') + '/'
        this.checksums_   = 'checksums-' if 'checksums-' in basename else ''
        this.archives_    = 'archives-'  if 'archives-'  in basename else ''
        this.voltype_     = basename.split('-')[-1].rstrip('/') + '/'

        this.volset_      = ''
        this.volset       = ''
        this.suffix       = ''
        this.version_message = ''
        this.version_rank = 0
        this.version_id   = ''

        this.volname_     = ''
        this.volname      = ''

        this.interior     = ''
        this.row_dicts    = []
        this.column_names = []

        this.permanent    = True
        this.is_virtual   = True

        this._exists_filled         = True
        this._islabel_filled        = False
        this._isdir_filled          = True
        this._split_filled          = (basename, '', '')
        this._global_anchor_filled  = basename
        this._childnames_filled     = []
        this._info_filled           = [None, None, None, '', (0,0)]
        this._date_filled           = ''
        this._formatted_size_filled = ''
        this._is_viewable_filled    = False
        this._info_basename_filled  = ''
        this._label_basename_filled = ''
        this._viewset_filled        = False
        this._local_viewset_filled  = False
        this._iconset_filled        = None
        this._internal_links_filled = []
        this._mime_type_filled      = ''
        this._opus_id_filled        = ''
        this._opus_type_filled      = ''
        this._opus_format_filled    = ''
        this._view_options_filled   = (False, False, False)
        this._volume_info_filled    = None
        this._description_and_icon_filled    = None
        this._volume_publication_date_filled = ''
        this._volume_version_id_filled       = ''
        this._volume_data_set_ids_filled     = ''
        this._version_ranks_filled           = []
        this._exact_archive_url_filled       = ''
        this._exact_checksum_url_filled      = ''
        this._associated_parallels_filled    = None

        return this

    def new_index_row_pdsfile(self, filename_key):
        """A PdsFile representing the content of one row of an index file. Used
        to enable views of individual rows of large index files."""

        this = self.copy()

        this.basename     = filename_key

        _filename_key = '/' + filename_key
        this.abspath      += _filename_key
        this.logical_path += _filename_key
        this.interior     += _filename_key

        this._exists_filled         = True
        this._islabel_filled        = False
        this._isdir_filled          = False
        this._split_filled          = (this.basename, '', '')
        this._global_anchor_filled  = None
        this._childnames_filled     = []
        this._info_filled           = [0, 0, 0, '', (0,0)]
        this._date_filled           = self.date
        this._formatted_size_filled = ''
        this._is_viewable_filled    = False
        this._info_basename_filled  = ''
        this._label_basename_filled = ''
        this._viewset_filled        = False
        this._local_viewset_filled  = False
        this._iconset_filled        = None
        this._internal_links_filled = []
        this._mime_type_filled      = 'text/plain'
        this._opus_id_filled        = ''
        this._opus_type_filled      = ''
        this._opus_format_filled    = ''
        this._view_options_filled   = (False, False, False)
        this._volume_info_filled    = self._volume_info
        this._description_and_icon_filled    = None
        this._volume_publication_date_filled = self.volume_publication_date
        this._volume_version_id_filled       = self.volume_version_id
        this._volume_data_set_ids_filled     = self.volume_data_set_ids
        this._version_ranks_filled           = self.version_ranks
        this._exact_archive_url_filled       = ''
        this._exact_checksum_url_filled      = ''
        this._associated_parallels_filled    = {}

        return this

    def new_pdsfile(self, key=None, copypath=False):
        """Empty PdsFile of the same subclass or a specified subclass."""

        if key is None:
            cls = type(self)
        elif key in PdsFile.SUBCLASSES:
            cls = PdsFile.SUBCLASSES[key]
        else:
            key2 = PdsFile.VOLSET_TRANSLATOR.first(key)
            cls = PdsFile.SUBCLASSES[key2]

        this = cls.__new__(cls)

        source = PdsFile()
        for (key, value) in source.__dict__.items():
            this.__dict__[key] = value

        if copypath:
            this.basename        = self.basename
            this.abspath         = self.abspath
            this.logical_path    = self.logical_path
            this.disk_           = self.disk_
            this.root_           = self.root_
            this.html_root_      = self.html_root_
            this.category_       = self.category_
            this.checksums_      = self.checksums_
            this.archives_       = self.archives_
            this.voltype_        = self.voltype_
            this.volset_         = self.volset_
            this.volset          = self.volset
            this.suffix          = self.suffix
            this.version_message = self.version_message
            this.version_rank    = self.version_rank
            this.version_id      = self.version_id
            this.volname_        = self.volname_
            this.volname         = self.volname
            this.interior        = self.interior

        return this

    def copy(self):
        cls = type(self)
        this = cls.__new__(cls)

        for (key, value) in self.__dict__.items():
            this.__dict__[key] = value

        return this

    ############################################################################
    # Properties
    ############################################################################

    @property
    def exists(self):
        """True if the file exists."""

        if self._exists_filled is not None:
            return self._exists_filled

        if self.is_virtual:
            self._exists_filled = True
        elif self.abspath is None:
            self._exists_filled = False
        else:
            self._exists_filled = os.path.exists(self.abspath)

        self._recache()
        return self._exists_filled

    @property
    def isdir(self):
        """True if the file is a directory."""

        if self._isdir_filled is not None:
            return self._isdir_filled

        if self.is_virtual:
            self._isdir_filled = True
        elif self.abspath is None:
            self._isdir_filled = False
        else:
            self._isdir_filled = os.path.isdir(self.abspath)

        self._recache()
        return self._isdir_filled

    @property
    def filespec(self):
        """volname or volname/interior."""

        if self.interior:
            return self.volname_ + self.interior
        else:
            return self.volname

    @property
    def absolute_or_logical_path(self):
        """The absolute path if this has one; otherwise the logical path."""

        if self.abspath:
            return self.abspath
        else:
            return self.logical_path

    @property
    def islabel(self):
        """True if the file is a PDS3 label."""

        if self._islabel_filled is not None:
            return self._islabel_filled

        self._islabel_filled = self.basename_is_label(self.basename)

        self._recache()
        return self._islabel_filled

    @property
    def is_viewable(self):
        """True if the file is viewable. Examples of viewable files are JPEGs,
        TIFFs, PNGs, etc."""

        if self._is_viewable_filled is not None:
            return self._is_viewable_filled

        self._is_viewable_filled = self.basename_is_viewable(self.basename)

        self._recache()
        return self._is_viewable_filled

    @property
    def html_path(self):
        """URL to this file after the domain name and slash, starting with
        "holdings"; alias for property "url".
        """

        # For a virtual path, return _something_, i.e., the first physical path
        if self.abspath is None:
            child_html_path = self.child(self.childnames[0]).html_path
            return child_html_path.rpartition('/')[0]

        return self.html_root_ + self.logical_path

    @property
    def url(self):
        """URL to this file after the domain name and slash, starting with
        "holdings"; alias for property "url".
        """

        return self.html_path

    @property
    def split(self):
        """Returns (anchor, suffix, extension)"""

        if self._split_filled is not None:
            return self._split_filled

        self._split_filled = self.split_basename()

        self._recache()
        return self._split_filled

    @property
    def anchor(self):
        """The anchor for this object. Objects with the same anchor are grouped
        together in the same row of a Viewmaster table."""

        return self.split[0]

    @property
    def global_anchor(self):
        """The global anchor is a unique string across all data products and
        is suitable for use in HTML pages."""

        if self._global_anchor_filled is not None:
            return self._global_anchor_filled

        path = self.parent_logical_path + '/' + self.anchor
        self._global_anchor_filled = path.replace('/', '-')

        self._recache()
        return self._global_anchor_filled

    @property
    def extension(self):
        """The extension of this file, after the first dot."""

        return self.split[2]

    @property
    def is_index(self):
        """True if this is _probably_ an index file but not cumulative."""

        logical_path_lc = self.logical_path.lower()
        if (logical_path_lc.endswith('.tab') and
            logical_path_lc.startswith('metadata/')):

            if '999' in self.volname: return False
            return True

        return False

    @property
    def childnames(self):
        """A list of all the child names if this is a directory."""

        if self._childnames_filled is not None:
            return self._childnames_filled

        self._childnames_filled = []
        logical_path_lc = self.logical_path.lower()

        if self.isdir and self.abspath:
            self._childnames_filled = get_childnames(self.abspath)

        # Support for table row views as "children" of index tables
        # For the sake of efficiency, we generate all the child objects at once
        # and allow them to be cached for a long time.
        if self.is_index:
            CACHE.pause()       # wait till all the changes are ready
            try:
                table = pdstable.PdsTable(self.label_abspath,
                                          filename_keylen=self.FILENAME_KEYLEN)

            # Not a valid index table; that means it has no children
            except (IOError, KeyError):
                PdsFile.LAST_EXC_INFO = sys.exc_info()
                self._childnames_filled = []

            # Otherwise generate all child objects and make them permanent
            else:
                table.index_rows_by_filename_key()
                self._childnames_filled = table.filename_keys

                column_names = table.get_keys()
                for childname in self._childnames_filled:
                    child = self.new_index_row_pdsfile(childname)
                    child.row_dicts = table.rows_by_filename_key(childname)
                    child.column_names = column_names
                    child._complete(must_exist=True, caching='all',
                                    lifetime=3*86400)   # cache for 3 days

                # Cache the table too because it contains all the childnames
                self._complete(caching='all')
                self._recache()
                return self._childnames_filled

            finally:
                CACHE.resume()

        self._recache()
        return self._childnames_filled

    @property
    def parent_logical_path(self):
        """A safe way to get the logical_path of the parent; works for virtual
        directories when parent is None:"""

        parent = self.parent()

        if self.parent() is None:
            return ''
        else:
            return parent.logical_path

    @property
    def _info(self):
        """Internal method to retrieve info from the info shelf file."""

        if self._info_filled is not None:
            return self._info_filled

        # Missing files and checksum files get no _info
        if not self.exists or self.checksums_:
            self._info_filled = (0, 0, None, '', (0,0))

        # For volsets that are not archives, fill in the needed info directly
        # from the filesystem
        elif not self.archives_ and self.volset and not self.volname:
            child_count = len(self.childnames)

            latest_modtime = datetime.datetime.min
            total_bytes = 0
            for volname in self.childnames:

                (bytes, _, timestring, _, _) = self.shelf_lookup('info',
                                                                 volname)

                if timestring == '' or bytes == 0: continue
                    # Some preview dirs are empty. Without this check, we get
                    # an error.

                # Convert formatted time to datetime
                yr = int(timestring[ 0:4])
                mo = int(timestring[ 5:7])
                da = int(timestring[ 8:10])
                hr = int(timestring[11:13])
                mi = int(timestring[14:16])
                sc = int(timestring[17:19])
                ms = int(timestring[20:])
                modtime = datetime.datetime(yr, mo, da, hr, mi, sc, ms)
                latest_modtime = max(modtime, latest_modtime)

                total_bytes += bytes

            # If no modtimes were found. Shouldn't happen but worth checking.
            if latest_modtime == datetime.datetime.min:
                latest_modtime = None

            self._info_filled = (total_bytes, child_count,
                                latest_modtime, '', (0,0))

        # Otherwise, get the info from a shelf file
        else:
            try:
                (bytes, child_count,
                 timestring, checksum, size) = self.shelf_lookup('info')

            # Shelf file failure
            except (IOError, KeyError, ValueError) as e:
                PdsFile.LAST_EXC_INFO = sys.exc_info()
                self._info_filled = (0, 0, None, '', (0,0))

            else:
                if timestring:
                    # Interpret the modtime
                    yr = int(timestring[ 0:4])
                    mo = int(timestring[ 5:7])
                    da = int(timestring[ 8:10])
                    hr = int(timestring[11:13])
                    mi = int(timestring[14:16])
                    sc = int(timestring[17:19])
                    ms = int(timestring[20:])
                    modtime = datetime.datetime(yr, mo, da, hr, mi, sc, ms)

                    self._info_filled = (bytes, child_count, modtime, checksum,
                                         size)

                # This can happen for empty directories
                else:
                    self._info_filled = (0, 0, None, '', (0,0))

        # Now format the date
        if self.modtime:
            self._date_filled = self.modtime.strftime('%Y-%m-%d %H:%M:%S')
        else:
            self._date_filled = ''

        # Format the byte count
        if self.size_bytes:
            self._formatted_size_filled = formatted_file_size(self.size_bytes)
        else:
            self._formatted_size_filled = ''

        self._recache()
        return self._info_filled

    @property
    def size_bytes(self):
        """Size in bytes represented as an int."""

        return self._info[0]

    @property
    def modtime(self):
        """Datetime object representing this file's modification date."""

        return self._info[2]

    @property
    def checksum(self):
        """MD5 checksum of this file."""

        return self._info[3]

    @property
    def width(self):
        """Width of this image in pixels if it is viewable."""

        return self._info[4][0]

    @property
    def height(self):
        """Height of this image in pixels if it is viewable."""

        return self._info[4][1]

    @property
    def alt(self):
        """Alt tag to use if this is a viewable object."""

        return self.basename

    @property
    def date(self):
        """Modification date/time of this file as a well-formatted string;
        otherwise blank."""

        if self._date_filled is not None:
            return self._date_filled

        _ = self._info

        self._recache()
        return self._date_filled

    @property
    def formatted_size(self):
        """Size of this file as a formatted string, e.g., "2.16 MB"."""

        if self._info is not None:
            return self._formatted_size_filled

        _ = self._info

        self._recache()
        return self._formatted_size_filled

    @property
    def _volume_info(self):
        """Internal method to retrieve information about this volume."""

        if self._volume_info_filled is None:

            base_key = self.volset + self.suffix
            if self.volname:
                base_key += '/' + self.volname

            # Try lookup using two different keys: with and without category.
            # Most of the time, _volume_info is independent of the category.
            # However, there are a few exceptions. This allows the _volume_info
            # for a particular category to differ from the default.
            keys = (self.category_ + base_key, base_key)
            for key in keys:
                try:
                    self._volume_info_filled = CACHE['$VOLINFO-' + key.lower()]
                except (KeyError, TypeError):
                    pass

            if self._volume_info_filled is None:
                self._volume_info_filled = ('', 'UNKNOWN', '', '', [])

        self._recache()
        return self._volume_info_filled

    @property
    def description(self):
        """Description text about this file as it appears in Viewmaster."""

        if self._description_and_icon_filled is not None:
            return self._description_and_icon_filled[0]

        if self.is_volume() or self.is_volset():
            pair = self._volume_info[:2]

            # Add annotation based on volume type
            if self.category_ == 'calibrated/':
                pair = ('Calibrated ' + pair[0], pair[1])
            elif self.category_ == 'diagrams/':
                pair = ('Diagrams for ' + pair[0], 'GEOMDIR')
            elif self.category_ == 'previews/':
                pair = ('Previews of ' + pair[0], 'BROWDIR')
            elif self.category_ == 'metadata/' and 'metadata' not in pair[0]:
                pair = ('Metadata for ' + pair[0], 'INDEXDIR')

        elif self.row_dicts:
            table_name = self.parent().basename
            if len(self.row_dicts) == 1:
                pair = ('Selected row of ' + table_name, 'INFO')
            else:
                pair = ('Selected rows of ' + table_name, 'INFO')

        else:
            pair = self.DESCRIPTION_AND_ICON.first(self.logical_path)

            if pair is None:
                pair = ['Unavailable', 'UNKNOWN']

        # Highlight top-level directories
        key = (self.category_, pair[1])
        if key in DESC_AND_ICON_FIXES:
            (suffix, new_icon_type) = DESC_AND_ICON_FIXES[key]
            new_desc = pair[0] # + suffix
            pair = [new_desc, new_icon_type]

        self._description_and_icon_filled = pair

        self._recache()
        return self._description_and_icon_filled[0]

    @property
    def icon_type(self):
        """Icon type for this file."""

        _ = self.description
        return self._description_and_icon_filled[1]

    @property
    def mime_type(self):
        """A best guess at the MIME type for this file. Blank for not
        displayable in a browser."""

        if self._mime_type_filled is not None:
            return self._mime_type_filled

        ext = self.extension[1:].lower()

        if self.isdir:
            self._mime_type_filled = ''
        elif ext in PLAIN_TEXT_EXTS:
            self._mime_type_filled = 'text/plain'
        elif ext in MIME_TYPES_VS_EXT:
            self._mime_type_filled = MIME_TYPES_VS_EXT[ext]
        else:
            self._mime_type_filled = ''

        self._recache()
        return self._mime_type_filled

    @property
    def opus_id(self):
        """The OPUS ID of this product if it has one; otherwise an empty string.
        """

        if self._opus_id_filled is None:
            with_slashes = self.FILESPEC_TO_OPUS_ID.first(self.filespec)
            if with_slashes is None:
                return None
            self._opus_id_filled = with_slashes.replace('-', '--').replace('/',
                                                                           '-')
            self._recache()

        return self._opus_id_filled

    @property
    def opus_format(self):
        """The OPUS format of this product, e.g., ('ASCII', 'Table') or
        ('Binary', 'FITS')."""

        if self._opus_format_filled is None:
            self._opus_format_filled = self.OPUS_FORMAT.first(self.logical_path)
            self._recache()

        return self._opus_format_filled

    @property
    def opus_type(self):
        """The OPUS type of this product, e.g., "Raw Data", "Calibrated Data",
        or "Preview Image (full-size)"."""

        if self._opus_type_filled is None:
            self._opus_type_filled = self.OPUS_TYPE.first(self.logical_path)
            self._recache()

        return self._opus_type_filled

    @property
    def info_basename(self):
        """Returns the basename of an informational file associated with this
        PdsFile object. This could be a file like "VOLDESC.CAT", "CATINFO.TXT",
        or the label file associated with a data product."""

        if self._info_basename_filled is not None:
            return self._info_basename_filled

        # Search based on rules
        self._info_basename_filled = \
            self.INFO_FILE_BASENAMES.first(self.childnames)

        # On failure, try the local label
        if not self._info_basename_filled:

            if self.islabel:
                self._info_basename_filled = self.basename

            elif self.label_basename:
                self._info_basename_filled = self.label_basename

            # Otherwise, there is no info file so change None to ''
            else:
                self._info_basename_filled = ''

        self._recache()
        return self._info_basename_filled

    @property
    def internal_link_info(self):
        """Returns a list of tuples [(recno, basename, abspath), ...], or else
        the abspath of the label for this file."""

        if self._internal_links_filled is not None:
            return self._internal_links_filled

        # Some file types never have links
        if self.isdir or self.checksums_ or self.archives_:
            self._internal_links_filled = []

        elif self.voltype_ not in ('volumes/', 'calibrated/', 'metadata/'):
            self._internal_links_filled = []

        # Otherwise, lookup the info in the shelf file
        else:
            try:
                values = self.shelf_lookup('links')

            # Shelf file failure
            except (IOError, KeyError, ValueError) as e:
                PdsFile.LAST_EXC_INFO = sys.exc_info()
                self._internal_links_filled = ()
                    # An empty _tuple_ indicates that link info is missing
                    # because of a shelf file failure; an empty _list_ object
                    # means that the file simply contains no links.
                    # This distinction is there if we ever care.

            else:
                volume_path_ = self.volume_abspath() + '/'

                # A string value means that this is actually the path from this
                # file to its external PDS label
                if type(values) == str:
                    if values:
                        self._internal_links_filled = volume_path_ + values
                    else:
                        self._internal_links_filled = []

                # A list value indicates that each value is a tuple:
                #   (recno, basename, internal_path)
                # The tuple indicates that this label file contains an external
                # link in line <recno>. The occurrence of string <basename> is
                # actually a link to a file with the path <internal_path>.
                # There is one tuple for each internal link in the label file.
                else:
                    new_list = []
                    for (recno, basename, internal_path) in values:
                        abspath = volume_path_ + internal_path
                        new_list.append((recno, basename, abspath))
                    self._internal_links_filled = new_list

        self._recache()
        return self._internal_links_filled

    @property
    def linked_abspaths(self):
        """Returns a list of absolute paths linked this PdsFile."""

        abspaths = [self.abspath]
        for (_, _, abspath) in self.internal_link_info:
            if abspath not in abspaths:
                abspaths.append(abspath)

        parent = self.parent()
        if self.label_basename and parent:
            label = parent.child(self.label_basename)
            for (_, _, abspath) in label.internal_link_info:
                if abspath not in abspaths:
                    abspaths.append(abspath)

        return abspaths

    @property
    def label_basename(self):
        """Basename of the label file associated with this data file."""

        if self._label_basename_filled is not None:
            return self._label_basename_filled

        _ = self.internal_link_info

        if type(self._internal_links_filled) == str:
            label_path = self._internal_links_filled
            if label_path:
                self._label_basename_filled = os.path.basename(label_path)

        elif type(self._internal_links_filled) == list:
            self._label_basename_filled = ''

        # otherwise, tuple means not found
        elif self.islabel:
            self._label_basename_filled = ''

        else:
            ext = self.extension.lower()
            if ext in ('.lbl', '.txt', '.cat', 'tar.gz'):
                self._label_basename_filled = ''
            elif self.extension.islower():
                self._label_basename_filled = self.basename[:-len(ext)] + '.lbl'
            else:
                self._label_basename_filled = self.basename[:-len(ext)] + '.LBL'

        self._recache()
        return self._label_basename_filled

    @property
    def label_abspath(self):
        """Absolute path to the label if it exists; blank otherwise."""

        if self.label_basename:
            parent_path = os.path.split(self.abspath)[0]
            return parent_path + '/' + self.label_basename
        else:
            return ''

    @property
    def viewset(self):
        """PdsViewSet to use for this object."""

        if self._viewset_filled is not None:
            return self._viewset_filled

        # Don't look for PdsViewSets at volume root; saves time
        if (self.exists and self.volname_ and
            not self.archives_ and not self.checksums_ and
            self.interior and ('/' in self.interior)):
                self._viewset_filled = self.viewset_lookup('default')

        if self._viewset_filled is None:
            self._viewset_filled = False

        self._recache()
        return self._viewset_filled

    @property
    def local_viewset(self):
        """PdsViewSet for this object if it is itself viewable; otherwise False.
        """

        if self._local_viewset_filled is not None:
            return self._local_viewset_filled

        if self.exists and self.basename_is_viewable():
            self._local_viewset_filled = \
                            pdsviewable.PdsViewSet.from_pdsfiles(self)
        else:
            self._local_viewset_filled = False

        self._recache()
        return self._local_viewset_filled

    @property
    def _iconset(self):
        """Internal method to return the PdsViewSet for this object's icon
        whether it is to be displayed in a closed or open state."""

        if self._iconset_filled is not None:
            return self._iconset_filled[0]

        self._iconset_filled = [pdsviewable.ICON_SET_BY_TYPE[self.icon_type,
                                                             False],
                                pdsviewable.ICON_SET_BY_TYPE[self.icon_type,
                                                             True]]

        self._recache()
        return self._iconset_filled[0]

    @property
    def iconset_open(self):
        """PdsViewSet for this object's icon if displayed in an open state."""

        _ = self._iconset
        return self._iconset_filled[1]

    @property
    def iconset_closed(self):
        """PdsViewSet for this object's icon if displayed in a closed state."""

        _ = self._iconset
        return self._iconset_filled[0]

    @property
    def volume_publication_date(self):
        """Publication date for this volume as a formatted string."""

        if self._volume_publication_date_filled is not None:
            return self._volume_publication_date_filled

        date = self._volume_info[3]
        if date == '':
            try:
                date = self.volume_pdsfile().date[:10]
            except ValueError:
                pass

        if date == '':
            try:
                date = self.volset_pdsfile().date[:10]
            except ValueError:
                pass

        if date == '':
            try:
                date = self.date[:10]
            except ValueError:
                pass

        self._volume_publication_date_filled = date

        self._recache()
        return self._volume_publication_date_filled

    @property
    def volume_version_id(self):
        """Version ID of this volume."""

        if self._volume_version_id_filled is None:
            self._volume_version_id_filled = self._volume_info[2]
            self._recache()

        return self._volume_version_id_filled

    @property
    def volume_data_set_ids(self):
        """A list of the dataset IDs found in this volume."""

        if self._volume_data_set_ids_filled is None:
            self._volume_data_set_ids_filled = self._volume_info[4]
            self._recache()

        return self._volume_data_set_ids_filled

    @property
    def version_ranks(self):
        """A list of the numeric version ranks associated with this file.

        This is an integer that always sorts versions from oldest to newest."""

        if self._version_ranks_filled is not None:
            return self._version_ranks_filled

        if not self.exists:
            version_ranks_filled = []
        else:
            try:
                ranks = CACHE['$RANKS-' + self.category_]

            except KeyError:
                if LOGGER:
                    LOGGER.warn('Missing rank info', self.logical_path)
                self._version_ranks_filled = []

            else:
                if self.volname:
                    key = self.volname.lower()
                    self._version_ranks_filled = ranks[key]

                elif self.volset:
                    key = self.volset.lower()
                    self._version_ranks_filled = ranks[key]

                else:
                    self._version_ranks_filled = []

        self._recache()
        return self._version_ranks_filled

    @property
    def exact_archive_url(self):
        """If an archive file contains the exact contents of this directory
        tree, return the URL of that archive. Otherwise return blank."""

        if self._exact_archive_url_filled is not None:
            return self._exact_archive_url_filled

        if not self.exists:
            self._exact_archive_url_filled = ''

        else:
            abspath = self.archive_path_if_exact()
            if abspath:
                pdsf = PdsFile.from_abspath(abspath)
                self._exact_archive_url_filled = pdsf.url
            else:
                self._exact_archive_url_filled = ''

        self._recache()
        return self._exact_archive_url_filled

    @property
    def exact_checksum_url(self):
        """If a checksum file contains the exact contents of this directory
        tree, return the URL of that file. Otherwise return blank."""

        if self._exact_checksum_url_filled is not None:
            return self._exact_checksum_url_filled

        if not self.exists:
            self._exact_checksum_url_filled = ''

        else:
            abspath = self.checksum_path_if_exact()
            if abspath:
                pdsf = PdsFile.from_abspath(abspath)
                self._exact_checksum_url_filled = pdsf.url
            else:
                self._exact_checksum_url_filled = ''

        self._recache()
        return self._exact_checksum_url_filled

    @property
    def grid_view_allowed(self):
        """True if this directory can be viewed as a grid inside Viewmaster."""

        if self._view_options_filled is not None:
            return self._view_options_filled[0]

        if not self.exists:
            self._view_options_filled = (False, False, False)

        elif self.isdir:
            self._view_options_filled = \
                                self.VIEW_OPTIONS.first(self.logical_path)
        else:
            self._view_options_filled = (False, False, False)

        self._recache()
        return self._view_options_filled[0]

    @property
    def multipage_view_allowed(self):
        """True if a multipage view starting from this directory is allowed
        inside Viewmaster."""

        _ = self.grid_view_allowed

        return self._view_options_filled[1]

    @property
    def continuous_view_allowed(self):
        """True if a continuous view of multiple directories starting from this
        one is allowed inside Viewmaster."""

        _ = self.grid_view_allowed

        return self._view_options_filled[2]

    @property
    def has_neighbor_rule(self):
        """True if a neighbor rule is available to go to the object just before
        or just after this one."""

        if self.NEIGHBORS.first(self.parent().logical_path):
            return True
        else:
            return False

    LATEST_VERSION_RANKS = [990100, 990200, 990300, 990400, 999999]

    @staticmethod
    def version_info(suffix):
        """Procedure to associate a volset suffix with a version rank value."""

        version_id = ''
        if suffix == '':
            version_message = 'Current version'
            version_rank = 999999
        elif suffix == '_in_prep':
            version_message = 'In preparation'
            version_rank = 990100
        elif suffix == '_prelim':
            version_message = 'Preliminary release'
            version_rank = 990200
        elif suffix == '_peer_review':
            version_message = 'In peer review'
            version_rank = 990300
        elif suffix == '_lien_resolution':
            version_message = 'In lien resolution'
            version_rank = 990400

        elif suffix.startswith('_v'):
            version_message = 'Version ' + suffix[2:] + ' (superseded)'

            # Version ranks:
            #   _v2 -> 20000
            #   _v2.1 -> 201000
            #   _v2.1.3 -> 201030
            subparts = suffix[2:].split('.')
            version_rank = int(subparts[0]) * 10000
            version_id = str(subparts[0])

            if len(subparts) > 1:
                version_rank += int(subparts[1]) * 100
                version_id += '.' + str(subparts[1])

            if len(subparts) > 2:
                version_rank += int(subparts[2])
                version_id += '.' + str(subparts[2])

        else:
            raise ValueError('Unrecognized volume set suffix "%s"' % suffix)

        return (version_rank, version_message, version_id)

    def viewset_lookup(self, name='default'):
        """Return the PdsViewSet associated with this file. If multiple
        PdsViewSets are available, they can be selected by name; "default" is
        assumed."""

        if not self.exists: return None

        # If this is a directory, return the PdsViewSet of the first child
        if self.isdir:
            basenames = self.sort_childnames()
            basenames = [b for b in basenames
                         if os.path.splitext(b)[1][1:].lower() in
                            (VIEWABLE_EXTS | DATAFILE_EXTS)]
            if len(basenames) > 20:     # Stop after 20 files max
                basenames = basenames[:20]

            for basename in basenames:
                pdsf = self.child(basename)
                if pdsf.isdir: continue

                viewset = pdsf.viewset_lookup(name)
                if viewset:
                    return viewset

            return None

        # If this is viewable, return the PdsViewSet of its viewable siblings
        # with the same anchor
        if self.is_viewable:
            parent = self.parent()
            if parent:
                sibnames = parent.viewable_childnames_by_anchor(self.anchor)
                siblings = parent.pdsfiles_for_basenames(sibnames)
            else:
                siblings = [self]

            return pdsviewable.PdsViewSet.from_pdsfiles(siblings)

        # Otherwise, check for associated viewables
        patterns = self.VIEWABLES[name].first(self.logical_path)
        if type(patterns) == str:
            patterns = [patterns]

        if patterns:
            abspaths = []
            for pattern in patterns:
                if '*' in pattern or '?' in pattern or '[' in pattern:
                    matches = glob.glob(self.root_ + pattern)
                    if not matches and LOGGER:
                        LOGGER.warn('No matching files', pattern)
                    abspaths += matches
                else:
                    abspaths += [self.root_ + pattern]

            viewables = PdsFile.pdsfiles_for_abspaths(abspaths, must_exist=True)
            return pdsviewable.PdsViewSet.from_pdsfiles(viewables)

        # We are out of options
        return pdsviewable.PdsViewSet([])

    def opus_products(self):
        """For this primary data product or label, return a dictionary keyed
        by the OPUS product type ("Raw Data", "Calibrated Data", etc.). For any
        key, this dictionary returns a list of sublists. Each sublist has the
        form:
            [PdsFile for a data product,
             PdsFile for its label (if any),
             PdsFile for the first embedded .FMT file (if any),
             PdsFile for the second embedded .FMT file (if any), etc.]
        This sublist contains every file that should be added to the OPUS
        results if that data product is requested.

        The dictionary actually returns a list of these subblists, because it is
        possible for multiple data products to have the same OPUS product type.
        However, most of the time, the list contains only one sublist.
        """

        opus_pdsfiles = {}

        # Get the associated absolute paths
        patterns = self.OPUS_PRODUCTS.all(self.logical_path)
        patterns = [self.root_ + p for p in patterns]

        abspaths = []
        for pattern in patterns:
            if '*' in pattern or '?' in pattern or '[' in pattern:
                abspaths += glob.glob(pattern)
            else:
                if os.path.exists(pattern):
                    abspaths.append(pattern)

        # Sort into disjoint sets of labels and data files
        abspaths = set(abspaths)
        label_pdsfiles = set()
        data_abspaths  = set()
        for abspath in abspaths:
            pdsf = PdsFile.from_abspath(abspath)
            if pdsf.islabel:
                label_pdsfiles.add(pdsf)
            else:
                data_abspaths.add(abspath)

        data_abspaths_handled = set()

        # Get the info about each labeled product
        for label_pdsfile in label_pdsfiles:
            linked_abspaths = set(label_pdsfile.linked_abspaths)
            fmts = [f for f in linked_abspaths if f[-4:] in ('.fmt', '.FMT')]
            fmts.sort()
            fmt_pdsfiles = PdsFile.pdsfiles_for_abspaths(fmts, must_exist=True)
            datapaths = linked_abspaths - set(fmts)

            label_prefix = os.path.splitext(label_pdsfile.abspath)[0]
            for datapath in datapaths:
                data_pdsfile = PdsFile.from_abspath(datapath)

                # Ignore links to this or other label files
                if data_pdsfile.islabel:
                    data_abspaths_handled.add(datapath)
                    continue

                # Be skeptical if datafile and label prefixes don't match
                # because it could be a random cross-reference in the label
                data_prefix = os.path.splitext(datapath)[0]
                if data_prefix != label_prefix:

                    # Check for a better label filename
                    if (data_prefix + '.lbl') in abspaths or \
                       (data_prefix + '.LBL') in abspaths:
                            data_abspaths_handled.add(datapath)
                            continue

                # Update the dictionary with the datafile, label, and FMT files
                opus_type = data_pdsfile.opus_type
                sublist = [data_pdsfile, label_pdsfile] + fmt_pdsfiles

                if opus_type not in opus_pdsfiles:
                    opus_pdsfiles[opus_type] = [sublist]
                else:
                    opus_pdsfiles[opus_type].append(sublist)

                data_abspaths_handled.add(datapath)

        # Any remaining files are unlabeled
        data_abspaths_remaining = data_abspaths - data_abspaths_handled
        for datapath in data_abspaths_remaining:
            data_pdsfile = PdsFile.from_abspath(datapath)
            opus_type = data_pdsfile.opus_type
            sublist = [data_pdsfile]

            if opus_type not in opus_pdsfiles:
                opus_pdsfiles[opus_type] = [sublist]
            else:
                opus_pdsfiles[opus_type].append(sublist)

        return opus_pdsfiles

    ############################################################################
    # Support for alternative constructors
    ############################################################################

    def _complete(self, must_exist=False, caching='default', lifetime=None):
        """General procedure to maintain the CACHE cache. It returns PdsFiles or
        subclasses from the cache if available; otherwise it caches PdsFiles if
        appropriate.

        If the file exists, then the capitalization must be correct!
        """

        # Confirm existence
        if must_exist and not self.exists and FILESYSTEM:
            raise IOError('File not found', self.abspath)

        if self.basename.strip() == '':     # Shouldn't happen, but just in case
            return self.parent()

        if LOGGER and DEBUGGING:
            LOGGER.debug('Completing', self.logical_path)

        # If we already have a PdsFile keyed by this absolute path, return it
        if self.abspath:
            try:
                return CACHE[self.abspath]
            except KeyError:
                pass

        # If there is no absolute path, return the PdsFile keyed by the logical
        # path
        else:
            try:
                return CACHE[self.logical_path]
            except KeyError:
                pass

        # Do not cache above the category level
        if not self.category_: return self

        # Do not cache nonexistent objects
        if FILESYSTEM and not self.exists: return self

        # Otherwise, cache if necessary
        if caching == 'default':
            caching = DEFAULT_CACHING

        if caching == 'all' or (caching == 'dir' and self.isdir):

            # Don't overwrite a virtual directory
            if self.logical_path not in CATEGORIES:
                CACHE.set(self.logical_path, self, lifetime=lifetime)

            if self.abspath:
                CACHE.set(self.abspath, self, lifetime=lifetime)

            if FILESYSTEM:
                self._update_ranks_and_vols()

        return self

    def _update_ranks_and_vols(self):
        """Maintains the RANKS and VOLS dictionaries. Must be called for all
        PdsFile objects down to the volume name level."""

        # CACHE['$RANKS-category_'] is keyed by [volume set or name] and returns
        # a sorted list of ranks.

        # CACHE['$VOLS-category_'] is keyed by [volume set or name][rank] and
        # returns a volset or volname PdsFile.

        if self.volset and not self.volname:
            key = self.volset
        elif self.volname and not self.volname_:
            key = self.volname
        elif self.volname_ and not self.interior:
            key = self.volname
        else:
            return

        key = key.lower()
        self.permanent = True       # VOLS entries are permanent!

        rank_dict = CACHE['$RANKS-' + self.category_]
        vols_dict = CACHE['$VOLS-'  + self.category_]

        changed = False
        if key not in rank_dict:
            rank_dict[key] = []
            vols_dict[key] = {}
            changed = True

        ranks = rank_dict[key]
        if self.version_rank not in ranks:
            rank_dict[key].append(self.version_rank)
            rank_dict[key].sort()
            changed = True

        if changed:
            vols_dict[key][self.version_rank] = self.abspath
            CACHE.set('$RANKS-' + self.category_, rank_dict, lifetime=0)
            CACHE.set('$VOLS-'  + self.category_, vols_dict, lifetime=0)

    def _recache(self):
        """Update the cache after this object has been modified, e.g., by having
        a previously empty field filled in."""

        if self.abspath and (self.abspath in CACHE):
            CACHE.set(self.abspath, self)

        if self.logical_path in CACHE and (self.is_virtual ==
                                           CACHE[self.logical_path].is_virtual):
            CACHE.set(self.logical_path, self)

    ############################################################################
    # Alternative constructors
    ############################################################################

    def child(self, basename, fix_case=True, must_exist=False,
                    caching='default', lifetime=None):
        """Constructor for a PdsFile of the proper subclass in this directory.

        Inputs:
            basename    name of the child.
            fix_case    True to fix the case of the child.
            must_exist  True to raise an exception if the parent or child does
                        not exist.
            caching     Type of caching to use.
            lifetime    Lifetime parameter for cache.
        """

        if must_exist and not self.exists:
            raise IOError('File not found: ' + self.logical_path)

        basename_lc = basename.lower()

        # Handle the special case of index rows
        if self.is_index:
            childnames = self.childnames
                # With this call, every child is permanently cached

            childnames_lc = [c.lower() for c in childnames]
            test_childname_lc = os.path.basename(basename.lower())
            test_childname_lc = os.path.splitext(test_childname_lc)[0]
            try:
                k = childnames_lc.index(test_childname_lc)

            except ValueError:  # If the test childname is not in the list
                pass

            else:
                logical_path = self.logical_path + '/' + childnames[k]
                return CACHE[logical_path]

            # Maybe the key is shorter than the filename
            for k in range(len(childnames_lc)):
                if test_childname_lc.startswith(childnames_lc[k]):
                    logical_path = self.logical_path + '/' + childnames[k]
                    return CACHE[logical_path]

            raise IOError('Index row does not exist: ' +
                          self.logical_path + '/' + basename)

        # Fix the case if possible
        if fix_case:
            for name in self.childnames:
                if basename_lc == name.lower():
                    return self.child(name, fix_case=False,
                                            must_exist=must_exist,
                                            caching=caching, lifetime=lifetime)

        if must_exist and basename not in self.childnames:
            raise IOError('File not found: ' +
                          self.logical_path + '/' + basename)

        # Look up by abspath or by logical path depending on parent
        child_logical_path = _clean_join(self.logical_path, basename)
        child_logical_path.rstrip('/')      # could happen at root level

        if self.abspath:
            child_abspath = _clean_join(self.abspath, basename)
            try:
                return CACHE[child_abspath]
            except KeyError:
                pass
        else:
            child_abspath = None

        # If the parent has no absolute path, neither can the child
        if not child_abspath:
            try:
                pdsf = CACHE[child_logical_path]
                if not pdsf.abspath: return pdsf    # child with no abspath
            except KeyError:
                pass

        # Select the correct subclass for the child...
        if self.volset:
            class_key = self.volset
        elif self.category_:
            matchobj = VOLSET_PLUS_REGEX_I.match(basename)  # used again
            if matchobj is None:
                raise ValueError('Illegal volume set directory "%s": %s' %
                                 (basename, self.logical_path))
            class_key = matchobj.group(1)
        else:
            class_key = 'default'

        # "this" is a copy of the parent object with internally cached values
        # removed but with path information duplicated.
        this = self.new_pdsfile(key=class_key, copypath=True)

        # Update the path for the child
        this.logical_path = child_logical_path
        this.abspath = child_abspath    # might be None
        this.basename = basename

        if self.interior:
            this.interior = _clean_join(self.interior, basename)
            return this._complete(must_exist, caching, lifetime)

        if self.volname_:
            this.interior = basename
            return this._complete(must_exist, caching, lifetime)

        if self.volset_:

            # Handle volume name
            matchobj = VOLNAME_PLUS_REGEX_I.match(basename)
            if matchobj is None:
                raise ValueError('Illegal volume name "%s": %s' %
                                 (basename, this.logical_path))

            this.volname_ = basename + '/'
            this.volname  = matchobj.group(1)

            if self.checksums_ or self.archives_:
                this.volname_ = ''
                this.interior = basename

            return this._complete(must_exist, caching, lifetime)

        if self.category_:

            # Handle volume set and suffix
            matchobj = VOLSET_PLUS_REGEX_I.match(basename)
            if matchobj is None:
                raise ValueError('Illegal volume set directory "%s": %s' %
                                 (basename, this.logical_path))

            this.volset_ = basename + '/'
            this.volset  = matchobj.group(1)
            this.suffix  = matchobj.group(2)

            if matchobj.group(3):
                this.volset_ = ''
                this.interior = basename
                parts = this.suffix.split('_')
                if parts[-1] == this.voltype_[:-1]:
                    this.suffix = '_'.join(parts[:-1])

            (this.version_rank,
             this.version_message,
             this.version_id) = self.version_info(this.suffix)

            # If this is the child of a category, then we must ensure that it is
            # added to the child list of the virtual parent.

            if self.abspath:
                virtual_parent = CACHE[self.logical_path]
                childnames = virtual_parent._childnames_filled
                if basename not in childnames:
                    virtual_parent._childnames_filled.append(basename)
                    virtual_parent._childnames_filled.sort()
                    CACHE.set(self.logical_path, virtual_parent, lifetime=0)

            return this._complete(must_exist, caching, lifetime)

        if not self.category_:

            # Handle voltype and category
            this.category_ = basename + '/'
            matchobj = CATEGORY_REGEX_I.match(basename)
            if matchobj is None:
                raise ValueError('Invalid category "%s": %s' %
                                 (basename, this.logical_path))

            if fix_case:
                this.checksums_ = matchobj.group(1).lower()
                this.archives_  = matchobj.group(2).lower()
                this.voltype_   = matchobj.group(3).lower() + '/'
            else:
                this.checksums_ = matchobj.group(1)
                this.archives_  = matchobj.group(2)
                this.voltype_   = matchobj.group(3) + '/'

            if this.voltype_[:-1] not in VOLTYPES:
                raise ValueError('Unrecognized volume type "%s": %s' %
                                 (this.voltype_[:-1], this.logical_path))

            return this._complete(must_exist, caching, lifetime)

        raise ValueError('Cannot define child from PDS root: ' +
                         this.logical_path)

    def parent(self, must_exist=False, caching='default', lifetime=None):
        """Constructor for the parent PdsFile of this PdsFile."""

        if self.is_virtual:    # virtual pdsdir
            return None

        # Return the virtual parent if there is one
        logical_path = os.path.split(self.logical_path)[0]
        if logical_path in CATEGORIES or not self.abspath:
            return PdsFile.from_logical_path(logical_path,
                                             must_exist=must_exist)
        else:
            abspath = os.path.split(self.abspath)[0]
            return PdsFile.from_abspath(abspath,
                                        must_exist=must_exist)

    @staticmethod
    def from_logical_path(path, fix_case=False, must_exist=False,
                                caching='default', lifetime=None):
        """Constructor for a PdsFile from a logical path."""

        if not path or path == '/':
            return None

        path = path.strip('/')

        # If the PdsFile with this logical path is in the cache, return it
        try:
            return CACHE[path]
        except KeyError:
            pass

        # Work upward through the path until something is found in the cache.
        # Case must match!
        parts = path.split('/')
        parts[0] = parts[0].lower()     # category is always lower case
        ancestor = None

        for lparts in range(len(parts)-1, 0, -1):
            ancestor_path = '/'.join(parts[:lparts])

            try:
                ancestor = CACHE[ancestor_path]
                break
            except KeyError:
                pass

        if ancestor is None:
            raise IOError('File not found: ' + path)

        # Handle the rest of the tree using child()
        this = ancestor
        for part in parts[lparts:]:
            this = this.child(part, fix_case=fix_case, must_exist=must_exist,
                                    caching=caching, lifetime=lifetime)

        return this

    @staticmethod
    def from_abspath(abspath, fix_case=False, must_exist=False,
                              caching='default', lifetime=None):
        """Constructor from an absolute path."""

        abspath = abspath.rstrip('/')
        try:
            return CACHE[abspath]
        except KeyError:
            pass

        # Make sure this is an absolute path
        # For Unix, it must start with "/"
        # For Windows, the first item must contain a colon
        # Note that all file paths must use forward slashes, not backslashes

        parts = abspath.split('/')

        # Windows can have the first part be '<drive>:' and that's OK
        drive_spec = ''
        if os.sep == '\\' and parts[0][-1] == ':':
            drive_spec = parts[0]
            parts[0] = ''
        if parts[0] != '':
            raise ValueError('Not an absolute path: ' + abspath)

        # Search for "holdings" or "shelves"
        parts_lc = [p.lower() for p in parts]
        try:
            holdings_index = parts_lc.index('holdings')
        except ValueError:
            try:
                holdings_index = parts_lc.index('shelves')
            except ValueError:
                raise ValueError('"holdings" directory not found in ' +
                                 abspath)

        # Fill in this.disk_, absolute path to "pdsdata*"
        this = PdsFile()
        this.disk_ = drive_spec + '/'.join(parts[:holdings_index]) + '/'

        # Get case right if possible
        if fix_case and (os.path.exists(this.disk_) and
                         os.path.isdir(this.disk_)):
            children = os.listdir(this.disk_)
            children_lc = [c.lower() for c in children]
            try:
                k = children_lc.index('holdings')
            except ValueError:
                raise ValueError('"holdings" directory not found inside ' +
                                 this.disk_)

            holdings_alone = children[k]
        else:
            holdings_alone = 'holdings'

        # Fill in the HTML root
        # ...pdsdata-whatever/holdings -> /holdings/
        # ...pdsdata2-whatever/holdings -> /holdings2/
        subparts = parts[holdings_index-1].split('-')
        suffix = subparts[0][-1]
        if suffix not in '123456789':
            suffix = ''

        this.root_ = this.disk_ + holdings_alone + '/'
        this.html_root_ = holdings_alone + suffix + '/'

        # Note: In Apache, the path "/holdings[n]/" must redirect to this root
        # directory

        this.logical_path = ''
        this.abspath = this.disk_ + holdings_alone
        this.basename = holdings_alone

        # Handle the rest of the tree using child()
        for part in parts[holdings_index + 1:]:
            this = this.child(part, fix_case=fix_case, must_exist=must_exist,
                                    caching=caching, lifetime=lifetime)

        if must_exist and not this.exists:
            raise IOError('File not found', this.abspath)

        return this

    def from_relative_path(self, path, fix_case=False, must_exist=False,
                                       caching='default', lifetime=None):
        """Constructor for a PdsFile given a path relative to this one."""

        path = path.rstrip('/')
        parts = path.split('/')

        if len(parts) == 0:
            return self._complete(must_exist, caching, lifetime)

        this = self
        for part in parts:
            this = this.child(part, fix_case=fix_case, must_exist=must_exist,
                                    caching=caching, lifetime=lifetime)

        return this

    @staticmethod
    def _from_absolute_or_logical_path(path, fix_case=False, must_exist=False,
                                       caching='default', lifetime=None):
        """Return a PdsFile based on either an absolute or a logical path."""

        if '/holdings/' in path:
            return PdsFile.from_abspath(path,
                                        fix_case=False, must_exist=False,
                                        caching='default', lifetime=None)
        else:
            return PdsFile.from_logical_path(path,
                                             fix_case=False, must_exist=False,
                                             caching='default', lifetime=None)

    @staticmethod
    def from_path(path, caching='default', lifetime=None):
        """Find the PdsFile, if possible based on anything roughly resembling
        an actual path in the filesystem, using sensible defaults for missing
        components."""

        path = str(path)    # make sure it isn't unicode

        if path == '': path = 'volumes'     # prevents an error below

        # Make a quick return if possible
        try:
            return CACHE[path]
        except KeyError:
            pass

        path = path.rstrip('/')
        path_lc = path.lower()

        # Reserve a row indicator for later
        k = path_lc.find('.tab/')
        if k >= 0:
            row_designator = path[k+5:]
            path = path[:k+4]
        else:
            row_designator = ''

        # Interpret the URL part by part
        parts = path.split('/')

        if path_lc.startswith('/volumes/pdsdata'):
            parts = parts[3:]

        if parts[0].lower().startswith('holdings'):
            parts = parts[1:]

        # Interpret leading parts
        this = PdsFile()

        # Look for checksums, archives, and voltypes, and an isolated suffix
        while len(parts) > 0:
            if '-' in parts[0]:
                parts = parts[0].split('-') + parts[1:]

            part = parts[0].lower()
            if part in ('archives', 'tar', 'targz', 'tar.gz'):
                this.archives_ = 'archives-'
            elif part in ('checksums', 'md5'):
                this.checksums_ = 'checksums-'
            elif part in VOLTYPES:
                this.voltype_ = part + '/'
            else:
                try:
                    _ = PdsFile.version_info('_' + part)
                    this.suffix = '_' + part
                except ValueError:
                    break

            parts = parts[1:]

        # Also check at end
        while len(parts) > 0:
            part = parts[-1].lower()
            if part in ('archives', 'tar', 'targz', 'tar.gz'):
                this.archives_ = 'archives-'
            elif part in ('checksums', 'md5'):
                this.checksums_ = 'checksums-'
            elif part in VOLTYPES:
                this.voltype_ = part + '/'
            else:
                try:
                    _ = PdsFile.version_info('_' + part)
                    this.suffix = '_' + part
                except ValueError:
                    break

            parts = parts[:-1]

        # Look for a volume set
        if len(parts) > 0:
            matchobj = VOLSET_PLUS_REGEX_I.match(parts[0])
            if matchobj:
                subparts = matchobj.group(1).partition('_')
                this.volset = subparts[0].upper() + '_' + subparts[2].lower()
                suffix    = matchobj.group(2).lower()
                extension = matchobj.group(3).lower()

                # Special file names
                if extension == '.tar.gz':
                    this.archives_ = 'archives-'
                elif extension == '_md5.txt':
                    this.checksums_ = 'checksums-'

                for test_type in VOLTYPES:
                    if suffix.endswith('_' + test_type):
                        this.voltype_ = test_type + '/'
                        suffix = suffix[:-len(test_type)-1]
                        break

                if suffix:
                    this.suffix = suffix

                parts = parts[1:]

        # Look for a volume name
        if len(parts) > 0:
            matchobj = VOLNAME_PLUS_REGEX_I.match(parts[0])
            if matchobj:
                this.volname = matchobj.group(1).upper()
                suffix    = matchobj.group(2).lower()
                extension = matchobj.group(3).lower()

                # Special file names
                if extension == '.tar.gz':
                     this.archives_ = 'archives-'
                elif extension == '_md5.txt':
                    this.checksums_ = 'checksums-'

                for test_type in VOLTYPES:
                    if suffix == '_' + test_type:
                        this.voltype_ = test_type + '/'
                        break

                parts = parts[1:]

        # Determine category
        if this.voltype_ == '':
            this.voltype_ = 'volumes/'

        this.category_ = this.checksums_ + this.archives_ + this.voltype_

        # Determine the volume set and path below
        if this.volname:
            volname = this.volname.lower()
            if this.suffix:
                rank = PdsFile.version_info(this.suffix)[0]
            else:
                rank = CACHE['$RANKS-' + this.category_][volname][-1]

            try:
                this_abspath = CACHE['$VOLS-' + this.category_][volname][rank]
            except KeyError:
                # Allow for change from, e.g., _peer_review to _lien_resolution
                if rank in PdsFile.LATEST_VERSION_RANKS[:-1]:
                    k = PdsFile.LATEST_VERSION_RANKS.index(rank)
                    alt_ranks = PdsFile.LATEST_VERSION_RANKS[k+1:]

                # Without suffix, find most recent
                elif rank == PdsFile.LATEST_VERSION_RANKS[-1]:
                    alt_ranks = PdsFile.LATEST_VERSION_RANKS[:-1][::-1]
                else:
                    alt_ranks = []

                this_abspath = None
                for alt_rank in alt_ranks:
                  try:
                    this_abspath = CACHE['$VOLS-' + this.category_][volname]\
                                                                   [alt_rank]
                    break
                  except KeyError:
                    continue

                if not this_abspath:
                    raise ValueError('Suffix "%s" not found: %s' %
                                     (this.suffix, path))

            this = PdsFile.from_abspath(this_abspath)

        elif this.volset:
            volset = this.volset.lower()
            if this.suffix:
                rank = PdsFile.version_info(this.suffix)[0]
            else:
                rank = CACHE['$RANKS-' + this.category_][volset][-1]

            try:
                this_abspath = CACHE['$VOLS-' + this.category_][volset][rank]
            except KeyError:
                # Allow for change from, e.g., _peer_review to _lien_resolution
                if rank in PdsFile.LATEST_VERSION_RANKS[:-1]:
                    k = PdsFile.LATEST_VERSION_RANKS.index(rank)
                    alt_ranks = PdsFile.LATEST_VERSION_RANKS[k+1:]
                # Without suffix, find most recent
                elif rank == PdsFile.LATEST_VERSION_RANKS[-1]:
                    alt_ranks = PdsFile.LATEST_VERSION_RANKS[:-1][::-1]
                else:
                    alt_ranks = []

                this_abspath = None
                for alt_rank in alt_ranks:
                  try:
                    this_abspath = CACHE['$VOLS-' + this.category_][volset]\
                                                                   [alt_rank]
                    break
                  except KeyError:
                    continue

                if not this_abspath:
                    raise ValueError('Suffix "%s" not found: %s' %
                                     (this.suffix, path))

            this = PdsFile.from_abspath(this_abspath)

        else:
            this = CACHE[this.category_[:-1]]

        if len(parts) == 0:
            return this._complete(False, caching, lifetime)

        # Resolve the path below
        for part in parts:
            this = this.child(part, fix_case=True,
                                    caching=caching, lifetime=lifetime)

        # If we have a row_designator, apply it now
        if row_designator:
            _ = this.childnames     # Fill in the child objectes
            this = this.child(row_designator, fix_case=False, must_exist=True)

        return this

    @staticmethod
    def from_filespec(filespec):
        """The PdsFile object based on a volume name plus file specification
        path, without the category or prefix specified. This is only implemented
        for products used by OPUS.
        """

        logical_path = PdsFile.FILESPEC_TO_LOGICAL_PATH.first(filespec)
        if not logical_path:
            raise ValueError('Unrecognized file specification: ' + filespec)

        # If the filespec contains a match pattern, search the filesystem for
        # matches and return the first.
        if ('*' in logical_path) or ('?' in logical_path) or \
           ('[' in logical_path):
            parts = logical_path.split('/')
            volset_logical_path = '/'.join(parts[:2])
            volset_pdsf = PdsFile.from_logical_path(volset_logical_path)
            abspath_pattern = volset_pdsf.abspath + '/' + '/'.join(parts[2:])
            abspaths = glob.glob(abspath_pattern)
            return PdsFile.from_abspath(abspaths[0])

        return PdsFile.from_logical_path(logical_path)

    @staticmethod
    def from_opus_id(opus_id):
        """The PdsFile of the primary data file associated with this OPUS ID.
        """

        with_slashes = opus_id.replace('-','/').replace('//', '-')
        filespec = PdsFile.OPUS_ID_TO_FILESPEC.first(with_slashes)
        if not filespec:
            raise ValueError('Unrecognized OPUS ID: ' + opus_id)

        return PdsFile.from_filespec(filespec)

    def volume_pdsfile(self):
        """PdsFile object for the root volume."""

        abspath = self.volume_abspath()
        if abspath:
            return PdsFile.from_abspath(abspath)
        else:
            raise ValueError('No associated volume for ' + self.abspath)

    def volume_pdsdir(self):
        """PdsFile object for the root volume, if it is a directory."""

        pdsf = self.volume_pdsfile()
        if pdsf.isdir:
            return pdsf
        else:
            raise ValueError('No associated volume directory for ' +
                             self.abspath)

    def volset_pdsfile(self):
        """PdsFile object for the root volume set."""

        abspath = self.volset_abspath()
        if abspath:
            return PdsFile.from_abspath(abspath)
        else:
            raise ValueError('No associated volume set for ' + self.abspath)

    def volset_pdsdir(self):
        """PdsFile object for the root volume set."""

        pdsf = self.volset_pdsfile()
        if pdsf.isdir:
            return pdsf
        else:
            raise ValueError('No associated volume set directory for ' +
                             self.abspath)

    ############################################################################
    # Path tests
    ############################################################################

    def is_volume_dir(self):
        return (self.volname_ and not self.interior)

    def is_volume_file(self):
        return (self.volname and not self.volname_)

    def is_volume(self):
        return self.is_volume_dir() or self.is_volume_file()

    def is_volset_dir(self):
        return (self.volset_ and not self.volname)

    def is_volset_file(self):
        return (self.volset and not self.volset_)

    def is_volset(self):
        return self.is_volset_dir() or self.is_volset_file()

    def is_category_dir(self):
        return (self.volset == '')

    def volume_abspath(self):
        """Return the absolute path to the volume associated with this object.
        """

        if not self.volname:
            return None
        elif self.volname_:
            return ''.join([self.root_, self.category_, self.volset_,
                            self.volname])
        else:
            return ''.join([self.root_, self.category_, self.volset_,
                            self.interior])

    def volset_abspath(self):
        """Return the absolute path to the volset associated with this object.
        """

        if not self.volset:
            return None
        elif self.volset_:
            return ''.join([self.root_, self.category_, self.volset,
                            self.suffix])
        else:
            return ''.join([self.root_, self.category_, self.interior])

    ############################################################################
    # Checksum path associations
    ############################################################################

    def checksum_path_and_lskip(self):
        """The absolute path to the checksum file associated with this PdsFile.
        Also return the number of characters to skip over in that absolute
        path to obtain the basename of the checksum file."""

        if self.checksums_:
            raise ValueError('No checksums of checksum files: ' +
                             self.logical_path)

        if self.voltype_ == 'volumes/':
            suffix = ''
        else:
            suffix = '_' + self.voltype_[:-1]

        if self.volname:
            abspath = ''.join([self.root_, 'checksums-', self.category_,
                               self.volset_, self.volname, suffix, '_md5.txt'])
            lskip = (len(self.root_) + len(self.category_) +
                     len(self.volset_))
        else:
            if not self.archives_:
                raise ValueError('Non-archive checksums require volumes: ' +
                                 self.logical_path)

            abspath = ''.join([self.root_, 'checksums-', self.category_,
                               self.volset, self.suffix, suffix, '_md5.txt'])
            lskip = (len(self.root_) + len(self.category_) +
                     len(self.volset_))

        return (abspath, lskip)

    def checksum_path_if_exact(self):
        """Absolute path to the checksum file with the exact same contents as
        this directory; otherwise blank."""

        if self.checksums_: return ''

        try:
            if self.archives_:
                dirpath = self.dirpath_and_prefix_for_archive()[0]
                pdsf = PdsFile.from_abspath(dirpath)
            else:
                pdsf = self
                if pdsf.interior: return ''
                if not pdsf.volname_: return ''

            return pdsf.checksum_path_and_lskip()[0]

        except (ValueError, TypeError):
            PdsFile.LAST_EXC_INFO = sys.exc_info()
            return ''

    def dirpath_and_prefix_for_checksum(self):
        """Absolute path to the directory associated with this checksum path.
        """

        if self.archives_:
            dirpath = ''.join([self.root_, self.archives_, self.voltype_,
                               self.volset, self.suffix])
            prefix_ = ''.join([self.root_, self.archives_, self.voltype_,
                               self.volset, self.suffix, '/'])
        else:
            dirpath = ''.join([self.root_, self.archives_, self.voltype_,
                               self.volset_, self.volname])
            prefix_ = ''.join([self.root_, self.voltype_, self.volset_])

        return (dirpath, prefix_)

    ############################################################################
    # Archive path associations
    ############################################################################

    def archive_path_and_lskip(self):
        """The absolute path to the archive file associated with this PdsFile.
        Also return the number of characters to skip over in that absolute
        path to obtain the basename of the archive file."""

        if self.checksums_:
            raise ValueError('No archives for checksum files: ' +
                             self.logical_path)

        if self.archives_:
            raise ValueError('No archives for archive files: ' +
                             self.logical_path)

        if self.voltype_ == 'volumes/':
            suffix = ''
        else:
            suffix = '_' + self.voltype_[:-1]

        if not self.volname:
            raise ValueError('Archives require volume names: ' +
                              self.logical_path)

        abspath = ''.join([self.root_, 'archives-', self.category_,
                           self.volset_, self.volname, suffix, '.tar.gz'])
        lskip = len(self.root_) + len(self.category_) + len(self.volset_)

        return (abspath, lskip)

    def archive_path_if_exact(self):
        """Absolute path to the archive file with the exact same contents as
        this directory; otherwise blank."""

        try:
            path = self.archive_path_and_lskip()[0]
        except ValueError:
            return ''

        if self.interior == '':
            return path

        return ''

    def dirpath_and_prefix_for_archive(self):
        """Absolute path to the directory associated with this archive path."""

        dirpath = ''.join([self.root_, self.voltype_,
                           self.volset_, self.volname])

        parent = ''.join([self.root_, self.voltype_, self.volset_])

        return (dirpath, parent)

    def archive_logpath(self, task):
        """Absolute path to the log file associated with this archive file."""

        this = self.copy()
        this.checksums_ = ''
        if this.archives_ == 'archives-':
            this.archives_ = ''
            this.category_ = this.voltype_

        return this.log_path_for_volume(id='targz', task=task, dir='archives')

    ############################################################################
    # Shelf support
    ############################################################################

    SHELF_CACHE = {}
    SHELF_ACCESS = {}
    SHELF_CACHE_SIZE = 160
    SHELF_CACHE_SLOP = 20
    SHELF_ACCESS_COUNT = 0

    SHELF_NULL_KEY_VALUES = {}

    def shelf_path_and_lskip(self, id='info', volname=''):
        """The absolute path to the shelf file associated with this PdsFile.
        Also return the number of characters to skip over in that absolute
        path to obtain the basename of the shelf file."""

        if self.checksums_:
            raise ValueError('No shelf files for checksums: ' +
                             self.logical_path)

        if self.archives_:
            if not self.volset_:
                raise ValueError('Archive shelves require volume sets: ' +
                                 self.logical_path)

            abspath = ''.join([self.disk_, 'shelves/', id, '/', self.category_,
                               self.volset, self.suffix, '_', id, '.shelf'])
            lskip = (len(self.root_) + len(self.category_) +
                     len(self.volset_))

        else:
            if not self.volname_ and not volname:
                raise ValueError('Non-archive shelves require volume names: ' +
                                 self.logical_path)

            if volname:
                this_volname = volname.rstrip('/')
            else:
                this_volname = self.volname

            abspath = ''.join([self.disk_, 'shelves/', id, '/', self.category_,
                               self.volset_, this_volname, '_', id, '.shelf'])
            lskip = (len(self.root_) + len(self.category_) +
                     len(self.volset_) + len(this_volname) + 1)

        return (abspath, lskip)

    def shelf_path_and_key(self, id='info', volname=''):
        """Absolute path to a shelf file, plus the key for this item."""

        (abspath, lskip) = self.shelf_path_and_lskip(id=id, volname=volname)
        if volname:
            return (abspath, '')
        else:
            return (abspath, self.interior)

    @staticmethod
    def _get_shelf(shelf_path):
        """Internal method to open a shelf file or pickle file. A limited number
        of shelf files are kept open at all times to reduce file IO."""

        # If the shelf is already open, update the access count and return it
        if shelf_path in PdsFile.SHELF_CACHE:
            PdsFile.SHELF_ACCESS[shelf_path] = PdsFile.SHELF_ACCESS_COUNT
            PdsFile.SHELF_ACCESS_COUNT += 1

            return PdsFile.SHELF_CACHE[shelf_path]

        # Open and cache the shelf
        if USE_PICKLES:
            shelf_path = shelf_path.rpartition('.')[0] + '.pickle'
            Name = 'Pickle'
            name = 'pickle'
        else:
            Name = 'Shelf'
            name = 'shelf'

        if LOGGER:
            LOGGER.debug('Opening %s file' % name, shelf_path)

        if not os.path.exists(shelf_path):
            raise IOError('%s file not found: %s' % (Name, shelf_path))

        try:
            if USE_PICKLES:
                with open(shelf_path, 'rb') as f:
                    shelf = pickle.load(f)
            else:
                shelf = shelve.open(shelf_path, flag='r')

        except Exception as e:
            raise IOError('Unable to open %s file: %s' % (name, shelf_path))

        # Save the null key values from the shelves. This can save a lot of
        # shelf open/close operations.
        if '' in shelf:
            PdsFile.SHELF_NULL_KEY_VALUES[shelf_path] = shelf['']

        PdsFile.SHELF_ACCESS[shelf_path] = PdsFile.SHELF_ACCESS_COUNT
        PdsFile.SHELF_ACCESS_COUNT += 1

        PdsFile.SHELF_CACHE[shelf_path] = shelf

        # Trim the cache if necessary
        if len(PdsFile.SHELF_CACHE) > (PdsFile.SHELF_CACHE_SIZE +
                                       PdsFile.SHELF_CACHE_SLOP):
            pairs = [(PdsFile.SHELF_ACCESS[k],k) for k in PdsFile.SHELF_CACHE]
            pairs.sort()

            shelf_paths = [p[1] for p in pairs]
            for shelf_path in shelf_paths[:-PdsFile.SHELF_CACHE_SIZE]:
                PdsFile._close_shelf(shelf_path)

        return shelf

    @staticmethod
    def _close_shelf(shelf_path):
        """Internal method to close a shelf file. A limited number of shelf
        fiels are kept open at all times to reduce file IO."""

        # If the shelf is not already open, return
        if shelf_path not in PdsFile.SHELF_CACHE:
            if LOGGER:
                if USE_PICKLES:
                    LOGGER.error('Cannot close pickle file; not currently open',
                                 shelf_path.rpartition('.') + '.pickle')
                else:
                    LOGGER.error('Cannot close shelf; not currently open',
                                 shelf_path)
                return

        # Close the shelf and remove from the cache
        if not USE_PICKLES:
            PdsFile.SHELF_CACHE[shelf_path].close()

        del PdsFile.SHELF_CACHE[shelf_path]
        del PdsFile.SHELF_ACCESS[shelf_path]

        if LOGGER:
            if USE_PICKLES:
                LOGGER.debug('Pickle file closed',
                             shelf_path.rpartition('.') + '.pickle')
            else:
                LOGGER.debug('Shelf closed', shelf_path)

    @staticmethod
    def close_all_shelves():
        """Close all shelf files."""

        for shelf_path in PdsFile.SHELF_CACHE.keys():   # use keys() so dict can
                                                        # be modified in loop!
            PdsFile._close_shelf(shelf_path)

    def shelf_lookup(self, id='info', volname=''):
        """Return the contents of the id'd shelf file associated with this
        object."""

        (shelf_path, key) = self.shelf_path_and_key(id, volname)

        # This potentially saves the need for a lot of opens and closes
        if key == '':
            if shelf_path not in PdsFile.SHELF_NULL_KEY_VALUES:
                value = self.shelf_null_key_value(id, volname)
                PdsFile.SHELF_NULL_KEY_VALUES[shelf_path] = value

            return PdsFile.SHELF_NULL_KEY_VALUES[shelf_path]

        shelf = PdsFile._get_shelf(shelf_path)
        if shelf is None:
            return None

        return shelf[key]

    def shelf_null_key_value(self, id='info', volname=''):
        """This is a quick hack to read the second line of the .py file
        instead of the shelf file. It speeds up the case of needing the size
        of each volume."""

        (shelf_path, key) = self.shelf_path_and_key(id, volname)
        dict_path = shelf_path.rpartition('.')[0] + '.py'
        with open(dict_path, 'r') as f:
            rec = f.readline()
            rec = f.readline()

        value = rec.partition(':')[2][:-2]  # after ':', before ',\n'
        return eval(value)

    ############################################################################
    # Log path associations
    ############################################################################

    LOG_ROOT_ = None

    @staticmethod
    def set_log_root(root=None):
        """Define the default root directory for logs. If None, use the "logs"
        directory parallel to "holdings"."""

        if root is None:
            PdsFile.LOG_ROOT_ = None
        else:
            PdsFile.LOG_ROOT_ = root.rstrip('/') + '/'

    def log_path_for_volume(self, id='', task='', dir='', place='default'):
        """Return a complete log file path for this volume.

        The file name is [dir/]category/volset/volname_id_timetag[_task].log.
        """

        # This option provides for a temporary override of the default log root
        if place == 'default':
            temporary_log_root = PdsFile.LOG_ROOT_
        elif place == 'parallel':
            temporary_log_root = None
        else:
            raise ValueError('unrecognized place option: ' + place)

        if temporary_log_root is None:
            parts = [self.disk_, 'logs/']
        else:
            parts = [temporary_log_root]

        if dir:
            parts += [dir, '/']

        parts += [self.category_, self.volset_, self.volname]

        if id:
            parts += ['_', id]

        timetag = datetime.datetime.now().strftime(LOGFILE_TIME_FMT)
        parts += ['_', timetag]

        if task:
            parts += ['_', task]

        parts += ['.log']

        return ''.join(parts)

    def log_path_for_volset(self, id='', task='', dir='', place='default'):
        """Return a complete log file path for this volume set.

        The file name is [dir/]category/volset_id_timetag[_task].log.
        """

        # This option provides for a temporary override of the default log root
        if place == 'default':
            temporary_log_root = PdsFile.LOG_ROOT_
        elif place == 'parallel':
            temporary_log_root = None
        else:
            raise ValueError('unrecognized place option: ' + place)

        if temporary_log_root is None:
            parts = [self.disk_, 'logs/']
        else:
            parts = [temporary_log_root]

        if dir:
            parts += [dir, '/']

        parts += [self.category_, self.volset, self.suffix]

        if id:
            parts += ['_', id]

        timetag = datetime.datetime.now().strftime(LOGFILE_TIME_FMT)
        parts += ['_', timetag]

        if task:
            parts += ['_', task]

        parts += ['.log']

        return ''.join(parts)

    ############################################################################
    # How to split and sort filenames
    ############################################################################

    def split_basename(self, basename=''):
        """Split into (anchor, suffix, extension).

        Default behavior is to split a file at first period; split a volume
        set name before the suffix. Can be overridden."""

        if basename == '':
            basename = self.basename

        # Special case: volset[_...], volset[_...]_md5.txt, volset[_...].tar.gz
        matchobj = VOLSET_PLUS_REGEX.match(basename)
        if matchobj is not None:
            return (matchobj.group(1), matchobj.group(2), matchobj.group(3))

        # Special case: volname[_...]_md5.txt, volname[_...].tar.gz
        matchobj = VOLNAME_PLUS_REGEX.match(basename)
        if matchobj is not None:
            return (matchobj.group(1), matchobj.group(2), matchobj.group(3))

        return self.SPLIT_RULES.first(basename)

    # Global default settings for sort ordering
    _LABELS_AFTER = True
    _DIRS_FIRST = False
    _DIRS_LAST = False
    _INFO_FIRST = True

    def sort_labels_after(labels_after):
        """If True, all label files will appear after their associated data
        files when sorted."""

        PdsFile._LABELS_AFTER = labels_after

    def sort_dirs_first(dirs_first):
        """If True, directories will appear before all files in a sorted list.
        """

        PdsFile._DIRS_FIRST = dirs_first

    def sort_dirs_last(dirs_last):
        """If True, directories will appear after all files in a sorted list.
        """

        PdsFile._DIRS_LAST = dirs_last

    def sort_info_first(info_first):
        """If True, info files will be listed first in all sorted lists."""

        PdsFile._INFO_FIRST = info_first

    def basename_is_label(self, basename):
        """True if this basename is a label. Override if label identification
        ever depends on the data set."""

        return (len(basename) > 4) and (basename[-4:].lower() == '.lbl')

    def basename_is_viewable(self, basename=None):
        """True if this basename is viewable. Override if viewable files can
        have extensions other than the usual set (.png, .jpg, etc.)."""

        if basename is None:
            basename = self.basename

        parts = basename.rpartition('.')
        if parts[1] != '.': return False

        return (parts[2].lower() in VIEWABLE_EXTS)

    def sort_basenames(self, basenames, labels_after=None, dirs_first=None,
                             dirs_last=None, info_first=None,
                             parent_abspath=''):
        """Sort basenames, including additional options. Input None for
        defaults."""

        def modified_sort_key(basename):

            # Volumes of the same name sort by decreasing version number
            matchobj = VOLSET_PLUS_REGEX.match(basename)
            if matchobj is not None:
                parts = [matchobj.group(1), matchobj.group(2),
                                            matchobj.group(3)]
                parts = [parts[0], -PdsFile.version_info(parts[1])[0], parts[2]]
                return parts

            # Default sort is based on split_basename()
            modified = self.SORT_KEY.first(basename)
            parts = list(self.split_basename(modified))

            if labels_after:
                parts[2:] = [self.basename_is_label(basename)] + parts[2:]

            if dirs_first and parent_abspath:
                abspath = _clean_join(parent_abspath, basename)
                parts = [not os.path.isdir(abspath)] + parts
            elif dirs_last and parent_abspath:
                abspath = _clean_join(parent_abspath, basename)
                parts = [os.path.isdir(abspath)] + parts

            if info_first:
                parts = [not basename.lower().endswith('info.txt')] + parts

            return parts

        if not parent_abspath:
            parent_abspath = self.abspath

        if labels_after is None:
            labels_after = PdsFile._LABELS_AFTER

        if dirs_first is None:
            dirs_first = PdsFile._DIRS_FIRST

        if dirs_last is None:
            dirs_last = PdsFile._DIRS_LAST

        if info_first is None:
            info_first = PdsFile._INFO_FIRST

        basenames = list(basenames)
        basenames.sort(key=modified_sort_key)
        return basenames

    def sort_childnames(self, labels_after=None, dirs_first=None):
        """A sorted list of the contents of this directory."""

        return self.sort_basenames(self.childnames, labels_after, dirs_first,
                                   parent_abspath=self.abspath)

    def viewable_childnames(self):
        """A sorted list of the files in this directory that are viewable."""

        basenames = self.sort_childnames()
        return [b for b in basenames if self.basename_is_viewable(b)]

    def childnames_by_anchor(self, anchor):
        """A list of child basenames having the given anchor."""

        matches = []
        for basename in self.childnames:
            parts = self.split_basename(basename)
            if parts[0] == anchor:
                matches.append(basename)

        return self.sort_basenames(matches)

    def viewable_childnames_by_anchor(self, anchor):
        """A list of viewable child names having the given anchor."""

        matches = self.childnames_by_anchor(anchor)
        return [m for m in matches if self.basename_is_viewable(m)]

    ############################################################################
    # Transformations
    ############################################################################

    #### ... for pdsfiles

    @staticmethod
    def abspaths_for_pdsfiles(pdsfiles, must_exist=False):
        if must_exist:
            return [p.abspath for p in pdsfiles if p.abspath is not None
                                                and p.exists]
        else:
            return [p.abspath for p in pdsfilesf if p.abspath is not None]

    @staticmethod
    def logicals_for_pdsfiles(pdsfiles, must_exist=False):
        if must_exist:
            return [p.logical_path for p in pdsfiles if p.exists]
        else:
            return [p.logical_path for p in pdsfiles]

    @staticmethod
    def basenames_for_pdsfiles(pdsfiles, must_exist=False):
        if must_exist:
            return [p.basename for p in pdsfiles if p.exists]
        else:
            return [p.basename for p in pdsfiles]

    #### ... for abspaths

    @staticmethod
    def pdsfiles_for_abspaths(abspaths, must_exist=False):
        pdsfiles = [PdsFile.from_abspath(p) for p in abspaths]
        if must_exist:
            pdsfiles = [pdsf for pdsf in pdsfiles if pdsf.exists]

        return pdsfiles

    @staticmethod
    def logicals_for_abspaths(abspaths, must_exist=False):
        if must_exist:
            abspaths = [p for p in abspaths if os.path.exists(p)]

        return [logical_path_from_path(p) for p in abspaths]

    @staticmethod
    def basenames_for_abspaths(abspaths, must_exist=False):
        if must_exist:
            abspaths = [p for p in abspaths if os.path.exists(p)]

        return [os.path.basename(p) for p in abspaths]

    #### ... for logicals

    @staticmethod
    def pdsfiles_for_logicals(logical_paths, must_exist=False):
        pdsfiles = [PdsFile.from_logical_path(p) for p in logical_paths]
        if must_exist:
            pdsfiles = [pdsf for pdsf in pdsfiles if pdsf.exists]

        return pdsfiles

    @staticmethod
    def abspaths_for_logicals(logical_paths, must_exist=False):
        pdsfiles = PdsFile.pdsfiles_for_logicals(logical_paths,
                                                 must_exist=must_exist)
        return [pdsf.abspath for pdsf in pdsfiles]

    @staticmethod
    def basenames_for_logicals(logical_paths, must_exist=False):
        if must_exist:
            pdsfiles = PdsFile.pdsfiles_for_logicals(logical_paths,
                                                     must_exist=must_exist)
            return PdsFile.basenames_for_pdsfiles(pdsfiles)
        else:
            return [os.path.basename(p) for p in logical_paths]

    #### ... for basenames

    def pdsfiles_for_basenames(self, basenames, must_exist=False):

        pdsfiles = [self.child(b) for b in basenames]

        if must_exist:
            pdsfiles = [pdsf for pdsf in pdsfiles if pdsf.exists]

        return pdsfiles

    def abspaths_for_basenames(self, basenames, must_exist=False):
        # shortcut
        if self.abspath and not must_exist:
            return [_clean_join(self.abspath, b) for b in basenames]

        pdsfiles = self.pdsfiles_for_basenames(basenames, must_exist=must_exist)
        return [pdsf.abspath for pdsf in pdsfiles]

    def logicals_for_basenames(self, basenames, must_exist=False):
        # shortcut
        if not must_exist:
            return [_clean_join(self.logical_path, b) for b in basenames]

        pdsfiles = self.pdsfiles_for_basenames(basenames, must_exist=must_exist)
        return [pdsf.logical_path for pdsf in pdsfiles]

    ############################################################################
    # Associations
    ############################################################################

    def associated_logical_paths(self, category, must_exist=True,
                                                 primary=False):

        if not self.volset: return []   # Not for virtual paths

        return self._associated_paths(category, must_exist=must_exist,
                                                primary=primary,
                                                use_abspaths=False)

    def associated_abspaths(self, category, must_exist=True,
                                            primary=False):

        return self._associated_paths(category, must_exist=must_exist,
                                                primary=primary,
                                                use_abspaths=True)

    def _associated_paths(self, category, must_exist=True,
                                          primary=False, use_abspaths=True):
        """A list of logical or absolute paths to files in the specified
        category.

        Inputs:
            category        the category of the associated paths.
            must_exist      True to return only paths that exist.
            primary         True to limit the list to the primary or best
                            match based on filename criteria.
            use_abspaths    True to return absolute paths; False to return
                            logical paths
        """

        def test_pattern(pattern):

            # Handle an index row by separating the filepath from the suffix
            if '.tab/' in pattern:
                parts = pattern.partition('.tab')
                pattern = parts[0] + parts[1]
                suffix = parts[2]
            else:
                suffix = ''

            # Find the file(s) that match the pattern
            if must_exist or ('*' in pattern or
                              '?' in pattern or
                              '[' in pattern):
                test_abspaths = glob.glob(pattern)
            else:
                test_abspaths = [pattern]

            # Without a suffix, we're done
            if not suffix:
                return test_abspaths

            # With a suffix, make sure it matches a row of the index
            filtered_abspaths = []
            for abspath in test_abspaths:
                pdsf = PdsFile.from_abspath(abspath)
                try:
                    row = pdsf.child(suffix[1:])
                    if row.exists:
                        filtered_abspaths.append(row.abspath)
                except Exception:
                    pass

            return filtered_abspaths

        # Begin active code...

        category = category.strip('/')

        # Handle checksums by finding associated files in subcategory
        if category.startswith('checksums-'):
            subcategory = category[len('checksums-'):]
            paths = self._associated_paths(subcategory,
                                           must_exist=must_exist,
                                           primary=primary,
                                           use_abspaths=use_abspaths)
            if not paths: return []

            this = PdsFile._from_absolute_or_logical_path(paths[0])
            try:
                checksum_abspath = this.checksum_path_and_lskip()[0]
            except ValueError:
                return []

            if must_exist and not os.path.exists(checksum_abspath):
                return []

            return [selected_path_from_path(checksum_abspath, use_abspaths)]

        # Handle archives by finding associated files in subcategory
        if category.startswith('archives-'):
            subcategory = category[len('archives-'):]
            paths = self._associated_paths(subcategory,
                                           must_exist=must_exist,
                                           primary=primary,
                                           use_abspaths=use_abspaths)
            if not paths: return []

            this = PdsFile._from_absolute_or_logical_path(paths[0])
            try:
                archive_abspath = this.archive_path_and_lskip()[0]
            except ValueError:
                return []

            if  must_exist and not os.path.exists(archive_abspath):
                return []

            return [selected_path_from_path(archive_abspath, use_abspaths)]

        # Get rid of checksums-
        if self.checksums_:
            if not self.volset:
                path = self.archives_ + self.voltype
            else:
                path = self.dirpath_and_prefix_for_checksum()[0]

            pdsf = PdsFile._from_absolute_or_logical_path(path)
            return pdsf._associated_paths(category,
                                          must_exist=must_exist,
                                          primary=primary,
                                          use_abspaths=use_abspaths)

        # Get rid of archives-
        if self.archives_:
            if not self.volset:
                path = self.voltype
            else:
                path = self.dirpath_and_prefix_for_archive()[0]

            pdsf = PdsFile._from_absolute_or_logical_path(path)
            return pdsf._associated_paths(category,
                                          must_exist=must_exist,
                                          primary=primary,
                                          use_abspaths=use_abspaths)

        # No more recursive calls...
        # Every path from here on is an abspath; translation to logical is only
        # upon return

        # Get the associated parallel inside volumes
        if self.category_ == 'volumes/':
            parallel_volume_pdsf = self
        else:
            parallel_volume_pdsf = self.associated_parallel('volumes')
            if parallel_volume_pdsf is None:
                return []

        # If our target is a volume, return results
        if category == 'volumes':
            abspaths = [parallel_volume_pdsf.abspath]

            patterns = self.ASSOCIATIONS_TO_VOLUMES.all(self.logical_path)
            patterns = [self.root_ + p for p in patterns]
            for pattern in patterns:
                abspaths += test_pattern(pattern)

            # Translate to additional volumes files if necessary
            if not primary:
                logical_paths = self.logicals_for_abspaths(abspaths)
                trans = self.VOLUMES_TO_ASSOCIATIONS['volumes']
                patterns = trans.all(logical_paths)
                patterns = [self.root_ + p for p in patterns]
                for pattern in patterns:
                    abspaths += test_pattern(pattern)

                # Add the linked abspaths to the set of matches
                if self.islabel:
                    abspaths += self.linked_abspaths

            # Remove duplicates and return
            abspaths = list(set(abspaths))
            if use_abspaths:
                return abspaths
            else:
                return PdsFile.logicals_for_abspaths(abspaths)

        # Translate to alternative voltypes as needed
        logical_paths = [parallel_volume_pdsf.logical_path]

        voltype = category.split('-')[-1]
        trans = parallel_volume_pdsf.VOLUMES_TO_ASSOCIATIONS[voltype]
        patterns = trans.all(logical_paths)
        patterns = [parallel_volume_pdsf.root_ + p for p in patterns]

        abspaths = []
        for pattern in patterns:
            abspaths += test_pattern(pattern)

        # Without checksums- or archives-, we're done
        if voltype == category:

            # Always include the associated parallel
            pdsf = parallel_volume_pdsf.associated_parallel(category=voltype)
            if pdsf:
                abspaths += [pdsf.abspath]

            # Remove duplicates and return
            abspaths = list(set(abspaths))
            if use_abspaths:
                return abspaths
            else:
                return PdsFile.logicals_for_abspaths(abspaths)

        # Handle archives-
        if 'archives-' in category:
            new_abspaths = []
            for abspath in abspaths:
                pdsf = PdsFile.from_abspath(abspath)
                new_abspaths.append(pdsf.archive_path_and_lskip()[0])

            abspaths = list(set(new_abspaths))

        # Without checksums-, we're done
        if 'checksums-' not in category:
            return abspaths

        # Handle checksums-
        new_abspaths = []
        for abspath in abspaths:
            pdsf = PdsFile.from_abspath(abspath)
            new_abspaths.append(pdsf.checksum_path_and_lskip())

        # Remove duplicates and return
        abspaths = list(set(abspaths))
        if use_abspaths:
            return abspaths
        else:
            return PdsFile.logicals_for_abspaths(abspaths)

    def associated_parallel(self, category=None, rank=None):
        """Rank can be number or 'latest', 'previous', 'next'; None for rank of
        this."""

        if category is None:
            category = self.category_

        category = category.rstrip('/')

        # Create the cached dictionary if necessary
        if self._associated_parallels_filled is None:
            self._associated_parallels_filled = {}

        # Return from dictionary if already available
        if rank is None and category in self._associated_parallels_filled:
            path = self._associated_parallels_filled[category]
            return PdsFile.from_logical_path(path)

        if (category, rank) in self._associated_parallels_filled:
            path = self._associated_parallels_filled[category, rank]
            return PdsFile.from_logical_path(path)

        # Handle special case of a virtual directory
        if not self.volset:
            target = CACHE.get(category)    # None if key not found

            if target is None:
                path = None
            else:
                path = target.logical_path

            self._associated_parallels_filled[category] = path
            self._associated_parallels_filled[category,     None] = path
            self._associated_parallels_filled[category, 'latest'] = path
            self._associated_parallels_filled[category,   999999] = path
            self._associated_parallels_filled[category,        0] = path
            self._associated_parallels_filled[category, 'previous'] = None
            self._associated_parallels_filled[category,     'next'] = None

            self._recache()
            if (category, rank) in self._associated_parallels_filled:
                return target
            else:
                return None

        # Interpret the rank
        original_rank = rank
        if rank is None:
            rank = self.version_rank
        elif rank == 'latest':
            rank = self.version_ranks[-1]
        elif type(rank) == str:
            try:
                k = self.version_ranks.index(self.version_rank)
                if rank == 'previous':
                    if k > 0:
                        rank = self.version_ranks[k-1]
                    else:
                        raise IndexError('')
                elif rank == 'next':
                    rank = self.version_ranks[k+1]

            except (IndexError, ValueError):
                PdsFile.LAST_EXC_INFO = sys.exc_info()
                self._associated_parallels_filled[category, rank] = None
                self._associated_parallels_filled[category, original_rank] = None
                self._recache()
                return None

        # If interpreted rank is in dictionary, return lookup
        if (category, rank) in self._associated_parallels_filled:
            self._associated_parallels_filled[category, original_rank] = \
                                self._associated_parallels_filled[category, rank]
            path = self._associated_parallels_filled[category, rank]
            return PdsFile.from_logical_path(path)

        # Search down from top for parallel file
        parts = []
        if self.volname:
            volkey = self.volname.lower()
            if self.interior:
                parts = self.interior.split('/')
        elif self.volset:
            volkey = self.volset.lower()
        else:
            volkey = None

        try:
            target_abspath = CACHE['$VOLS-' + category + '/'][volkey][rank]
        except KeyError:
            target = None
        else:
            target = PdsFile.from_abspath(target_abspath)

        if target is None:
            self._associated_parallels_filled[category, rank] = None
            self._associated_parallels_filled[category, original_rank] = None
            self._recache()
            return None

        if target.isdir:
            for part in parts:
                child = target.child(part, fix_case=True)
                if os.path.exists(child.abspath):
                    target = child
                else:
                    break

            # Last item might match by anchor
            if parts and part == parts[-1]:
                childnames = target.childnames_by_anchor(self.anchor)
                if childnames:
                    target = target.child(childnames[0])

        path = target.logical_path
        self._associated_parallels_filled[category, rank] = path
        self._associated_parallels_filled[category, original_rank] = path
        self._recache()
        return target

    ############################################################################
    # File grouping
    ############################################################################

    def group_children(self, basenames=None):
        """Return children as a list of PdsGroup objects."""

        if basenames is None:
            basenames = self.childnames

        # Group basenames by anchor
        anchor_dict = {}
        for basename in basenames:
            anchor = self.split_basename(basename)[0]
            if anchor not in anchor_dict:
                anchor_dict[anchor] = []

            anchor_dict[anchor].append(basename)

        # Sort basenames within each group; re-key by first basename
        basename_dict = {}
        for (anchor, basenames) in anchor_dict.items():
            sorted = self.sort_basenames(basenames, labels_after=True)
            basename_dict[sorted[0]] = sorted

        # Sort keys
        keys = basename_dict.keys()
        keys = self.sort_basenames(keys)

        # Return a list of lists of PdsGroup objects
        groups = []
        for key in keys:
            basenames = basename_dict[key]
            groups.append(PdsGroup(self.pdsfiles_for_basenames(basenames)))

        return groups

################################################################################
# File grouping class. An ordered set of PdsFiles, some of which may be hidden.
# They must share a common parent and anchor. In Viewmaster, they appear on the
# same row of a table, where a row is identified by alternation between gray
# and white.
################################################################################

class PdsGroup(object):

    def __init__(self, pdsfiles=[], parent=False, anchor=None, hidden=[]):

        self.parent_pdsf = parent   # False means un-initialized; None means a
                                    # virtual directory
        self.anchor = None
        self.rows = []
        self.hidden = set(hidden)

        self._isdir_filled = None
        self._iconset_filled = None
        self._viewset_filled = None
        self._local_viewset_filled = None

        if type(pdsfiles) in (list, tuple):
            for pdsf in pdsfiles:
                self.append(pdsf)
        else:
            self.append(pdsfiles)

    def __len__(self):
        return len(self.rows) - len(self.hidden)

    def copy(self):
        this = PdsGroup()
        this.parent_pdsf = self.parent_pdsf
        this.anchor = self.anchor
        this.rows = list(self.rows)
        this.hidden = self.hidden.copy()

        this._isdir_filled = self._isdir_filled
        this._iconset_filled = self._iconset_filled
        this._viewset_filled = self._viewset_filled
        this._local_viewset_filled = self._local_viewset_filled

        return this

    @property
    def parent_logical_path(self):
        if self.parent_pdsf:
            return self.parent_pdsf.logical_path
        else:
            return ''

    @property
    def isdir(self):
        if self._isdir_filled is None:
            self._isdir_filled = any([p.isdir for p in self.rows])

        return self._isdir_filled

    @property
    def _iconset(self):
        """Internal method to return the PdsViewSet of this object's icon
        whether it is to be displayed in a closed or open state."""

        if self._iconset_filled is None:
            self._iconset_filled = {}
            for open in (False, True):
                best_set = pdsviewable.ICON_SET_BY_TYPE[self.rows[0].icon_type,
                                                        open]
                for pdsf in self.rows[1:]:
                    test = pdsviewable.ICON_SET_BY_TYPE[pdsf.icon_type, open]
                    if test.priority > best_set.priority:
                        best_set = test

                self._iconset_filled[open] = best_set

        return self._iconset_filled[False]

    @property
    def iconset_closed(self):
        _ = self._iconset
        return self._iconset_filled[0]

    @property
    def iconset_open(self):
        _ = self._iconset
        return self._iconset_filled[1]

    @property
    def viewset(self):
        """The local PdsViewSet if it exists; otherwise, the first PdsViewSet.
        """

        if self._viewset_filled is None:

            if self.local_viewset:
                self._viewset_filled = self.local_viewset

            else:
                self._viewset_filled = []
                for pdsf in self.rows:
                    if pdsf.viewset:
                        self._viewset_filled = pdsf.viewset
                        break

        return self._viewset_filled

    @property
    def local_viewset(self):
        """The PdsViewSet of this object if it is viewable; False otherwise.
        """

        if self._local_viewset_filled is None:

            viewset = pdsviewable.PdsViewSet()
            for pdsf in self.rows:
                if pdsf.local_viewset:
                    viewset.append(pdsf.local_viewset)

            if len(viewset) == len(self):
                self._local_viewset_filled = viewset
            else:
                self._local_viewset_filled = False

        return self._local_viewset_filled

    @property
    def global_anchor(self):
        if self.parent_pdsf is False:
            raise ValueError('PdsGroup has not been initialized')

        if self.parent_pdsf is None:        # if a virtual dir
            return self.anchor
        else:
            return self.parent_pdsf.global_anchor + '-' + self.anchor

    def sort(self, labels_after=None, dirs_first=None, dirs_last=None,
                   info_first=None):

        basename_dict = {}
        for pdsf in self.rows:
            basename_dict[pdsf.basename] = pdsf

        if self.parent_pdsf:
            sorted = self.parent_pdsf.sort_basenames(basename_dict.keys(),
                                                labels_after=labels_after,
                                                dirs_first=dirs_first,
                                                dirs_last=dirs_last,
                                                info_first=info_first)
        else:
            sorted = list(basename_dict.keys())     # for virtual dirs
            sorted.sort()

        self.rows = [basename_dict[key] for key in sorted]

    def append(self, pdsf, hidden=False):

        # Initialize if necessary
        if self.parent_pdsf is False:
            self.parent_pdsf = pdsf.parent()
            self.rows = [pdsf]
            self.anchor = pdsf.anchor
            return

        # Same parent required
        if pdsf.parent_logical_path != self.parent_logical_path:
            raise ValueError('PdsFile does not match parent of PdsGroup: ' +
                             pdsf.parent_logical_path + ', ' +
                             self.parent_logical_path)

        # Same anchor required
        if pdsf.anchor != self.anchor:
            raise ValueError('PdsFile does not match anchor of PdsGroup: ' +
                             pdsf.anchor + ', ' + self.anchor)

        # Ignore duplicates
        for row in self.rows:
            if pdsf.logical_path == row.logical_path:
                return

        self.rows.append(pdsf)
        if hidden:
            self.hidden |= {pdsf.logical_path}

        self._isdir_filled = None
        self._iconset_filled = None
        self._viewset_filled = None
        self._local_viewset_filled = None

    def remove(self, pdsf):

        for k in range(len(self.rows)):
            logical_path = self.rows[k].logical_path
            if logical_path == pdsf.logical_path:
                del self.rows[k]
                self.hidden -= {logical_path}
                return True

        return False

    def hide(self, pdsf):

        for k in range(len(self.rows)):
            if self.rows[k].logical_path == pdsf.logical_path:
                if pdsf.logical_path not in self.hidden:
                    self.hidden |= {pdsf.logical_path}
                    return True

        return False

    def hide_all(self):
        paths = [f.logical_path for f in self.rows]
        self.hidden = set(paths)

    def unhide(self, pdsf):

        for k in range(len(self.rows)):
            if self.rows[k].logical_path == pdsf.logical_path:
                if pdf.logical_path in self.hidden:
                    self.hidden -= {pdsf.logical_path}
                    return True

        return False

    def unhide_all(self, pdsf):
        self.hidden = set()

    def iterator(self):
        return [r for r in self.rows if r.logical_path not in self.hidden]

    def iterator_for_all(self):
        return [r for r in self.rows]

    def iterator_for_hidden(self):
        return [r for r in self.rows if r.logical_path in self.hidden]

################################################################################
# PdsGroupTable class. An ordered set of PdsGroups sharing a common parent.
# Some may be hidden. These are grouped together within a single table in
# Viewmaster.
################################################################################

class PdsGroupTable(object):

    def __init__(self, pdsgroups=[], parent=False):

        self.parent_pdsf = parent   # False for un-initialized; None for virtual
        self.groups = []

        self._levels_filled = None

        for group in pdsgroups:
            self.insert_group(group)

    def copy(self):
        this = PdsGroupTable()
        this.parent_pdsf = self.parent_pdsf
        this.groups = [g.copy() for g in self.groups]
        this._levels_filled = self._levels_filled

        return this

    @property
    def parent_logical_path(self):
        if self.parent_pdsf:
            return self.parent_pdsf.logical_path
        else:
            return ''

    @property
    def levels(self):
        if self._levels_filled is None:
            levels = []
            pdsf = self.parent_pdsf
            while pdsf:
                levels.append(pdsf)
                pdsf = pdsf.parent()

            self._levels_filled = levels

        return self._levels_filled

    @property
    def levels_plus_one(self):
        return [self.groups[0].rows[0]] + self.levels

    def iterator(self):
        return [g for g in self.groups if len(g) > 0]

    def iterator_for_all(self):
        return [g for g in self.groups]

    def iterator_for_hidden(self):
        return [g for g in self.groups if len(g) == 0]

    def pdsfile_iterator(self):
        pdsfiles = []
        for group in self.groups:
            pdsfiles += group.iterator()

        return pdsfiles

    def pdsfile_iterator_for_all(self):
        pdsfiles = []
        for group in self.groups:
            pdsfiles += group.iterator_for_all()

        return pdsfiles

    def pdsfile_iterator_for_hidden(self):
        pdsfiles = []
        for group in self.groups:
            pdsfiles += group.iterator_for_hidden()

        return pdsfiles

    def __len__(self):
        return len(self.iterator())

    def insert_group(self, group, merge=True):

        if len(group.rows) == 0: return

        # Matching parent
        if self.parent_pdsf is False:
            self.parent_pdsf = group.parent_pdsf
        elif group.parent_logical_path != self.parent_logical_path:
            raise ValueError('PdsGroup parent does not match PdsGroupTable ' +
                             'parent')

        # Append to existing group if anchor matches
        if merge:
            for existing_group in self.groups:
                if existing_group.anchor == group.anchor:
                    for pdsf in group.rows:
                        hidden = (pdsf.logical_path in group.hidden)
                        existing_group.append(pdsf, hidden)

                    return

        # Otherwise, just append
        self.groups.append(group)

    def insert_file(self, pdsf, hidden=False):

        parent_pdsf = pdsf.parent()
        if self.parent_pdsf is False:
            self.parent_pdsf = parent_pdsf

        # Append to existing group if anchor matches
        for existing_group in self.groups:
            if existing_group.anchor == pdsf.anchor:
                existing_group.append(pdsf, hidden)
                return

        # Otherwise, append a new group
        if hidden:
            self.insert_group(PdsGroup([pdsf], hidden=[pdsf.logical_path]))
        else:
            self.insert_group(PdsGroup([pdsf]))

    def insert(self, things):

        if type(things) in (list,tuple):
            for thing in things:
                self.insert(thing)

            return

        thing = things

        if type(thing) == str:
            try:
                pdsf = PdsFile.from_logical_path(thing)
            except ValueError:
                pdsf = PdsFile.from_abspath(thing)

            self.insert_file(pdsf)

        elif isinstance(thing, PdsGroupTable):
            for group in thing.groups:
                self.insert_group(group)

        elif isinstance(thing, PdsGroup):
            self.insert_group(thing)

        elif isinstance(thing, PdsFile):
            self.insert_file(thing)

        else:
            raise TypeError('Unrecognized type for insert: ' +
                            type(thing).__name__)

    def sort_in_groups(self, labels_after=None, dirs_first=None, dirs_last=None,
                             info_first=None):

        for group in self.groups:
            group.sort(labels_after=labels_after,
                       dirs_first=dirs_first,
                       dirs_last=dirs_last,
                       info_first=info_first)

    def sort_groups(self, labels_after=None, dirs_first=None, dirs_last=None,
                          info_first=None):

        first_basenames = []
        group_dict = {}
        for group in self.groups:
            if group.rows:          # delete empty groups
                first_basename = group.rows[0].basename
                first_basenames.append(first_basename)
                group_dict[first_basename] = group

        if self.parent_pdsf:
            sorted_basenames = self.parent_pdsf.sort_basenames(first_basenames,
                                                      labels_after=labels_after,
                                                      dirs_first=dirs_first,
                                                      dirs_last=dirs_last,
                                                      info_first=info_first)
        else:
            sorted_basenames = list(first_basenames)
            sorted_basenames.sort()

        new_groups = [group_dict[k] for k in sorted_basenames]
        self.groups = new_groups

    def hide_pdsfile(self, pdsf):
        for group in self.groups:
            test = group.hide(pdsf)
            if test: return test

        return False

    def remove_pdsfile(self):
        for group in self.groups:
            test = group.remove(pdsf)
            if test: return test

        return False

    def filter(self, regex):
        for pdsf in self.pdsfile_iterator():
            if not regex.match(pdsf.basename):
                self.hide_pdsfile(pdsf)

    @staticmethod
    def sort_tables(tables):
        sort_paths = []
        table_dict = {}
        for table in tables:
            if table.parent_pdsf is None:
                sort_path = ''
            else:
                sort_path = table.parent_logical_path

            sort_paths.append(sort_path)
            table_dict[sort_path] = table

        sort_paths.sort()
        return [table_dict[k] for k in sort_paths]

    @staticmethod
    def tables_from_pdsfiles(pdsfiles, exclusions=set(), hidden=set(),
                                       labels_after=None, dirs_first=None,
                                       dirs_last=None, info_first=None):
        """Return a sorted list of PdsGroupTables accommodating the given list
        of PdsFiles."""

        table_dict = {}
        for pdsf in pdsfiles:
            if type(pdsf) == str:
                pdsf = PdsFile._from_absolute_or_logical_path(pdsf)

            if pdsf.logical_path in exclusions: continue
            if pdsf.abspath in exclusions: continue

            parent_pdsf = pdsf.parent()
            parent_path = pdsf.parent_logical_path

            if parent_path not in table_dict:
                table_dict[parent_path] = PdsGroupTable(parent=parent_pdsf)

            table = table_dict[parent_path]
            is_hidden = (pdsf.logical_path in hidden)
            table.insert_file(pdsf, is_hidden)

        # If an excluded file happens to fall in the same parent directory as
        # one of these, include it after all.
#         for exclusion in exclusions:
#             parent_path = '/'.join(exclusion.split('/')[:-1])
#             if parent_path in table_dict and \
#                 not PdsFile.from_logical_path(exclusion).isdir:
#
#                 table_dict[parent_path].insert_file(
#                                         PdsFile.from_logical_path(exclusion))

        tables = table_dict.values()
        for table in tables:
            table.sort_in_groups(labels_after=labels_after,
                                 dirs_first=dirs_first,
                                 dirs_last=dirs_last,
                                 info_first=info_first)

            table.sort_groups(labels_after=labels_after,
                              dirs_first=dirs_first,
                              dirs_last=dirs_last,
                              info_first=info_first)

        tables = PdsGroupTable.sort_tables(tables)
        return tables

    def remove_hidden(self):
        new_table = self.copy()

        new_groups = []
        for group in self.groups:
            new_rows = list(group.iterator())
            if new_rows:
                new_group = group.copy()
                new_group.rows = new_rows
                new_group.hidden = set()
                new_groups.append(new_group)

        new_table.groups = new_groups
        return new_table

################################################################################
# Initialize the global registry of subclasses
################################################################################

PdsFile.SUBCLASSES['default'] = PdsFile

################################################################################
# After the constructors are defined, always create and cache permanent,
# category-level virtual directories. These are roots of the cache tree and they
# are also virtual directories, meaning that their childen can be assembled from
# multiple physical directories.

# Note that this cache will be replaced by a call to preload(), so it will need
# to be initialized again.
################################################################################

for category in CATEGORIES:
    if category not in CACHE:
        CACHE.set(category, PdsFile.new_virtual(category), lifetime=0)

################################################################################
# Support functions
################################################################################

def _clean_join(a, b):
    return os.path.join(a,b).replace('\\', '/')

def repair_case(abspath):
    """Return a file's absolute path with capitalization exactly as it appears
    in the file system. Raises IOError if the file is not found.
    """

    trailing_slash = abspath.endswith('/')  # must preserve a trailing slash!
    abspath = os.path.abspath(abspath)
    if os.sep == '\\':
        abspath = abspath.replace('\\', '/')

    # Fields are separated by slashes
    parts = abspath.split('/')
    if parts[-1] == '':
        parts = parts[:-1]       # Remove trailing slash

    parts[0] = ''
    parts[1] = 'Volumes'   # In Mac OS, absolute paths start with '/Volumes'

    # For each subsequent field (between slashes)...
    for k in range(2, len(parts)):

        # Convert it to lower case for matching
        part_lower = parts[k].lower()

        # Construct the name of the parent directory and list its contents. This
        # will raise an IOError if the file does not exist or is not a
        # directory.
        basenames = os.listdir('/'.join(parts[:k]))

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
        f = open(abspath, 'r')

    return abspath

FILE_BYTE_UNITS = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

def formatted_file_size(size):
    order = int(math.log10(size) // 3) if size else 0
    return '{:.3g} {}'.format(size / 1000.**order, FILE_BYTE_UNITS[order])

def get_childnames(abspath):
    """A list of all the child names for a directory abspath. Invisible files
    are deleted and the list is sorted into alphabetical order."""

    basenames = os.listdir(abspath)
    basenames = [n for n in basenames if (n != '.DS_Store' and
                                          not n.startswith('._'))]
    basenames.sort()
    return basenames

def is_logical_path(path):
    """Quick test returns True if this appears to be a logical path; False
    otherwise."""

    return ('/holdings/' in path)

def logical_path_from_path(abspath):
    """Logical path derived from either a logical or an absolute path."""

    parts = abspath.partition('/holdings/')
    if parts[1]:
        return parts[2]
    else:
        return abspath

def selected_path_from_path(path, abspaths=True):
    """Logical path or absolute path derived from a logical or an absolute
    path."""

    if abspaths:
        if is_logical_path(path):
            raise ValueError('Unable to derive absolute path for ' + path)
        return path

    else:
        return logical_path_from_path(path)

################################################################################
# PdsFile subclass support. Only imported when needed.
################################################################################

def FROM_RULES_IMPORT_STAR():
#     from rules import *           # Illegal in Python (It's a long story.)

    import rules.ASTROM_xxxx
    import rules.COCIRS_xxxx
    import rules.COISS_xxxx
    import rules.CORSS_8xxx
    import rules.COUVIS_0xxx
    import rules.COUVIS_8xxx
    import rules.COVIMS_0xxx
    import rules.COVIMS_8xxx
    import rules.EBROCC_xxxx
    import rules.GO_0xxx
    import rules.HSTxx_xxxx
    import rules.NHSP_xxxx
    import rules.NHxxxx_xxxx
    import rules.RES_xxxx
    import rules.RPX_xxxx
    import rules.VG_0xxx
    import rules.VG_20xx
    import rules.VG_28xx
    import rules.VGIRIS_xxxx
    import rules.VGISS_xxxx

def reload_rules():
    reload(rules.ASTROM_xxxx)
    reload(rules.COCIRS_xxxx)
    reload(rules.COISS_xxxx)
    reload(rules.CORSS_8xxx)
    reload(rules.COUVIS_0xxx)
    reload(rules.COUVIS_8xxx)
    reload(rules.COVIMS_0xxx)
    reload(rules.COVIMS_8xxx)
    reload(rules.EBROCC_xxxx)
    reload(rules.GO_0xxx)
    reload(rules.HSTxx_xxxx)
    reload(rules.NHSP_xxxx)
    reload(rules.NHxxxx_xxxx)
    reload(rules.RES_xxxx)
    reload(rules.RPX_xxxx)
    reload(rules.VG_0xxx)
    reload(rules.VG_20xx)
    reload(rules.VG_28xx)
    reload(rules.VGIRIS_xxxx)
    reload(rules.VGISS_xxxx)

# from rules import *
FROM_RULES_IMPORT_STAR()

################################################################################
