##########################################################################################
# pdsfile/pds4file/__init__.py
# pds4file subpackage & Pds4File subclass with PdsFile as the parent class
##########################################################################################

from pdsfile import *
from . import rules

from pdsfile.preload_and_cache import cache_lifetime_for_class

cfg.BUNDLESET_REGEX = re.compile(r'^(uranus_occs_earthbased|^cassini_iss|^cassini_vims)$')
cfg.BUNDLESET_PLUS_REGEX   = re.compile(cfg.BUNDLESET_REGEX.pattern[:-1] +
                        r'(_v[0-9]+\.[0-9]+\.[0-9]+|_v[0-9]+\.[0-9]+|_v[0-9]+|'+
                        r'_in_prep|_prelim|_peer_review|_lien_resolution|)' +
                        r'((|_calibrated|_diagrams|_metadata|_previews)' +
                        r'(|_md5\.txt|\.tar\.gz))$')
cfg.BUNDLESET_PLUS_REGEX_I = re.compile(cfg.BUNDLESET_PLUS_REGEX.pattern, re.I)

cfg.BUNDLENAME_REGEX = re.compile(r'((^uranus_occ_u\d{0,4}._[a-z]*_(fos|\d{2,3}cm))'+
                                  r'|(^cassini\_[a-z]{3,4}\_cruise))$')
cfg.BUNDLENAME_PLUS_REGEX  = re.compile(cfg.BUNDLENAME_REGEX.pattern[:-1] +
                                  r'(|_[a-z]+)(|_md5\.txt|\.tar\.gz)$')
cfg.BUNDLENAME_PLUS_REGEX_I = re.compile(cfg.BUNDLENAME_PLUS_REGEX.pattern, re.I)


def cache_lifetime(arg):
    return cache_lifetime_for_class(arg, Pds4File)

# Initialize the cache
MEMCACHE_PORT = 0           # default is to use a DictionaryCache instead


class Pds4File(PdsFile):

    # Class variables
    PDS_HOLDINGS = 'pds4-holdings'
    BUNDLE_DIR_NAME = 'bundles'

    # Logger
    LOGGER = pdslogger.NullLogger()

    # CACHE
    DICTIONARY_CACHE_LIMIT = 200000
    CACHE = pdscache.DictionaryCache(lifetime=cache_lifetime,
                                     limit=DICTIONARY_CACHE_LIMIT,
                                     logger=LOGGER)

    # Override the rules
    DESCRIPTION_AND_ICON = rules.DESCRIPTION_AND_ICON
    ASSOCIATIONS = rules.ASSOCIATIONS
    VERSIONS = rules.VERSIONS
    INFO_FILE_BASENAMES = rules.INFO_FILE_BASENAMES
    NEIGHBORS = rules.NEIGHBORS
    SIBLINGS = rules.SIBLINGS       # just used by Viewmaster right now
    SORT_KEY = rules.SORT_KEY
    SPLIT_RULES = rules.SPLIT_RULES
    VIEW_OPTIONS = rules.VIEW_OPTIONS
    VIEWABLES = rules.VIEWABLES
    LID_AFTER_DSID = rules.LID_AFTER_DSID
    DATA_SET_ID = rules.DATA_SET_ID

    OPUS_TYPE = rules.OPUS_TYPE
    OPUS_FORMAT = rules.OPUS_FORMAT
    OPUS_PRODUCTS = rules.OPUS_PRODUCTS
    OPUS_ID = rules.OPUS_ID
    OPUS_ID_TO_PRIMARY_LOGICAL_PATH = rules.OPUS_ID_TO_PRIMARY_LOGICAL_PATH

    OPUS_ID_TO_SUBCLASS = rules.OPUS_ID_TO_SUBCLASS
    FILESPEC_TO_VOLSET = rules.FILESPEC_TO_VOLSET
    FILESPEC_TO_BUNDLESET = FILESPEC_TO_VOLSET

    def __init__(self):
        super().__init__()

    # Override functions
    def __repr__(self):
        if self.abspath is None:
            return 'Pds4File-logical("' + self.logical_path + '")'
        elif type(self) == Pds4File:
            return 'Pds4File("' + self.abspath + '")'
        else:
            return ('Pds4File.' + type(self).__name__ + '("' +
                    self.abspath + '")')


##########################################################################################
# Initialize the global registry of subclasses
##########################################################################################

Pds4File.SUBCLASSES['default'] = Pds4File

##########################################################################################
# This import must wait until after the Pds4File class has been fully initialized
# because all bundle set specific rules are the subclasses of Pds4File
##########################################################################################

try:
    # Data set-specific rules are implemented as subclasses of Pds4File
    # from pdsfile_reorg.Pds4File.rules import *
    from .rules import (cassini_iss,
                        cassini_vims,
                        uranus_occs_earthbased)
except AttributeError:
    pass                    # This occurs when running pytests on individual
                            # rule subclasses, where pdsfile can be imported
                            # recursively.
