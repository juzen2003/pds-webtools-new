import os
import pdsfile_reorg.pds4file as pds4file

from pdsfile_reorg.general_helper import instantiate_target_pdsfile_for_class

try:
    PDS4_HOLDINGS_DIR = os.environ['PDS4_HOLDINGS_DIR']
except KeyError: # pragma: no cover
    # TODO: update this when we know the actual path of pds4 holdings on the webserver
    PDS4_HOLDINGS_DIR = os.path.realpath('/Library/WebServer/Documents/holdings')

PDS4_BUNDLES_DIR = f'{PDS4_HOLDINGS_DIR}/bundles'

def instantiate_target_pdsfile(path, is_abspath=True):
    return instantiate_target_pdsfile_for_class(path, pds4file.Pds4File,
                                                PDS4_BUNDLES_DIR, is_abspath)
