################################################################################
# Store global variables that will be modified or have different values in both
# pds3 & pds4 subclasses
################################################################################
import pdscache
import pdslogger
import re

PDS_HOLDINGS = 'holdings'

# Flag
SHELVES_ONLY = False
SHELVES_REQUIRED = False
FS_IS_CASE_INSENSITIVE = True

# CACHE
LOCAL_PRELOADED = []
CACHE = None

# REGEX
BUNDLESET_REGEX        = re.compile(r'^([A-Z][A-Z0-9x]{1,5}_[0-9x]{3}x)$')
BUNDLESET_REGEX_I      = re.compile(BUNDLESET_REGEX.pattern, re.I)
BUNDLESET_PLUS_REGEX   = re.compile(BUNDLESET_REGEX.pattern[:-1] +
                        r'(_v[0-9]+\.[0-9]+\.[0-9]+|_v[0-9]+\.[0-9]+|_v[0-9]+|'+
                        r'_in_prep|_prelim|_peer_review|_lien_resolution|)' +
                        r'((|_calibrated|_diagrams|_metadata|_previews)' +
                        r'(|_md5\.txt|\.tar\.gz))$')
BUNDLESET_PLUS_REGEX_I = re.compile(BUNDLESET_PLUS_REGEX.pattern, re.I)

BUNDLENAME_REGEX       = re.compile(r'^([A-Z][A-Z0-9]{1,5}_(?:[0-9]{4}))$')
BUNDLENAME_REGEX_I     = re.compile(BUNDLENAME_REGEX.pattern, re.I)
BUNDLENAME_PLUS_REGEX  = re.compile(BUNDLENAME_REGEX.pattern[:-1] +
                                  r'(|_[a-z]+)(|_md5\.txt|\.tar\.gz)$')
BUNDLENAME_PLUS_REGEX_I = re.compile(BUNDLENAME_PLUS_REGEX.pattern, re.I)
BUNDLENAME_VERSION     = re.compile(BUNDLENAME_REGEX.pattern[:-1] +
                        r'(_v[0-9]+\.[0-9]+\.[0-9]+|_v[0-9]+\.[0-9]+|_v[0-9]+|'+
                        r'_in_prep|_prelim|_peer_review|_lien_resolution)$')
BUNDLENAME_VERSION_I   = re.compile(BUNDLENAME_VERSION.pattern, re.I)
