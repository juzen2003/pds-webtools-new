import os
import pdsfile_reorg.pds3file as pds3file
import pdslogger
import pytest

try:
    PDS_HOLDINGS_DIR = os.environ['PDS_HOLDINGS_DIR']
except KeyError: # pragma: no cover
    PDS_HOLDINGS_DIR = os.path.realpath('/Library/WebServer/Documents/holdings')

################################################################################
# Setup before all tests
################################################################################
# def pytest_addoption(parser):
#     parser.addoption("--mode", action="store")

def turn_on_logger(filename):
    LOGGER = pdslogger.PdsLogger(filename)
    pds3file.set_logger(LOGGER)

# We only use use_pickles and use_shelves_only
@pytest.fixture(scope='session', autouse=True)
def setup(request):
    mode = request.config.option.mode
    if mode == '1':
        pds3file.use_shelves_only(True)
    elif mode == '2':
        pds3file.use_shelves_only(False)
    else: # pragma: no cover
        pds3file.use_shelves_only(True)

    # turn_on_logger("test_log.txt")
    pds3file.Pds3File.preload(PDS_HOLDINGS_DIR)
