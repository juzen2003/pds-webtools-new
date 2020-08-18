import os
import pdsfile
import pdslogger
import pytest

PDS_DATA_DIR = os.environ['PDS_DATA_DIR']
################################################################################
# Setup before all tests
################################################################################
def pytest_addoption(parser):
    parser.addoption("--mode", action="store")

def turn_on_logger(filename):
    LOGGER = pdslogger.PdsLogger(filename)
    pdsfile.set_logger(LOGGER)

# We only use use_pickles and use_shelves_only
@pytest.fixture(scope='session', autouse=True)
def setup(request):
    mode = request.config.option.mode
    if mode == '1':
        pdsfile.use_pickles(True)
        pdsfile.use_shelves_only(True)
    elif mode == '2':
        pdsfile.use_pickles(True)
        pdsfile.use_shelves_only(False)
    elif mode == '3':
        pdsfile.use_pickles(False)
        pdsfile.use_shelves_only(True)
    elif mode == '4':
        pdsfile.use_pickles(False)
        pdsfile.use_shelves_only(False)
    else: # default
        pdsfile.use_pickles(True)
        pdsfile.use_shelves_only(True)
    # turn_on_logger("test_log.txt")
    pdsfile.preload(PDS_DATA_DIR)
