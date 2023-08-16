################################################################################
# pds3file subpackage & Pds3File subclass with PdsFile as the parent class
################################################################################

from pdsfile_reorg import *

################################################################################
# Constants specific to the pds4file package
################################################################################
# FILESPEC_TO_BUNDLESET = pdsfile_rules.FILESPEC_TO_VOLSET
PDS_HOLDINGS = 'holdings'

class Pds3File(PdsFile):
# class Pds3File(pdsfile_reorg.PdsFile):
    FILESPEC_TO_BUNDLESET = pdsfile_rules.FILESPEC_TO_VOLSET

    def __init__(self):
        super().__init__()

    # @property
    # def is_volset(self):
    #     return self.is_bundleset
    # @staticmethod
    # def preload(holdings_list, port=0, clear=False,
    #             force_reload=False, icon_color='blue'):
    #     return pdsfile_reorg.preload(holdings_list, port, clear, force_reload, icon_color)

    # Alias
    # is_volset = self.is_bundleset


################################################################################
# Initialize the global registry of subclasses
################################################################################

Pds3File.SUBCLASSES['default'] = Pds3File
