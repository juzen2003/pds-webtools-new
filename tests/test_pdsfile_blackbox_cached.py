import datetime
import os
import pdsfile
import pdsviewable
import pytest

from tests.helper import instantiate_target_pdsfile, get_pdsfiles

PDS_DATA_DIR = os.environ['PDS_DATA_DIR']
PDS_TESTING_ROOT = PDS_DATA_DIR[:PDS_DATA_DIR.index('pdsdata')]
ICON_ROOT_ = PDS_TESTING_ROOT + '/icons-local/'
ICON_URL_  = 'icons-local/'
ICON_COLOR = 'blue'
################################################################################
# Blackbox test for internal cached in PdsFile class
################################################################################
class TestPdsFileBlackBox:
    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/VGISS_6xxx/VGISS_6101/DATA/C27830XX/C2783018_RAW.IMG',
             False),
            ('volumes/VGISS_6xxx/VGISS_6101/DATA/C27830XX', True),
            ('volumes/RES_xxxx_prelim/RES_0001/data/601_cas.tab', False)
        ]
    )
    def test_isdir(self, input_path, expected):
        """isdir: return self._isdir_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.isdir
        res2 = target_pdsfile.isdir
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/RES_xxxx_prelim/RES_0001/data/601_cas.lbl', True),
            ('volumes/VGISS_7xxx/VGISS_7201/DATA/C24476XX/C2447654_RAW.lbl',
             True),
            ('previews/VGISS_6xxx/VGISS_6101/DATA/C27830XX/C2783018_med.jpg',
             False)
        ]
    )
    def test_islabel(self, input_path, expected):
        """islabel: return self._islabel_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.islabel
        res2 = target_pdsfile.islabel
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('previews/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/'
             + 'lor_0003103486_0x630_eng_thumb.jpg', True),
            ('volumes/NHxxLO_xxxx/NHLALO_1001/data/20060224_000310/'
             + 'lor_0003103486_0x630_eng.fit', False),
            ('volumes/HSTUx_xxxx/HSTU0_5167/DATA/VISIT_04/U2NO0404T.asc', False)
        ]
    )
    def test_is_viewable(self, input_path, expected):
        """is_viewable: return self._is_viewable_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.is_viewable
        res2 = target_pdsfile.is_viewable
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('metadata/VGISS_7xxx/VGISS_7201/VGISS_7201_inventory.tab',
             ('VGISS_7201', '_inventory', '.tab')),
            ('previews/NHxxMV_xxxx/NHLAMV_1001/data/20060321_000526/mc1_0005261846_0x536_eng_1_thumb.jpg',
             ('mc1_0005261846_0x536_eng_1', '_thumb', '.jpg')),
            ('previews/VGISS_7xxx/VGISS_7201/DATA/C24476XX/C2447654_small.jpg',
             ('C2447654', '_small', '.jpg')),
        ]
    )
    def test_split(self, input_path, expected):
        """split: return self._split_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.split
        res2 = target_pdsfile.split
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/RPX_xxxx/RPX_0001/CALIB/F130LP.lbl',
             'volumes-RPX_xxxx-RPX_0001-CALIB-F130LP'),
            ('volumes/VGIRIS_xxxx_peer_review/VGIRIS_0001/DATA/JUPITER_VG1/C1547XXX.tab',
             'volumes-VGIRIS_xxxx_peer_review-VGIRIS_0001-DATA-JUPITER_VG1-C1547XXX'),
        ]
    )
    def test_global_anchor(self, input_path, expected):
        """global_anchor: return self._global_anchor_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.global_anchor
        res2 = target_pdsfile.global_anchor
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/RPX_xxxx/RPX_0001/CALIB/F130LP.lbl', []),
            ('previews/VGISS_5xxx/VGISS_5101/DATA/C13854XX',
             [
                'C1385455_full.jpg', 'C1385455_med.jpg',
                'C1385455_small.jpg', 'C1385455_thumb.jpg'
             ])
        ]
    )
    def test_childnames(self, input_path, expected):
        """childnames: return self._childnames_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.childnames
        res2 = target_pdsfile.childnames
        for child in expected:
            assert child in res1
        for child in res1:
            assert child in res2

    @pytest.mark.parametrize(
        'input_path',
        [
            ('volumes/VGISS_8xxx/VGISS_8201/DATA/C08966XX'),
            ('volumes/VGISS_8xxx/VGISS_8201/DATA/C08966XXx'),
            ('volumes/COISS_0xxx'),
            ('volumes/VGISS_8xxx'),
        ]
    )
    def test__info(self, input_path):
        """_info: return self._info_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile._info
        res2 = target_pdsfile._info
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/VG_20xx/VG_2001/JUPITER/CALIB/VG1PREJT.DAT',
             '2011-05-05 10:43:33')
        ]
    )
    def test_date(self, input_path, expected):
        """date: return self._date_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.date
        res2 = target_pdsfile.date
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/VG_20xx/VG_2001/JUPITER/CALIB/VG1PREJT.LBL', '33 KB'),
            ('volumes/VG_28xx/VG_2801/EDITDATA/PN1D01.DAT', '610 KB'),
        ]
    )
    def test_formatted_size(self, input_path, expected):
        """formatted_size: return self._formatted_size_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.formatted_size
        res2 = target_pdsfile.formatted_size
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460960868_1.lbl',
             (
                'Cassini ISS Saturn images 2004-04-18 to 2004-05-18 (SC clock 1460960653-1463538454)',
                'VOLUME', '1.0', '2005-07-01', ['CO-S-ISSNA/ISSWA-2-EDR-V1.0']
             )),
            ('metadata/COVIMS_0xxx/COVIMS_0001',
             (
                'Cassini VIMS near IR image cubes 1999-01-10 to 2000-09-18 (SC clock 1294638283-1347975444)',
                'VOLUME', '1.0', '2005-07-01', ['CO-E/V/J/S-VIMS-2-QUBE-V1.0']
             )),
        ]
    )
    def test__volume_info(self, input_path, expected):
        """_volume_info: return self._volume_info_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile._volume_info
        res2 = target_pdsfile._volume_info
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/VGIRIS_xxxx_peer_review/VGIRIS_0001/DATA/JUPITER_VG1/C1547XXX.lbl', 'PDS3 label'),
            ('previews/NHxxMV_xxxx/NHLAMV_1001/data/20060321_000526/mc1_0005261846_0x536_eng_1_thumb.jpg', 'Thumbnail preview image'),
        ]
    )
    def test_description(self, input_path, expected):
        """description: return part of self._description_and_icon_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.description
        res2 = target_pdsfile.description
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('metadata/VGISS_5xxx/VGISS_5101/VGISS_5101_supplemental_index.tab',
             'INDEX')
        ]
    )
    def test_icon_type(self, input_path, expected):
        """icon_type: return part of self._description_and_icon_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.icon_type
        res2 = target_pdsfile.icon_type
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/NHxxMV_xxxx/NHLAMV_1001/data/20060321_000526/mc0_0005261846_0x536_eng_1.fit', 'image/fits'),
            ('volumes/RPX_xxxx/RPX_0001/CALIB/F130LP.tab', 'text/plain'),
            ('previews/HSTUx_xxxx/HSTU0_5167/DATA/VISIT_04/U2NO0401T_thumb.jpg',
             'image/jpg')
        ]
    )
    def test_mime_type(self, input_path, expected):
        """mime_type: return self._mime_type_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.mime_type
        res2 = target_pdsfile.mime_type
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COVIMS_0xxx/COVIMS_0001/data/1999010T054026_1999010T060958/v1294638283_1.qub',
             'co-vims-v1294638283')
        ]
    )
    def test_opus_id(self, input_path, expected):
        """opus_id: return self._opus_id_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.opus_id
        res2 = target_pdsfile.opus_id
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('metadata/COUVIS_0xxx/COUVIS_0001/COUVIS_0001_index.tab',
             ('ASCII', 'Table')),
            ('volumes/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007/HDAC1999_007_16_31.LBL',
             ('ASCII', 'PDS3 Label')),
            ('previews/COISS_2xxx/COISS_2002/data/1460960653_1461048959/N1460960908_1_thumb.jpg',
             ('Binary', 'JPEG')),
        ]
    )
    def test_opus_format(self, input_path, expected):
        """opus_format: return self._opus_format_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.opus_format
        res2 = target_pdsfile.opus_format
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COCIRS_6xxx/COCIRS_6004/DATA/GEODATA/GEO1004021018_699.TAB',
             ('Cassini CIRS', 110, 'cocirs_geo',  'System Geometry')),
            ('previews/VGISS_8xxx/VGISS_8201/DATA/C08966XX/C0896631_thumb.jpg',
             ('browse', 10, 'browse_thumb', 'Browse Image (thumbnail)')),
        ]
    )
    def test_opus_type(self, input_path, expected):
        """opus_type: return self._opus_type_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.opus_type
        res2 = target_pdsfile.opus_type
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/VGISS_8xxx/VGISS_8201', 'VOLDESC.CAT'),
            ('volumes/VG_28xx/VG_2801/EDITDATA/PN1D01.LBL', 'PN1D01.LBL'),
        ]
    )
    def test_info_basename(self, input_path, expected):
        """info_basename: return self._info_basename_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.info_basename
        res2 = target_pdsfile.info_basename
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/EUV2004_274_01_39.lbl', ()),
            ('volumes/COCIRS_0xxx/COCIRS_0012/DATA', []),
            ('previews/COISS_1xxx/COISS_1001/data/1294561143_1295221348/W1294561261_1_thumb.jpg', []),
            ('volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.LBL',
             [
                (24, 'GEO00120100.DAT', PDS_DATA_DIR + '/volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.DAT'),
                (25, 'GEO00120100.DAT', PDS_DATA_DIR + '/volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.DAT'),
                (32, 'GEO.FMT', PDS_DATA_DIR + '/volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO.FMT')
             ])
        ]
    )
    def test_internal_link_info(self, input_path, expected):
        """internal_link_info: return self._internal_links_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.internal_link_info
        res2 = target_pdsfile.internal_link_info
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COUVIS_8xxx/COUVIS_8001/data/UVIS_HSP_2017_228_BETORI_I_TAU10KM.tab',
             'UVIS_HSP_2017_228_BETORI_I_TAU10KM.lbl')
        ]
    )
    def test_label_basename(self, input_path, expected):
        """label_basename: return self._label_basename_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.label_basename
        res2 = target_pdsfile.label_basename
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('previews/COCIRS_1xxx/COCIRS_1001/DATA/CUBE/EQUIRECTANGULAR/123RI_EQLBS002_____CI____699_F1_039E_thumb.jpg',
             pdsviewable.PdsViewSet)
        ]
    )
    def test_viewset(self, input_path, expected):
        """viewset: return self._viewset_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.viewset
        res2 = target_pdsfile.viewset
        assert isinstance(res1, expected)
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('previews/HSTIx_xxxx/HSTI1_1556/DATA/VISIT_01/IB4W01I5Q_thumb.jpg',
             True),
            ('volumes/HSTIx_xxxx/HSTI1_1556/DATA/VISIT_01/IB4W01I5Q.asc', False)
        ]
    )
    def test_local_viewset(self, input_path, expected):
        """local_viewset: return self._local_viewset_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.local_viewset
        res2 = target_pdsfile.local_viewset
        assert isinstance(res1, pdsviewable.PdsViewSet) == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('previews/HSTJx_xxxx/HSTJ0_9296/DATA/VISIT_B1/', '2018-03-25'),
        ]
    )
    def test_volume_publication_date(self, input_path, expected):
        """volume_publication_date: return self._volume_publication_date_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.volume_publication_date
        res2 = target_pdsfile.volume_publication_date
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/COUVIS_0xxx_v1/COUVIS_0009/DATA/D2004_274/EUV2004_274_01_39.lbl', '1.0'),
            ('volumes/COCIRS_1xxx/COCIRS_1001/DATA/TSDR/NAV_DATA/TAR10013100.DAT'
             , '4.0'),
            ('volumes/COCIRS_0xxx_v3/COCIRS_0401/DATA/TSDR/NAV_DATA/TAR04012400.DAT', '3.0'),
        ]
    )
    def test_volume_version_id(self, input_path, expected):
        """volume_version_id: return self._volume_version_id_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.volume_version_id
        res2 = target_pdsfile.volume_version_id
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/VGISS_7xxx/VGISS_7201/DATA/C24476XX/C2447654_RAW.IMG',
             ['VG2-U-ISS-2/3/4/6-PROCESSED-V1.0']),
        ]
    )
    def test_volume_data_set_ids(self, input_path, expected):
        """volume_data_set_ids: return self._volume_data_set_ids_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.volume_data_set_ids
        res2 = target_pdsfile.volume_data_set_ids
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('volumes/VGISS_8xxx/VGISS_8201/DATA/C08966XX/C0896631_RAW.LBL',
             [999999]),
        ]
    )
    def test_version_ranks(self, input_path, expected):
        """version_ranks: return self._version_ranks_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.version_ranks
        res2 = target_pdsfile.version_ranks
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('metadata/VGISS_7xxx/VGISS_7201/VGISS_7201_inventory.tab', 8),
            ('metadata/HSTJx_xxxx/HSTJ0_9296/HSTJ0_9296_index.tab', 9),
        ]
    )
    def test_filename_keylen(self, input_path, expected):
        """filename_keylen: return self._filename_keylen_filled"""
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.filename_keylen
        res2 = target_pdsfile.filename_keylen
        assert res1 == expected
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007',
             pdsviewable.PdsViewSet)
        ]
    )
    def test__iconset(self, input_path, expected):
        """filename_keylen: return self._iconset_filled[0]"""
        pdsviewable.load_icons(path=ICON_ROOT_, url=ICON_URL_, color=ICON_COLOR)
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile._iconset
        res2 = target_pdsfile._iconset
        assert isinstance(res1, expected)
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007',
             pdsviewable.PdsViewSet)
        ]
    )

    def test_iconset_open(self, input_path, expected):
        """filename_keylen: return self._iconset_filled[0]"""
        pdsviewable.load_icons(path=ICON_ROOT_, url=ICON_URL_, color=ICON_COLOR)
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.iconset_open
        res2 = target_pdsfile.iconset_open
        assert isinstance(res1, expected)
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_path,expected',
        [
            ('previews/COUVIS_0xxx/COUVIS_0001/DATA/D1999_007',
             pdsviewable.PdsViewSet)
        ]
    )

    def test_iconset_closed(self, input_path, expected):
        """filename_keylen: return self._iconset_filled[0]"""
        pdsviewable.load_icons(path=ICON_ROOT_, url=ICON_URL_, color=ICON_COLOR)
        target_pdsfile = instantiate_target_pdsfile(input_path)
        res1 = target_pdsfile.iconset_closed
        res2 = target_pdsfile.iconset_closed
        assert isinstance(res1, expected)
        assert res1 == res2

################################################################################
# Blackbox test for internal cached in PdsGroup class
################################################################################
class TestPdsGroupBlackBox:
    @pytest.mark.parametrize(
        'input_paths,expected',
        [
            ([
                'volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.DAT',
                'volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.LBL'
             ],
             pdsviewable.PdsViewSet)
        ]
    )
    def test__iconset(self, input_paths, expected):
        """filename_keylen: return self._iconset_filled[0]"""
        pdsviewable.load_icons(path=ICON_ROOT_, url=ICON_URL_, color=ICON_COLOR)
        target_pdsfile = get_pdsfiles(input_paths)
        target_pdsgroup = pdsfile.PdsGroup(pdsfiles=target_pdsfile)
        res1 = target_pdsgroup._iconset
        res2 = target_pdsgroup._iconset
        assert isinstance(res1, expected)
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_paths,expected',
        [
            ([
                'volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.DAT',
                'volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.LBL'
             ],
             pdsviewable.PdsViewSet)
        ]
    )
    def test_iconset_open(self, input_paths, expected):
        """filename_keylen: return self._iconset_filled[0]"""
        pdsviewable.load_icons(path=ICON_ROOT_, url=ICON_URL_, color=ICON_COLOR)
        target_pdsfile = get_pdsfiles(input_paths)
        target_pdsgroup = pdsfile.PdsGroup(pdsfiles=target_pdsfile)
        res1 = target_pdsgroup.iconset_open
        res2 = target_pdsgroup.iconset_open
        assert isinstance(res1, expected)
        assert res1 == res2

    @pytest.mark.parametrize(
        'input_paths,expected',
        [
            ([
                'volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.DAT',
                'volumes/COCIRS_0xxx/COCIRS_0012/DATA/NAV_DATA/GEO00120100.LBL'
             ],
             pdsviewable.PdsViewSet)
        ]
    )
    def test_iconset_closed(self, input_paths, expected):
        """filename_keylen: return self._iconset_filled[0]"""
        pdsviewable.load_icons(path=ICON_ROOT_, url=ICON_URL_, color=ICON_COLOR)
        target_pdsfile = get_pdsfiles(input_paths)
        target_pdsgroup = pdsfile.PdsGroup(pdsfiles=target_pdsfile)
        res1 = target_pdsgroup.iconset_closed
        res2 = target_pdsgroup.iconset_closed
        assert isinstance(res1, expected)
        assert res1 == res2
