################################################################################
# pds3file subpackage & Pds3File subclass with PdsFile as the parent class
################################################################################

from pdsfile_reorg import *
from .rules import pds3file_rules as pdsfile_rules

def cache_lifetime(arg):
    """Used by caches. Given any object, it returns the default lifetime in
    seconds. A returned lifetime of zero means keep forever.
    """

    # Keep Viewmaster HTML for 12 hours
    if isinstance(arg, str):
        return 12 * 60 * 60

    # Keep RANKS, VOLS, etc. forever
    elif not isinstance(arg, Pds3File):
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

# Initialize the cache
MEMCACHE_PORT = 0           # default is to use a DictionaryCache instead
DICTIONARY_CACHE_LIMIT = 200000
cfg.CACHE = pdscache.DictionaryCache(lifetime=cache_lifetime,
                                 limit=DICTIONARY_CACHE_LIMIT,
                                 logger=LOGGER)

DEFAULT_CACHING = 'dir'
PRELOAD_TRIES = 3

def preload(holdings_list, port=0, clear=False, force_reload=False,
            icon_color='blue'):
    """Cache the top-level directories, starting from the given holdings
    directories.

    Input:
        holdings_list       a single abslute path to a holdings directory, or
                            else a list of absolute paths.
        port                port to use for memcached; zero to prevent use of
                            memcached.
        clear               True to clear the cache before preloading.
        force_reload        Re-load the cache regardless of whether the cache
                            appears to contain the needed holdings.
        icon_color          color of the icons to load from each holdings
                            directory; default "blue".
    """

    global MEMCACHE_PORT, DEFAULT_CACHING, PRELOAD_TRIES

    # Convert holdings to a list of absolute paths
    if not isinstance(holdings_list, (list,tuple)):
        holdings_list = [holdings_list]

    holdings_list = [_clean_abspath(h) for h in holdings_list]

    # Use cache as requested
    if (port == 0 and MEMCACHE_PORT == 0) or not HAS_PYLIBMC:
        if not isinstance(cfg.CACHE, pdscache.DictionaryCache):
            cfg.CACHE = pdscache.DictionaryCache(lifetime=cache_lifetime,
                                             limit=DICTIONARY_CACHE_LIMIT,
                                             logger=LOGGER)
        LOGGER.info('Using local dictionary cache')

    else:
        MEMCACHE_PORT = MEMCACHE_PORT or port

        for k in range(PRELOAD_TRIES):
          try:
            cfg.CACHE = pdscache.MemcachedCache(MEMCACHE_PORT,
                                            lifetime=cache_lifetime,
                                            logger=LOGGER)
            LOGGER.info('Connecting to PdsFile Memcache [%s]' % MEMCACHE_PORT)
            break

          except pylibmc.Error:
            if k < PRELOAD_TRIES - 1:
                LOGGER.warn(('Failed to connect PdsFile Memcache [%s]; ' +
                             'trying again in %d sec') % (MEMCACHE_PORT, 2**k))
                time.sleep(2.**k)       # try then wait 1 sec, then 2 sec

            else:       # give up after three tries
                LOGGER.error(('Failed to connect PdsFile Memcache [%s]; '+
                              'using dictionary instead') %  MEMCACHE_PORT)

                MEMCACHE_PORT = 0
                if not isinstance(cfg.CACHE, pdscache.DictionaryCache):
                    cfg.CACHE = pdscache.DictionaryCache(lifetime=cache_lifetime,
                                                limit=DICTIONARY_CACHE_LIMIT,
                                                logger=LOGGER)

    # Define default caching based on whether MemCache is active
    if MEMCACHE_PORT == 0:
        DEFAULT_CACHING = 'dir'
    else:
        DEFAULT_CACHING = 'all'

    # This suppresses long absolute paths in the logs
    LOGGER.add_root(holdings_list)

    #### Get the current list of preloaded holdings directories and decide how
    #### to proceed

    if clear:
        cfg.CACHE.clear(block=True) # For a MemcachedCache, this will pause for any
                                # other thread's block, then clear, and retain
                                # the block until the preload is finished.
        cfg.LOCAL_PRELOADED = []
        LOGGER.info('Cache cleared')

    elif force_reload:
        cfg.LOCAL_PRELOADED = []
        LOGGER.info('Forcing a complete new preload')
        cfg.CACHE.wait_and_block()

    else:
        while True:
            cfg.LOCAL_PRELOADED = cfg.CACHE.get_now('$PRELOADED') or []

            # Report status
            something_is_missing = False
            for holdings in holdings_list:
                if holdings in cfg.LOCAL_PRELOADED:
                    LOGGER.info('Holdings are already cached', holdings)
                else:
                    something_is_missing = True

            if not something_is_missing:
                if MEMCACHE_PORT:
                    get_permanent_values(holdings_list, MEMCACHE_PORT)
                    # Note that if any permanently cached values are missing,
                    # this call will recursively clear the cache and preload
                    # again. This reduces the chance of a corrupted cache.

                return

            waited = cfg.CACHE.wait_and_block()
            if not waited:      # A wait suggests the answer might have changed,
                                # so try again.
                break

            cfg.CACHE.unblock()

    # At this point, the cache is blocked.

    # Pause the cache before proceeding--saves I/O
    cfg.CACHE.pause()       # Paused means no local changes will be flushed to the
                        # external cache until resume() is called.

    ############################################################################
    # Interior function to recursively preload one physical directory
    ############################################################################

    def _preload_dir(pdsdir):
        if not pdsdir.isdir: return

        # Log category directories as info
        if pdsdir.is_category_dir:
            LOGGER.info('Pre-loading: ' + pdsdir.abspath)

        # Log bundlesets as debug
        elif pdsdir.is_bundleset:
            LOGGER.debug('Pre-loading: ' + pdsdir.abspath)

        # Don't go deeper
        else:
            return

        # Preloaded dirs are permanent
        pdsdir.permanent = True

        # Make recursive calls and cache
        for basename in pdsdir.childnames:
            try:
                child = pdsdir.child(basename, fix_case=False, lifetime=0)
                _preload_dir(child)
            except ValueError:              # Skip out-of-place files
                pdsdir._childnames_filled.remove(basename)

    #### Fill CACHE

    try:    # we will undo the pause and block in the "finally" clause below

        # Create and cache permanent, category-level merged directories. These
        # are roots of the cache tree and their list of children is merged from
        # multiple physical directories. This makes it possible for our data
        # sets to exist on multiple physical drives in a way that is invisible
        # to the user.
        for category in CATEGORY_LIST:
            cfg.CACHE.set(category, Pds3File.new_merged_dir(category), lifetime=0)

        # Initialize RANKS, VOLS and category list
        for category in CATEGORY_LIST:
          category_ = category + '/'
          key = '$RANKS-' + category_
          try:
              _ = cfg.CACHE[key]
          except KeyError:
              cfg.CACHE.set(key, {}, lifetime=0)

          key = '$VOLS-'  + category_
          try:
              _ = cfg.CACHE[key]
          except KeyError:
              cfg.CACHE.set(key, {}, lifetime=0)

        # Cache all of the top-level PdsFile directories
        for h,holdings in enumerate(holdings_list):

            if holdings in cfg.LOCAL_PRELOADED:
                LOGGER.info('Pre-load not needed for ' + holdings)
                continue

            cfg.LOCAL_PRELOADED.append(holdings)
            LOGGER.info('Pre-loading ' + holdings)

            # Load volume info
            load_volume_info(holdings)

            # Load directories starting from here
            holdings_ = holdings.rstrip('/') + '/'

            for c in CATEGORY_LIST:
                category_abspath = holdings_ + c
                if not Pds3File.os_path_exists(category_abspath):
                    LOGGER.warn('Missing category dir: ' + category_abspath)
                    continue
                if not Pds3File.os_path_isdir(category_abspath):
                    LOGGER.warn('Not a directory, ignored: ' + category_abspath)

                # This is a physical PdsFile, but from_abspath also adds its
                # childnames to the list of children for the category-level
                # merged directory.
                pdsdir = Pds3File.from_abspath(category_abspath, fix_case=False,
                                              caching='all', lifetime=0)
                _preload_dir(pdsdir)

            # Load the icons
            icon_path = _clean_join(holdings, '_icons')
            if os.path.exists(icon_path):
                icon_url = '/holdings' + (str(h) if h > 0 else '') + '/_icons'
                pdsviewable.load_icons(icon_path, icon_url, icon_color, LOGGER)

    finally:
        cfg.CACHE.set('$PRELOADED', cfg.LOCAL_PRELOADED, lifetime=0)
        cfg.CACHE.resume()
        cfg.CACHE.unblock(flush=True)

    LOGGER.info('PdsFile preloading completed')

    # Determine if the file system is case-sensitive
    # If any physical bundle is case-insensitive, then we treat the whole file
    # system as case-insensitive.
    cfg.FS_IS_CASE_INSENSITIVE = False
    for holdings_dir in cfg.LOCAL_PRELOADED:
        testfile = holdings_dir.replace('/holdings', '/HoLdInGs')
        if os.path.exists(testfile):
            cfg.FS_IS_CASE_INSENSITIVE = True
            break

class Pds3File(PdsFile):
    # Override the rules
    DESCRIPTION_AND_ICON = pdsfile_rules.DESCRIPTION_AND_ICON
    ASSOCIATIONS = pdsfile_rules.ASSOCIATIONS
    VERSIONS = pdsfile_rules.VERSIONS
    INFO_FILE_BASENAMES = pdsfile_rules.INFO_FILE_BASENAMES
    NEIGHBORS = pdsfile_rules.NEIGHBORS
    SIBLINGS = pdsfile_rules.SIBLINGS       # just used by Viewmaster right now
    SORT_KEY = pdsfile_rules.SORT_KEY
    SPLIT_RULES = pdsfile_rules.SPLIT_RULES
    VIEW_OPTIONS = pdsfile_rules.VIEW_OPTIONS
    VIEWABLES = pdsfile_rules.VIEWABLES
    LID_AFTER_DSID = pdsfile_rules.LID_AFTER_DSID
    DATA_SET_ID = pdsfile_rules.DATA_SET_ID

    OPUS_TYPE = pdsfile_rules.OPUS_TYPE
    OPUS_FORMAT = pdsfile_rules.OPUS_FORMAT
    OPUS_PRODUCTS = pdsfile_rules.OPUS_PRODUCTS
    OPUS_ID = pdsfile_rules.OPUS_ID
    OPUS_ID_TO_PRIMARY_LOGICAL_PATH = pdsfile_rules.OPUS_ID_TO_PRIMARY_LOGICAL_PATH

    OPUS_ID_TO_SUBCLASS = pdsfile_rules.OPUS_ID_TO_SUBCLASS
    FILESPEC_TO_VOLSET = pdsfile_rules.FILESPEC_TO_VOLSET
    FILESPEC_TO_BUNDLESET = FILESPEC_TO_VOLSET

    BUNDLE_DIR_NAME = 'volumes'

    def __init__(self):
        super().__init__()
        # alias for attributes
        self.volset_  = self.bundleset_
        self.volset   = self.bundleset
        self.volname_ = self.bundlename_
        self.volname  = self.bundlename

    # Alias, compatible with old function/property names
    @property
    def is_volset(self):
        return self.is_bundleset

    @property
    def is_volset_file(self):
        return self.is_bundleset_file

    @property
    def is_volset_dir(self):
        return self.is_bundleset_dir

    @property
    def is_volume(self):
        return self.is_bundle

    @property
    def is_volume_file(self):
        return self.is_bundle_file

    @property
    def is_volume_dir(self):
        return self.is_bundle_dir

    def log_path_for_volset(self, suffix='', task='', dir='', place='default'):
        return self.log_path_for_bundleset(suffix, task, dir, place)

    def log_path_for_volume(self, suffix='', task='', dir='', place='default'):
        return self.log_path_for_bundle(suffix, task, dir, place)

    # Override functions
    def __repr__(self):
        if self.abspath is None:
            return 'Pds3File-logical("' + self.logical_path + '")'
        elif type(self) == Pds3File:
            return 'Pds3File("' + self.abspath + '")'
        else:
            return ('Pds3File.' + type(self).__name__ + '("' +
                    self.abspath + '")')



################################################################################
# Initialize the global registry of subclasses
################################################################################

Pds3File.SUBCLASSES['default'] = Pds3File

################################################################################
# This import must wait until after the PdsFile class has been fully initialized
################################################################################

try:
    # Data set-specific rules are implemented as subclasses of Pds3File
    # from pdsfile_reorg.pds3file.rules import *
    from pdsfile_reorg.pds3file.rules import (ASTROM_xxxx,
                                              COCIRS_xxxx,
                                              COISS_xxxx,
                                              CORSS_8xxx,
                                              COSP_xxxx,
                                              COUVIS_0xxx,
                                              COUVIS_8xxx,
                                              COVIMS_0xxx,
                                              COVIMS_8xxx,
                                              EBROCC_xxxx,
                                              GO_0xxx,
                                              HSTxx_xxxx,
                                              JNOJIR_xxxx,
                                              JNOJNC_xxxx,
                                              JNOSP_xxxx,
                                              NHSP_xxxx,
                                              NHxxxx_xxxx,
                                              RES_xxxx,
                                              RPX_xxxx,
                                              VG_0xxx,
                                              VG_20xx,
                                              VG_28xx,
                                              VGIRIS_xxxx,
                                              VGISS_xxxx)
except AttributeError:
    pass                    # This occurs when running pytests on individual
                            # rule subclasses, where pdsfile can be imported
                            # recursively.

################################################################################
# Support functions
################################################################################

def _clean_join(a, b):
#     joined = os.path.join(a,b).replace('\\', '/')
    if a:
        return a + '/' + b
    else:
        return b

def _clean_abspath(path):
    abspath = os.path.abspath(path)
    if os.sep == '\\':
        abspath = abspath.replace('\\', '/')
    return abspath
