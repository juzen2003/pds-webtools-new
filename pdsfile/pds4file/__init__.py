################################################################################
# pds4file subpackage & Pds4File subclass with PdsFile as the parent class
################################################################################

from pdsfile import *
from .rules import pds4file_rules as pdsfile_rules

from pdsfile.general_helper import cache_lifetime_for_class

cfg.PDS_HOLDINGS = 'pds4-holdings'
cfg.SHELVES_ONLY = False
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
DICTIONARY_CACHE_LIMIT = 200000
cfg.CACHE = pdscache.DictionaryCache(lifetime=cache_lifetime,
                                 limit=DICTIONARY_CACHE_LIMIT,
                                 logger=LOGGER)

class Pds4File(PdsFile):
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

    BUNDLE_DIR_NAME = 'bundles'

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


################################################################################
# Initialize the global registry of subclasses
################################################################################

Pds4File.SUBCLASSES['default'] = Pds4File

################################################################################
# This import must wait until after the PdsFile class has been fully initialized
################################################################################

try:
    # Data set-specific rules are implemented as subclasses of Pds4File
    # from pdsfile_reorg.Pds4File.rules import *
    from pdsfile.pds4file.rules import (cassini_iss,
                                              cassini_vims,
                                              uranus_occs_earthbased)
except AttributeError:
    pass                    # This occurs when running pytests on individual
                            # rule subclasses, where pdsfile can be imported
                            # recursively.