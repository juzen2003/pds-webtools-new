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
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
])

####################################################################################################################################
# OPUS_FORMAT
####################################################################################################################################

opus_format = translator.TranslatorByRegex([
    (r'.*\.IMG', 0, ('Binary', 'VICAR')),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

opus_products = translator.TranslatorByRegex([
])

####################################################################################################################################
# OPUS_ID
####################################################################################################################################

opus_id = translator.TranslatorByRegex([
    (r'.*/COISS_[12]xxx.*/([NW][0-9]{10})_[0-9]+.*', 0, r'co-iss-#LOWER#\1'),
])

####################################################################################################################################
# OPUS_ID_TO_PRIMARY_LOGICAL_PATH
####################################################################################################################################

opus_id_to_primary_logical_path = translator.TranslatorByRegex([
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class VG_28xx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('VG_28xxx', re.I, 'VG_28xx')]) + \
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


# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS = translator.TranslatorByRegex([(r'TBD', 0, VG_28xx)]) + \
                                      pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['VG_28xx'] = VG_28xx

####################################################################################################################################
