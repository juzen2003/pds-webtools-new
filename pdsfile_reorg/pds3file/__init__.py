################################################################################
# pds3file subpackage & Pds3File subclass with PdsFile as the parent class
################################################################################

from pdsfile_reorg import *

################################################################################
# Constants specific to the pds4file package
################################################################################


# def preload(holdings_list, port=0, clear=False,
#             force_reload=False, icon_color='blue'):
#         return pdsfile_reorg.preload(holdings_list, port, clear, force_reload, icon_color)

# def use_shelves_only(status=True):
#     return pdsfile_reorg.use_shelves_only(status)

class Pds3File(PdsFile):
# class Pds3File(pdsfile_reorg.PdsFile):
    pass
    # @staticmethod
    # def preload(holdings_list, port=0, clear=False,
    #             force_reload=False, icon_color='blue'):
    #     return pdsfile_reorg.preload(holdings_list, port, clear, force_reload, icon_color)
