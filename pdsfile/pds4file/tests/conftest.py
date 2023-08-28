##########################################################################################
# pds4file/tests/conftest.py
#
# Configuration & setup before running tests on pds4file
##########################################################################################

import os
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
    pds4file.set_logger(LOGGER)

@pytest.fixture(scope='session', autouse=True)
def setup(request):
    mode = request.config.option.mode
    if mode == '1':
        pds4file.use_shelves_only(True)
    elif mode == '2':
        pds4file.use_shelves_only(False)
    else: # pragma: no cover
        pds4file.use_shelves_only(True)

    # turn_on_logger("test_log.txt")
    pds4file.Pds4File.preload(PDS4_HOLDINGS_DIR)
