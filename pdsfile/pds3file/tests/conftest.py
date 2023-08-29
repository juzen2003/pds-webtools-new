##########################################################################################
# pds3file/tests/conftest.py
#
# Configuration & setup before running tests on pds3file
##########################################################################################

import os
import pdsfile.pds3file as pds3file
from pdsfile.cfg import PDS_HOLDINGS_DIR
import pdslogger
import pytest


##########################################################################################
# Setup before all tests
##########################################################################################
def pytest_addoption(parser):
    parser.addoption("--mode", action="store")

def turn_on_logger(filename):
    LOGGER = pdslogger.PdsLogger(filename)
    pds3file.set_logger(LOGGER)

# We only use use_pickles and use_shelves_only
@pytest.fixture(scope='session', autouse=True)
def setup(request):
    mode = request.config.option.mode
    if mode == 's':
        pds3file.use_shelves_only(True)
    elif mode == 'ns':
        pds3file.use_shelves_only(False)
    else: # pragma: no cover
        pds3file.use_shelves_only(True)

    # turn_on_logger("test_log.txt")
    pds3file.Pds3File.preload(PDS_HOLDINGS_DIR)
