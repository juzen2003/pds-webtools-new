##########################################################################################
# pdsfile/preload_and_cache.py
# Store the code for preload management and cache
##########################################################################################


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
