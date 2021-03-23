################################################################################
# rules/__init__.py
#
# Subclasses of PdsFile, encompassing dataset-specific information
################################################################################

__all__ = [
    "ASTROM_xxxx",
    "COCIRS_xxxx",
    "COISS_xxxx" ,
    "CORSS_8xxx" ,
    "COSP_8xxx"  ,
    "COUVIS_0xxx",
    "COUVIS_8xxx",
    "COVIMS_0xxx",
    "COVIMS_8xxx",
    "EBROCC_xxxx",
    "GO_0xxx"    ,
    "HSTxx_xxxx" ,
    "NHSP_xxxx"  ,
    "NHxxxx_xxxx",
    "RES_xxxx"   ,
    "RPX_xxxx"   ,
    "VG_0xxx"    ,
    "VG_20xx"    ,
    "VG_28xx"    ,
    "VGIRIS_xxxx",
    "VGISS_xxxx" ,
]

# Methods used for rule debugging
import pdsfile
import translator
import re

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
