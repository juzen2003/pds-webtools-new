################################################################################
# pds4file subpackage & Pds4File subclass with PdsFile as the parent class
################################################################################

from pdsfile_reorg import *

# TODO: REMOVE BUNDLESET & BUNDLENAME REGEX

class Pds4File(PdsFile):
    pass


################################################################################
# Initialize the global registry of subclasses
################################################################################

Pds4File.SUBCLASSES['default'] = Pds4File
