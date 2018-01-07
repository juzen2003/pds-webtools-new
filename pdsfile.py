import os
import re
import datetime
import glob
import shelve
import gdbm
import math
import time
import random
import pylibmc

import pdscache
import pdsviewable
import pdsfile_rules        # Default rules
import rules                # Rules unique to each volume set
import translator

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

# DESC_AND_ICON_FIXES is used to revise information about top-level directories
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

  ('archives-volumes/',    'VOLUME'): (' (<b>tar.gz</b>)', 'TARBALL'),
  ('archives-volumes/',    'VOLDIR'): (' (<b>tar.gz</b>)', 'TARDIR' ),
  ('archives-calibrated/', 'VOLUME'): (' (<b>calibrated tar.gz</b>)','TARBALL'),
  ('archives-calibrated/', 'VOLDIR'): (' (<b>calibrated tar.gz</b>)','TARDIR' ),
  ('archives-metadata/',   'VOLUME'): (' (<b>metadata tar.gz</b>)',  'TARBALL'),
  ('archives-metadata/',   'VOLDIR'): (' (<b>metadata tar.gz</b>)',  'TARDIR' ),
  ('archives-previews/',   'VOLUME'): (' (<b>previews tar.gz</b>)',  'TARBALL'),
  ('archives-previews/',   'VOLDIR'): (' (<b>previews tar.gz</b>)',  'TARDIR' ),
  ('archives-diagrams/',   'VOLUME'): (' (<b>diagrams tar.gz</b>)',  'TARBALL'),
  ('archives-diagrams/',   'VOLDIR'): (' (<b>diagrams tar.gz</b>)',  'TARDIR' ),
}

################################################################################
# PdsLogger support
################################################################################

def set_logger(logger, debugging=False):

    global LOGGER, DEBUGGING

    LOGGER = logger
    DEBUGGING = debugging

################################################################################
# Global cache and memcached support
################################################################################

MEMCACHE_PORT = 0
PATHS = pdscache.DictionaryCache()
                    # Cache of PdsFile objects keyed by absolute path and by
                    # logical path (starting from category_). Keys are
                    # case-sensitive.

PATHS['$RANKS'] = {}# Dictionary keyed by [category_][volset or volname]
                    # returns a sorted list of ranks. Keys are lower case.

PATHS['$VOLS'] = {} # Dict keyed by [category_][volset or volname][rank]
                    # returns the PATHS key of the volset or name. Keys are
                    # lower case.

PATHS['$PRELOADED'] = []    # List of preloaded holdings abspaths

PATHS['$VOLUME_INFO'] = {}  # Returns (version, publication date,
                            # list of data set IDs) for volnames and volsets

DEFAULT_CACHING = 'none' # 'dir', 'all' or 'none'; use 'dir' for Viewmaster

LOGGER = None       # Optional logger
DEBUGGING = False   # True for extra-detailed debugging logs

# Initialize internal caches

def load_volume_info(volume_info_path):

    execfile(volume_info_path, globals())
    volume_info_dict = globals()['VOLUME_INFO']
    if LOGGER:
        LOGGER.info('Volume info loaded', volume_info_path)

    return volume_info_dict

def cache_lifetime(arg):
    if type(arg) == str:                    # HTML
        return 24 * 60 * 60
    elif not isinstance(arg, PdsFile):      # RANKS, VOLS, PRELOADED, etc.
        return 0
    elif arg.permanent:
        return 0
    elif arg.isdir:
        return 96 * 60 * 60
    else:
        return 12 * 60 * 60

def preload(holdings_list, volume_info_path, port=0, clear=False):
    """Cache the top-level directories, starting from the given holdings
    directory."""

    global PATHS, MEMCACHE_PORT, DEFAULT_CACHING

    # Convert holdings to a list of strings
    if type(holdings_list) == str:
        holdings_list = [holdings_list]

    blocking = False

    # Use cache as requested
    if port == 0 and MEMCACHE_PORT == 0:
        PATHS = pdscache.DictionaryCache(lifetime=cache_lifetime,
                                         limit=100000, logger=LOGGER)

        if LOGGER:
            LOGGER.info('Caching PdsFile objects in local dictionary')

    else:
        MEMCACHE_PORT = MEMCACHE_PORT or port
        try:
            PATHS = pdscache.MemcachedCache(MEMCACHE_PORT,
                                            lifetime=cache_lifetime,
                                            logger=LOGGER)

            if LOGGER:
                LOGGER.info('Connecting to PdsFile Memcache [%s]' %
                            MEMCACHE_PORT)

            # Clear if necessary
            if clear and not PATHS.is_blocked():
                PATHS.clear(block=True)
                blocking = True

        except pylibmc.Error as e:
            if LOGGER:
                LOGGER.error(('Failed to connect PdsFile Memcache [%s]; '+
                               'using dictionary instead') %
                              MEMCACHE_PORT)

            MEMCACHE_PORT = 0
            PATHS = pdscache.DictionaryCache(lifetime=cache_lifetime,
                                             limit=10000)

    ####################################
    # Recursive interior function
    ####################################

    def _preload_dir(pdsdir):
        if not pdsdir.isdir: return []

        if LOGGER and not pdsdir.volset:
            LOGGER.info('Caching', pdsdir.logical_path)

        pdsdir.permanent = True
        if pdsdir.logical_path.startswith('volumes/'):
            key = pdsdir.logical_path[8:]    # Skip over 'volumes/'
            try:
                (version, pubdate, dsids) = PATHS.get_local('$VOLUME_INFO')[key]
                pdsdir.volume_version_id_filled = ("%3.1f" % version)
                pdsdir.volume_publication_date_filled = pubdate
                pdsdir.volume_data_set_ids_filled = dsids
            except KeyError:
                if LOGGER:
                    LOGGER.warn('Volume info not found', pdsdir.logical_path)

        if pdsdir.volname: return       # don't go deeper than volume name

        basenames = list(pdsdir.childnames)     # copy in case of update
        for basename in basenames:
            try:
                child = pdsdir.child(basename, validate=False,
                                     caching='all', lifetime=0)
                _preload_dir(child)
            except ValueError:
                pdsdir.childnames.remove(basename)  # Ignore out-of-place files

    ####################################
    # Begin active code
    ####################################

    try:
        preloaded = PATHS.get('$PRELOADED')

        already_loaded = True
        for holdings in holdings_list:
            if holdings not in preloaded:
                already_loaded = False

        if already_loaded:
            if LOGGER:
                LOGGER.info('Holdings are already cached')
            return

    except (KeyError, TypeError):
        preloaded = []

    if not blocking:
        PATHS.block()

    PATHS.pause()
    PATHS.set_local('$VOLUME_INFO', load_volume_info(volume_info_path),
                                    lifetime=0)

    if MEMCACHE_PORT:
        DEFAULT_CACHING = 'all'

    # Intiailize RANKS, VOLS and category list
    ranks = {}
    vols = {}
    categories = []
    for checksums_ in ('', 'checksums-'):
        for archives_ in ('', 'archives-'):
            for voltype in VOLTYPES:
                category = checksums_ + archives_ + voltype
                category_ = category + '/'
                ranks[category_] = {}
                vols[category_] = {}
                categories.append(category)

    PATHS.set_local('$RANKS', ranks, lifetime=0)
    PATHS.set_local('$VOLS', vols, lifetime=0)

    # Prepare dictionary of top-level PdsFiles
    try:
        for holdings in holdings_list:
            if holdings in preloaded:
                continue

            holdings = os.path.abspath(holdings)
            if LOGGER: LOGGER.info('Pre-loading ' + holdings)

            pds_holdings = PdsFile.from_abspath(holdings, caching='none')

            for c in categories:        # Order counts!
                if c not in pds_holdings.childnames: continue
                pdsdir = pds_holdings.child(c, validate=False,
                                               caching='all', lifetime=0)
                _preload_dir(pdsdir)

    finally:
        PATHS.set_local('$PRELOADED', holdings_list, lifetime=0)
        PATHS.unblock(flush=True)
        PATHS.resume()

def pause_caching():
    global PATHS
    PATHS.pause()

def resume_caching():
    global PATHS
    PATHS.resume()

def clear_cache():
    global PATHS
    PATHS.clear()

################################################################################
# PdsFile class
################################################################################

class PdsFile(object):

    # Global registry of subclasses
    SUBCLASSES = {}

    # Translator from volume set ID to key in global registry
    VOLSET_TRANSLATOR = translator.TranslatorByRegex([('.*', 0, 'default')])

    # Default translators, can be overridden
    DESCRIPTION_AND_ICON = pdsfile_rules.DESCRIPTION_AND_ICON
    VOLUMES_TO_ASSOCIATIONS = pdsfile_rules.VOLUMES_TO_ASSOCIATIONS
    ASSOCIATIONS_TO_VOLUMES = pdsfile_rules.ASSOCIATIONS_TO_VOLUMES
    INFO_FILE_BASENAMES = pdsfile_rules.INFO_FILE_BASENAMES
    NEIGHBORS = pdsfile_rules.NEIGHBORS
    SORT_KEY = pdsfile_rules.SORT_KEY
    SPLIT_RULES = pdsfile_rules.SPLIT_RULES
    VIEW_OPTIONS = pdsfile_rules.VIEW_OPTIONS
    VIEWABLES = pdsfile_rules.VIEWABLES

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
        self.html_root_   = ''      # '/holdings/', '/holdings2/', etc.

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

        self.permanent    = False
        self.is_virtual   = False
        self.is_local     = False

        self.exists_filled          = None
        self.islabel_filled         = None
        self.isdir_filled           = None
        self.split_filled           = None
        self.global_anchor_filled   = None
        self.childnames_filled      = None
        self.info_filled            = None
        self.date_filled            = None
        self.formatted_size_filled  = None
        self.is_viewable_filled     = None
        self.info_basename_filled   = None
        self.label_basename_filled  = None
        self.viewset_filled         = None
        self.local_viewset_filled   = None
        self.iconset_filled         = None
        self.internal_links_filled  = None
        self.mime_type_filled       = None
        self.view_options_filled    = None
        self.description_and_icon_filled    = None
        self.volume_publication_date_filled = None
        self.volume_version_id_filled       = None
        self.volume_data_set_ids_filled     = None
        self.version_ranks_filled           = None
        self.exact_archive_url_filled       = None
        self.exact_checksum_url_filled      = None
        self.associated_parallels_filled    = None

    def make_virtual(self):
        self.abspath      = None
        self.disk_        = None
        self.root_        = None
        self.html_root_   = None

        self.permanent    = True
        self.is_virtual   = True

        self.exists_filled          = True
        self.islabel_filled         = False
        self.isdir_filled           = True
        self.split_filled           = (self.basename, '', '')
        self.global_anchor_filled   = self.basename
        # self.childnames_filled      = None
        self.info_filled            = [0, 0, 0, '', (0,0)]
        self.date_filled            = ''
        self.formatted_size_filled  = ''
        self.is_viewable_filled     = False
        self.info_basename_filled   = ''
        self.label_basename_filled  = ''
        self.viewset_filled         = False
        self.local_viewset_filled   = False
        self.iconset_filled         = None
        self.internal_links_filled  = []
        self.mime_type_filled       = ''
        self.view_options_filled    = (False, False, False)
        self.description_and_icon_filled    = None
        self.volume_publication_date_filled = ''
        self.volume_version_id_filled       = ''
        self.volume_data_set_ids_filled     = ''
        self.version_ranks_filled           = []
        self.exact_archive_url_filled       = ''
        self.exact_checksum_url_filled      = ''
        # self.associated_parallels_filled    = None

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
        for (key, value) in source.__dict__.iteritems():
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

        for (key, value) in self.__dict__.iteritems():
            this.__dict__[key] = value

        return this

    ############################################################################
    # Properties
    ############################################################################

    @property
    def exists(self):
        if self.exists_filled is not None:
            return self.exists_filled

        if self.is_virtual:
            self.exists_filled = True
        elif self.abspath is None:
            self.exists_filled = False
        else:
            self.exists_filled = os.path.exists(self.abspath)

        self.recache()
        return self.exists_filled

    @property
    def isdir(self):
        if self.isdir_filled is not None:
            return self.isdir_filled

        if self.is_virtual:
            self.isdir_filled = True
        elif self.abspath is None:
            self.isdir_filled = False
        else:
            self.isdir_filled = os.path.isdir(self.abspath)

        self.recache()
        return self.isdir_filled

    @property
    def islabel(self):
        if self.islabel_filled is not None:
            return self.islabel_filled

        self.islabel_filled = self.basename_is_label(self.basename)

        self.recache()
        return self.islabel_filled

    @property
    def is_viewable(self):
        if self.is_viewable_filled is not None:
            return self.is_viewable_filled

        self.is_viewable_filled = self.basename_is_viewable(self.basename)

        self.recache()
        return self.is_viewable_filled

    @property
    def html_path(self):
        return self.html_root_ + self.logical_path

    @property
    def split(self):
        """(anchor, suffix, extension)"""

        if self.split_filled is not None:
            return self.split_filled

        self.split_filled = self.split_basename()

        self.recache()
        return self.split_filled

    @property
    def anchor(self):
        return self.split[0]

    @property
    def global_anchor(self):
        if self.global_anchor_filled is not None:
            return self.global_anchor_filled

        path = self.parent_logical_path + '/' + self.anchor
        self.global_anchor_filled = path.replace('/', '-')

        self.recache()
        return self.global_anchor_filled

    @property
    def extension(self):
        return self.split[2]

    @property
    def childnames(self):
        if self.childnames_filled is not None:
            return self.childnames_filled

        self.childnames_filled = []
        if self.isdir and self.abspath:
            basenames = os.listdir(self.abspath)
            basenames = [n for n in basenames if (n != '.DS_Store' and
                                                  not n.startswith('._'))]
            self.childnames_filled = basenames

        self.recache()
        return self.childnames_filled

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
    def info(self):
        if self.info_filled is not None:
            return self.info_filled

        if not self.exists or self.checksums_:
            self.info_filled = (0, 0, None, '', (0,0))

        else:
            try:
                (bytes, child_count,
                 timestring, checksum, size) = self.shelf_lookup('info')

                yr = int(timestring[ 0:4])
                mo = int(timestring[ 5:7])
                da = int(timestring[ 8:10])
                hr = int(timestring[11:13])
                mi = int(timestring[14:16])
                sc = int(timestring[17:19])
                ms = int(timestring[20:])

                modtime = datetime.datetime(yr, mo, da, hr, mi, sc, ms)
                self.info_filled = (bytes, child_count, modtime, checksum, size)

            except (IOError, KeyError, ValueError) as e:
                self.info_filled = (0, 0, None, '', (0,0))

                if not self.archives_ and not self.volname:
                    child_count = len(self.childnames)

                    latest_modtime = datetime.datetime.min
                    total_bytes = 0
                    for volname in self.childnames:

                        (bytes, _, timestring,
                         _, _) = self.shelf_lookup('info', volname)

                        if timestring == '' or bytes == 0: continue
                            # Some preview dirs contain no files. Without this
                            # line it causes an error.

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

                    if latest_modtime == datetime.datetime.min:
                        latest_modtime = None

                    self.info_filled = (total_bytes, child_count,
                                        latest_modtime, '', (0,0))

        if self.modtime:
            self.date_filled = self.modtime.strftime('%Y-%m-%d %H:%M:%S')
        else:
            self.date_filled = ''

        if self.size_bytes:
            self.formatted_size_filled = formatted_file_size(self.size_bytes)
        else:
            self.formatted_size_filled = ''

        self.recache()
        return self.info_filled

    @property
    def size_bytes(self):
        return self.info[0]

    @property
    def modtime(self):
        return self.info[2]

    @property
    def checksum(self):
        return self.info[3]

    @property
    def url(self):
        return self.html_root_ + self.logical_path

    @property
    def width(self):
        return self.info[4][0]

    @property
    def height(self):
        return self.info[4][1]

    @property
    def alt(self):
        return self.basename

    @property
    def date(self):
        if self.date_filled is not None:
            return self.date_filled

        _ = self.info

        self.recache()
        return self.date_filled

    @property
    def formatted_size(self):
        if self.info is not None:
            return self.formatted_size_filled

        _ = self.info

        self.recache()
        return self.formatted_size_filled

    @property
    def description(self):
        if self.description_and_icon_filled is not None:
            return self.description_and_icon_filled[0]

        pair = self.DESCRIPTION_AND_ICON.first(self.logical_path)
        self.description_and_icon_filled = pair

        # Add annotation based on volume type
        if pair and self.volset and not self.interior:
          if self.category_ == 'calibrated/':
            self.description_and_icon_filled = ('Calibrated ' + pair[0],
                                                pair[1])
          elif self.category_ == 'diagrams/':
            self.description_and_icon_filled = ('Diagrams for ' + pair[0],
                                                'GEOMDIR')
          elif self.category_ == 'previews/':
            self.description_and_icon_filled = ('Previews of ' + pair[0],
                                                'BROWDIR')
          elif self.category_ == 'metadata/' and 'metadata' not in pair[0]:
            self.description_and_icon_filled = ('Metadata for ' + pair[0],
                                                'INDEXDIR')

        if not self.description_and_icon_filled:
            self.description_and_icon_filled = ['Unavailable', 'UNKNOWN']

        # Highlight top-level directories
        key = (self.category_, self.description_and_icon_filled[1])
        if key in DESC_AND_ICON_FIXES:
            (suffix, new_icon_type) = DESC_AND_ICON_FIXES[key]
            new_desc = self.description_and_icon_filled[0] # + suffix
            self.description_and_icon_filled = [new_desc, new_icon_type]

        self.recache()
        return self.description_and_icon_filled[0]

    @property
    def icon_type(self):
        _ = self.description
        return self.description_and_icon_filled[1]

    @property
    def mime_type(self):
        """A best guess at the MIME type for this file. Blank for not
        displayable in a browser."""

        if self.mime_type_filled is not None:
            return self.mime_type_filled

        ext = self.extension[1:].lower()

        if self.isdir:
            self.mime_type_filled = ''
        elif ext in PLAIN_TEXT_EXTS:
            self.mime_type_filled = 'text/plain'
        elif ext in MIME_TYPES_VS_EXT:
            self.mime_type_filled = MIME_TYPES_VS_EXT[ext]
        else:
            self.mime_type_filled = ''

        self.recache()
        return self.mime_type_filled

    @property
    def info_basename(self):
        if self.info_basename_filled is not None:
            return self.info_basename_filled

        self.info_basename_filled = \
            self.INFO_FILE_BASENAMES.first(self.childnames)

        if self.info_basename_filled is None:
            self.info_basename_filled = ''

        self.recache()
        return self.info_basename_filled

    @property
    def internal_link_info(self):
        """Returns a list of tuples [(recno, basename, abspath), ...], or else
        the abspath of the label for this file."""

        if self.internal_links_filled is not None:
            return self.internal_links_filled

        if self.isdir or self.checksums_ or self.archives_:
            self.internal_links_filled = []
        elif self.voltype_ not in ('volumes/', 'calibrated/', 'metadata/'):
            self.internal_links_filled = []
        else:
            volume_path_ = self.volume_abspath() + '/'
            try:
                values = self.shelf_lookup('links')

                if type(values) == str:
                    if values:
                        self.internal_links_filled = volume_path_ + values
                    else:
                        self.internal_links_filled = []
                else:
                    new_list = []
                    for (recno, basename, internal_path) in values:
                        abspath = volume_path_ + internal_path
                        new_list.append((recno, basename, abspath))
                    self.internal_links_filled = new_list

            except IOError:
                self.internal_links_filled = ()     # tuple instead of list

        self.recache()
        return self.internal_links_filled

    @property
    def linked_abspaths(self):
        """Returns a list of absolute paths to linked files."""

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
        if self.label_basename_filled is not None:
            return self.label_basename_filled

        _ = self.internal_link_info

        if type(self.internal_links_filled) == str:
            label_path = self.internal_links_filled
            if label_path:
                self.label_basename_filled = os.path.basename(label_path)

        elif type(self.internal_links_filled) == list:
            self.label_basename_filled = ''

        # otherwise, tuple means not found
        elif self.is_label:
            self.label_basename_filled = ''

        else:
            ext = self.extension.lower()
            if ext in ('.lbl', '.txt', '.cat', 'tar.gz'):
                self.label_basename_filled = ''
            elif self.extension.islower():
                self.label_basename_filled = self.basename[:-len(ext)] + '.lbl'
            else:
                self.label_basename_filled = self.basename[:-len(ext)] + '.LBL'

        self.recache()
        return self.label_basename_filled

    @property
    def viewset(self):
        if self.viewset_filled is not None:
            return self.viewset_filled

        # Don't look for viewsets at volume root; saves time
        if (self.exists and self.volname_ and
            not self.archives_ and not self.checksums_ and
            self.interior and ('/' in self.interior)):
                self.viewset_filled = self.viewset_lookup('default')

        if self.viewset_filled is None:
            self.viewset_filled = False

        self.recache()
        return self.viewset_filled

    @property
    def local_viewset(self):
        if self.local_viewset_filled is not None:
            return self.local_viewset_filled

        if self.exists and self.basename_is_viewable():
            self.local_viewset_filled = \
                            pdsviewable.PdsViewSet.from_pdsfiles(self)
        else:
            self.local_viewset_filled = False

        self.recache()
        return self.local_viewset_filled

    @property
    def iconset(self):
        if self.iconset_filled is not None:
            return self.iconset_filled[0]

        self.iconset_filled = [pdsviewable.ICON_SET_BY_TYPE[self.icon_type,
                                                            False],
                               pdsviewable.ICON_SET_BY_TYPE[self.icon_type,
                                                            True]]

        self.recache()
        return self.iconset_filled[0]

    @property
    def iconset_open(self):
        _ = self.iconset
        return self.iconset_filled[1]

    @property
    def iconset_closed(self):
        _ = self.iconset
        return self.iconset_filled[0]

    @property
    def volume_publication_date(self):

        if self.volume_publication_date_filled is not None:
            return self.volume_publication_date_filled

        self.volume_publication_date_filled = ''
        if self.exists and self.volset:
            if self.volname:
                key = self.category_ + self.volset_ + self.volname
            else:
                key = self.category_ + self.volset_[:-1]

            try:
                pdsf = PATHS[key]
                if pdsf.volume_publication_date_filled:
                    self.volume_publication_date_filled = \
                                    pdsf.volume_publication_date_filled
            except KeyError:
                self.volume_publication_date_filled = self.date[:10]

        self.recache()
        return self.volume_publication_date_filled

    @property
    def volume_version_id(self):
        if self.volume_version_id_filled is not None:
            return self.volume_version_id_filled

        self.volume_version_id_filled = ''
        if self.exists and self.volset:

            if self.volname:
                key = self.category_ + self.volset_ + self.volname
            else:
                key = self.category_ + self.volset_[:-1]
    
            try:
                pdsf = PATHS[key]
                if pdsf.volume_version_id_filled:
                    self.volume_version_id_filled = \
                                            pdsf.volume_version_id_filled
            except KeyError:
                _ = self.version_info(self.suffix)

                # Use the version ID from the volset
                if self.version_id:
                    self.volume_version_id_filled = self.version_id
                    return self.volume_version_id_filled

                # Increment the version ID of the previous volset
                if len(self.version_ranks) > 1 and \
                        self.version_ranks[-1] == 999999:
                    prev_rank = self.version_ranks[-2]
                    if prev_rank > 900000:
                        return self.volume_version_id_filled

                    part0 = prev_rank // 10000
                    prev_rank -= 10000 * part0
                    part1 = prev_rank // 100 + 1
                    self.volume_version_id_filled = str(part0) + '.' + \
                                                    str(part1)

        self.recache()
        return self.volume_version_id_filled

    @property
    def volume_data_set_ids(self):
        if self.volume_data_set_ids_filled is not None:
            return self.volume_data_set_ids_filled

        self.volume_data_set_ids_filled = ''
        if self.exists:
            if self.volset:
                if self.volname:
                    key = self.category_ + self.volset_ + self.volname
                else:
                    key = self.category_ + self.volset_[:-1]

                try:
                    pdsf = PATHS[key]
                    if pdsf.volume_data_set_ids_filled:
                        self.volume_data_set_ids_filled = \
                                        pdsf.volume_data_set_ids_filled
                except KeyError:
                    pass

        self.recache()
        return self.volume_data_set_ids_filled

    @property
    def version_ranks(self):
        if self.version_ranks_filled is not None:
            return self.version_ranks_filled

        if not self.exists:
            version_ranks_filled = []

        else:
            try:
                ranks = PATHS['$RANKS']
                if self.volname:
                    key = self.volname.lower()
                    self.version_ranks_filled = ranks[self.category_][key]
                elif self.volset:
                    key = self.volset.lower()
                    self.version_ranks_filled = ranks[self.category_][key]
                else:
                    self.version_ranks_filled = []

            except KeyError as e:
                if LOGGER:
                    LOGGER.warn('Missing rank info', self.logical_path)
                self.version_ranks_filled = []

        self.recache()
        return self.version_ranks_filled

    @property
    def exact_archive_url(self):
        if self.exact_archive_url_filled is not None:
            return self.exact_archive_url_filled

        if not self.exists:
            self.exact_archive_url_filled = ''

        else:
            abspath = self.archive_path_if_exact()
            if abspath:
                pdsf = PdsFile.from_abspath(abspath)
                self.exact_archive_url_filled = pdsf.url
            else:
                self.exact_archive_url_filled = ''

        self.recache()
        return self.exact_archive_url_filled

    @property
    def exact_checksum_url(self):
        if self.exact_checksum_url_filled is not None:
            return self.exact_checksum_url_filled

        if not self.exists:
            self.exact_checksum_url_filled = ''

        else:
            abspath = self.checksum_path_if_exact()
            if abspath:
                pdsf = PdsFile.from_abspath(abspath)
                self.exact_checksum_url_filled = pdsf.url
            else:
                self.exact_checksum_url_filled = ''

        self.recache()
        return self.exact_checksum_url_filled

    @property
    def grid_view_allowed(self):
        if self.view_options_filled is not None:
            return self.view_options_filled[0]

        if not self.exists:
            self.view_options_filled = (False, False, False)

        elif self.isdir:
            self.view_options_filled = \
                                self.VIEW_OPTIONS.first(self.logical_path)
        else:
            self.view_options_filled = (False, False, False)

        self.recache()
        return self.view_options_filled[0]

    @property
    def multipage_view_allowed(self):
        _ = self.grid_view_allowed

        return self.view_options_filled[1]

    @property
    def continuous_view_allowed(self):
        _ = self.grid_view_allowed

        return self.view_options_filled[2]

    @property
    def has_neighbor_rule(self):
        if self.NEIGHBORS.first(self.parent().logical_path):
            return True
        else:
            return False

    LATEST_VERSION_RANKS = [990100, 990200, 990300, 990400, 999999]

    @staticmethod
    def version_info(suffix):
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
        if not self.exists: return None

        # If this is a directory, return the viewset of the first child
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

        # If this is viewable, return the viewset of its viewable siblings with
        # the same anchor
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

            viewables = PdsFile.pdsfiles_for_abspaths(abspaths, exists=True)
            return pdsviewable.PdsViewSet.from_pdsfiles(viewables)

        # We are out of options
        return pdsviewable.PdsViewSet([])

    ############################################################################
    # Support for alternative constructors
    ############################################################################

    def _complete(self, exists=False, caching='default', lifetime=None):
        """General procedure to maintain the PATHS cache. It returns PdsFiles or
        subclasses from the cache if available; otherwise it caches PdsFiles if
        appropriate.

        If the file exists, then the capitalization must be correct!
        """

        global PATHS

        # Confirm existence
        if exists and not self.exists:
            raise IOError('File not found', self.abspath)

        # Never cache local paths
        if self.is_local: return self

        if self.basename.strip() == '':     # Shouldn't happen, but just in case
            return self.parent()

        if LOGGER and DEBUGGING:
            LOGGER.debug('Completing', self.logical_path)

        # Check cache first
        if self.abspath is not None:
            try:
                return PATHS[self.abspath]
            except KeyError:
                pass

        if self.logical_path is not None:
            try:
                return PATHS[self.logical_path]
            except KeyError:
                pass

        # Do not cache nonexistent objects
        if not self.exists: return self

        # Do not cache above the category level
        if not self.category_: return self

        # Cache if necessary
        if caching == 'default':
            caching = DEFAULT_CACHING

        if caching == 'all' or (caching == 'dir' and self.isdir):

            PATHS.pause()
            try:
                # Merge contents of the virtual directories; do not cache self
                if not self.volset:
                    try:
                        pdsf = PATHS[self.logical_path].copy()
                        merged = list(set(pdsf.childnames + self.childnames))
                        pdsf.childnames_filled = merged
                        PATHS.set(self.logical_path, pdsf, lifetime=0)
                    except KeyError:
                        pdsf = self.copy()
                        pdsf.make_virtual()
                        pdsf.childnames_filled = self.childnames
                        PATHS.set(self.logical_path, pdsf, lifetime=0)

                # Otherwise, cache by absolute and logical paths
                else:
                    _ = self.exists
                    _ = self.isdir

                    PATHS.set(self.abspath, self, lifetime=lifetime)
                    PATHS.set(self.logical_path, self, lifetime=lifetime)

                self._update_ranks_and_vols()

            finally:
                PATHS.resume()

        return self

    def _update_ranks_and_vols(self):
        """Maintains the RANKS and VOLS dictionaries. Must be called for all
        PdsFile objects down to the volume name level."""

        # RANKS is keyed by [category_][volume set or name] and returns a sorted
        # list of ranks.

        # VOLS is keyed by [category_][volume set or name][rank] and returns a 
        # volset or volname PdsFile.

        if self.volset and not self.volname:
            key = self.volset.lower()
        elif self.volname and not self.volname_:
            key = self.volname.lower()
        elif self.volname_ and not self.interior:
            key = self.volname.lower()
        else:
            return

        self.permanent = True       # VOLS entries are permanent!

        RANKS = PATHS['$RANKS']
        VOLS  = PATHS['$VOLS']
        rank_dict = RANKS[self.category_]
        vols_dict = VOLS[self.category_]

        changed = False
        if key not in rank_dict:
            rank_dict[key] = []
            vols_dict[key] = {}
            changed = True

        ranks = rank_dict[key]
        if self.version_rank not in ranks:
            ranks.append(self.version_rank)
            ranks.sort()
            changed = True

        if changed:
            vols_dict[key][self.version_rank] = self.abspath
            PATHS['$RANKS'] = RANKS
            PATHS['$VOLS'] = VOLS

    def recache(self):
        if self.abspath and (self.abspath in PATHS):
            PATHS.set(self.abspath, self)
        if self.logical_path in PATHS:
            PATHS.set(self.logical_path, self)

    ############################################################################
    # Alternative constructors
    ############################################################################

    def child(self, basename, validate=True, exists=False,
                    caching='default', lifetime=None, root_=None):
        """Constructor for a PdsFile of the proper subclass in this directory.

        Optional parameter root_ is needed to override the missing absolute
        path for children of virtual directories.
        """

        # Fix the case if possible and if validation is on
        if validate and self.abspath and self.exists:
            basename_lc = basename.lower()
            for name in self.childnames:
                if basename_lc == name.lower():
                    return self.child(name, validate=False, exists=exists,
                                            caching=caching, lifetime=lifetime)

        # Look up by absolute path
        if self.abspath:
            child_abspath = os.path.join(self.abspath, basename)
        elif root_:
            child_abspath = os.path.join(root_ + self.logical_path, basename)
        else:
            child_abspath = None

        if child_abspath:
            try:
                return PATHS[child_abspath]
            except KeyError:
                pass

        # Look up by logical path
        child_logical_path = os.path.join(self.logical_path, basename)
        child_logical_path.rstrip('/')    # could happen at root level
        try:
            child_pdsf = PATHS[child_logical_path]
            if child_pdsf.abspath:
                return child_pdsf
        except KeyError:
            pass

        # Construct child from parent; modify as needed...
        if self.volset:
            class_key = self.volset
        elif self.category_:
            matchobj = VOLSET_PLUS_REGEX_I.match(basename) # used again
            if matchobj is None:
                raise ValueError('Illegal volume set directory "%s": %s' %
                                 (basename, self.logical_path))
            class_key = matchobj.group(1)
        else:
            class_key = 'default'

        this = self.new_pdsfile(key=class_key, copypath=True)

        this.abspath = child_abspath
        if child_abspath and not self.abspath:
            this.root_ = root_

        this.logical_path = child_logical_path
        this.basename = basename

        if this.interior:
            this.interior = os.path.join(this.interior, basename)
            return this._complete(exists, caching, lifetime)

        if this.volname_:
            this.interior = basename
            return this._complete(exists, caching, lifetime)

        if this.volset_:

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

            return this._complete(exists, caching, lifetime)

        if this.category_:

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

            return this._complete(exists, caching, lifetime)

        if not this.category_:

            # Handle voltype and category
            this.category_ = basename + '/'
            matchobj = CATEGORY_REGEX_I.match(basename)
            if matchobj is None:
                raise ValueError('Invalid category "%s": %s' %
                                 (basename, this.logical_path))

            if validate:
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

            return this._complete(exists, caching, lifetime)

        raise ValueError('Cannot define child from PDS root: ' +
                         this.logical_path)

    def parent(self, exists=False, caching='default', lifetime=None):
        """Constructor for the parent of this file."""

        if self.abspath is None:    # virtual pdsdir
            return None

        abspath = os.path.split(self.abspath)[0]
        try:
            return PATHS[abspath]
        except KeyError:
            pass

        logical_path = os.path.split(self.logical_path)[0]
        try:
            return PATHS[logical_path]
        except KeyError:
            pass

        if self.volname:
            this = self.new_pdsfile(copypath=True)
        else:
            this = PdsFile()

        this.abspath = abspath
        this.logical_path = logical_path

        this.basename = os.path.basename(this.abspath)

        if this.interior and this.volname_:
            this.interior = os.path.split(this.interior)[0]
            return this._complete(exists, caching, lifetime)

        if this.volname:
            this.volname_ = ''
            this.volname  = ''
            this.interior = ''
            return this._complete(exists, caching, lifetime)

        if this.volset:
            this.volset_  = ''
            this.volset   = ''
            this.suffix   = ''
            this.volname_ = ''
            this.volname  = ''
            this.interior = ''
            this.version_message = ''
            this.version_rank = ''
            return this._complete(exists, caching, lifetime)

        if this.category_:
            this.category_  = ''
            this.voltype_   = ''
            this.archives_  = ''
            this.checksums_ = ''
            return this._complete(exists, caching, lifetime)

        return None

    def from_relative_path(self, path, validate=False, exists=False,
                                       caching='default', lifetime=None):

        path = path.rstrip('/')
        parts = path.split('/')

        if len(parts) == 0:
            return self._complete(exists, caching, lifetime)

        this = self
        for part in parts:
            this = this.child(part, validate=validate, exists=exists,
                                    caching=caching, lifetime=lifetime)

        return this

    @staticmethod
    def from_logical_path(path, validate=False, exists=exists,
                                caching='default', lifetime=None):
        """Constructor from a logical path."""

        if path is None: return None

        path = path.rstrip('/')

        try:
            return PATHS[path]
        except KeyError:
            pass

        parts = path.split('/')
        ancestor = None
        for lparts in range(len(parts)-1, 0, -1):
            ancestor_path = '/'.join(parts[:lparts])

            try:
                ancestor = PATHS[ancestor_path]
                break
            except KeyError:
                pass

            # For validation, experiment with case
            for key in [ancestor_path.lower(), ancestor_path.upper(),
                        ancestor_path.capitalize()]:
                try:
                    ancestor = PATHS[key]
                    break
                except KeyError:
                    pass

        # Handle the rest of the tree using child()
        if ancestor is None:
            raise IOError('File not found: ' + path)

        this = ancestor
        for part in parts[lparts:]:
            this = this.child(part, validate=validate, exists=exists,
                                    caching=caching, lifetime=lifetime)

        return this

    @staticmethod
    def from_abspath(abspath, validate=False, exists=False,
                              caching='default', lifetime=None):
        """Constructor from an absolute path."""

        abspath = abspath.rstrip('/')
        try:
            return PATHS[abspath]
        except KeyError:
            pass

        this = PdsFile()

        parts = abspath.split('/')
        if parts[0] != '':
            raise ValueError('Not an absolute path: ' + this.abspath)

        pdsdata_found = False
        for k in range(len(parts)):
            if parts[k].startswith('pdsdata'):
                pdsdata_found = True
                break

        if not pdsdata_found:
            raise ValueError('"pdsdata" not found in abspath', abspath)

        if k == 2 and parts[1].lower() == 'volumes':
            if len(parts) < 4:
                raise ValueError('Absolute path is too short: ' + abspath)
            if validate or exists:
                parts[1] = 'Volumes'
                parts[2] = parts[2].lower()
                parts[3] = parts[3].lower()

        else:
            parts = ['', '/'.join(parts[1:k])] + parts[k:]
            this.is_local = True

            if validate or exists:
                parts[2] = parts[2].lower()
                parts[3] = parts[3].lower()

        pdsdata = parts[2].split('-')[0]  # ignore anything after dash
            # pdsdata-server2 -> pdsdata
            # pdsdata2-local -> pdsdata2

        # Handle root directory
        if parts[3] != 'holdings':
            raise ValueError('Invalid holdings directory "%s": %s' %
                             (parts[3], this.abspath))

        this.disk_ = '/'.join(parts[:3]) + '/'
        this.root_ = '/'.join(parts[:4]) + '/'
        this.html_root_ = '/' + parts[3] + pdsdata[len('pdsdata'):] + '/'
            # /Volumes/pdsdata-whatever/holdings -> /holdings/
            # /Volumes/pdsdata2-whatever/holdings -> /holdings2/

            # In Apache, /Volumes/pdsdata[n]-whatever must redirect to
            # /Volumes/pdsdata[n]

        root_ = this.root_

        this.logical_path = ''
        this.abspath = this.root_[:-1]
        this.basename = parts[3]

        if len(parts) <= 4:
            return this._complete(False, caching='none')

        # Handle the rest of the tree using child()
        for part in parts[4:]:
            this = this.child(part, validate=validate, exists=exists,
                                    caching=caching, lifetime=lifetime,
                                    root_=root_)

        if exists and not os.path.exists(this.abspath):
            raise IOError('File not found', this.abspath)

        return this

    @staticmethod
    def from_path(path, caching='default', lifetime=None):
        """Find the PdsFile, if possible based on anything roughly resembling
        an actual path in the filesystem, using sensible defaults for missing
        components."""

        path = str(path)    # make sure it isn't unicode

        if path == '': path = 'volumes'     # prevents an error below

        # Make a quick return if possible
        try:
            return PATHS[path]
        except KeyError:
            pass
    
        path = path.rstrip('/')
        parts = path.split('/')

        if path.lower().startswith('/volumes/pdsdata'):
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
                rank = PATHS['$RANKS'][this.category_][volname][-1]

            try:
                this_abspath = PATHS['$VOLS'][this.category_][volname][rank]
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
                    this_abspath = PATHS['$VOLS'][this.category_][volname]\
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
                rank = PATHS['$RANKS'][this.category_][volset][-1]

            try:
                this_abspath = PATHS['$VOLS'][this.category_][volset][rank]
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
                    this_abspath = PATHS['$VOLS'][this.category_][volset]\
                                                 [alt_rank]
                    break
                  except KeyError:
                    continue

                if not this_abspath:
                    raise ValueError('Suffix "%s" not found: %s' %
                                     (this.suffix, path))

            this = PdsFile.from_abspath(this_abspath)

        else:
            this = PATHS[this.category_[:-1]]

        if len(parts) == 0:
            return this._complete(False, caching, lifetime)

        # Resolve the path below
        for part in parts:
            this = this.child(part, validate=True,
                                    caching=caching, lifetime=lifetime)

        return this

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
        if not self.volname:
            return None
        elif self.volname_:
            return ''.join([self.root_, self.category_, self.volset_,
                            self.volname])
        else:
            return ''.join([self.root_, self.category_, self.volset_,
                            self.interior])

    def volset_abspath(self):
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
            lskip = len(self.root_) + len(self.category_) + len(self.volset_)
        else:
            if not self.archives_:
                raise ValueError('Non-archive checksums require volumes: ' +
                                 self.logical_path)

            abspath = ''.join([self.root_, 'checksums-', self.category_,
                               self.volset, self.suffix, suffix, '_md5.txt'])
            lskip = len(self.root_) + len(self.category_) + len(self.volset_)

        return (abspath, lskip)

    def checksum_path_if_exact(self):

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

        if self.checksums_:
            raise ValueError('No shelf files for checksums: ' +
                             self.logical_path)

        if self.archives_:
            if not self.volset_:
                raise ValueError('Archive shelves require volume sets: ' +
                                 self.logical_path)

            abspath = ''.join([self.disk_, 'shelves/', id, '/', self.category_,
                               self.volset, self.suffix, '_', id, '.shelf'])
            lskip = len(self.root_) + len(self.category_) + len(self.volset_)

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
            lskip = len(self.root_) + len(self.category_) + \
                    len(self.volset_) + len(this_volname) + 1

        return (abspath, lskip)

    def shelf_path_and_key(self, id='info', volname=''):
        """Absolute path to a shelf file, plus the key for this item."""

        (abspath, lskip) = self.shelf_path_and_lskip(id=id, volname=volname)
        if volname:
            return (abspath, '')
        else:
            return (abspath, self.interior)

    @staticmethod
    def get_shelf(shelf_path):

        # If the shelf is already open, update the access count and return it
        if shelf_path in PdsFile.SHELF_CACHE:
            PdsFile.SHELF_ACCESS[shelf_path] = PdsFile.SHELF_ACCESS_COUNT
            PdsFile.SHELF_ACCESS_COUNT += 1

            return PdsFile.SHELF_CACHE[shelf_path]

        # Open and cache the shelf
        if LOGGER:
            LOGGER.debug('Opening shelf', shelf_path)

        try:
            shelf = shelve.open(shelf_path, flag='r')
        except Exception as e:
            raise IOError('File not found: ' + shelf_path)

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
                PdsFile.close_shelf(shelf_path)

        return shelf

    @staticmethod
    def close_shelf(shelf_path):

        # If the shelf is not already open, return
        if shelf_path not in PdsFile.SHELF_CACHE:
            if LOGGER:
                LOGGER.error('Cannot close shelf; not currently open',
                             shelf_path)
                return

        # Close the shelf and remove from the cache
        PdsFile.SHELF_CACHE[shelf_path].close()
        del PdsFile.SHELF_CACHE[shelf_path]
        del PdsFile.SHELF_ACCESS[shelf_path]

        if LOGGER: LOGGER.debug('Shelf closed', shelf_path)

    @staticmethod
    def close_all_shelves():
        for shelf_path in PdsFile.SHELF_CACHE.keys():   # use keys() so dict can
                                                        # be modified in loop!
            PdsFile.close_shelf(shelf_path)

    def shelf_lookup(self, id='info', volname=''):
        (shelf_path, key) = self.shelf_path_and_key(id, volname)

        # This potentially saves the need for a lot of opens and closes
        if key == '' and shelf_path in PdsFile.SHELF_NULL_KEY_VALUES:
            return PdsFile.SHELF_NULL_KEY_VALUES[shelf_path]

        shelf = PdsFile.get_shelf(shelf_path)
        if shelf is None:
            return None
    
        return shelf[key]

    ############################################################################
    # Log path associations
    ############################################################################

    LOG_ROOT_ = None

    @staticmethod
    def set_log_root(root=None):
        if root is None:
            PdsFile.LOG_ROOT_ = None
        else:
            PdsFile.LOG_ROOT_ = root.rstrip('/') + '/'

    def log_path_for_volume(self, id='', task='', dir=''):

        if PdsFile.LOG_ROOT_ is None:
            parts = [self.disk_, 'logs/', id, '/']
        else:
            parts = [PdsFile.LOG_ROOT_]

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

    def log_path_for_volset(self, id='', task='', dir=''):

        if PdsFile.LOG_ROOT_ is None:
            parts = [self.disk_, 'logs/', id, '/']
        else:
            parts = [PdsFile.LOG_ROOT_]

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

    @staticmethod
    def log_path_for_shelf(shelf_file, task='', selection=''):

        parts = shelf_file.split('/')
        k = parts.index('shelves')
        id = parts[k+1]
    
        if PdsFile.LOG_ROOT_:
            parts = [id.rstrip('s') + 'shelf'] + parts[k+2:]
            log_path = PdsFile.LOG_ROOT_ + '/'.join(parts)
        else:
            parts[k] = 'logs'
            parts[k+1] += 'shelf'
            log_path = '/'.join(parts)

        timetag = datetime.datetime.now().strftime(LOGFILE_TIME_FMT)
        suffix = ['_', timetag]

        if task:
            suffix += ['_', task]

        if selection:
            parts = selection.split('_')
            if len(parts) > 2:
                parts = parts[:2]

            suffix += ['_', '_'.join(parts)]

        suffix += ['.log']

        log_path = log_path.replace('.shelf', ''.join(suffix))
        return log_path

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
        PdsFile._LABELS_AFTER = labels_after

    def sort_dirs_first(dirs_first):
        PdsFile._DIRS_FIRST = dirs_first

    def sort_dirs_last(dirs_last):
        PdsFile._DIRS_LAST = dirs_last

    def sort_info_first(info_first):
        PdsFile._INFO_FIRST = info_first

    def basename_is_label(self, basename):
        """Override if label identification ever depends on the data set."""
        return (len(basename) > 4) and (basename[-4:].lower() == '.lbl')

    def basename_is_viewable(self, basename=None):
        """Override if viewable files can have other extensions."""

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
                abspath = os.path.join(parent_abspath, basename)
                parts = [not os.path.isdir(abspath)] + parts
            elif dirs_last and parent_abspath:
                abspath = os.path.join(parent_abspath, basename)
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
        return self.sort_basenames(self.childnames, labels_after, dirs_first,
                                   parent_abspath=self.abspath)

    def viewable_childnames(self):
        basenames = self.sort_childnames()
        return [b for b in basenames if self.basename_is_viewable(b)]

    def childnames_by_anchor(self, anchor):
        """Return a list of child basenames having the given anchor."""

        matches = []
        for basename in self.childnames:
            parts = self.split_basename(basename)
            if parts[0] == anchor:
                matches.append(basename)

        return self.sort_basenames(matches)

    def viewable_childnames_by_anchor(self, anchor):
        """Return a list of viewable child names having the given anchor."""

        matches = self.childnames_by_anchor(anchor)
        return [m for m in matches if self.basename_is_viewable(m)]

    ############################################################################
    # Transformations
    ############################################################################

    #### ... for pdsfiles

    @staticmethod
    def abspaths_for_pdsfiles(pdsfiles, exists=False):
        if exists:
            return [p.abspath for p in pdsfiles if p.exists]
        else:
            return [p.abspath for p in pdsfiles]

    @staticmethod
    def logicals_for_pdsfiles(pdsfiles, exists=False):
        if exists:
            return [p.logical_path for p in pdsfiles if p.exists]
        else:
            return [p.logical_path for p in pdsfiles]

    @staticmethod
    def basenames_for_pdsfiles(pdsfiles, exists=False):
        if exists:
            return [p.basename for p in pdsfiles if p.exists]
        else:
            return [p.basename for p in pdsfiles]

    #### ... for abspaths

    @staticmethod
    def pdsfiles_for_abspaths(abspaths, exists=False):
        pdsfiles = [PdsFile.from_abspath(p) for p in abspaths]
        if exists:
            pdsfiles = [f for f in pdsfiles if f.exists]

        return pdsfiles

    @staticmethod
    def logicals_for_abspaths(abspaths, exists=False):
        pdsfiles = PdsFile.pdsfiles_for_abspaths(abspaths, exists=exists)
        return [f.logical_path for f in pdsfiles]

    @staticmethod
    def basenames_for_abspaths(abspaths, exists=False):
        if exists:
            return [os.path.basename(p) for p in abspaths if os.path.exists(p)]
        else:
            return [os.path.basename(p) for p in abspaths]

    #### ... for logicals

    @staticmethod
    def pdsfiles_for_logicals(logical_paths, exists=False):
        pdsfiles = [PdsFile.from_logical_path(p) for p in logical_paths]
        if exists:
            pdsfiles = [f for f in pdsfiles if f.exists]

        return pdsfiles

    @staticmethod
    def abspaths_for_logicals(logical_paths, exists=False):
        pdsfiles = PdsFile.pdsfiles_for_logicals(logical_paths, exists=exists)
        return [p.abspath for p in pdsfiles]

    @staticmethod
    def basenames_for_logicals(logical_paths, exists=False):
        if exists:
            pdsfiles = PdsFile.pdsfiles_for_logicals(logical_paths,
                                                     exists=exists)
            return PdsFile.basenames_for_pdsfiles(pdsfiles)

        return [os.path.basename(p) for p in logical_paths]

    #### ... for basenames

    def pdsfiles_for_basenames(self, basenames, exists=False):

        pdsfiles = [self.child(b) for b in basenames]

        if exists:
            pdsfiles = [f for f in pdsfiles if f.exists]

        return pdsfiles

    def abspaths_for_basenames(self, basenames, exists=False):
        # shortcut
        if self.abspath and not exists:
            return [os.path.join(self.abspath, b) for b in basenames]

        pdsfiles = self.pdsfiles_for_basenames(basenames, exists=exists)
        return [f.abspath for f in pdsfiles]

    def logicals_for_basenames(self, basenames, exists=False):
        # shortcut
        if not exists:
            return [os.path.join(self.logical_path, b) for b in basenames]

        pdsfiles = self.pdsfiles_for_basenames(basenames, exists=exists)
        return [f.logical_path for f in pdsfiles]

    ############################################################################
    # Associations
    ############################################################################

    def associated_logical_paths(self, category, exists=True, primary=False):

        if not self.abspath:
            return []

        abspaths = self.associated_abspaths(category, exists=exists,
                                                      primary=primary)
        return PdsFile.logicals_for_abspaths(abspaths)

    def associated_abspaths(self, category, exists=True, primary=False):

        category = category.rstrip('/')

        # Handle checksums by finding associated files in subcategory
        if category.startswith('checksums-'):
            subcategory = category[len('checksums-'):]
            abspaths = self.associated_abspaths(subcategory, exists)
            if not abspaths: return []

            this = PdsFile.from_abspath(abspaths[0])
            try:
                checksum_abspath = this.checksum_path_and_lskip()[0]
            except ValueError:
                return []

            if exists and not os.path.exists(checksum_abspath):
                return []

            return [checksum_abspath]

        # Handle archives by finding associated files in subcategory
        if category.startswith('archives-'):
            subcategory = category[len('archives-'):]
            abspaths = self.associated_abspaths(subcategory, exists)
            if not abspaths:
                return []

            this = PdsFile.from_abspath(abspaths[0])
            try:
                archive_abspath = this.archive_path_and_lskip()[0]
            except ValueError:
                return []

            if exists and not os.path.exists(archive_abspath):
                return []

            return [archive_abspath]

        # Get rid of checksums-
        if self.checksums_:
            abspath = self.dirpath_and_prefix_for_checksum()[0]
            pdsfile = PdsFile.from_abspath(abspath)
            return pdsfile.associated_abspaths(category, exists)

        # Get rid of archives-
        if self.archives_:
            abspath = self.dirpath_and_prefix_for_archive()[0]
            pdsfile = PdsFile.from_abspath(abspath)
            return pdsfile.associated_abspaths(category, exists)

        # No more recursive calls...

        # Get the associated parallel inside volumes
        if self.category_ == 'volumes/':
            parallel_volume_pdsf = self
        else:
            parallel_volume_pdsf = self.associated_parallel(category='volumes')
            if parallel_volume_pdsf is None:
                return []

        # If our target is a volume, return results
        if category == 'volumes':
            abspaths = [parallel_volume_pdsf.abspath]

            patterns = self.ASSOCIATIONS_TO_VOLUMES.all(self.logical_path)
            patterns = [self.root_ + p for p in patterns]

            for pattern in patterns:
                if exists or ('*' in pattern or
                              '?' in pattern or
                              '[' in pattern):
                    abspaths += glob.glob(pattern)
                else:
                    abspaths += [pattern]

            # Translate to additional volumes files if necessary
            if not primary:
                logical_paths = self.logicals_for_abspaths(abspaths)
                trans = self.VOLUMES_TO_ASSOCIATIONS['volumes']
                patterns = trans.all(logical_paths)
                patterns = [self.root_ + p for p in patterns]

                for pattern in patterns:
                    if exists or ('*' in pattern or
                                  '?' in pattern or
                                  '[' in pattern):
                        abspaths += glob.glob(pattern)
                    else:
                        abspaths += [pattern]

                # Add the linked abspaths to the set of matches
                if self.islabel:
                    abspaths += self.linked_abspaths

            # Remove duplicates and return
            abspaths = list(set(abspaths))
            return abspaths

        # Translate to alternative voltypes as needed
        logical_paths = [parallel_volume_pdsf.logical_path]

        voltype = category.split('-')[-1]
        trans = parallel_volume_pdsf.VOLUMES_TO_ASSOCIATIONS[voltype]
        patterns = trans.all(logical_paths)
        patterns = [parallel_volume_pdsf.root_ + p for p in patterns]

        abspaths = []
        for pattern in patterns:
            if exists or ('*' in pattern or
                          '?' in pattern or
                          '[' in pattern):
                abspaths += glob.glob(pattern)
            else:
                abspaths += [pattern]

        # Without checksums- or archives-, we're done
        if voltype == category:

            # Always include the associated parallel
            pdsf = parallel_volume_pdsf.associated_parallel(category=voltype)
            if pdsf:
                abspaths += [pdsf.abspath]

            abspaths = list(set(abspaths))
            return abspaths

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

        abspaths = list(set(new_abspaths))
        return abspaths

    def associated_parallel(self, category=None, rank=None):
        """Rank can be number or 'latest', 'previous', 'next'; None for rank of
        this."""

        if category is None:
            category = self.category_

        category = category.rstrip('/')

        # Create the cached dictionary if necessary
        if self.associated_parallels_filled is None:
            self.associated_parallels_filled = {}

        # Return from dictionary if already available
        if rank is None and category in self.associated_parallels_filled:
            path = self.associated_parallels_filled[category]
            return PdsFile.from_logical_path(path)

        if (category, rank) in self.associated_parallels_filled:
            path = self.associated_parallels_filled[category, rank]
            return PdsFile.from_logical_path(path)

        # Handle special case of a virtual directory
        if not self.volset:
            target = PATHS.get(category)    # None if key not found

            if target is None:
                path = None
            else:
                path = target.logical_path

            self.associated_parallels_filled[category] = path
            self.associated_parallels_filled[category,     None] = path
            self.associated_parallels_filled[category, 'latest'] = path
            self.associated_parallels_filled[category,   999999] = path
            self.associated_parallels_filled[category,        0] = path
            self.associated_parallels_filled[category, 'previous'] = None
            self.associated_parallels_filled[category,     'next'] = None

            self.recache()
            if (category, rank) in self.associated_parallels_filled:
                return target
            else:
                return None

        # Interpret rank
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
                self.associated_parallels_filled[category, rank] = None
                self.associated_parallels_filled[category, original_rank] = None
                self.recache()
                return None

        # If interpreted rank is in dictionary, return lookup
        if (category, rank) in self.associated_parallels_filled:
            self.associated_parallels_filled[category, original_rank] = \
                                self.associated_parallels_filled[category, rank]
            path = self.associated_parallels_filled[category, rank]
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
            target_abspath = PATHS['$VOLS'][category + '/'][volkey][rank]
            target = PdsFile.from_abspath(target_abspath)
        except KeyError:
            target = None

        if target is None:
            self.associated_parallels_filled[category, rank] = None
            self.associated_parallels_filled[category, original_rank] = None
            self.recache()
            return None

        if target.isdir:
            for part in parts:
                child = target.child(part, validate=True)
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
        self.associated_parallels_filled[category, rank] = path
        self.associated_parallels_filled[category, original_rank] = path
        self.recache()
        return target

    ############################################################################
    # File grouping
    ############################################################################

    def group_children(self, basenames=None):
        """Return children as a list of x objects."""

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
        for (anchor, basenames) in anchor_dict.iteritems():
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
# They must share a common parent and anchor.
################################################################################

class PdsGroup(object):

    def __init__(self, pdsfiles=[], parent=False, anchor=None, hidden=[]):

        self.parent = parent        # False means un-initialized because None
                                    # means a virtual directory
        self.anchor = None
        self.rows = []
        self.hidden = set(hidden)

        self.isdir_filled = None
        self.iconset_filled = None
        self.viewset_filled = None
        self.local_viewset_filled = None

        if type(pdsfiles) in (list, tuple):
            for pdsf in pdsfiles:
                self.append(pdsf)
        else:
            self.append(pdsfiles)

    def __len__(self):
        return len(self.rows) - len(self.hidden)

    def copy(self):
        this = PdsGroup()
        this.parent = self.parent
        this.anchor = self.anchor
        this.rows = list(self.rows)
        this.hidden = self.hidden.copy()

        this.isdir_filled = self.isdir_filled
        this.iconset_filled = self.iconset_filled
        this.viewset_filled = self.viewset_filled
        this.local_viewset_filled = self.local_viewset_filled

        return this

    @property
    def parent_logical_path(self):
        if self.parent:
            return self.parent.logical_path
        else:
            return ''

    @property
    def isdir(self):
        if self.isdir_filled is None:
            self.isdir_filled = any([p.isdir for p in self.rows])

        return self.isdir_filled

    @property
    def iconset(self):
        if self.iconset_filled is None:
            self.iconset_filled = {}
            for open in (False, True):
                best_set = pdsviewable.ICON_SET_BY_TYPE[self.rows[0].icon_type,
                                                        open]
                for pdsf in self.rows[1:]:
                    test = pdsviewable.ICON_SET_BY_TYPE[pdsf.icon_type, open]
                    if test.priority > best_set.priority:
                        best_set = test

                self.iconset_filled[open] = best_set

        return self.iconset_filled[False]

    @property
    def iconset_closed(self):
        _ = self.iconset
        return self.iconset_filled[0]

    @property
    def iconset_open(self):
        _ = self.iconset
        return self.iconset_filled[1]

    @property
    def viewset(self):
        """The local viewset if it exists; otherwise, the first viewset."""

        if self.viewset_filled is None:

            if self.local_viewset:
                self.viewset_filled = self.local_viewset

            else:
                self.viewset_filled = []
                for pdsf in self.rows:
                    if pdsf.viewset:
                        self.viewset_filled = pdsf.viewset
                        break

        return self.viewset_filled

    @property
    def local_viewset(self):
        """False unless every item in the group is part of the viewset.
        """

        if self.local_viewset_filled is None:

            viewset = pdsviewable.PdsViewSet()
            for pdsf in self.rows:
                if pdsf.local_viewset:
                    viewset.append(pdsf.local_viewset)

            if len(viewset) == len(self):
                self.local_viewset_filled = viewset
            else:
                self.local_viewset_filled = False

        return self.local_viewset_filled

    @property
    def global_anchor(self):
        if self.parent is False:
            raise ValueError('PdsGroup has not been initialized')

        if self.parent is None:         # if a virtual dir
            return self.anchor
        else:
            return self.parent.global_anchor + '-' + self.anchor

    def sort(self, labels_after=None, dirs_first=None, dirs_last=None,
                   info_first=None):

        basename_dict = {}
        for pdsf in self.rows:
            basename_dict[pdsf.basename] = pdsf

        if self.parent:
            sorted = self.parent.sort_basenames(basename_dict.keys(),
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
        if self.parent is False:
            self.parent = pdsf.parent()
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

        self.isdir_filled = None
        self.iconset_filled = None
        self.viewset_filled = None
        self.local_viewset_filled = None

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
# Table class. An ordered set of PdsGroups sharing a common parent. Some may be
# hidden.
################################################################################

class PdsTable(object):

    def __init__(self, pdsgroups=[], parent=False):

        self.parent = parent    # False for un-initialized; None for virtual
        self.groups = []

        self.levels_filled = None

        for group in pdsgroups:
            self.insert_group(group)

    def copy(self):
        this = PdsTable()
        this.parent = self.parent
        this.groups = [g.copy() for g in self.groups]
        this.levels_filled = self.levels_filled

        return this

    @property
    def parent_logical_path(self):
        if self.parent:
            return self.parent.logical_path
        else:
            return ''

    @property
    def levels(self):
        if self.levels_filled is None:
            levels = []
            pdsf = self.parent
            while pdsf is not None:
                levels.append(pdsf)
                pdsf = pdsf.parent()

            self.levels_filled = levels

        return self.levels_filled

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
        if self.parent is False:
            self.parent = group.parent
        elif group.parent_logical_path != self.parent_logical_path:
            raise ValueError('PdsGroup parent does not match PdsTable parent')

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

        parent = pdsf.parent()
        if self.parent is False:
            self.parent = parent

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

        elif isinstance(thing, PdsTable):
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

        if self.parent:
            sorted_basenames = self.parent.sort_basenames(first_basenames,
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
            if table.parent is None:
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
        """Return a sorted list of PdsTables accommodating the given list of
        PdsFiles."""

        table_dict = {}
        for pdsf in pdsfiles:
            if type(pdsf) == str:
                pdsf = PdsFile.from_logical_path(pdsf)

            if pdsf.logical_path in exclusions: continue

            parent = pdsf.parent()
            parent_path = pdsf.parent_logical_path

            if parent_path not in table_dict:
                table_dict[parent_path] = PdsTable(parent=parent)

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

        tables = PdsTable.sort_tables(tables)
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
# Support functions
################################################################################

def repair_case(abspath):
    """Return a file's absolute path with capitalization exactly as it appears
    in the file system. Raises IOError if the file is not found.
    """

    trailing_slash = abspath.endswith('/')  # must preserve a trailing slash!
    abspath = os.path.abspath(abspath)

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

################################################################################
