import os
import pytest

from tests.helper import instantiate_target_pdsfile

# Check environment variables or else look in the default places
try:
    PDS4_HOLDINGS_DIR = os.environ['PDS4_HOLDINGS_DIR']
except KeyError: # pragma: no cover
    # TODO: update this when we know the actual path of pds4 holdings on the webserver
    PDS4_HOLDINGS_DIR = os.path.realpath('/Library/WebServer/Documents/holdings')

################################################################################
# Blackbox tests for pds4file.py
################################################################################
class TestPds4FileBlackBox:
    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/atmosphere/u0_kao_91cm_734nm_counts-v-time_atmos_ingress.xml',
             'opus-id-placehodler'),
        ]
    )
    def test_opus_id(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.opus_id
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm',
             f'{PDS4_HOLDINGS_DIR}/uranus_occs_earthbased/uranus_occ_u0_kao_91cm'),
        ]
    )
    def test_abspath(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.abspath
        assert res == expected
