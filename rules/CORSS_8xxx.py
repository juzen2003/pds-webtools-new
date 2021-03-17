####################################################################################################################################
# rules/CORSS_8xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*/data/Rev(...)',               re.I, (r'Data for Cassini orbit \1',         'DATADIR')),
    (r'volumes/.*/data/Rev(...)/Rev\w+E',       re.I, (r'Data for Cassini orbit \1 egress',  'SERIESDIR')),
    (r'volumes/.*/data/Rev(...)/Rev\w+I',       re.I, (r'Data for Cassini orbit \1 ingress', 'SERIESDIR')),
    (r'volumes/.*/Rev\w+_([KSX])(\d\d)_[IE]',   re.I, (r'\1-band data from DSN ground station \2', 'SERIESDIR')),

    (r'volumes/.*/RSS\w+_CAL\.TAB',             re.I, ('Calibration parameters',       'TABLE')),
    (r'volumes/.*/RSS\w+_DLP_.*\.TAB',          re.I, ('Diffraction-limited profile',  'TABLE')),
    (r'volumes/.*/RSS\w+_GEO\.TAB',             re.I, ('Geometry table',               'TABLE')),
    (r'volumes/.*/RSS\w+_TAU.*\.TAB',           re.I, ('Optical depth profile',        'SERIES')),
    (r'volumes/.*/Rev\w+_Summary.*\.pdf',       re.I, ('Observation description',      'INFO')),

    (r'previews/.*/Rev\d\d\dC?[IE]_full\.jpg',    re.I, ('Large observation diagram',    'DIAGRAM')),
    (r'previews/.*/Rev\d\d\dC?[IE]_med\.jpg',     re.I, ('Medium observation diagram',   'DIAGRAM')),
    (r'previews/.*/Rev\d\d\dC?[IE]_small\.jpg',   re.I, ('Small observation diagram',    'DIAGRAM')),
    (r'previews/.*/Rev\d\d\dC?[IE]_thumb\.jpg',   re.I, ('Thumbnail obervation diagram', 'DIAGRAM')),

    (r'previews/.*/Rev\d\d\dC?[IE]_full\.jpg',    re.I, ('Large observation diagram',    'DIAGRAM')),
    (r'previews/.*/Rev\d\d\dC?[IE]_med\.jpg',     re.I, ('Medium observation diagram',   'DIAGRAM')),
    (r'previews/.*/Rev\d\d\dC?[IE]_small\.jpg',   re.I, ('Small observation diagram',    'DIAGRAM')),
    (r'previews/.*/Rev\d\d\dC?[IE]_thumb\.jpg',   re.I, ('Thumbnail obervation diagram', 'DIAGRAM')),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl', re.I, ''),
    (r'volumes/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/(browse|data)/(.*)\.pdf', 0,
                    r'previews/CORSS_8xxx/\2/\3/\4_*.jpg'),
    (r'volumes/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/(data/Rev.../Rev...C?[IE])', 0,
                    r'previews/CORSS_8xxx/\2/\3_*.jpg'),
    (r'volumes/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/(data/Rev.../Rev...C?[IE])/(Rev...C?[IE])_(RSS\w+)', 0,
                    r'previews/CORSS_8xxx/\2/\3/\4_\5/\5_GEO_*.jpg'),
    (r'volumes/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/(data/.*)_(TAU|GEO).*\.TAB', 0,
                    r'previews/CORSS_8xxx/\2/\3_\4_*.jpg'),

    (r'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev(..)(C?[IE])_RSS_(\w+)/(\w+)_(GEO|TAU)(\.TAB|_.*M\.TAB)', 0,
                    r'previews/CORSS_8xxx/CORSS_8001/data/Rev0\1/Rev0\1\2/Rev0\1\2_RSS_\3/\4_\5_*.jpg'),
    (r'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev(..)(C?[IE])_RSS_(\w+)/Rev..[IE]_(RSS.*Summary).pdf', 0,
                    r'previews/CORSS_8xxx/CORSS_8001/data/Rev0\1/Rev0\1\2/Rev0\1\2_RSS_\3/Rev0\1\2_\4_*.jpg'),
    (r'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev(..)(C?[IE])_RSS_(\w+)', 0,
                    r'previews/CORSS_8xxx/CORSS_8001/data/Rev0\1/Rev0\1\2/Rev0\1\2_RSS_\3_*.jpg'),
])

diagram_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl', re.I, ''),
    (r'volumes/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/.*/(Rev...)(C?[IE]_RSS_2..._..._..._[IE])', 0,
                    r'diagrams/CORSS_8xxx/\2/data/\3/\3\4_*.jpg'),
])

def test_default_viewables():
    TESTS = [
        (0, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007_DSN_Elevation.LBL'),
        (4, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007_DSN_Elevation.pdf'),
        (4, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007_TimeLine_Figure.pdf'),
        (4, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007_TimeLine_Table.pdf'),
        (4, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E'),
        (4, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E'),
        (0, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_CAL.TAB'),
        (0, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_DLP_500M.TAB'),
        (4, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_GEO.TAB'),
        (4, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_TAU_01KM.TAB'),
        (4, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_TAU_10KM.TAB'),
        (4, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev137/Rev137E/Rev137E_RSS_2010_245_S24_E/RSS_2010_245_S24_E_TAU_1600M.TAB'),
        (4, 'volumes/CORSS_8xxx/CORSS_8001/browse/Rev007_OccTrack_Geometry.pdf'),
        (4, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev07E_RSS_2005_123_X43_E/Rev07E_RSS_2005_123_X43_E_Summary.pdf'),
        (0, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev07E_RSS_2005_123_X43_E/RSS_2005_123_X43_E_CAL.TAB'),
        (4, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev07E_RSS_2005_123_X43_E/RSS_2005_123_X43_E_TAU_01KM.TAB'),
        (4, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev07E_RSS_2005_123_X43_E/RSS_2005_123_X43_E_TAU_10KM.TAB'),
    ]

    for (count, path) in TESTS:
        abspaths = pdsfile.rules.translate_first(default_viewables, path)
        trimmed = [p.rpartition('holdings/')[-1] for p in abspaths]
        assert len(abspaths) == count, f'{path} {len(abspaths)} {trimmed}'

def test_diagram_viewables():
    TESTS = [
        (0, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007_DSN_Elevation.LBL'),
        (0, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007_DSN_Elevation.pdf'),
        (0, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007_TimeLine_Figure.pdf'),
        (0, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007_TimeLine_Table.pdf'),
        (0, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E'),
        (4, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E'),
        (0, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_CAL.TAB'),
        (0, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_DLP_500M.TAB'),
        (0, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_GEO.TAB'),
        (0, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_TAU_01KM.TAB'),
        (0, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_TAU_10KM.TAB'),
        (0, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev137/Rev137E/Rev137E_RSS_2010_245_S24_E/RSS_2010_245_S24_E_TAU_1600M.TAB'),
        (0, 'volumes/CORSS_8xxx/CORSS_8001/browse/Rev007_OccTrack_Geometry.pdf'),
        (0, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev07E_RSS_2005_123_X43_E/Rev07E_RSS_2005_123_X43_E_Summary.pdf'),
        (0, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev07E_RSS_2005_123_X43_E/RSS_2005_123_X43_E_CAL.TAB'),
        (0, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev07E_RSS_2005_123_X43_E/RSS_2005_123_X43_E_TAU_01KM.TAB'),
        (0, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev07E_RSS_2005_123_X43_E/RSS_2005_123_X43_E_TAU_10KM.TAB'),
    ]

    for (count, path) in TESTS:
        abspaths = pdsfile.rules.translate_first(diagram_viewables, path)
        trimmed = [p.rpartition('holdings/')[-1] for p in abspaths]
        assert len(abspaths) == count, f'Miscount: {path} {len(abspaths)} {trimmed}'

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'.*/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/(data|browse)', 0,
                    [r'volumes/CORSS_8xxx\1/\2/data',
                     r'volumes/CORSS_8xxx\1/\2/browse',
                    ]),
    (r'previews/(CORSS_8xxx/CORSS_8.../.*)_[a-z]+\.jpg', 0,
                    r'volumes/\1*'),
    (r'previews/(CORSS_8xxx/CORSS_8.../[^\.]+)', 0,
                    r'volumes/\1'),
    (r'diagrams/(CORSS_8xxx/CORSS_8.../data/Rev...)/(Rev...C?[IE])(_RSS.*)_[a-z]+\.jpg', 0,
                    r'volumes/\1/\2/\2\3'),
    (r'volumes/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/browse/(Rev...).*', 0,
                    r'volumes/CORSS_8xxx\1/\2/data/\3'),
    (r'volumes/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/data/(Rev...).*', 0,
                    r'volumes/CORSS_8xxx\1/\2/browse/\3_OccTrack_Geometry.*'),
    (r'volumes/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/data/(Rev...)/(Rev...C?[EI]).*', 0,
                    r'volumes/CORSS_8xxx\1/\2/data/\3/\3_*'),
    (r'volumes/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/data/(Rev.../Rev...C?[EI]/\w+)/.*', 0,
                    r'volumes/CORSS_8xxx\1/\2/data/\3/*'),
    (r'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA', 0,
                    [r'volumes/CORSS_8xxx/CORSS_8001/data',
                     r'volumes/CORSS_8xxx/CORSS_8001/browse',
                    ]),
    (r'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev(\d\d)(C?[EI])(\w+)(|/.*)', 0,
                    r'volumes/CORSS_8xxx/CORSS_8001/data/Rev0\1/Rev0\1\2/Rev0\1\2\3'),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'.*/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/(data|browse|EASYDATA)', 0,
                    [r'previews/CORSS_8xxx/\2/data',
                     r'previews/CORSS_8xxx/\2/browse'
                    ]),
    (r'previews/CORSS_8xxx/(CORSS_8.../.*)_[a-z]+\.jpg', 0,
                    r'previews/CORSS_8xxx/\1_*.jpg'),
    (r'diagrams/CORSS_8xxx/(CORSS_8...)/.*/(Rev...)(C?[IE])_(RSS_2..._..._..._[IE]).*', 0,
                    r'previews/CORSS_8xxx/\1/data/\2/\2\3/\2\3_\4'),
    (r'volumes/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/.*/(Rev\d\d\d)(|_.*)', 0,
                    [r'previews/CORSS_8xxx/\2/data/\3',
                     r'previews/CORSS_8xxx/\2/browse/\3_OccTrack_Geometry_*.jpg',
                    ]),
    (r'volumes/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/data/(Rev...)/(Rev...C?[IE])(|_.*)', 0,
                    [r'previews/CORSS_8xxx/\2/data/\3/\4',
                     r'previews/CORSS_8xxx/\2/data/\3/\4_*.jpg',
                    ]),
    (r'volumes/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/.*/(Rev...)(C?[IE])_(RSS_2..._..._..._[IE])(|/.*)', 0,
                    r'previews/CORSS_8xxx/\2/data/\3/\3\4/\3\4_\5'),
    (r'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev(\d\d)(C?[EI])_(RSS_2..._..._..._[EI])(|/.*)', 0,
                    r'previews/CORSS_8xxx/CORSS_8001/data/Rev0\1/Rev0\1\2/Rev0\1\2_\3'),
])

associations_to_diagrams = translator.TranslatorByRegex([
    (r'.*/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/(data|browse|EASYDATA)', 0,
                    r'diagrams/CORSS_8xxx/\2/data'),
    (r'.*/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/.*/(Rev...)(C?[IE]_RSS_2..._..._..._[IE]).*', 0,
                    r'diagrams/CORSS_8xxx/\2/data/\3/\3\4_*.jpg'),
    (r'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev(\d\d)(C?[EI])_(RSS_2..._..._..._[IE]).*', 0,
                    r'diagrams/CORSS_8xxx/CORSS_8001/data/Rev0\1/Rev0\1\2_\3_*.jpg'),
])

associations_to_metadata = translator.TranslatorByRegex([
    (r'volumes/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/data.*/(\w+)\..*', 0,
                    r'metadata/CORSS_8xxx/\2/\2_index.tab/\3'),
    (r'volumes/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/data.*/(\w+)_TAU.*', 0,
                    [r'metadata/CORSS_8xxx/\2/\2_profile_index.tab/\3_TAU_01KM',
                     r'metadata/CORSS_8xxx/\2/\2_profile_index.tab/\3_TAU_1400M',
                     r'metadata/CORSS_8xxx/\2/\2_profile_index.tab/\3_TAU_1600M',
                     r'metadata/CORSS_8xxx/\2/\2_profile_index.tab/\3_TAU_2400M',
                     r'metadata/CORSS_8xxx/\2/\2_profile_index.tab/\3_TAU_3000M',
                     r'metadata/CORSS_8xxx/\2/\2_profile_index.tab/\3_TAU_4000M',
                     r'metadata/CORSS_8xxx/\2/\2_supplemental_index.tab/\3_TAU_01KM',
                     r'metadata/CORSS_8xxx/\2/\2_supplemental_index.tab/\3_TAU_1400M',
                     r'metadata/CORSS_8xxx/\2/\2_supplemental_index.tab/\3_TAU_1600M',
                     r'metadata/CORSS_8xxx/\2/\2_supplemental_index.tab/\3_TAU_2400M',
                     r'metadata/CORSS_8xxx/\2/\2_supplemental_index.tab/\3_TAU_3000M',
                     r'metadata/CORSS_8xxx/\2/\2_supplemental_index.tab/\3_TAU_4000M',
                    ]),
])

def test_associations_to_volumes():
    TESTS = [
        (2, 'volumes/CORSS_8xxx/CORSS_8001/data'),
        (2, 'volumes/CORSS_8xxx/CORSS_8001/browse'),
        (2, 'previews/CORSS_8xxx/CORSS_8001/data'),
        (2, 'previews/CORSS_8xxx/CORSS_8001/browse'),
        (2, 'diagrams/CORSS_8xxx/CORSS_8001/data'),
        (2, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA'),
        (2, 'previews/CORSS_8xxx/CORSS_8001/browse/Rev007_OccTrack_Geometry_full.jpg'),
        (2, 'previews/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007_DSN_Elevation_full.jpg'),
        (1, 'previews/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E_full.jpg'),
        (2, 'previews/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/Rev007E_RSS_2005_123_K34_E_Summary_thumb.jpg'),
        (2, 'previews/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_GEO_thumb.jpg'),
        (4, 'previews/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_TAU_thumb.jpg'),
        (2, 'previews/CORSS_8xxx/CORSS_8001/browse/Rev054_OccTrack_Geometry_full.jpg'),
        (2, 'previews/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054_DSN_Elevation_full.jpg'),
        (2, 'previews/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054_TimeLine_Figure_full.jpg'),
        (2, 'previews/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054_TimeLine_Table_full.jpg'),
        (1, 'previews/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE_full.jpg'),
        (2, 'previews/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE/Rev054CE_RSS_2007_353_K55_E/Rev054CE_RSS_2007_353_K55_E_Summary_thumb.jpg'),
        (2, 'previews/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE/Rev054CE_RSS_2007_353_K55_E/RSS_2007_353_K55_E_GEO_thumb.jpg'),
        (4, 'previews/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE/Rev054CE_RSS_2007_353_K55_E/RSS_2007_353_K55_E_TAU_thumb.jpg'),
        (1, 'diagrams/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E_RSS_2005_123_K34_E_full.jpg'),
        (1, 'diagrams/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE_RSS_2007_353_K55_E_full.jpg'),
        (1, 'volumes/CORSS_8xxx/CORSS_8001/browse/Rev007_OccTrack_Geometry.pdf'),
        (1, 'volumes/CORSS_8xxx/CORSS_8001/browse/Rev007_OccTrack_Geometry.LBL'),
        (2, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007'),
        (8, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E'),
        (8, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E'),
        (20, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_TAU_01KM.TAB'),
        (20, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_TAU_01KM.LBL'),
        (20, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_TAU_10KM.TAB'),
        (20, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_CAL.TAB'),
        (20, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_DLP_500M.TAB'),
        (20, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_GEO.TAB'),
        (8, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE'),
        (8, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE/Rev054CE_RSS_2007_353_K55_E'),
        (20, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE/Rev054CE_RSS_2007_353_K55_E/RSS_2007_353_K55_E_TAU_01KM.TAB'),
        (20, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE/Rev054CE_RSS_2007_353_K55_E/RSS_2007_353_K55_E_TAU_01KM.LBL'),
        (20, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE/Rev054CE_RSS_2007_353_K55_E/RSS_2007_353_K55_E_TAU_10KM.TAB'),
        (20, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE/Rev054CE_RSS_2007_353_K55_E/RSS_2007_353_K55_E_CAL.TAB'),
        (20, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE/Rev054CE_RSS_2007_353_K55_E/RSS_2007_353_K55_E_DLP_500M.TAB'),
        (20, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE/Rev054CE_RSS_2007_353_K55_E/RSS_2007_353_K55_E_GEO.TAB'),
        (20, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE/Rev054CE_RSS_2007_353_K55_E/Rev054CE_RSS_2007_353_K55_E_Summary.pdf'),
        (1, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev07E_RSS_2005_123_K34_E'),
        (1, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev07E_RSS_2005_123_X43_E/RSS_2005_123_X43_E_TAU_01KM.TAB'),
        (1, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev07E_RSS_2005_123_X43_E/RSS_2005_123_X43_E_TAU_01KM.LBL'),
        (1, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev07E_RSS_2005_123_X43_E/RSS_2005_123_X43_E_TAU_10KM.TAB'),
        (1, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev07E_RSS_2005_123_X43_E/RSS_2005_123_X43_E_CAL.TAB'),
        (1, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev07E_RSS_2005_123_X43_E/RSS_2005_123_X43_E_GEO.TAB'),
        (1, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev07E_RSS_2005_123_X43_E/Rev07E_RSS_2005_123_X43_E_Summary.pdf'),
    ]

    for (count, path) in TESTS:
        unmatched = pdsfile.rules.unmatched_patterns(associations_to_volumes, path)
        trimmed = [p.rpartition('holdings/')[-1] for p in unmatched]
        assert len(unmatched) == 0, f'Unmatched: {path} {trimmed}'

        abspaths = pdsfile.rules.translate_all(associations_to_volumes, path)
        trimmed = [p.rpartition('holdings/')[-1] for p in abspaths]
        assert len(abspaths) == count, f'Miscount: {path} {len(abspaths)} {trimmed}'

def test_associations_to_previews():
    TESTS = [
        (2, 'volumes/CORSS_8xxx/CORSS_8001/data'),
        (2, 'volumes/CORSS_8xxx/CORSS_8001/browse'),
        (2, 'previews/CORSS_8xxx/CORSS_8001/data'),
        (2, 'previews/CORSS_8xxx/CORSS_8001/browse'),
        (2, 'diagrams/CORSS_8xxx/CORSS_8001/data'),
        (2, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA'),
        (4, 'previews/CORSS_8xxx/CORSS_8001/browse/Rev007_OccTrack_Geometry_full.jpg'),
        (4, 'previews/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007_DSN_Elevation_full.jpg'),
        (4, 'previews/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E_full.jpg'),
        (4, 'previews/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/Rev007E_RSS_2005_123_K34_E_Summary_thumb.jpg'),
        (4, 'previews/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_GEO_thumb.jpg'),
        (4, 'previews/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_TAU_thumb.jpg'),
        (4, 'previews/CORSS_8xxx/CORSS_8001/browse/Rev054_OccTrack_Geometry_full.jpg'),
        (4, 'previews/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054_DSN_Elevation_full.jpg'),
        (4, 'previews/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054_TimeLine_Figure_full.jpg'),
        (4, 'previews/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054_TimeLine_Table_full.jpg'),
        (4, 'previews/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE_full.jpg'),
        (4, 'previews/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE/Rev054CE_RSS_2007_353_K55_E/Rev054CE_RSS_2007_353_K55_E_Summary_thumb.jpg'),
        (4, 'previews/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE/Rev054CE_RSS_2007_353_K55_E/RSS_2007_353_K55_E_GEO_thumb.jpg'),
        (4, 'previews/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE/Rev054CE_RSS_2007_353_K55_E/RSS_2007_353_K55_E_TAU_thumb.jpg'),
        (1, 'diagrams/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E_RSS_2005_123_K34_E_full.jpg'),
        (1, 'diagrams/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE_RSS_2007_353_K55_E_full.jpg'),
        (5, 'volumes/CORSS_8xxx/CORSS_8001/browse/Rev007_OccTrack_Geometry.pdf'),
        (5, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007'),
        (5, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E'),
        (1, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E'),
        (1, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_TAU_01KM.TAB'),
        (5, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE'),
        (1, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE/Rev054CE_RSS_2007_353_K55_E'),
        (1, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE/Rev054CE_RSS_2007_353_K55_E/RSS_2007_353_K55_E_TAU_01KM.TAB'),
        (1, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev07E_RSS_2005_123_K34_E'),
        (1, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev07E_RSS_2005_123_X43_E/RSS_2005_123_X43_E_TAU_01KM.TAB'),
    ]

    for (count, path) in TESTS:
        unmatched = pdsfile.rules.unmatched_patterns(associations_to_previews, path)
        trimmed = [p.rpartition('holdings/')[-1] for p in unmatched]
        assert len(unmatched) == 0, f'Unmatched: {path} {trimmed}'

        abspaths = pdsfile.rules.translate_all(associations_to_previews, path)
        trimmed = [p.rpartition('holdings/')[-1] for p in abspaths]
        assert len(abspaths) == count, f'Miscount: {path} {len(abspaths)} {trimmed}'

def test_associations_to_diagrams():
    TESTS = [
        (1, 'volumes/CORSS_8xxx/CORSS_8001/data'),
        (1, 'volumes/CORSS_8xxx/CORSS_8001/browse'),
        (1, 'previews/CORSS_8xxx/CORSS_8001/data'),
        (1, 'previews/CORSS_8xxx/CORSS_8001/browse'),
        (1, 'diagrams/CORSS_8xxx/CORSS_8001/data'),
        (1, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA'),
        (0, 'previews/CORSS_8xxx/CORSS_8001/browse/Rev007_OccTrack_Geometry_full.jpg'),
        (0, 'previews/CORSS_8xxx/CORSS_8001/data/Rev007'),
        (0, 'previews/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E_full.jpg'),
        (4, 'previews/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/Rev007E_RSS_2005_123_K34_E_Summary_thumb.jpg'),
        (4, 'previews/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_GEO_thumb.jpg'),
        (4, 'previews/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE/Rev054CE_RSS_2007_353_K55_E/Rev054CE_RSS_2007_353_K55_E_Summary_thumb.jpg'),
        (4, 'previews/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE/Rev054CE_RSS_2007_353_K55_E/RSS_2007_353_K55_E_GEO_thumb.jpg'),
        (4, 'diagrams/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E_RSS_2005_123_K34_E_full.jpg'),
        (4, 'diagrams/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE_RSS_2007_353_K55_E_full.jpg'),
        (0, 'volumes/CORSS_8xxx/CORSS_8001/browse/Rev007_OccTrack_Geometry.pdf'),
        (0, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E'),
        (4, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E'),
        (4, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev007/Rev007E/Rev007E_RSS_2005_123_K34_E/RSS_2005_123_K34_E_TAU_01KM.TAB'),
        (0, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE'),
        (4, 'volumes/CORSS_8xxx/CORSS_8001/data/Rev054/Rev054CE/Rev054CE_RSS_2007_353_K55_E'),
        (4, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev07E_RSS_2005_123_K34_E'),
        (4, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev07E_RSS_2005_123_X43_E/RSS_2005_123_X43_E_TAU_01KM.TAB'),
        (4, 'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev07E_RSS_2005_123_X43_E/Rev07E_RSS_2005_123_X43_E_Summary.pdf'),
    ]

    for (count, path) in TESTS:
        unmatched = pdsfile.rules.unmatched_patterns(associations_to_diagrams, path)
        trimmed = [p.rpartition('holdings/')[-1] for p in unmatched]
        assert len(unmatched) == 0, f'Unmatched: {path} {trimmed}'

        abspaths = pdsfile.rules.translate_all(associations_to_diagrams, path)
        trimmed = [p.rpartition('holdings/')[-1] for p in abspaths]
        assert len(abspaths) == count, f'Miscount: {path} {len(abspaths)} {trimmed}'

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|diagrams|previews)/.*/(data|browse)/.*', 0, (True, True, True)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'(.*)/Rev...',                    0, r'\1/Rev*'),
    (r'(.*)/Rev.../Rev...C?[IE]',       0, r'\1/Rev*/Rev*[IE]'),
    (r'(.*)/Rev.../Rev...C?[IE]/Rev.*', 0, r'\1/Rev*/Rev*/Rev*'),
    (r'(.*)/EASYDATA/Rev\w+',           0, r'\1/EASYDATA/*'),
])

####################################################################################################################################
# SPLIT_RULES
####################################################################################################################################

split_rules = translator.TranslatorByRegex([
    (r'(RSS_...._..._\w+_[IE])_(TAU\w+)\.(.*)', 0, (r'\1', r'_\2', r'.\3')),
])

####################################################################################################################################
# OPUS_TYPE
#
# Used for indicating the type of a data file as it will appear in OPUS, e.g., "Raw Data", "Calibrated Data", etc. The tuple
# returned is (category, rank, slug, title, selected) where:
#   category is 'browse', 'diagram', or a meaningful header for special cases like 'Voyager ISS', 'Cassini CIRS'
#   rank is the sort order within the category
#   slug is a short string that will appear in URLs
#   title is a meaning title for product, e.g., 'Raw Data (when calibrated is unavailable)'
#   selected is True if the type is selected by default, False otherwise.
#
# These translations take a file's logical path and return a string indicating the file's OPUS_TYPE.
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/.*_TAU_01KM\.(TAB|LBL)',  0, ('Cassini RSS', 10, 'corss_occ_best_res', 'Occultation Profile (~1 km res)', True)),
    (r'volumes/.*_TAU_1400M\.(TAB|LBL)', 0, ('Cassini RSS', 10, 'corss_occ_best_res', 'Occultation Profile (~1 km res)', True)),
    (r'volumes/.*_TAU_1600M\.(TAB|LBL)', 0, ('Cassini RSS', 10, 'corss_occ_best_res', 'Occultation Profile (~1 km res)', True)),
    (r'volumes/.*_TAU_2400M\.(TAB|LBL)', 0, ('Cassini RSS', 10, 'corss_occ_best_res', 'Occultation Profile (~1 km res)', True)),
    (r'volumes/.*_TAU_3000M\.(TAB|LBL)', 0, ('Cassini RSS', 10, 'corss_occ_best_res', 'Occultation Profile (~1 km res)', True)),
    (r'volumes/.*_TAU_4000M\.(TAB|LBL)', 0, ('Cassini RSS', 10, 'corss_occ_best_res', 'Occultation Profile (~1 km res)', True)),
    (r'volumes/.*_TAU_10KM\.(TAB|LBL)',  0, ('Cassini RSS', 20, 'corss_occ_10km_res', 'Occultation Profile (10 km res)', True)),

    (r'volumes/.*_DLP_500M\.(TAB|LBL)',  0, ('Cassini RSS', 30, 'corss_occ_dlp', 'Diffraction-Ltd Occultation Profile', True)),
    (r'volumes/.*_CAL\.(TAB|LBL)',       0, ('Cassini RSS', 40, 'corss_occ_cal', 'Occultation Calibration Parameters',  True)),
    (r'volumes/.*_GEO\.(TAB|LBL)',       0, ('Cassini RSS', 50, 'corss_occ_geo', 'Occultation Geometry Parameters',     True)),

    (r'volumes/.*_(DSN_Elevation|TimeLine_Figure|TimeLine_Table|Summary|OccTrack_Geometry)\.(pdf|LBL)',
                                         0, ('Cassini RSS', 60, 'corss_occ_doc', 'Occultation Documentation', True)),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

opus_products = translator.TranslatorByRegex([
    (r'.*/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/.*/(Rev...)(C?[IE])_(RSS_...._..._..._[EI]).*', 0,
                [r'volumes/CORSS_8xxx*/\2/data/\3/\3\4/\3\4_\5/*',
                 r'volumes/CORSS_8xxx_v1/\2/EASYDATA/\3\4_\5/*',
                 r'volumes/CORSS_8xxx*/\2/data/\3/\3_DSN_Elevation.LBL',
                 r'volumes/CORSS_8xxx*/\2/data/\3/\3_DSN_Elevation.pdf',
                 r'volumes/CORSS_8xxx*/\2/data/\3/\3_TimeLine_Figure.LBL',
                 r'volumes/CORSS_8xxx*/\2/data/\3/\3_TimeLine_Figure.pdf',
                 r'volumes/CORSS_8xxx*/\2/data/\3/\3_TimeLine_Table.LBL',
                 r'volumes/CORSS_8xxx*/\2/data/\3/\3_TimeLine_Table.pdf',
                 r'volumes/CORSS_8xxx*/\2/browse/\3_OccTrack_Geometry.LBL',
                 r'volumes/CORSS_8xxx*/\2/browse/\3_OccTrack_Geometry.pdf',
                 r'previews/CORSS_8xxx/\2/data/\3/\3\4/\3\4_\5/*',
                 r'previews/CORSS_8xxx/\2/data/\3/\3_DSN_Elevation_full.jpg',
                 r'previews/CORSS_8xxx/\2/data/\3/\3_DSN_Elevation_med.jpg',
                 r'previews/CORSS_8xxx/\2/data/\3/\3_DSN_Elevation_small.jpg',
                 r'previews/CORSS_8xxx/\2/data/\3/\3_DSN_Elevation_thumb.jpg',
                 r'previews/CORSS_8xxx/\2/data/\3/\3_TimeLine_Figure_full.jpg',
                 r'previews/CORSS_8xxx/\2/data/\3/\3_TimeLine_Figure_med.jpg',
                 r'previews/CORSS_8xxx/\2/data/\3/\3_TimeLine_Figure_small.jpg',
                 r'previews/CORSS_8xxx/\2/data/\3/\3_TimeLine_Figure_thumb.jpg',
                 r'previews/CORSS_8xxx/\2/data/\3/\3_TimeLine_Table_full.jpg',
                 r'previews/CORSS_8xxx/\2/data/\3/\3_TimeLine_Table_med.jpg',
                 r'previews/CORSS_8xxx/\2/data/\3/\3_TimeLine_Table_small.jpg',
                 r'previews/CORSS_8xxx/\2/data/\3/\3_TimeLine_Table_thumb.jpg',
                 r'previews/CORSS_8xxx/\2/browse/\3_OccTrack_Geometry_full.jpg',
                 r'previews/CORSS_8xxx/\2/browse/\3_OccTrack_Geometry_med.jpg',
                 r'previews/CORSS_8xxx/\2/browse/\3_OccTrack_Geometry_small.jpg',
                 r'previews/CORSS_8xxx/\2/browse/\3_OccTrack_Geometry_thumb.jpg',
                 r'metadata/CORSS_8xxx/\2/CORSS_8001_index.lbl',
                 r'metadata/CORSS_8xxx/\2/CORSS_8001_index.tab',
                 r'metadata/CORSS_8xxx/\2/CORSS_8001_profile_index.lbl',
                 r'metadata/CORSS_8xxx/\2/CORSS_8001_profile_index.tab',
                 r'metadata/CORSS_8xxx/\2/CORSS_8001_supplemental_index.lbl',
                 r'metadata/CORSS_8xxx/\2/CORSS_8001_supplemental_index.tab',
                ]),
])

####################################################################################################################################
# OPUS_ID
####################################################################################################################################

opus_id = translator.TranslatorByRegex([
    (r'.*/CORSS_8xxx.*/CORSS_8.../(data|browse).*/(Rev...C?)[IE]_RSS_(....)_(...)_(...)_([IE]).*', 0,
                        r'co-rss-occ-\3-\4-#LOWER#\2-\5-\6'),
    (r'.*/CORSS_8xxx_v1/CORSS_8.../EASYDATA.*/Rev(\d\d)(C?)[IE]_RSS_(....)_(...)_(...)_([IE]).*', 0,
                        r'co-rss-occ-\3-\4-#LOWER#rev0\1\2-\5-\6'),
])

####################################################################################################################################
# OPUS_ID_TO_PRIMARY_LOGICAL_PATH
####################################################################################################################################

opus_id_to_primary_logical_path = translator.TranslatorByRegex([
  (r'co-rss-occ-rev(...)(c?)(i|e)-(\d{4})-(\d{3})-(\w{3})', 0,
    [r'volumes/CORSS_8xxx/CORSS_8001/data/Rev\1/Rev\1#UPPER#\2\3#MIXED#/Rev\1#UPPER#\2\3_RSS_\4_\5_\6_\3/RSS_\4_\5_\6_\3_TAU_01KM.TAB',
     r'volumes/CORSS_8xxx/CORSS_8001/data/Rev\1/Rev\1#UPPER#\2\3#MIXED#/Rev\1#UPPER#\2\3_RSS_\4_\5_\6_\3/RSS_\4_\5_\6_\3_TAU_*00M.TAB']),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class CORSS_8xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('CORSS_8xxx', re.I, 'CORSS_8xxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS
    SPLIT_RULES = split_rules + pdsfile.PdsFile.SPLIT_RULES

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_PRODUCTS = opus_products
    OPUS_ID = opus_id
    OPUS_ID_TO_PRIMARY_LOGICAL_PATH = opus_id_to_primary_logical_path

    VIEWABLES = {
        'default': default_viewables,
        'diagram': diagram_viewables,
    }

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']  = associations_to_volumes
    ASSOCIATIONS['previews'] = associations_to_previews
    ASSOCIATIONS['diagrams'] = associations_to_diagrams
    ASSOCIATIONS['metadata'] = associations_to_metadata

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS = translator.TranslatorByRegex([(r'co-rss-occ-.*', 0, CORSS_8xxx)]) + \
                                      pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['CORSS_8xxx'] = CORSS_8xxx

####################################################################################################################################
