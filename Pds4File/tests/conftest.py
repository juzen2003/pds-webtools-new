import os
import pds4file
import pdslogger
import pytest

try:
    PDS4_HOLDINGS_DIR = os.environ['PDS4_HOLDINGS_DIR']
except KeyError: # pragma: no cover
    # TODO: update this when we know the actual path of pds4 holdings on the webserver
    PDS4_HOLDINGS_DIR = os.path.realpath('/Library/WebServer/Documents/holdings')
################################################################################
# Setup before all tests
################################################################################
@pytest.fixture(scope='session', autouse=True)
def setup(request):
    pds4file.use_shelves_only(False) # pragma: no cover
    pds4file.preload(PDS4_HOLDINGS_DIR)
