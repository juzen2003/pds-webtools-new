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
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/atmosphere/u0_kao_91cm_734nm_counts-v-time_atmos_ingress.xml',
#             'uranus_occ_u0_kao_91cm'),
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/global/u0_kao_91cm_734nm_counts-v-time_occult.xml',
#             'uranus_occ_u0_kao_91cm'),
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/rings/u0_kao_91cm_734nm_radius_alpha_egress_1000m.tab',
#             'uranus_occ_u0_kao_91cm'),
            ('cassini_iss/cassini_iss_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947228n.img',
             'co-iss-n1308947228'),
            ('cassini_iss/cassini_iss_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947880n.xml',
             'co-iss-n1308947880'),
            ('cassini_iss/cassini_iss_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947440w.img',
             'co-iss-w1308947440'),
            ('cassini_iss/cassini_iss_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947440w.img',
             'co-iss-w1308947440'),
            ('cassini_iss/cassini_iss_cruise/browse_raw/130xxxxxxx/13089xxxxx/1308947440w-full.png',
             'co-iss-w1308947440'),
            ('cassini_iss/cassini_iss_cruise/browse_raw/130xxxxxxx/13089xxxxx/1308947880n-full.xml',
             'co-iss-n1308947880'),
            ('cassini_vims/cassini_vims_cruise/data_raw/130xxxxxxx/13089xxxxx/1308946681_xxx/1308946681_002.qub',
             'co-vims-v1308946681_002'),
            ('cassini_vims/cassini_vims_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947235.qub',
             'co-vims-v1308947235'),
            ('cassini_vims/cassini_vims_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947009_xxx/1308947009_002.qub',
             'co-vims-v1308947009_002'),
            ('cassini_vims/cassini_vims_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947715.xml',
             'co-vims-v1308947715'),
            ('cassini_vims/cassini_vims_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947926_xxx/1308947926_008.qub',
             'co-vims-v1308947926_008'),
            ('cassini_vims/cassini_vims_cruise/browse_raw/130xxxxxxx/13089xxxxx/1308947235-full.png',
             'co-vims-v1308947235'),
            ('cassini_vims/cassini_vims_cruise/browse_raw/130xxxxxxx/13089xxxxx/1308947079_xxx/1308947079_001-full.xml',
             'co-vims-v1308947079_001'),
            ('cassini_vims/cassini_vims_cruise/browse_raw/130xxxxxxx/13089xxxxx/1308947009_xxx/1308947009_002-full.png',
             'co-vims-v1308947009_002'),
            ('cassini_vims/cassini_vims_cruise/browse_raw/130xxxxxxx/13089xxxxx/1308947715-full.png',
             'co-vims-v1308947715'),
        ]
    )
    def test_opus_id(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.opus_id
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm',
#             f'{PDS4_HOLDINGS_DIR}/uranus_occs_earthbased/uranus_occ_u0_kao_91cm'),
             ('cassini_iss/cassini_iss_cruise',
             f'{PDS4_HOLDINGS_DIR}/cassini_iss/cassini_iss_cruise'),
             ('cassini_vims/cassini_vims_cruise',
             f'{PDS4_HOLDINGS_DIR}/cassini_vims/cassini_vims_cruise'),
        ]
    )
    def test_abspath(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.abspath
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/rings/u0_kao_91cm_734nm_radius_alpha_egress_1000m.xml',
#            'bundles/uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/rings/u0_kao_91cm_734nm_radius_alpha_egress_1000m.xml'),
            ('cassini_iss/cassini_iss_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947228n.img',
            'bundles/cassini_iss/cassini_iss_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947228n.img'),
            ('cassini_vims/cassini_vims_cruise/data_raw/130xxxxxxx/13089xxxxx/1308946681_xxx/1308946681_002.qub',
            'bundles/cassini_vims/cassini_vims_cruise/data_raw/130xxxxxxx/13089xxxxx/1308946681_xxx/1308946681_002.qub'),
            ('cassini_vims/cassini_vims_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947235.qub',
            'bundles/cassini_vims/cassini_vims_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947235.qub'),
        ]
    )
    def test_logical_path(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.logical_path
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/rings/u0_kao_91cm_734nm_radius_alpha_egress_1000m.xml',
#             True),
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/rings/non-existent-filename.txt',
#             False),
            ('cassini_iss/cassini_iss_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947228n.xml',
            True),
            ('cassini_vims/cassini_vims_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947235.xml',
            True),
            ('cassini_vims/cassini_vims_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947009_xxx/1308947009_002.qub',
            True),
    ]
    )
    def test_exists(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.exists
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
#            ('uranus_occs_earthbased/',
#             ''), # bundlesets currently have empty string instead of False
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm',
#             True),
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/bundle.xml',
#             False),
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/atmosphere/u0_kao_91cm_734nm_counts-v-time_atmos_egress.xml',
#             False),
            ('cassini_iss',
             ''), # bundlesets currently have empty string instead of False
            ('cassini_iss/cassini_iss_cruise',
             True),
            ('cassini_iss/cassini_iss_cruise/bundle.xml',
             False),
            ('cassini_iss/cassini_iss_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947228n.img',
             False),
            ('cassini_vims',
             ''), # bundlesets currently have empty string instead of False
            ('cassini_vims/cassini_vims_cruise',
             True),
            ('cassini_vims/cassini_vims_cruise/bundle.xml',
             False),
            ('cassini_vims/cassini_vims_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947235.qub',
             False),
            ('cassini_vims/cassini_vims_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947926_xxx/1308947926_008.xml',
             False),
        ]
    )
    def test_is_bundle(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.is_bundle
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm',
#             True), # This test fails with `ValueError: Illegal bundle set directory "": bundles`, because of match failure with BUNDLE_SET_PLUS_REGEX_I on line 3254 of pds4file.py
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/browse',
#             False),
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/xml_schema/collection_xml_schema.csv',
#             False),
#            ('uranus_occs_earthbased',
#             ''), # Bundlesets return empty string, rather than False at the moment
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/bundle.xml',
#             False),
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/atmosphere/u0_kao_91cm_734nm_counts-v-time_atmos_egress.xml',
#             False),
#            ('uranus_occs_earthbased/',
#             ''), # bundlesets currently have empty string instead of False
            ('cassini_iss',
             ''), # bundlesets currently have empty string instead of False
            ('cassini_iss/cassini_iss_cruise',
             True), 
            ('cassini_iss/cassini_iss_cruise/browse',
             False),
            ('cassini_iss/cassini_iss_cruise/xml_schema/collection_xml_schema.csv',
             False),
            ('cassini_iss/cassini_iss_cruise',
             True), 
            ('cassini_iss/cassini_iss_cruise/bundle.xml',
             False),
            ('cassini_iss/cassini_iss_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947228n.img',
             False),
            ('cassini_iss/cassini_iss_cruise/',
             True), 
            ('cassini_vims',
             ''), # bundlesets currently have empty string instead of False
            ('cassini_vims/cassini_vims_cruise',
             True), 
            ('cassini_vims/cassini_vims_cruise/calibration',
             False),
            ('cassini_vims/cassini_vims_cruise/xml_schema/collection_xml_schema.csv',
             False),
            ('cassini_vims/cassini_vims_cruise',
             True), 
            ('cassini_vims/cassini_vims_cruise/bundle.xml',
             False),
            ('cassini_vims/cassini_vims_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947926_xxx/1308947926_008.qub',
             False),
            ('cassini_vims/cassini_vims_cruise/data_raw/130xxxxxxx/13089xxxxx//1308947715.xml',
             False),
            ('cassini_vims/cassini_vims_cruise/',
             True), 
        ]
    )
    def test_is_bundle_dir(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.is_bundle_dir
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/rings/u0_kao_91cm_734nm_radius_alpha_egress_1000m.xml',
#             False),
#             ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/bundle.xml',
#             False),
             ('cassini_iss/cassini_iss_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947228n.img',
             False),
             ('cassini_iss/cassini_iss_cruise/bundle.xml',
             False),
             ('cassini_vims/cassini_vims_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947926_xxx/1308947926_008.qub',
             False),
             ('cassini_vims/cassini_vims_cruise/bundle.xml',
             False),
        ]
    )
    def test_is_bundle_file(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.is_bundle_file
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
#            ('uranus_occs_earthbased',
#             True),
#            ('uranus_occs_earthbased/',
#             True),
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/bundle.xml',
#             False),
            ('cassini_iss',
             True),
            ('cassini_vims/',
             True),
            ('cassini_iss/cassini_iss_cruise/bundle.xml',
             False),
            ('cassini_iss/cassini_iss_cruise/',
             False),
            ('cassini_vims/cassini_vims_cruise',
             False),
      ]
    )
    def test_is_bundleset(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.is_bundleset
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
#            ('uranus_occs_earthbased',
#             True),
#            ('uranus_occs_earthbased/',
#             True),
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/bundle.xml',
#             False),
            ('cassini_vims',
             True),
            ('cassini_iss/',
             True),
            ('cassini_iss/cassini_iss_cruise/bundle.xml',
             False),
            ('cassini_iss/cassini_iss_cruise',
             False),
            ('cassini_vims/cassini_vims_cruise',
             False),
        ]
    )
    def test_is_bundleset_dir(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.is_bundleset_dir
        assert res == expected

    @pytest.mark.parametrize(
        'input_path,expected',
        [
#            ('uranus_occs_earthbased/',
#             'uranus_occs_earthbased'),
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm',
#             'uranus_occs_earthbased'),
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/bundle.xml',
#             'uranus_occs_earthbased'),
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/atmosphere/u0_kao_91cm_734nm_counts-v-time_atmos_ingress.tab',
#             'uranus_occs_earthbased'),
            ('cassini_iss/',
             'cassini_iss'),
            ('cassini_iss/cassini_iss_cruise',
             'cassini_iss'),
            ('cassini_iss/cassini_iss_cruise/bundle.xml',
             'cassini_iss'),
            ('cassini_iss/cassini_iss_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947228n.img',
             'cassini_iss'),
            ('cassini_vims/',
             'cassini_vims'),
            ('cassini_vims/cassini_vims_cruise',
             'cassini_vims'),
            ('cassini_vims/cassini_vims_cruise/bundle.xml',
             'cassini_vims'),
            ('cassini_vims/cassini_vims_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947926_xxx/1308947926_008.qub',
             'cassini_vims'),
            ('cassini_vims/cassini_vims_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947235.qub',
             'cassini_vims'),
        ]
    )
    def test_bundleset(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.bundleset
        assert res == expected


    @pytest.mark.parametrize(
        'input_path,expected',
        [
#            ('uranus_occs_earthbased/',
#             ['uranus_occ_u0_kao_91cm']),
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm',
#             ['browse', 'bundle.xml', 'bundle_member_index.csv', 'bundle_member_index230313.csv', 'context', 'data', 'document', 'readme.txt', 'xml_schema']),
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/bundle.xml',
#             []),
#            ('uranus_occs_earthbased/uranus_occ_u0_kao_91cm/data/atmosphere/u0_kao_91cm_734nm_counts-v-time_atmos_egress.xml',
#             []),
            ('cassini_iss/',
             ['cassini_iss_cruise']),
            ('cassini_iss/cassini_iss_cruise',
             ['browse_raw', 'bundle.xml', 'context', 'data_raw', 'document','xml_schema']),
            ('cassini_iss/cassini_iss_cruise/bundle.xml',
             []),
            ('cassini_iss/cassini_iss_cruise/data_raw/130xxxxxxx/13089xxxxx/1308947228n.xml',
             []),
            ('cassini_vims/',
             ['cassini_vims_cruise']),
            ('cassini_vims/cassini_vims_cruise',
             ['browse_raw', 'bundle.xml', 'calibration', 'context', 'data_raw', 'document','xml_schema']),
            ('cassini_vims/cassini_vims_cruise/bundle.xml',
             []),
            ('cassini_vims/cassini_vims_cruise/data_raw/130xxxxxxx/13089xxxxx/1308946681_xxx/1308946681_002.qub',
             []),
            ('cassini_vims/cassini_vims_cruise/data_raw/130xxxxxxx/13089xxxxx/13089xxxxx/1308947235.xml',
             []),
        ]
    )
    def test_childnames(self, input_path, expected):
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res = target_pdsfile.childnames
        assert res == expected

