####################################################################################################################################
# rules/VG_28xx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

SUN_DICT = """{
    "N1": "Neptune",
    "S1": "Saturn",
    "U1": "Uranus sigma Sgr",
    "U2": "Uranus beta Per"}""".replace('\n','')

SU_DICT = """{
    "S": "Saturn",
    "U": "Uranus"}""".replace('\n','')

URING_DICT = """{
    "6": "six",
    "5": "five",
    "4": "four",
    "A": "alpha",
    "B": "beta",
    "N": "eta",
    "G": "gamma",
    "D": "delta",
    "L": "lambda",
    "E": "epsilon"}""".replace('\n','')

IE_DICT = """{
    "I": " ingress",
    "E": " egress"}""".replace('\n','')

KIND = """{
    "C": " calibration model",
    "D": " edited raw data",
    "G": " geometry model",
    "J": " jitter data",
    "N": " stellar background data",
    "R": " raw data",
    "T": " trajectory data",
    "V": " vector table",
    "W": " spectral time series"}""".replace('\n','')

KIND_UC = """{
    "C": "Calibration model",
    "D": "Edited raw data",
    "F": "Sub-sampled/filtered ring profiles",
    "G": "Geometry model",
    "J": "Jitter data",
    "N": "Stellar background data",
    "R": "Raw data",
    "T": "Trajectory data",
    "V": "Vector table",
    "W": "Spectral time series"}""".replace('\n','')

NEXT = """{
    "5": "6",
    "6": "7",
    "7": "8",
    "8": "9",
    "9": "10",
    "10": "11",
    "11": "12",
    "12": "13",
    "13": "14"}""".replace('\n','')

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'.*/EDITDATA', re.I, ('Edited raw data',                  'SERIESDIR')),
    (r'.*/FOVMAPS',  re.I, ('Field-of-view maps',               'IMAGEDIR' )),
    (r'.*/IMAGES',   re.I, ('Star reference image files',       'IMAGEDIR' )),
    (r'.*/JITTER',   re.I, ('Pointing data',                    'GEOMDIR'  )),
    (r'.*/NOISDATA', re.I, ('Stellar background data',          'DATADIR'  )),
    (r'.*/RAWDATA',  re.I, ('Raw data',                         'DATADIR'  )),
    (r'.*/TRAJECT',  re.I, ('Trajectory data',                  'GEOMDIR'  )),
    (r'.*/VECTORS',  re.I, ('Pointing data',                    'GEOMDIR'  )),
    (r'.*/S_RINGS',  re.I, ('Saturn ring occultation data',     'SERIESDIR')),
    (r'.*/U_RINGS',  re.I, ('Uranian ring occultation data',    'SERIESDIR')),
    (r'.*/VECTORS/B1950',    re.I, ('B1950 coordinates',        'GEOMDIR'  )),
    (r'.*/VECTORS/J2000',    re.I, ('J2000 coordinates',        'GEOMDIR'  )),
    (r'.*/VECTORS/RINGANOM', re.I, ('Ring plane coordinates',   'GEOMDIR'  )),

    (r'.*/KM0+_(\d+)',              0, (r'Ring profiles, 0.\1 km sampling'                  , 'SERIESDIR')),
    (r'.*/KM0*(\d+)',               0, (r'Ring profiles, \1 km sampling'                    , 'SERIESDIR')),
    (r'.*/FILTER01',                0, (r'Ring profiles at full resolution'                 , 'SERIESDIR')),
    (r'.*/FILTER0\d',               0, (r'Sub-sampled ring profiles'                        , 'SERIESDIR')),

    (r'.*/[PU]N1C..A\.TAB',         0, (r'Neptune Adams ring calibration model'             , 'SERIES')),
    (r'.*/[PU]N1C..L\.TAB',         0, (r'Neptune LeVerrier ring calibration model'         , 'SERIES')),

    (r'.*/[PU]N1P..\.TAB',          0, (r'Neptune sigma Sgr ring profile'                   , 'SERIES')),
    (r'.*/[PU]N1P..04\.TAB',        0, (r'Neptune sigma Sgr ring profile, 42,500-50,000 km' , 'SERIES')),
    (r'.*/[PU]N1P..07\.TAB',        0, (r'Neptune sigma Sgr ring profile, 70,000-76,000 km' , 'SERIES')),
    (r'.*/[PU]N1P..0(\d)\.TAB',     0, (r'Neptune sigma Sgr ring profile, \g<1>0,000-' + NEXT + r'["\1"]0,000 km', 'SERIES')),
    (r'.*/[PU]S1P..\.TAB',          0, (r'Saturn delta Sco ring profile'                    , 'SERIES')),
    (r'.*/[PU]S1P..07\.TAB',        0, (r'Saturn delta Sco ring profile, 72,000-80,000 km'  , 'SERIES')),
    (r'.*/[PU]S1P..14\.TAB',        0, (r'Saturn delta Sco ring profile, 140,000-142,500 km', 'SERIES')),
    (r'.*/[PU]S1P..0*(\d+)\.TAB',   0, (r'Saturn delta Sco ring profile, \g<1>0,000-' + NEXT + r'["\1"]0,000 km', 'SERIES')),
    (r'.*/[PU]S1P..\.TAB',          0, (r'Saturn delta Sco ring profile'                    , 'SERIES')),

    (r'.*/US2P\w+\.(DAT|TAB)',      0, (r'Saturn delta Sco brief ingress ring profile'      , 'SERIES')),
    (r'.*/US3P\w+\.(DAT|TAB)',      0, (r'Saturn iota Her C ring profile (Voyager 1)'       , 'SERIES')),
    (r'.*/US2D\w+\.(DAT|TAB)',      0, (r'Saturn delta Sco ingress edited raw data'         , 'SERIES')),
    (r'.*/US3D\w+\.(DAT|TAB)',      0, (r'Saturn iota Her C ring edited raw data'           , 'SERIES')),
    (r'.*/US2R\w+\.(DAT|TAB)',      0, (r'Saturn delta Sco ingress raw data'                , 'SERIES')),
    (r'.*/US3R\w+\.(DAT|TAB)',      0, (r'Saturn iota Her C ring raw data'                  , 'SERIES')),
    (r'.*/US2T\w+\.(DAT|TAB)',      0, (r'Saturn delta Sco ingress trajectory data'         , 'SERIES')),
    (r'.*/US3T\w+\.(DAT|TAB)',      0, (r'Saturn iota Her C ring trajectory data'           , 'SERIES')),
    (r'.*/US2W\w+\.(DAT|TAB)',      0, (r'Saturn delta Sco ingress edited raw spectra'      , 'SERIES')),
    (r'.*/US3W\w+\.(DAT|TAB)',      0, (r'Saturn iota Her C ring edited raw spectra'        , 'SERIES')),

    (r'.*/[PU](U[12])P..X(I|E)\.(TAB|DAT)', 0,
            (SUN_DICT   + r'["\1"]' +
             IE_DICT    + r'["\2"]' + ' profile for the equator plane'                      , 'SERIES')),
    (r'.*/[PU](U1|U2)P..([654ABNGDLE])(I|E)\.(TAB|DAT)', 0,
            (SUN_DICT   + r'["\1"]' +
             IE_DICT    + r'["\3"]' + ' profile for ring ' +
             URING_DICT + r'["\2"]'                                                         , 'SERIES')),

    (r'.*/PS2([CDGR])\w+\.(TAB|DAT)', 0,
            (KIND_UC +  r'["\1"] for the Saturn ring occultation, low-rate extension'       , 'SERIES')),
    (r'.*/P(S|U)[3-9](D|R)\w+\.(TAB|DAT)', 0,
            ('Un-occulted star ' +
             KIND    + r'["\2"] from the ' +
             SU_DICT + r'["\1"] flyby'                                                      , 'SERIES')),

    (r'.*/[PU](U[12])([CDGJNRTVW])..([654ABNGDLE])(I|E)\.(TAB|DAT)', 0,
            (KIND_UC    + r'["\2"] for the ' +
             SUN_DICT   + r'["\1"] occultation, ring ' +
             URING_DICT + r'["\3"]' +
             IE_DICT    + r'["\4"]'                                                         , 'SERIES')),
    (r'.*/[PU]([SN]1|U[12])([CDGJNRTVWå])\w+\.(TAB|DAT)', 0,
            (KIND_UC    + r'["\2"] for the ' +
             SUN_DICT   + r'["\1"] ring occultation'                                        , 'SERIES')),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([

    (r'volumes/VG_28xx/VG_2801/[^D].*/P([SUN]\d)[A-Z]\d\d(\w*)\.\w+', 0,
            [r'volumes/VG_28xx/VG_2801/[^D]*/P\1???\2.*',
             r'volumes/VG_28xx/VG_2801/[^D]*/*/P\1???\2.*',
            ]),
    (r'volumes/VG_28xx/VG_2801/[^D].*/P([SUN]\d)[A-Z]\d\d(\d\d)\.\w+', 0,
            [r'volumes/VG_28xx/VG_2801/[^D]*/P\1???.*',
             r'volumes/VG_28xx/VG_2801/[^D]*/*/P\1???.*',
            ]),
    (r'volumes/VG_28xx/VG_2801/[^D].*/P([SUN]\d)[A-Z]\d\d\.\w+', 0,
            [r'volumes/VG_28xx/VG_2801/[^D]*/P\1???[01][0-9].*',
             r'volumes/VG_28xx/VG_2801/[^D]*/*/P\1???[01][0-9].*',
            ]),
    (r'volumes/VG_28xx/VG_2801/[^D].*/P(U\d)[A-Z]\d\d([A-Z][IE]?)\.\w+', 0,
            [r'volumes/VG_28xx/VG_2801/[^D]*/P\1???.*',
             r'volumes/VG_28xx/VG_2801/[^D]*/*/P\1???.*',
            ]),
    (r'volumes/VG_28xx/VG_2801/[^D].*/P([SUN]\d)[A-Z]\d\d\.\w+', 0,
            [r'volumes/VG_28xx/VG_2801/[^D]*/P\1\2???[A-Z][IE].*',
             r'volumes/VG_28xx/VG_2801/[^D]*/P\1\2???[A-Z].*',
            ]),

    (r'volumes/VG_28xx/VG_2802/[^D].*/U([SUN]\d)[A-Z]\d\d(\w*)\.\w+', 0,
            [r'volumes/VG_28xx/VG_2802/[^D]*/U\1???\2.*',
             r'volumes/VG_28xx/VG_2802/[^D]*/*/U\1???\2.*',
            ]),
    (r'volumes/VG_28xx/VG_2802/[^D].*/U(U\d)[A-Z]\d\d([A-Z][IE]?)\.\w+', 0,
            [r'volumes/VG_28xx/VG_2802/[^D]*/U\1???.*',
             r'volumes/VG_28xx/VG_2802/[^D]*/*/U\1???.*',
            ]),
    (r'volumes/VG_28xx/VG_2802/[^D].*/U(U\d)[A-Z]\d\d\.\w+', 0,
            [r'volumes/VG_28xx/VG_2802/[^D]*/U\1???[A-Z][IE].*',
             r'volumes/VG_28xx/VG_2802/[^D]*/U\1???[A-Z].*',
            ]),

    (r'volumes/VG_28xx/VG_2803/([SU]_RINGS)/\w+(|/\w+)/(R[SU]\d)[A-Z]\d(S|U)(\w+)\.\w+', 0,
            [r'volumes/VG_28xx/VG_2803/\1/*/\3..\4\5.*',
             r'volumes/VG_28xx/VG_2803/\1/*/*/\3..\4\5.*',
            ]),
    (r'volumes/VG_28xx/VG_2803/([SU]_RINGS)/\w+(|/\w+)/(R[SU]\d)[A-Z]\d(S|U)\.\w+', 0,
            [r'volumes/VG_28xx/VG_2803/\1/*/\3..\4*.*',
             r'volumes/VG_28xx/VG_2803/\1/*/*/\3..\4*.*',
            ]),
    (r'volumes/VG_28xx/VG_2803/([SU]_RINGS)/\w+(|/\w+)/(R[SU]\d)[A-Z]\d(S|U)(\w+)\.\w+', 0,
            [r'volumes/VG_28xx/VG_2803/\1/*/\3..\4.*',
             r'volumes/VG_28xx/VG_2803/\1/*/*/\3..\4.*',
            ]),
])

associations_to_metadata = translator.TranslatorByRegex([
    (r'volumes/(VG_28xx/VG_28..)/[^D].*/([PUR][SUN]\d[A-Z]\d[SX\d]\w*)\.(TAB|DAT|LBL)', 0,
            r'metadata/\1/*.TAB\2'),
])

associations_to_documents = translator.TranslatorByRegex([
    (r'(volumes/VG_28xx/VG_28..)/\w+/.+', 0, r'\1/DOCUMENT/TUTORIAL.TXT'),
])


####################################################################################################################################
# OPUS_FORMAT
####################################################################################################################################

opus_format = translator.TranslatorByRegex([
    (r'.*\.IMG', 0, ('Binary', 'VICAR')),
])


####################################################################################################################################
# SPLIT_RULES
####################################################################################################################################

split_rules = translator.TranslatorByRegex([
    # VG_2810
    (r'(IS[12]_....._...)_(\w+)\.(.*)$', 0, (r'\1', r'_\2', r'.\3')),
])


####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    # VG_2801
    (r'volumes/.*/VG_2801/EASYDATA/KM000_1/(.*)\.(TAB|LBL)', 0, ('Voyager PPS', 10, 'vgpps_occ_0_1', 'Occultation Profile (0.1 km)', True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM000_2/(.*)\.(TAB|LBL)', 0, ('Voyager PPS', 20, 'vgpps_occ_0_2', 'Occultation Profile (0.2 km)', True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM000_5/(.*)\.(TAB|LBL)', 0, ('Voyager PPS', 30, 'vgpps_occ_0_5', 'Occultation Profile (0.5 km)', True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM001/(.*)\.(TAB|LBL)',   0, ('Voyager PPS', 40, 'vgpps_occ_01',  'Occultation Profile (1 km)',   True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM002/(.*)\.(TAB|LBL)',   0, ('Voyager PPS', 50, 'vgpps_occ_02',  'Occultation Profile (2 km)',   True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM005/(.*)\.(TAB|LBL)',   0, ('Voyager PPS', 60, 'vgpps_occ_05',  'Occultation Profile (5 km)',   True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM010/(.*)\.(TAB|LBL)',   0, ('Voyager PPS', 70, 'vgpps_occ_10',  'Occultation Profile (10 km)',  True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM020/(.*)\.(TAB|LBL)',   0, ('Voyager PPS', 80, 'vgpps_occ_20',  'Occultation Profile (20 km)',  True)),
    (r'volumes/.*/VG_2801/EASYDATA/KM050/(.*)\.(TAB|LBL)',   0, ('Voyager PPS', 90, 'vgpps_occ_50',  'Occultation Profile (50 km)',  True)),

    # VG_2802
    (r'volumes/.*/VG_2802/EASYDATA/FILTER01/(.*)\.(TAB|LBL)', 0, ('Voyager UVS', 10,  'vguvs_occ_full_res',  'Occultation Profile (full res)', True)),
    (r'volumes/.*/VG_2802/EASYDATA/FILTER02/(.*)\.(TAB|LBL)', 0, ('Voyager UVS', 20,  'vguvs_occ_sampled_2', 'Occultation Profile (1/2 res)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/FILTER03/(.*)\.(TAB|LBL)', 0, ('Voyager UVS', 30,  'vguvs_occ_sampled_3', 'Occultation Profile (1/3 res)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/FILTER04/(.*)\.(TAB|LBL)', 0, ('Voyager UVS', 40,  'vguvs_occ_sampled_4', 'Occultation Profile (1/4 res)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/FILTER05/(.*)\.(TAB|LBL)', 0, ('Voyager UVS', 50,  'vguvs_occ_sampled_5', 'Occultation Profile (1/5 res)',  True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM000_2/(.*)\.(TAB|LBL)',  0, ('Voyager UVS', 60,  'vguvs_occ_0_2',       'Occultation Profile (0.2 km)',   True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM000_5/(.*)\.(TAB|LBL)',  0, ('Voyager UVS', 70,  'vguvs_occ_0_5',       'Occultation Profile (0.5 km)',   True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM001/(.*)\.(TAB|LBL)',    0, ('Voyager UVS', 80,  'vguvs_occ_01',        'Occultation Profile (1 km)',     True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM002/(.*)\.(TAB|LBL)',    0, ('Voyager UVS', 90,  'vguvs_occ_02',        'Occultation Profile (2 km)',     True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM005/(.*)\.(TAB|LBL)',    0, ('Voyager UVS', 100, 'vguvs_occ_05',        'Occultation Profile (5 km)',     True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM010/(.*)\.(TAB|LBL)',    0, ('Voyager UVS', 110, 'vguvs_occ_10',        'Occultation Profile (10 km)',    True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM020/(.*)\.(TAB|LBL)',    0, ('Voyager UVS', 120, 'vguvs_occ_20',        'Occultation Profile (20 km)',    True)),
    (r'volumes/.*/VG_2802/EASYDATA/KM050/(.*)\.(TAB|LBL)',    0, ('Voyager UVS', 130, 'vguvs_occ_50',        'Occultation Profile (50 km)',    True)),

    # VG_2803
    (r'volumes/.*/VG_2803/S_RINGS/EASYDATA/KM0.*/RS1P2.*\.(TAB|LBL)', 0, ('Voyager RSS', 10, 'vgrss_occ_s1', '1984 0.4 km reconstruction', True)),
    (r'volumes/.*/VG_2803/S_RINGS/EASYDATA/KM0.*/RS2P2.*\.(TAB|LBL)', 0, ('Voyager RSS', 20, 'vgrss_occ_s2', '1989 0.4 km reconstruction', True)),
    (r'volumes/.*/VG_2803/S_RINGS/EASYDATA/KM0.*/RS3P2.*\.(TAB|LBL)', 0, ('Voyager RSS', 30, 'vgrss_occ_s3', 'Final 1 km reconstruction',  True)),
    (r'volumes/.*/VG_2803/S_RINGS/EASYDATA/KM0.*/RS4P2.*\.(TAB|LBL)', 0, ('Voyager RSS', 40, 'vgrss_occ_s4', 'Final 5 km reconstruction',  True)),
    (r'volumes/.*/VG_2803/U_RINGS/EASYDATA/KM0.*/RU1P2.*\.(TAB|LBL)', 0, ('Voyager RSS', 10, 'vgrss_occ_u1', '0.05 km reconstruction',     True)),
    (r'volumes/.*/VG_2803/U_RINGS/EASYDATA/KM0.*/RU2P2.*\.(TAB|LBL)', 0, ('Voyager RSS', 20, 'vgrss_occ_u2', '0.2 km reconstruction',      True)),
    (r'volumes/.*/VG_2803/U_RINGS/EASYDATA/KM0.*/RU3P2.*\.(TAB|LBL)', 0, ('Voyager RSS', 30, 'vgrss_occ_u3', '0.2 km reconstruction',      True)),
    (r'volumes/.*/VG_2803/U_RINGS/EASYDATA/KM0.*/RU4P2.*\.(TAB|LBL)', 0, ('Voyager RSS', 40, 'vgrss_occ_u4', '0.5 km reconstruction',      True)),
    (r'volumes/.*/VG_2803/U_RINGS/EASYDATA/KM0.*/RU5P2.*\.(TAB|LBL)', 0, ('Voyager RSS', 50, 'vgrss_occ_u5', '1.0 km reconstruction',      True)),

    # VG_2810
    (r'volumes/.*/VG_2810/DATA/.*KM002\.(TAB|LBL)', 0, ('Voyager ISS', 10, 'vgiss_prof_02', 'Intensity Profile (2 km)',  True)),
    (r'volumes/.*/VG_2810/DATA/.*KM004\.(TAB|LBL)', 0, ('Voyager ISS', 20, 'vgiss_prof_04', 'Intensity Profile (4 km)',  True)),
    (r'volumes/.*/VG_2810/DATA/.*KM010\.(TAB|LBL)', 0, ('Voyager ISS', 30, 'vgiss_prof_10', 'Intensity Profile (10 km)', True)),
    (r'volumes/.*/VG_2810/DATA/.*KM020\.(TAB|LBL)', 0, ('Voyager ISS', 40, 'vgiss_prof_20', 'Intensity Profile (20 km)', True)),
])


####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################
# Use of explicit file names means we don't need to invoke glob.glob(); this goes much faster
# TODO: Need to add images when they are available
opus_products = translator.TranslatorByRegex([
    # VG_2801
    # We want files from all resolutions.
    (r'.*/VG_28xx/(VG_28..)/EASYDATA/KM0.*/(PS.|PN.).*\..*', 0,
            [r'volumes/VG_28xx/\1/EASYDATA/KM000_1/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_1/\2*.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_2/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_2/\2*.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_5/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_5/\2*.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM001/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM001/\2*.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM002/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM002/\2*.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM005/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM005/\2*.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM010/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM010/\2*.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM020/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM020/\2*.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM050/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM050/\2*.TAB',
             r'metadata/VG_28xx/\1/\1_index.lbl',
             r'metadata/VG_28xx/\1/\1_index.tab',
             r'metadata/VG_28xx/\1/\1_profile_index.lbl',
             r'metadata/VG_28xx/\1/\1_profile_index.tab',
             r'metadata/VG_28xx/\1/\1_supplemental_index.lbl',
             r'metadata/VG_28xx/\1/\1_supplemental_index.tab',
            ]),
    (r'.*/VG_28xx/(VG_28..)/EASYDATA/KM0.*/(PU.).*((?:6|5|4|A|B|N|G|D|E|L|X)(?:I|E))\..*', 0,
            [r'volumes/VG_28xx/\1/EASYDATA/KM000_1/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_1/\2*\3.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_2/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_2/\2*\3.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_5/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_5/\2*\3.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM001/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM001/\2*\3.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM002/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM002/\2*\3.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM005/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM005/\2*\3.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM010/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM010/\2*\3.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM020/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM020/\2*\3.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM050/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM050/\2*\3.TAB',
             r'metadata/VG_28xx/\1/\1_index.lbl',
             r'metadata/VG_28xx/\1/\1_index.tab',
             r'metadata/VG_28xx/\1/\1_profile_index.lbl',
             r'metadata/VG_28xx/\1/\1_profile_index.tab',
             r'metadata/VG_28xx/\1/\1_supplemental_index.lbl',
             r'metadata/VG_28xx/\1/\1_supplemental_index.tab',
            ]),

    # VG_2802
    # We want files from all resolutions.
    (r'.*/VG_28xx/(VG_28..)/EASYDATA/(?:FILTER.*|KM0.*)/(US.|UN).*\..*', 0,
            [r'volumes/VG_28xx/\1/EASYDATA/FILTER01/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER01/\2*.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER02/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER02/\2*.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER03/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER03/\2*.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER04/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER04/\2*.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER05/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER05/\2*.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_1/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_1/\2*.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_2/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_2/\2*.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_5/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_5/\2*.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM001/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM001/\2*.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM002/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM002/\2*.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM005/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM005/\2*.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM010/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM010/\2*.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM020/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM020/\2*.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM050/\2*.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM050/\2*.TAB',
             r'metadata/VG_28xx/\1/\1_index.lbl',
             r'metadata/VG_28xx/\1/\1_index.tab',
             r'metadata/VG_28xx/\1/\1_profile_index.lbl',
             r'metadata/VG_28xx/\1/\1_profile_index.tab',
             r'metadata/VG_28xx/\1/\1_supplemental_index.lbl',
             r'metadata/VG_28xx/\1/\1_supplemental_index.tab',
            ]),
    (r'.*/VG_28xx/(VG_28..)/EASYDATA/(?:FILTER.*|KM0.*)/(UU).*((?:6|5|4|A|B|N|G|D|E|L|X)(?:I|E))\..*', 0,
            [r'volumes/VG_28xx/\1/EASYDATA/FILTER01/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER01/\2*\3.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER02/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER02/\2*\3.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER03/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER03/\2*\3.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER04/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER04/\2*\3.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER05/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/FILTER05/\2*\3.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_1/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_1/\2*\3.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_2/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_2/\2*\3.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_5/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM000_5/\2*\3.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM001/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM001/\2*\3.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM002/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM002/\2*\3.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM005/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM005/\2*\3.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM010/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM010/\2*\3.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM020/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM020/\2*\3.TAB',
             r'volumes/VG_28xx/\1/EASYDATA/KM050/\2*\3.LBL',
             r'volumes/VG_28xx/\1/EASYDATA/KM050/\2*\3.TAB',
             r'metadata/VG_28xx/\1/\1_index.lbl',
             r'metadata/VG_28xx/\1/\1_index.tab',
             r'metadata/VG_28xx/\1/\1_profile_index.lbl',
             r'metadata/VG_28xx/\1/\1_profile_index.tab',
             r'metadata/VG_28xx/\1/\1_supplemental_index.lbl',
             r'metadata/VG_28xx/\1/\1_supplemental_index.tab',
            ]),

    # VG_2803
    # We want files from the best (smallest) resolutions
    (r'.*/VG_28xx/(VG_28..)/S_RINGS/EASYDATA/KM0.*/RS.*2(S|X).*\..*', 0,
            [r'volumes/VG_28xx/\1/S_RINGS/EASYDATA/KM000_2/RS1P2\2*.LBL',
             r'volumes/VG_28xx/\1/S_RINGS/EASYDATA/KM000_2/RS1P2\2*.TAB',
             r'volumes/VG_28xx/\1/S_RINGS/EASYDATA/KM000_2/RS2P2\2*.LBL',
             r'volumes/VG_28xx/\1/S_RINGS/EASYDATA/KM000_2/RS2P2\2*.TAB',
             r'volumes/VG_28xx/\1/S_RINGS/EASYDATA/KM000_5/RS3P2\2*.LBL',
             r'volumes/VG_28xx/\1/S_RINGS/EASYDATA/KM000_5/RS3P2\2*.TAB',
             r'volumes/VG_28xx/\1/S_RINGS/EASYDATA/KM002_5/RS4P2\2*.LBL',
             r'volumes/VG_28xx/\1/S_RINGS/EASYDATA/KM002_5/RS4P2\2*.TAB',
             r'metadata/VG_28xx/\1/\1_index.lbl',
             r'metadata/VG_28xx/\1/\1_index.tab',
             r'metadata/VG_28xx/\1/\1_profile_index.lbl',
             r'metadata/VG_28xx/\1/\1_profile_index.tab',
             r'metadata/VG_28xx/\1/\1_supplemental_index.lbl',
             r'metadata/VG_28xx/\1/\1_supplemental_index.tab',
            ]),
    (r'.*/VG_28xx/(VG_28..)/U_RINGS/EASYDATA/KM0.*/RU.*2((?:S|X)(?:\w)(?:I|E))\..*', 0,
            [r'volumes/VG_28xx/\1/U_RINGS/EASYDATA/KM00_025/RU1P2\2.LBL',
             r'volumes/VG_28xx/\1/U_RINGS/EASYDATA/KM00_025/RU1P2\2.TAB',
             r'volumes/VG_28xx/\1/U_RINGS/EASYDATA/KM00_025/RU2P2\2.LBL',
             r'volumes/VG_28xx/\1/U_RINGS/EASYDATA/KM00_025/RU2P2\2.TAB',
             r'volumes/VG_28xx/\1/U_RINGS/EASYDATA/KM00_05/RU3P2\2.LBL',
             r'volumes/VG_28xx/\1/U_RINGS/EASYDATA/KM00_05/RU3P2\2.TAB',
             r'volumes/VG_28xx/\1/U_RINGS/EASYDATA/KM00_25/RU4P2\2.LBL',
             r'volumes/VG_28xx/\1/U_RINGS/EASYDATA/KM00_25/RU4P2\2.TAB',
             r'volumes/VG_28xx/\1/U_RINGS/EASYDATA/KM00_05/RU5P2\2.LBL',
             r'volumes/VG_28xx/\1/U_RINGS/EASYDATA/KM00_05/RU5P2\2.TAB',
             r'metadata/VG_28xx/\1/\1_index.lbl',
             r'metadata/VG_28xx/\1/\1_index.tab',
             r'metadata/VG_28xx/\1/\1_profile_index.lbl',
             r'metadata/VG_28xx/\1/\1_profile_index.tab',
             r'metadata/VG_28xx/\1/\1_supplemental_index.lbl',
             r'metadata/VG_28xx/\1/\1_supplemental_index.tab',
            ]),

    # VG_2810
    (r'.*/VG_28xx/(VG_28..)/DATA/(IS\d_P...._...)_KM0.*\..*', 0,
            [r'volumes/VG_28xx/\1/DATA/\2_KM002.LBL',
             r'volumes/VG_28xx/\1/DATA/\2_KM002.TAB',
             r'volumes/VG_28xx/\1/DATA/\2_KM004.LBL',
             r'volumes/VG_28xx/\1/DATA/\2_KM004.TAB',
             r'volumes/VG_28xx/\1/DATA/\2_KM010.LBL',
             r'volumes/VG_28xx/\1/DATA/\2_KM010.TAB',
             r'volumes/VG_28xx/\1/DATA/\2_KM020.LBL',
             r'volumes/VG_28xx/\1/DATA/\2_KM020.TAB',
             r'metadata/VG_28xx/\1/\1_index.lbl',
             r'metadata/VG_28xx/\1/\1_index.tab',
             r'metadata/VG_28xx/\1/\1_profile_index.lbl',
             r'metadata/VG_28xx/\1/\1_profile_index.tab',
             r'metadata/VG_28xx/\1/\1_supplemental_index.lbl',
             r'metadata/VG_28xx/\1/\1_supplemental_index.tab',
            ]),
])


####################################################################################################################################
# OPUS_ID
####################################################################################################################################

opus_id = translator.TranslatorByRegex([
    # VG_2801
    # S RINGS (1981-08-26, egress):
    # 'mission'-'inst'-'inst host'-planet-occ-'year'-'day of year'-'star name'-'direction'
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PS.*\..*',        0, r'vg-pps-2-s-occ-1981-238-delsco-e'),
    # U RINGS (1986-01-24):
    # 'mission'-'inst'-'inst host'-planet-occ-'year'-'day of year'-'ring name'-'star name'-'direction'
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PU1.*6(I|E)\..*', 0, r'vg-pps-2-u-occ-1986-024-six-sigsgr-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PU1.*5(I|E)\..*', 0, r'vg-pps-2-u-occ-1986-024-five-sigsgr-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PU1.*4(I|E)\..*', 0, r'vg-pps-2-u-occ-1986-024-four-sigsgr-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PU1.*A(I|E)\..*', 0, r'vg-pps-2-u-occ-1986-024-alpha-sigsgr-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PU1.*B(I|E)\..*', 0, r'vg-pps-2-u-occ-1986-024-beta-sigsgr-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PU1.*N(I|E)\..*', 0, r'vg-pps-2-u-occ-1986-024-eta-sigsgr-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PU1.*G(I|E)\..*', 0, r'vg-pps-2-u-occ-1986-024-gamma-sigsgr-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PU1.*D(I|E)\..*', 0, r'vg-pps-2-u-occ-1986-024-delta-sigsgr-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PU1.*L(I|E)\..*', 0, r'vg-pps-2-u-occ-1986-024-lambda-sigsgr-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PU1.*E(I|E)\..*', 0, r'vg-pps-2-u-occ-1986-024-epsilon-sigsgr-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PU1.*X(I|E)\..*', 0, r'vg-pps-2-u-occ-1986-024-ringpl-sigsgr-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PU2.*6(I|E)\..*', 0, r'vg-pps-2-u-occ-1986-024-six-betper-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PU2.*5(I|E)\..*', 0, r'vg-pps-2-u-occ-1986-024-five-betper-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PU2.*4(I|E)\..*', 0, r'vg-pps-2-u-occ-1986-024-four-betper-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PU2.*A(I|E)\..*', 0, r'vg-pps-2-u-occ-1986-024-alpha-betper-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PU2.*B(I|E)\..*', 0, r'vg-pps-2-u-occ-1986-024-beta-betper-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PU2.*N(I|E)\..*', 0, r'vg-pps-2-u-occ-1986-024-eta-betper-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PU2.*G(I|E)\..*', 0, r'vg-pps-2-u-occ-1986-024-gamma-betper-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PU2.*D(I|E)\..*', 0, r'vg-pps-2-u-occ-1986-024-delta-betper-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PU2.*L(I|E)\..*', 0, r'vg-pps-2-u-occ-1986-024-lambda-betper-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PU2.*E(I|E)\..*', 0, r'vg-pps-2-u-occ-1986-024-epsilon-betper-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PU2.*X(I|E)\..*', 0, r'vg-pps-2-u-occ-1986-024-ringpl-betper-#LOWER#\1'),
    # N RINGS (1989-08-24, ingress):
    # 'mission'-'inst'-'inst host'-planet-occ-'year'-'day of year'-'star name'-'direction'
    (r'.*/VG_28xx/VG_2801/EASYDATA/KM0.*/PN.*\..*',        0, r'vg-pps-2-n-occ-1989-236-sigsgr-i'),

    # VG_2802
    # S RINGS:
    # 'mission'-'inst'-'inst host'-planet-occ-'year'-'day of year'-'star name'-'direction'
    # US1 (1981-08-26, egress), US2 (1981-08-25, ingress), US3 (1980-11-12, egress)
    (r'.*/VG_28xx/VG_2802/EASYDATA/(?:FILTER.*|KM0.*)/US1.*\..*',       0, r'vg-uvs-2-s-occ-1981-238-delsco-e'),
    (r'.*/VG_28xx/VG_2802/EASYDATA/(?:FILTER.*|KM0.*)/US2.*\..*',       0, r'vg-uvs-2-s-occ-1981-237-delsco-i'),
    (r'.*/VG_28xx/VG_2802/EASYDATA/(?:FILTER.*|KM0.*)/US3.*\..*',       0, r'vg-uvs-1-s-occ-1980-317-iother-e'),
    # U RINGS (1986-01-24):
    # 'mission'-'inst'-'inst host'-planet-occ-'year'-'day of year'-'ring name'-'star name'-'direction'
    (r'.*/VG_28xx/VG_2802/EASYDATA/(?:FILTER.*|KM0.*)/UU..*6(I|E)\..*', 0, r'vg-uvs-2-u-occ-1986-024-six-sigsgr-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2802/EASYDATA/(?:FILTER.*|KM0.*)/UU..*5(I|E)\..*', 0, r'vg-uvs-2-u-occ-1986-024-five-sigsgr-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2802/EASYDATA/(?:FILTER.*|KM0.*)/UU..*4(I|E)\..*', 0, r'vg-uvs-2-u-occ-1986-024-four-sigsgr-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2802/EASYDATA/(?:FILTER.*|KM0.*)/UU..*A(I|E)\..*', 0, r'vg-uvs-2-u-occ-1986-024-alpha-sigsgr-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2802/EASYDATA/(?:FILTER.*|KM0.*)/UU..*B(I|E)\..*', 0, r'vg-uvs-2-u-occ-1986-024-beta-sigsgr-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2802/EASYDATA/(?:FILTER.*|KM0.*)/UU..*N(I|E)\..*', 0, r'vg-uvs-2-u-occ-1986-024-eta-sigsgr-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2802/EASYDATA/(?:FILTER.*|KM0.*)/UU..*G(I|E)\..*', 0, r'vg-uvs-2-u-occ-1986-024-gamma-sigsgr-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2802/EASYDATA/(?:FILTER.*|KM0.*)/UU..*D(I|E)\..*', 0, r'vg-uvs-2-u-occ-1986-024-delta-sigsgr-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2802/EASYDATA/(?:FILTER.*|KM0.*)/UU..*L(I|E)\..*', 0, r'vg-uvs-2-u-occ-1986-024-lambda-sigsgr-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2802/EASYDATA/(?:FILTER.*|KM0.*)/UU..*E(I|E)\..*', 0, r'vg-uvs-2-u-occ-1986-024-epsilon-sigsgr-#LOWER#\1'),
    (r'.*/VG_28xx/VG_2802/EASYDATA/(?:FILTER.*|KM0.*)/UU..*X(I|E)\..*', 0, r'vg-uvs-2-u-occ-1986-024-ringpl-sigsgr-#LOWER#\1'),
    # N RINGS (1989-08-24):
    # 'mission'-'inst'-'inst host'-planet-occ-'year'-'day of year'-'star name'-'direction'
    (r'.*/VG_28xx/VG_2802/EASYDATA/(?:FILTER.*|KM0.*)/UN..*\..*',       0, r'vg-uvs-2-n-occ-1989-236-sigsgr-i'),

    # VG_2803
    # S RINGS (1980-11-13, egress):
    # 'mission'-'inst'-'inst host'-planet-occ-'year'-'day of year'-'band name + 2-digit DSN'-'direction'
    # NOTE: replace matched group from \n to \g<n> to make sure match_obj.expand
    # return the correct result when numbers are right after the matched group.
    (r'.*/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM0.*/RS.*2(S|X)..\..*',     0, r'vg-rss-1-s-occ-1980-318-#LOWER#\g<1>63-e'),
    # U RINGS (1986-01-24):
    # 'mission'-'inst'-'inst host'-planet-occ-'year'-'day of year'-'ring name'-'band name + 2-digit DSN'-'direction'
    (r'.*/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM0.*/RU.*2(S|X)6(I|E)\..*', 0, r'vg-rss-2-u-occ-1986-024-six-#LOWER#\g<1>43-\2'),
    (r'.*/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM0.*/RU.*2(S|X)5(I|E)\..*', 0, r'vg-rss-2-u-occ-1986-024-five-#LOWER#\g<1>43-\2'),
    (r'.*/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM0.*/RU.*2(S|X)4(I|E)\..*', 0, r'vg-rss-2-u-occ-1986-024-four-#LOWER#\g<1>43-\2'),
    (r'.*/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM0.*/RU.*2(S|X)A(I|E)\..*', 0, r'vg-rss-2-u-occ-1986-024-alpha-#LOWER#\g<1>43-\2'),
    (r'.*/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM0.*/RU.*2(S|X)B(I|E)\..*', 0, r'vg-rss-2-u-occ-1986-024-beta-#LOWER#\g<1>43-\2'),
    (r'.*/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM0.*/RU.*2(S|X)N(I|E)\..*', 0, r'vg-rss-2-u-occ-1986-024-eta-#LOWER#\g<1>43-\2'),
    (r'.*/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM0.*/RU.*2(S|X)G(I|E)\..*', 0, r'vg-rss-2-u-occ-1986-024-gamma-#LOWER#\g<1>43-\2'),
    (r'.*/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM0.*/RU.*2(S|X)D(I|E)\..*', 0, r'vg-rss-2-u-occ-1986-024-delta-#LOWER#\g<1>43-\2'),
    (r'.*/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM0.*/RU.*2(S|X)L(I|E)\..*', 0, r'vg-rss-2-u-occ-1986-024-lambda-#LOWER#\g<1>43-\2'),
    (r'.*/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM0.*/RU.*2(S|X)E(I|E)\..*', 0, r'vg-rss-2-u-occ-1986-024-epsilon-#LOWER#\g<1>43-\2'),

    # VG_2810
    # 'mission'-'inst'-'inst host'-prof
    (r'.*/VG_28xx/VG_2810/DATA/IS(\d)_P.*\..*', 0, r'vg-iss-\1-prof'),
])


####################################################################################################################################
# FILESPEC_TO_VOLSET
####################################################################################################################################

filespec_to_volset = translator.TranslatorByRegex([
    (r'VG_28\d{2}.*', 0, r'VG_28xx'),
])

####################################################################################################################################
# OPUS_ID_TO_PRIMARY_LOGICAL_PATH
####################################################################################################################################

opus_id_to_primary_logical_path = translator.TranslatorByRegex([
    # VG_2801, Satrun: PS1 in KM000_2, Uranus: PU1 in KM000_1, PU2 in KM001
    # Neptune: PN1 in KM002
    (r'vg-pps-2-s-occ-1981-238-(.*)-e',                  0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PS1P0107.TAB'),
    (r'vg-pps-2-u-occ-1986-024-six-sigsgr-([ie])',       0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM000_1/PU1P016#UPPER#\1.TAB'),
    (r'vg-pps-2-u-occ-1986-024-five-sigsgr-([ie])',      0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM000_1/PU1P015#UPPER#\1.TAB'),
    (r'vg-pps-2-u-occ-1986-024-four-sigsgr-([ie])',      0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM000_1/PU1P014#UPPER#\1.TAB'),
    (r'vg-pps-2-u-occ-1986-024-alpha-sigsgr-([ie])',     0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM000_1/PU1P01A#UPPER#\1.TAB'),
    (r'vg-pps-2-u-occ-1986-024-beta-sigsgr-([ie])',      0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM000_1/PU1P01B#UPPER#\1.TAB'),
    (r'vg-pps-2-u-occ-1986-024-eta-sigsgr-([ie])',       0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM000_1/PU1P01N#UPPER#\1.TAB'),
    (r'vg-pps-2-u-occ-1986-024-gamma-sigsgr-([ie])',     0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM000_1/PU1P01G#UPPER#\1.TAB'),
    (r'vg-pps-2-u-occ-1986-024-delta-sigsgr-([ie])',     0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM000_1/PU1P01D#UPPER#\1.TAB'),
    (r'vg-pps-2-u-occ-1986-024-lambda-sigsgr-([ie])',    0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM000_1/PU1P01L#UPPER#\1.TAB'),
    (r'vg-pps-2-u-occ-1986-024-epsilon-sigsgr-([ie])',   0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM000_1/PU1P01E#UPPER#\1.TAB'),
    (r'vg-pps-2-u-occ-1986-024-ringpl-sigsgr-([ie])', 0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM000_1/PU1P01X#UPPER#\1.TAB'),
    (r'vg-pps-2-u-occ-1986-024-six-betper-([ie])',       0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PU2P016#UPPER#\1.TAB'),
    (r'vg-pps-2-u-occ-1986-024-five-betper-([ie])',      0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PU2P015#UPPER#\1.TAB'),
    (r'vg-pps-2-u-occ-1986-024-four-betper-([ie])',      0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PU2P014#UPPER#\1.TAB'),
    (r'vg-pps-2-u-occ-1986-024-alpha-betper-([ie])',     0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PU2P01A#UPPER#\1.TAB'),
    (r'vg-pps-2-u-occ-1986-024-beta-betper-([ie])',      0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PU2P01B#UPPER#\1.TAB'),
    (r'vg-pps-2-u-occ-1986-024-eta-betper-([ie])',       0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PU2P01N#UPPER#\1.TAB'),
    (r'vg-pps-2-u-occ-1986-024-gamma-betper-([ie])',     0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PU2P01G#UPPER#\1.TAB'),
    (r'vg-pps-2-u-occ-1986-024-delta-betper-([ie])',     0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PU2P01D#UPPER#\1.TAB'),
    (r'vg-pps-2-u-occ-1986-024-lambda-betper-([ie])',    0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PU2P01L#UPPER#\1.TAB'),
    (r'vg-pps-2-u-occ-1986-024-epsilon-betper-([ie])',   0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PU2P01E#UPPER#\1.TAB'),
    (r'vg-pps-2-u-occ-1986-024-ringpl-betper-([ie])', 0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PU2P01X#UPPER#\1.TAB'),
    (r'vg-pps-2-n-occ-1989-236-(.*)-i',                  0, r'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PN1P104.TAB'),

    # VG_2802, Satrun: FILTER01, Uranus: FILTER01, Neptune: FILTER01
    (r'vg-uvs-2-s-occ-1981-238-delsco-e',                0, r'volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/US1F01.TAB'),
    (r'vg-uvs-2-s-occ-1981-237-delsco-i',                0, r'volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/US2F01.TAB'),
    (r'vg-uvs-1-s-occ-1980-317-iother-e',                0, r'volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/US3F01.TAB'),
    (r'vg-uvs-2-u-occ-1986-024-six-sigsgr-([ie])',       0, r'volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/UU1F016#UPPER#\1.TAB'),
    (r'vg-uvs-2-u-occ-1986-024-five-sigsgr-([ie])',      0, r'volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/UU1F015#UPPER#\1.TAB'),
    (r'vg-uvs-2-u-occ-1986-024-four-sigsgr-([ie])',      0, r'volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/UU1F014#UPPER#\1.TAB'),
    (r'vg-uvs-2-u-occ-1986-024-alpha-sigsgr-([ie])',     0, r'volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/UU1F01A#UPPER#\1.TAB'),
    (r'vg-uvs-2-u-occ-1986-024-beta-sigsgr-([ie])',      0, r'volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/UU1F01B#UPPER#\1.TAB'),
    (r'vg-uvs-2-u-occ-1986-024-eta-sigsgr-([ie])',       0, r'volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/UU1F01N#UPPER#\1.TAB'),
    (r'vg-uvs-2-u-occ-1986-024-gamma-sigsgr-([ie])',     0, r'volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/UU1F01G#UPPER#\1.TAB'),
    (r'vg-uvs-2-u-occ-1986-024-delta-sigsgr-([ie])',     0, r'volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/UU1F01D#UPPER#\1.TAB'),
    (r'vg-uvs-2-u-occ-1986-024-lambda-sigsgr-([ie])',    0, r'volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/UU1F01L#UPPER#\1.TAB'),
    (r'vg-uvs-2-u-occ-1986-024-epsilon-sigsgr-([ie])',   0, r'volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/UU1F01E#UPPER#\1.TAB'),
    (r'vg-uvs-2-u-occ-1986-024-ringpl-sigsgr-([ie])', 0, r'volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/UU1F01X#UPPER#\1.TAB'),
    (r'vg-uvs-2-n-occ-1989-236-sigsgr-i',                0, r'volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/UN1F01.TAB'),

    # VG_2803, pick the smallest resolutions
    # S RINGS: KM000_2, U RINGS: KM00_25
    (r'vg-rss-1-s-occ-1980-318-(.*)63-e',              0, r'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_2/RS1P2#UPPER#\g<1>07.TAB'),
    (r'vg-rss-2-u-occ-1986-024-six-(.*)43-([ie])',     0, r'volumes/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM00_25/RU4P2#UPPER#\g<1>6\2.TAB'),
    (r'vg-rss-2-u-occ-1986-024-five-(.*)43-([ie])',    0, r'volumes/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM00_25/RU4P2#UPPER#\g<1>5\2.TAB'),
    (r'vg-rss-2-u-occ-1986-024-four-(.*)43-([ie])',    0, r'volumes/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM00_25/RU4P2#UPPER#\g<1>4\2.TAB'),
    (r'vg-rss-2-u-occ-1986-024-alpha-(.*)43-([ie])',   0, r'volumes/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM00_25/RU4P2#UPPER#\g<1>A\2.TAB'),
    (r'vg-rss-2-u-occ-1986-024-beta-(.*)43-([ie])',    0, r'volumes/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM00_25/RU4P2#UPPER#\g<1>B\2.TAB'),
    (r'vg-rss-2-u-occ-1986-024-eta-(.*)43-([ie])',     0, r'volumes/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM00_25/RU4P2#UPPER#\g<1>N\2.TAB'),
    (r'vg-rss-2-u-occ-1986-024-gamma-(.*)43-([ie])',   0, r'volumes/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM00_25/RU4P2#UPPER#\g<1>G\2.TAB'),
    (r'vg-rss-2-u-occ-1986-024-delta-(.*)43-([ie])',   0, r'volumes/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM00_25/RU4P2#UPPER#\g<1>D\2.TAB'),
    (r'vg-rss-2-u-occ-1986-024-lambda-(.*)43-([ie])',  0, r'volumes/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM00_25/RU4P2#UPPER#\g<1>L\2.TAB'),
    (r'vg-rss-2-u-occ-1986-024-epsilon-(.*)43-([ie])', 0, r'volumes/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM00_25/RU4P2#UPPER#\g<1>E\2.TAB'),

    # VG_2810, pick the smallest resolutions
    (r'vg-iss-([12])-prof', 0, r'volumes/VG_28xx/VG_2810/DATA/IS\1_*_KM002.TAB'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class VG_28xx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('VG_28xx', re.I, 'VG_28xx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_FORMAT = opus_format + pdsfile.PdsFile.OPUS_FORMAT
    OPUS_PRODUCTS = opus_products
    OPUS_ID = opus_id
    OPUS_ID_TO_PRIMARY_LOGICAL_PATH = opus_id_to_primary_logical_path

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']   += associations_to_volumes
    ASSOCIATIONS['metadata']  += associations_to_metadata
    ASSOCIATIONS['documents'] += associations_to_documents

    pdsfile.PdsFile.FILESPEC_TO_VOLSET = filespec_to_volset + pdsfile.PdsFile.FILESPEC_TO_VOLSET

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS = translator.TranslatorByRegex([(r'TBD', 0, VG_28xx)]) + \
                                      pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS = translator.TranslatorByRegex([(r'vg-pps.*occ.*', 0, VG_28xx)]) + \
                                      translator.TranslatorByRegex([(r'vg-uvs.*occ.*', 0, VG_28xx)]) + \
                                      translator.TranslatorByRegex([(r'vg-rss.*occ.*', 0, VG_28xx)]) + \
                                      translator.TranslatorByRegex([(r'vg-iss.*prof', 0, VG_28xx)]) + \
                                      pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS


####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['VG_28xx'] = VG_28xx

####################################################################################################################################


####################################################################################################################################
# Unit tests
####################################################################################################################################

import pytest
from .pytest_support import *
# TODO: Need to update the expected results to have profile index files when
# shelves files are updated.
@pytest.mark.parametrize(
    'input_path,expected',
    [
        # VG_2801
        ('volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PS1P0107.TAB',
            {('Voyager PPS',
              20,
              'vgpps_occ_0_2',
              'Occultation Profile (0.2 km)',
              True): ['volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PS1P0114.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PS1P0114.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PS1P0113.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PS1P0113.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PS1P0112.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PS1P0112.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PS1P0111.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PS1P0111.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PS1P0110.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PS1P0110.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PS1P0109.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PS1P0109.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PS1P0108.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PS1P0108.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PS1P0107.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PS1P0107.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PS1P0107.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PS1P0107.LBL'],
             ('Voyager PPS',
              30,
              'vgpps_occ_0_5',
              'Occultation Profile (0.5 km)',
              True): ['volumes/VG_28xx/VG_2801/EASYDATA/KM000_5/PS1P0114.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_5/PS1P0114.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_5/PS1P0113.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_5/PS1P0113.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_5/PS1P0112.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_5/PS1P0112.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_5/PS1P0111.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_5/PS1P0111.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_5/PS1P0110.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_5/PS1P0110.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_5/PS1P0109.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_5/PS1P0109.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_5/PS1P0108.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_5/PS1P0108.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_5/PS1P0107.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_5/PS1P0107.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_5/PS1P0107.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_5/PS1P0107.LBL'],
             ('Voyager PPS',
              40,
              'vgpps_occ_01',
              'Occultation Profile (1 km)',
              True): ['volumes/VG_28xx/VG_2801/EASYDATA/KM001/PS1P0114.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PS1P0114.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PS1P0113.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PS1P0113.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PS1P0112.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PS1P0112.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PS1P0111.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PS1P0111.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PS1P0110.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PS1P0110.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PS1P0109.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PS1P0109.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PS1P0108.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PS1P0108.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PS1P0107.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PS1P0107.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PS1P0107.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PS1P0107.LBL'],
             ('Voyager PPS',
              50,
              'vgpps_occ_02',
              'Occultation Profile (2 km)',
              True): ['volumes/VG_28xx/VG_2801/EASYDATA/KM002/PS1P0114.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM002/PS1P0114.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM002/PS1P0113.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM002/PS1P0113.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM002/PS1P0112.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM002/PS1P0112.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM002/PS1P0111.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM002/PS1P0111.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM002/PS1P0110.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM002/PS1P0110.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM002/PS1P0109.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM002/PS1P0109.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM002/PS1P0108.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM002/PS1P0108.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM002/PS1P0107.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM002/PS1P0107.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM002/PS1P0107.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM002/PS1P0107.LBL'],
             ('Voyager PPS',
              60,
              'vgpps_occ_05',
              'Occultation Profile (5 km)',
              True): ['volumes/VG_28xx/VG_2801/EASYDATA/KM005/PS1P01.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM005/PS1P01.LBL'],
             ('Voyager PPS',
              70,
              'vgpps_occ_10',
              'Occultation Profile (10 km)',
              True): ['volumes/VG_28xx/VG_2801/EASYDATA/KM010/PS1P01.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM010/PS1P01.LBL'],
             ('Voyager PPS',
              80,
              'vgpps_occ_20',
              'Occultation Profile (20 km)',
              True): ['volumes/VG_28xx/VG_2801/EASYDATA/KM020/PS1P01.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM020/PS1P01.LBL'],
             ('Voyager PPS',
              90,
              'vgpps_occ_50',
              'Occultation Profile (50 km)',
              True): ['volumes/VG_28xx/VG_2801/EASYDATA/KM050/PS1P01.TAB',
               'volumes/VG_28xx/VG_2801/EASYDATA/KM050/PS1P01.LBL'],
             ('metadata',
              5,
              'rms_index',
              'RMS Node Augmented Index',
              False): ['metadata/VG_28xx/VG_2801/VG_2801_index.tab',
                       'metadata/VG_28xx/VG_2801/VG_2801_index.lbl'],
             ('metadata',
              9,
              'supplemental_index',
              'Supplemental Index',
              False): ['metadata/VG_28xx/VG_2801/VG_2801_supplemental_index.tab',
                       'metadata/VG_28xx/VG_2801/VG_2801_supplemental_index.lbl']}
        ),
        ('volumes/VG_28xx/VG_2801/EASYDATA/KM000_1/PU1P01DE.TAB',
            {('Voyager PPS',
              10,
              'vgpps_occ_0_1',
              'Occultation Profile (0.1 km)',
              True): ['volumes/VG_28xx/VG_2801/EASYDATA/KM000_1/PU1P01DE.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_1/PU1P01DE.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_1/PU1P01DE.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_1/PU1P01DE.LBL'],
             ('Voyager PPS',
              20,
              'vgpps_occ_0_2',
              'Occultation Profile (0.2 km)',
              True): ['volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PU1P01DE.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PU1P01DE.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PU1P01DE.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_2/PU1P01DE.LBL'],
             ('Voyager PPS',
              30,
              'vgpps_occ_0_5',
              'Occultation Profile (0.5 km)',
              True): ['volumes/VG_28xx/VG_2801/EASYDATA/KM000_5/PU1P01DE.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_5/PU1P01DE.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_5/PU1P01DE.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM000_5/PU1P01DE.LBL'],
             ('Voyager PPS',
              40,
              'vgpps_occ_01',
              'Occultation Profile (1 km)',
              True): ['volumes/VG_28xx/VG_2801/EASYDATA/KM001/PU1P01DE.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PU1P01DE.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PU1P01DE.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM001/PU1P01DE.LBL'],
             ('Voyager PPS',
              50,
              'vgpps_occ_02',
              'Occultation Profile (2 km)',
              True): ['volumes/VG_28xx/VG_2801/EASYDATA/KM002/PU1P01DE.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM002/PU1P01DE.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM002/PU1P01DE.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM002/PU1P01DE.LBL'],
             ('Voyager PPS',
              60,
              'vgpps_occ_05',
              'Occultation Profile (5 km)',
              True): ['volumes/VG_28xx/VG_2801/EASYDATA/KM005/PU1P01DE.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM005/PU1P01DE.LBL',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM005/PU1P01DE.TAB',
                      'volumes/VG_28xx/VG_2801/EASYDATA/KM005/PU1P01DE.LBL'],
             ('metadata',
              5,
              'rms_index',
              'RMS Node Augmented Index',
              False): ['metadata/VG_28xx/VG_2801/VG_2801_index.tab',
                       'metadata/VG_28xx/VG_2801/VG_2801_index.lbl'],
             ('metadata',
              9,
              'supplemental_index',
              'Supplemental Index',
              False): ['metadata/VG_28xx/VG_2801/VG_2801_supplemental_index.tab',
                       'metadata/VG_28xx/VG_2801/VG_2801_supplemental_index.lbl']}
        ),
        # VG_2802
        ('volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/US1F01.TAB',
            {('Voyager UVS',
              10,
              'vguvs_occ_full_res',
              'Occultation Profile (full res)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/US1F01.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/US1F01.LBL'],
             ('Voyager UVS',
              20,
              'vguvs_occ_sampled_2',
              'Occultation Profile (1/2 res)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/FILTER02/US1F01.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/FILTER02/US1F01.LBL'],
             ('Voyager UVS',
              30,
              'vguvs_occ_sampled_3',
              'Occultation Profile (1/3 res)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/FILTER03/US1F01.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/FILTER03/US1F01.LBL'],
             ('Voyager UVS',
              40,
              'vguvs_occ_sampled_4',
              'Occultation Profile (1/4 res)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/FILTER04/US1F01.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/FILTER04/US1F01.LBL'],
             ('Voyager UVS',
              50,
              'vguvs_occ_sampled_5',
              'Occultation Profile (1/5 res)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/FILTER05/US1F01.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/FILTER05/US1F01.LBL'],
             ('Voyager UVS',
              100,
              'vguvs_occ_05',
              'Occultation Profile (5 km)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/KM005/US1P01.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/KM005/US1P01.LBL'],
             ('Voyager UVS',
              110,
              'vguvs_occ_10',
              'Occultation Profile (10 km)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/KM010/US1P01.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/KM010/US1P01.LBL'],
             ('Voyager UVS',
              120,
              'vguvs_occ_20',
              'Occultation Profile (20 km)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/KM020/US1P01.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/KM020/US1P01.LBL'],
             ('Voyager UVS',
              130,
              'vguvs_occ_50',
              'Occultation Profile (50 km)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/KM050/US1P01.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/KM050/US1P01.LBL'],
             ('metadata',
              5,
              'rms_index',
              'RMS Node Augmented Index',
              False): ['metadata/VG_28xx/VG_2802/VG_2802_index.tab',
                       'metadata/VG_28xx/VG_2802/VG_2802_index.lbl'],
             ('metadata',
              9,
              'supplemental_index',
              'Supplemental Index',
              False): ['metadata/VG_28xx/VG_2802/VG_2802_supplemental_index.tab',
                       'metadata/VG_28xx/VG_2802/VG_2802_supplemental_index.lbl']}
        ),
        ('volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/UU1F01EE.TAB',
            {('Voyager UVS',
              10,
              'vguvs_occ_full_res',
              'Occultation Profile (full res)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/UU1F01EE.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/UU1F01EE.LBL'],
             ('Voyager UVS',
              20,
              'vguvs_occ_sampled_2',
              'Occultation Profile (1/2 res)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/FILTER02/UU1F01EE.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/FILTER02/UU1F01EE.LBL'],
             ('Voyager UVS',
              30,
              'vguvs_occ_sampled_3',
              'Occultation Profile (1/3 res)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/FILTER03/UU1F01EE.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/FILTER03/UU1F01EE.LBL'],
             ('Voyager UVS',
              40,
              'vguvs_occ_sampled_4',
              'Occultation Profile (1/4 res)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/FILTER04/UU1F01EE.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/FILTER04/UU1F01EE.LBL'],
             ('Voyager UVS',
              50,
              'vguvs_occ_sampled_5',
              'Occultation Profile (1/5 res)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/FILTER05/UU1F01EE.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/FILTER05/UU1F01EE.LBL'],
             ('Voyager UVS',
              70,
              'vguvs_occ_0_5',
              'Occultation Profile (0.5 km)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/KM000_5/UU1P01EE.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/KM000_5/UU1P01EE.LBL'],
             ('Voyager UVS',
              80,
              'vguvs_occ_01',
              'Occultation Profile (1 km)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/KM001/UU1P01EE.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/KM001/UU1P01EE.LBL'],
             ('Voyager UVS',
              90,
              'vguvs_occ_02',
              'Occultation Profile (2 km)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/KM002/UU1P01EE.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/KM002/UU1P01EE.LBL'],
             ('Voyager UVS',
              100,
              'vguvs_occ_05',
              'Occultation Profile (5 km)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/KM005/UU1P01EE.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/KM005/UU1P01EE.LBL'],
             ('metadata',
              5,
              'rms_index',
              'RMS Node Augmented Index',
              False): ['metadata/VG_28xx/VG_2802/VG_2802_index.tab',
                       'metadata/VG_28xx/VG_2802/VG_2802_index.lbl'],
             ('metadata',
              9,
              'supplemental_index',
              'Supplemental Index',
              False): ['metadata/VG_28xx/VG_2802/VG_2802_supplemental_index.tab',
                       'metadata/VG_28xx/VG_2802/VG_2802_supplemental_index.lbl']}
        ),
        ('volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/UN1F01.TAB',
            {('Voyager UVS',
              10,
              'vguvs_occ_full_res',
              'Occultation Profile (full res)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/UN1F01.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/FILTER01/UN1F01.LBL'],
             ('Voyager UVS',
              20,
              'vguvs_occ_sampled_2',
              'Occultation Profile (1/2 res)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/FILTER02/UN1F01.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/FILTER02/UN1F01.LBL'],
             ('Voyager UVS',
              30,
              'vguvs_occ_sampled_3',
              'Occultation Profile (1/3 res)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/FILTER03/UN1F01.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/FILTER03/UN1F01.LBL'],
             ('Voyager UVS',
              40,
              'vguvs_occ_sampled_4',
              'Occultation Profile (1/4 res)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/FILTER04/UN1F01.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/FILTER04/UN1F01.LBL'],
             ('Voyager UVS',
              50,
              'vguvs_occ_sampled_5',
              'Occultation Profile (1/5 res)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/FILTER05/UN1F01.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/FILTER05/UN1F01.LBL'],
             ('Voyager UVS',
              90,
              'vguvs_occ_02',
              'Occultation Profile (2 km)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/KM002/UN1P01.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/KM002/UN1P01.LBL'],
             ('Voyager UVS',
              100,
              'vguvs_occ_05',
              'Occultation Profile (5 km)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/KM005/UN1P01.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/KM005/UN1P01.LBL'],
             ('Voyager UVS',
              110,
              'vguvs_occ_10',
              'Occultation Profile (10 km)',
              True): ['volumes/VG_28xx/VG_2802/EASYDATA/KM010/UN1P01.TAB',
                      'volumes/VG_28xx/VG_2802/EASYDATA/KM010/UN1P01.LBL'],
             ('metadata',
              5,
              'rms_index',
              'RMS Node Augmented Index',
              False): ['metadata/VG_28xx/VG_2802/VG_2802_index.tab',
                       'metadata/VG_28xx/VG_2802/VG_2802_index.lbl'],
             ('metadata',
              9,
              'supplemental_index',
              'Supplemental Index',
              False): ['metadata/VG_28xx/VG_2802/VG_2802_supplemental_index.tab',
                       'metadata/VG_28xx/VG_2802/VG_2802_supplemental_index.lbl']}
        ),
        # VG_2803
        ('volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_2/RS1P2X07.LBL',
            {('Voyager RSS',
              10,
              'vgrss_occ_s1',
              '1984 0.4 km reconstruction',
              True): ['volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_2/RS1P2X14.TAB',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_2/RS1P2X14.LBL',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_2/RS1P2X13.TAB',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_2/RS1P2X13.LBL',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_2/RS1P2X12.TAB',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_2/RS1P2X12.LBL',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_2/RS1P2X11.TAB',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_2/RS1P2X11.LBL',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_2/RS1P2X10.TAB',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_2/RS1P2X10.LBL',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_2/RS1P2X09.TAB',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_2/RS1P2X09.LBL',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_2/RS1P2X08.TAB',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_2/RS1P2X08.LBL',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_2/RS1P2X07.TAB',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_2/RS1P2X07.LBL'],
             ('Voyager RSS',
              30,
              'vgrss_occ_s3',
              'Final 1 km reconstruction',
              True): ['volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_5/RS3P2X14.TAB',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_5/RS3P2X14.LBL',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_5/RS3P2X13.TAB',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_5/RS3P2X13.LBL',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_5/RS3P2X12.TAB',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_5/RS3P2X12.LBL',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_5/RS3P2X11.TAB',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_5/RS3P2X11.LBL',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_5/RS3P2X10.TAB',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_5/RS3P2X10.LBL',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_5/RS3P2X09.TAB',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_5/RS3P2X09.LBL',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_5/RS3P2X08.TAB',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_5/RS3P2X08.LBL',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_5/RS3P2X07.TAB',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM000_5/RS3P2X07.LBL'],
             ('Voyager RSS',
              40,
              'vgrss_occ_s4',
              'Final 5 km reconstruction',
              True): ['volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM002_5/RS4P2X.TAB',
                      'volumes/VG_28xx/VG_2803/S_RINGS/EASYDATA/KM002_5/RS4P2X.LBL'],
             ('metadata',
              5,
              'rms_index',
              'RMS Node Augmented Index',
              False): ['metadata/VG_28xx/VG_2803/VG_2803_index.tab',
                       'metadata/VG_28xx/VG_2803/VG_2803_index.lbl'],
             ('metadata',
              9,
              'supplemental_index',
              'Supplemental Index',
              False): ['metadata/VG_28xx/VG_2803/VG_2803_supplemental_index.tab',
                       'metadata/VG_28xx/VG_2803/VG_2803_supplemental_index.lbl']}
        ),
        ('volumes/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM00_2/RU1P2X4I.TAB',
            {('Voyager RSS',
              10,
              'vgrss_occ_u1',
              '0.05 km reconstruction',
              True): ['volumes/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM00_025/RU1P2X4I.TAB',
                      'volumes/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM00_025/RU1P2X4I.LBL'],
             ('Voyager RSS',
              40,
              'vgrss_occ_u4',
              '0.5 km reconstruction',
              True): ['volumes/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM00_25/RU4P2X4I.TAB',
                      'volumes/VG_28xx/VG_2803/U_RINGS/EASYDATA/KM00_25/RU4P2X4I.LBL'],
             ('metadata',
              5,
              'rms_index',
              'RMS Node Augmented Index',
              False): ['metadata/VG_28xx/VG_2803/VG_2803_index.tab',
                       'metadata/VG_28xx/VG_2803/VG_2803_index.lbl'],
             ('metadata',
              9,
              'supplemental_index',
              'Supplemental Index',
              False): ['metadata/VG_28xx/VG_2803/VG_2803_supplemental_index.tab',
                       'metadata/VG_28xx/VG_2803/VG_2803_supplemental_index.lbl']}
        ),
        # VG_2810
        ('volumes/VG_28xx/VG_2810/DATA/IS2_P0001_V01_KM002.TAB',
            {('Voyager ISS',
              10,
              'vgiss_prof_02',
              'Intensity Profile (2 km)',
              True): ['volumes/VG_28xx/VG_2810/DATA/IS2_P0001_V01_KM002.TAB',
                      'volumes/VG_28xx/VG_2810/DATA/IS2_P0001_V01_KM002.LBL'],
             ('Voyager ISS',
              20,
              'vgiss_prof_04',
              'Intensity Profile (4 km)',
              True): ['volumes/VG_28xx/VG_2810/DATA/IS2_P0001_V01_KM004.TAB',
                      'volumes/VG_28xx/VG_2810/DATA/IS2_P0001_V01_KM004.LBL'],
             ('Voyager ISS',
              30,
              'vgiss_prof_10',
              'Intensity Profile (10 km)',
              True): ['volumes/VG_28xx/VG_2810/DATA/IS2_P0001_V01_KM010.TAB',
                      'volumes/VG_28xx/VG_2810/DATA/IS2_P0001_V01_KM010.LBL'],
             ('Voyager ISS',
              40,
              'vgiss_prof_20',
              'Intensity Profile (20 km)',
              True): ['volumes/VG_28xx/VG_2810/DATA/IS2_P0001_V01_KM020.TAB',
                      'volumes/VG_28xx/VG_2810/DATA/IS2_P0001_V01_KM020.LBL'],
             ('metadata',
              5,
              'rms_index',
              'RMS Node Augmented Index',
              False): ['metadata/VG_28xx/VG_2810/VG_2810_index.tab',
                       'metadata/VG_28xx/VG_2810/VG_2810_index.lbl'],
             ('metadata',
              9,
              'supplemental_index',
              'Supplemental Index',
              False): ['metadata/VG_28xx/VG_2810/VG_2810_supplemental_index.tab',
                       'metadata/VG_28xx/VG_2810/VG_2810_supplemental_index.lbl']}
        ),
    ]
)
def test_opus_products(input_path, expected):
    opus_products_test(input_path, expected)
