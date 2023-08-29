##########################################################################################
# pds4file/tests/conftest.py
#
# Configuration & setup before running tests on pds4file
##########################################################################################

import os
import pdsfile.pds3file as pds3file
from pdsfile.cfg import PDS_HOLDINGS_DIR
import pdsfile.pds4file as pds4file
from pdsfile.cfg import PDS4_HOLDINGS_DIR
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
    pds4file.set_logger(LOGGER)

@pytest.fixture(scope='session', autouse=True)
def setup(request):
    mode = request.config.option.mode
    if mode == '1':
        pds3file.use_shelves_only(True)
        pds4file.use_shelves_only(True)
    elif mode == '2':
        pds3file.use_shelves_only(False)
        pds4file.use_shelves_only(False)
    else: # pragma: no cover
        pds3file.use_shelves_only(True)
        pds4file.use_shelves_only(True)

    # turn_on_logger("test_log.txt")
    pds3file.Pds3File.preload(PDS_HOLDINGS_DIR)
    pds4file.Pds4File.preload(PDS4_HOLDINGS_DIR)
