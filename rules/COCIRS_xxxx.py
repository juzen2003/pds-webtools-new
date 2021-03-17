####################################################################################################################################
# rules/COCIRS_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*/data/cube',               re.I, ('Derived spectral image cubes',  'CUBEDIR')),
    (r'volumes/.*/data/cube/[^/]',          re.I, ('Image cubes by projection',     'CUBEDIR')),
    (r'volumes/.*/data/tsdr',               re.I, ('Data files',                    'DATADIR')),
    (r'volumes/.*/data/apodspec',           re.I, ('Calibrated spectra',            'DATADIR')),
    (r'volumes/.*/data/hsk_data',           re.I, ('Housekeeping data',             'DATADIR')),
    (r'volumes/.*/data/nav_data',           re.I, ('Geometry data',                 'GEOMDIR')),
    (r'volumes/.*/data/uncalibr',           re.I, ('Uncalibrated data',             'DATADIR')),
    (r'volumes/.*/cube*/equirectangular',   re.I, ('Synthesized surface maps',      'DATADIR')),
    (r'volumes/.*/cube*/point_perspective', re.I, ('Synthesized images',            'DATADIR')),
    (r'volumes/.*/cube*/ring_polar',        re.I, ('Synthesized ring maps',         'DATADIR')),

    (r'volumes/.*/extras/cube_overview/equirectangular',   re.I, ('JPEGs of synthesized surface maps', 'BROWDIR')),
    (r'volumes/.*/extras/cube_overview/point_perspective', re.I, ('JPEGs of synthesized images',       'BROWDIR')),
    (r'volumes/.*/extras/cube_overview/ring_polar',        re.I, ('JPEGs of synthesized ring maps',    'BROWDIR')),

    (r'volumes/COCIRS_[56].*\.png',         re.I, ('Browse diagram',                'DIAGRAM' )),
    (r'diagrams/COCIRS_[56].*\.png',        re.I, ('Observation diagram',           'DIAGRAM' )),
    (r'volumes/COCIRS_[56].*/BROWSE',       re.I, ('Observation diagrams',          'DIAGDIR' )),
    (r'diagrams/COCIRS_[56].*/BROWSE',      re.I, ('Observation diagrams',          'DIAGDIR' )),

    (r'volumes/.*/data/apodspec/.*\.DAT',   re.I, ('Calibrated spectra',               'DATA')),
    (r'volumes/.*/data/ispmdata/.*\.TAB',   re.I, ('Interferogram metadata index',     'INDEX')),
    (r'volumes/.*/data/poidata/.*\.TAB',    re.I, ('Target intercept geometry index',  'INDEX')),
    (r'volumes/.*/data/rindata/.*\.TAB',    re.I, ('Ring intercept geometry index',    'INDEX')),
    (r'volumes/.*/data/tardata/.*\.TAB',    re.I, ('Observed body index',              'INDEX')),

    (r'volumes/.*/data/geodata',            re.I, ('Body viewing geometry',            'GEOMDIR')),
    (r'volumes/.*/data/ispmdata',           re.I, ('Interferogram metadata',           'INDEXDIR')),
    (r'volumes/.*/data/poidata',            re.I, ('Target intercept geometry',        'GEOMDIR')),
    (r'volumes/.*/data/rindata',            re.I, ('Ring intercept geometry',          'GEOMDIR')),
    (r'volumes/.*/data/tardata',            re.I, ('Observed body indentifications',   'GEOMDIR')),

    (r'volumes/.*/data/geodata/.*599\.TAB', re.I, ('Body geometry index (Jupiter)',    'INDEX')),
    (r'volumes/.*/data/geodata/.*501\.TAB', re.I, ('Body geometry index (Io)',         'INDEX')),
    (r'volumes/.*/data/geodata/.*502\.TAB', re.I, ('Body geometry index (Europa)',     'INDEX')),
    (r'volumes/.*/data/geodata/.*503\.TAB', re.I, ('Body geometry index (Ganymede)',   'INDEX')),
    (r'volumes/.*/data/geodata/.*504\.TAB', re.I, ('Body geometry index (Callisto)',   'INDEX')),
    (r'volumes/.*/data/geodata/.*699\.TAB', re.I, ('Body geometry index (Saturn)',     'INDEX')),
    (r'volumes/.*/data/geodata/.*601\.TAB', re.I, ('Body geometry index (Mimas)',      'INDEX')),
    (r'volumes/.*/data/geodata/.*602\.TAB', re.I, ('Body geometry index (Enceladus)',  'INDEX')),
    (r'volumes/.*/data/geodata/.*603\.TAB', re.I, ('Body geometry index (Tethys)',     'INDEX')),
    (r'volumes/.*/data/geodata/.*604\.TAB', re.I, ('Body geometry index (Dione)',      'INDEX')),
    (r'volumes/.*/data/geodata/.*605\.TAB', re.I, ('Body geometry index (Rhea)',       'INDEX')),
    (r'volumes/.*/data/geodata/.*606\.TAB', re.I, ('Body geometry index (Titan)',      'INDEX')),
    (r'volumes/.*/data/geodata/.*607\.TAB', re.I, ('Body geometry index (Hyperion)',   'INDEX')),
    (r'volumes/.*/data/geodata/.*608\.TAB', re.I, ('Body geometry index (Iapetus)',    'INDEX')),
    (r'volumes/.*/data/geodata/.*609\.TAB', re.I, ('Body geometry index (Phoebe)',     'INDEX')),
    (r'volumes/.*/data/geodata/.*610\.TAB', re.I, ('Body geometry index (Janus)',      'INDEX')),
    (r'volumes/.*/data/geodata/.*611\.TAB', re.I, ('Body geometry index (Epimetheus)', 'INDEX')),
    (r'volumes/.*/data/geodata/.*612\.TAB', re.I, ('Body geometry index (Helene)',     'INDEX')),
    (r'volumes/.*/data/geodata/.*613\.TAB', re.I, ('Body geometry index (Telesto)',    'INDEX')),
    (r'volumes/.*/data/geodata/.*614\.TAB', re.I, ('Body geometry index (Calypso)',    'INDEX')),
    (r'volumes/.*/data/geodata/.*615\.TAB', re.I, ('Body geometry index (Atlas)',      'INDEX')),
    (r'volumes/.*/data/geodata/.*616\.TAB', re.I, ('Body geometry index (Prometheus)', 'INDEX')),
    (r'volumes/.*/data/geodata/.*617\.TAB', re.I, ('Body geometry index (Pandora)',    'INDEX')),
    (r'volumes/.*/data/geodata/.*618\.TAB', re.I, ('Body geometry index (Pan)',        'INDEX')),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([

    (r'\w+/(COCIRS_[56]xxx.*/COCIRS_[56]...)/.*/[A-Z]+([0-9]+)_(FP.).*', 0,
                    [r'volumes/\1/DATA/APODSPEC/SPEC\2_\3.DAT',
                     r'volumes/\1/DATA/APODSPEC/SPEC\2_\3.LBL',
                     r'volumes/\1/DATA/ISPMDATA/ISPM\2_\3.TAB',
                     r'volumes/\1/DATA/ISPMDATA/ISPM\2_\3.LBL',
                     r'volumes/\1/DATA/TARDATA/TAR\2_\3.TAB',
                     r'volumes/\1/DATA/TARDATA/TAR\2_\3.LBL',
                     r'volumes/\1/BROWSE/TARGETS/IMG\2_\3.PNG',
                     r'volumes/\1/BROWSE/TARGETS/IMG\2_\3.LBL',
                    ]),

    (r'\w+/(COCIRS_[56]xxx.*/COCIRS_[56]...)/.*/(IMG|SPEC|ISPM|TAR)([0-9]+)_(FP.)(|_[a-z]+)\..*', 0,
                    [r'volumes/\1/DATA/POIDATA/POI\3_\4.TAB',
                     r'volumes/\1/DATA/POIDATA/POI\3_\4.LBL',
                     r'volumes/\1/DATA/GEODATA/GEO\3_*',
                     r'volumes/\1/BROWSE/*/POI\3_\4*',
                    ]),

    (r'\w+/(COCIRS_[56]xxx.*/COCIRS_[56]...)/DATA/.*/POI([0-9]+)_(FP.)\..*', 0,
                    [r'volumes/\1/DATA/POIDATA/POI\2_\3.TAB',
                     r'volumes/\1/DATA/POIDATA/POI\2_\3.LBL',
                     r'volumes/\1/DATA/GEODATA/GEO\2_*',
                     r'volumes/\1/BROWSE/*/POI\2_\3*',
                    ]),

    (r'\w+/(COCIRS_[56]xxx.*/COCIRS_[56]...)/BROWSE/SATURN/POI([0-9]+)_(FP.)(|_[a-z]+)\..*', 0,
                    [r'volumes/\1/DATA/POIDATA/POI\2_\3.TAB',
                     r'volumes/\1/DATA/POIDATA/POI\2_\3.LBL',
                     r'volumes/\1/DATA/GEODATA/GEO\2_699.TAB',
                     r'volumes/\1/DATA/GEODATA/GEO\2_699.LBL',
                     r'volumes/\1/BROWSE/SATURN/POI\2_\3.PNG',
                     r'volumes/\1/BROWSE/SATURN/POI\2_\3.LBL',
                    ]),

    (r'\w+/(COCIRS_[56]xxx.*/COCIRS_[56]...)/.*/POI([0-9]+)_(FP.)_(6..).*', 0,
                    [r'volumes/\1/DATA/POIDATA/POI\2_\3.TAB',
                     r'volumes/\1/DATA/POIDATA/POI\2_\3.LBL',
                     r'volumes/\1/DATA/GEODATA/GEO\2_\4.TAB',
                     r'volumes/\1/DATA/GEODATA/GEO\2_\4.LBL',
                    ]),

    (r'\w+/(COCIRS_[56]xxx.*/COCIRS_[56]...)/.*/POI([0-9]+)_(FP.)_(6[0-8].).*', 0,
                    [r'volumes/\1/BROWSE/*/POI\2_\3_\4.PNG',
                     r'volumes/\1/BROWSE/*/POI\2_\3_\4.LBL',
                    ]),

    (r'\w+/(COCIRS_[56]xxx.*/COCIRS_[56]...)/.*/POI([0-9]+)_(FP.)_699.*', 0,
                    [r'volumes/\1/BROWSE/SATURN/POI\2_\3.PNG',
                     r'volumes/\1/BROWSE/SATURN/POI\2_\3.LBL',
                    ]),

    (r'\w+/(COCIRS_[56]xxx.*/COCIRS_[56]...)/.*/RIN([0-9]+)_(FP.)(|_[a-z]+)\..*', 0,
                    [r'volumes/\1/DATA/RINDATA/RIN\2_\3.TAB',
                     r'volumes/\1/DATA/RINDATA/RIN\2_\3.LBL',
                     r'volumes/\1/BROWSE/S_RINGS/RIN\2_\3.PNG',
                     r'volumes/\1/BROWSE/S_RINGS/RIN\2_\3.LBL',
                    ]),

    (r'\w+/(COCIRS_[56]xxx/COCIRS_[56]...)/.*/[A-Z]+([0-9]+)_(6..).*', 0,
                    [r'volumes/\1/DATA/GEODATA/GEO\2_\3.TAB',
                     r'volumes/\1/DATA/GEODATA/GEO\2_\3.LBL',
                     r'volumes/\1/DATA/APODSPEC/SPEC\2_FP1.DAT',
                     r'volumes/\1/DATA/APODSPEC/SPEC\2_FP1.LBL',
                     r'volumes/\1/DATA/APODSPEC/SPEC\2_FP3.DAT',
                     r'volumes/\1/DATA/APODSPEC/SPEC\2_FP3.LBL',
                     r'volumes/\1/DATA/APODSPEC/SPEC\2_FP4.DAT',
                     r'volumes/\1/DATA/APODSPEC/SPEC\2_FP4.LBL',
                     r'volumes/\1/DATA/ISPMDATA/ISPM\2_FP1.TAB',
                     r'volumes/\1/DATA/ISPMDATA/ISPM\2_FP1.LBL',
                     r'volumes/\1/DATA/ISPMDATA/ISPM\2_FP3.TAB',
                     r'volumes/\1/DATA/ISPMDATA/ISPM\2_FP3.LBL',
                     r'volumes/\1/DATA/ISPMDATA/ISPM\2_FP4.TAB',
                     r'volumes/\1/DATA/ISPMDATA/ISPM\2_FP4.LBL',
                     r'volumes/\1/DATA/POIDATA/POI\2_FP1.TAB',
                     r'volumes/\1/DATA/POIDATA/POI\2_FP1.LBL',
                     r'volumes/\1/DATA/POIDATA/POI\2_FP3.TAB',
                     r'volumes/\1/DATA/POIDATA/POI\2_FP3.LBL',
                     r'volumes/\1/DATA/POIDATA/POI\2_FP4.TAB',
                     r'volumes/\1/DATA/POIDATA/POI\2_FP4.LBL',
                     r'volumes/\1/DATA/TARDATA/TAR\2_FP1.TAB',
                     r'volumes/\1/DATA/TARDATA/TAR\2_FP1.LBL',
                     r'volumes/\1/DATA/TARDATA/TAR\2_FP3.TAB',
                     r'volumes/\1/DATA/TARDATA/TAR\2_FP3.LBL',
                     r'volumes/\1/DATA/TARDATA/TAR\2_FP4.TAB',
                     r'volumes/\1/DATA/TARDATA/TAR\2_FP4.LBL',
                    ]),

    (r'\w+/(COCIRS_[56]xxx/COCIRS_[56]...)/.*/[A-Z]+([0-9]+)_(6[0-8].).*', 0,
                    [r'volumes/\1/BROWSE/*/POI\2_FP1_\3.PNG',
                     r'volumes/\1/BROWSE/*/POI\2_FP1_\3.LBL',
                     r'volumes/\1/BROWSE/*/POI\2_FP3_\3.PNG',
                     r'volumes/\1/BROWSE/*/POI\2_FP3_\3.LBL',
                     r'volumes/\1/BROWSE/*/POI\2_FP4_\3.PNG',
                     r'volumes/\1/BROWSE/*/POI\2_FP4_\3.LBL',
                    ]),

    (r'\w+/(COCIRS_[56]xxx/COCIRS_[56]...)/.*/[A-Z]+([0-9]+)_699.*', 0,
                    [r'volumes/\1/BROWSE/SATURN/POI\2_FP1.PNG',
                     r'volumes/\1/BROWSE/SATURN/POI\2_FP1.LBL',
                     r'volumes/\1/BROWSE/SATURN/POI\2_FP3.PNG',
                     r'volumes/\1/BROWSE/SATURN/POI\2_FP3.LBL',
                     r'volumes/\1/BROWSE/SATURN/POI\2_FP4.PNG',
                     r'volumes/\1/BROWSE/SATURN/POI\2_FP4.LBL',
                    ]),

    (r'volumes/(COCIRS_[56]xxx/COCIRS_[56]...)/DATA/\w+', 0,
                    [r'volumes/\1/BROWSE',
                     r'volumes/\1/DATA/*'
                    ]),

    (r'volumes/(COCIRS_[56]xxx/COCIRS_[56]...)/DATA', 0,
                    r'volumes/\1/BROWSE'),

    (r'\w+/(COCIRS_[56]xxx/COCIRS_[56]...)/BROWSE(|/\w+)', 0,
                    r'volumes/\1/DATA'),

    # COCIRS_[01]xxx, previews to volumes/DATA and volumes/EXTRAS
    (r'previews/(COCIRS_[01]xxx.*/COCIRS_....)/DATA/CUBE/(\w+/\w+_F[134]_[^_\.]+).*', 0,
                    [r'volumes/\1/DATA/CUBE/\2.*',
                     r'volumes/\1/EXTRAS/CUBE_OVERVIEW/\2.*'
                    ]),
    (r'previews/(COCIRS_[01]xxx.*/COCIRS_....)/DATA/CUBE/(\w+)', 0,
                    [r'volumes/\1/DATA/CUBE/\2',
                     r'volumes/\1/EXTRAS/CUBE_OVERVIEW/\2'
                    ]),
    (r'previews/(COCIRS_[01]xxx.*/COCIRS_....)/DATA/CUBE', 0,
                    [r'volumes/\1/DATA/CUBE',
                     r'volumes/\1/EXTRAS/CUBE_OVERVIEW'
                    ]),

    # COCIRS_[01]xxx, volumes/DATA to volumes/DATA and volumes/EXTRAS
    (r'(volumes/COCIRS_[01]xxx.*/COCIRS_....)/DATA/CUBE/\w+/(\w+_F[134]).*', 0,
                    [r'\1/DATA/CUBE/*/\2*',
                     r'\1/DATA/EXTRAS/*/\2*'
                    ]),
    (r'(volumes/COCIRS_[01]xxx.*/COCIRS_....)/DATA/CUBE/(\w+/\w+)\..*', 0,
                    r'\1/EXTRAS/CUBE_OVERVIEW/\2.*'),
    (r'(volumes/COCIRS_[01]xxx.*/COCIRS_....)/DATA/CUBE/(\w+)', 0,
                    r'\1/EXTRAS/CUBE_OVERVIEW/\2'),
    (r'(volumes/COCIRS_[01]xxx.*/COCIRS_....)/DATA/CUBE', 0,
                    r'\1/EXTRAS/CUBE_OVERVIEW'),

    # COCIRS_[01]xxx, volumes/EXTRAS to volumes/DATA and volumes/EXTRAS
    (r'(volumes/COCIRS_[01]xxx.*/COCIRS_....)/EXTRAS/CUBE_OVERVIEW/\w+/(\w+_F[134]).*', 0,
                    [r'\1/DATA/CUBE/*/\2*',
                     r'\1/EXTRAS/CUBE_OVERVIEW/*/\2*',
                    ]),
    (r'(volumes/COCIRS_[01]xxx.*/COCIRS_....)/EXTRAS/CUBE_OVERVIEW/(\w+)',  0,  r'\1/DATA/CUBE/\2'),
    (r'(volumes/COCIRS_[01]xxx.*/COCIRS_....)/EXTRAS/CUBE_OVERVIEW',        0,  r'\1/DATA/CUBE'),
    (r'(volumes/COCIRS_[01]xxx.*/COCIRS_....)/EXTRAS',                      0,  r'\1/DATA'),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'.*/(COCIRS_[01]xxx)(|_v2)/(COCIRS_[01]...)/(DATA/CUBE|EXTRAS/CUBE_OVERVIEW)/(\w+/\w+_F[134]_\w+).*', 0,
                    [r'previews/\1/\3/DATA/CUBE/\5_full.jpg',
                     r'previews/\1/\3/DATA/CUBE/\5_med.jpg',
                     r'previews/\1/\3/DATA/CUBE/\5_small.jpg',
                     r'previews/\1/\3/DATA/CUBE/\5_thumb.jpg',
                    ]),
    (r'.*/(COCIRS_[01]xxx_v3/COCIRS_[01]...)/(DATA/CUBE|EXTRAS/CUBE_OVERVIEW)/(\w+/\w+_F[134]_\w+).*', 0,
                    [r'previews/\1/DATA/CUBE/\3_full.jpg',
                     r'previews/\1/DATA/CUBE/\3_med.jpg',
                     r'previews/\1/DATA/CUBE/\3_small.jpg',
                     r'previews/\1/DATA/CUBE/\3_thumb.jpg',
                    ]),
    (r'.*/(COCIRS_[01]xxx)(|v2)/(COCIRS_[01]...)/(DATA/CUBE|EXTRAS/CUBE_OVERVIEW)/(\w+)', 0,
                    r'previews/\1/\3/DATA/CUBE/\5'),
    (r'.*/(COCIRS_[01]xxx_v3/COCIRS_[01]...)/(DATA/CUBE|EXTRAS/CUBE_OVERVIEW)/(\w+)', 0,
                    r'previews/\1/DATA/CUBE/\3'),
    (r'.*/(COCIRS_[01]xxx)(|v2)/(COCIRS_[01]...)/(DATA/CUBE|EXTRAS/CUBE_OVERVIEW)', 0,
                    r'previews/\1/\3/DATA/CUBE'),
    (r'.*/(COCIRS_[01]xxx_v3/COCIRS_[01]...)/(DATA/CUBE|EXTRAS/CUBE_OVERVIEW)', 0,
                    r'previews/\1/DATA/CUBE'),
])

associations_to_diagrams = translator.TranslatorByRegex([
    (r'diagrams/(COCIRS_[56]xxx.*/COCIRS_[56]...)/BROWSE/.*/[A-Z]+([0-9]{10}_FP.).*', 0,
                    [r'diagrams/\1/BROWSE/*/POI\2_*',
                     r'diagrams/\1/BROWSE/TARGETS/IMG\2_full.jpg',
                     r'diagrams/\1/BROWSE/TARGETS/IMG\2_med.jpg',
                     r'diagrams/\1/BROWSE/TARGETS/IMG\2_small.jpg',
                     r'diagrams/\1/BROWSE/TARGETS/IMG\2_thumb.jpg',
                     r'diagrams/\1/BROWSE/S_RINGS/RIN\2_full.jpg',
                     r'diagrams/\1/BROWSE/S_RINGS/RIN\2_med.jpg',
                     r'diagrams/\1/BROWSE/S_RINGS/RIN\2_small.jpg',
                     r'diagrams/\1/BROWSE/S_RINGS/RIN\2_thumb.jpg',
                    ]),
    (r'volumes/(COCIRS_[56]xxx.*/COCIRS_[56]...)/BROWSE/(.*)\..*', 0,
                    [r'diagrams/\1/BROWSE/\2_full.jpg',
                     r'diagrams/\1/BROWSE/\2_med.jpg',
                     r'diagrams/\1/BROWSE/\2_small.jpg',
                     r'diagrams/\1/BROWSE/\2_thumb.jpg',
                    ]),
    (r'volumes/(COCIRS_[56]xxx.*/COCIRS_[56]...)/BROWSE/(\w+/[A-Z]+[0-9]{10}_FP.).*', 0,
                    [r'diagrams/\1/BROWSE/\2_full.jpg',
                     r'diagrams/\1/BROWSE/\2_med.jpg',
                     r'diagrams/\1/BROWSE/\2_small.jpg',
                     r'diagrams/\1/BROWSE/\2_thumb.jpg',
                    ]),
    (r'volumes/(COCIRS_[56]xxx.*/COCIRS_[56]...)/BROWSE/(\w+)', 0,
                    r'diagrams/\1/BROWSE/\2'),
    (r'volumes/(COCIRS_[56]xxx.*/COCIRS_[56]...)/BROWSE', 0,
                    r'diagrams/\1/BROWSE'),

    (r'volumes/(COCIRS_[56]xxx.*/COCIRS_[56]...)/DATA/.*/[A-Z]+(\d{10})_(FP.)\..*', 0,
                    [r'diagrams/\1/BROWSE/TARGETS/IMG\2_\3_full.jpg',
                     r'diagrams/\1/BROWSE/TARGETS/IMG\2_\3_med.jpg',
                     r'diagrams/\1/BROWSE/TARGETS/IMG\2_\3_small.jpg',
                     r'diagrams/\1/BROWSE/TARGETS/IMG\2_\3_thumb.jpg',
                    ]),
    (r'volumes/(COCIRS_[56]xxx.*/COCIRS_[56]...)/DATA/.*/[A-Z]+(\d{10})_(6..)\..*', 0,
                    [r'diagrams/\1/BROWSE/TARGETS/IMG\2_FP1_full.jpg',
                     r'diagrams/\1/BROWSE/TARGETS/IMG\2_FP1_med.jpg',
                     r'diagrams/\1/BROWSE/TARGETS/IMG\2_FP1_small.jpg',
                     r'diagrams/\1/BROWSE/TARGETS/IMG\2_FP1_thumb.jpg',
                     r'diagrams/\1/BROWSE/TARGETS/IMG\2_FP3_full.jpg',
                     r'diagrams/\1/BROWSE/TARGETS/IMG\2_FP3_med.jpg',
                     r'diagrams/\1/BROWSE/TARGETS/IMG\2_FP3_small.jpg',
                     r'diagrams/\1/BROWSE/TARGETS/IMG\2_FP3_thumb.jpg',
                     r'diagrams/\1/BROWSE/TARGETS/IMG\2_FP4_full.jpg',
                     r'diagrams/\1/BROWSE/TARGETS/IMG\2_FP4_med.jpg',
                     r'diagrams/\1/BROWSE/TARGETS/IMG\2_FP4_small.jpg',
                     r'diagrams/\1/BROWSE/TARGETS/IMG\2_FP4_thumb.jpg',
                    ]),
    (r'volumes/(COCIRS_[56]xxx.*/COCIRS_[56]...)/DATA/RINDATA/(SPEC|ISPM|TAR|RIN)(\d{10}_FP.)\..*', 0,
                    [r'diagrams/\1/BROWSE/S_RINGS/RIN\3_full.jpg',
                     r'diagrams/\1/BROWSE/S_RINGS/RIN\3_med.jpg',
                     r'diagrams/\1/BROWSE/S_RINGS/RIN\3_small.jpg',
                     r'diagrams/\1/BROWSE/S_RINGS/RIN\3_thumb.jpg',
                    ]),
    (r'volumes/(COCIRS_[56]xxx.*/COCIRS_[56]...)/DATA/GEODATA/GEO(\w+)_(6[0-8].)\..*', 0,
                    [r'diagrams/\1/BROWSE/*/POI\2_FP1_\3_full.jpg',
                     r'diagrams/\1/BROWSE/*/POI\2_FP1_\3_med.jpg',
                     r'diagrams/\1/BROWSE/*/POI\2_FP1_\3_small.jpg',
                     r'diagrams/\1/BROWSE/*/POI\2_FP1_\3_thumb.jpg',
                     r'diagrams/\1/BROWSE/*/POI\2_FP3_\3_full.jpg',
                     r'diagrams/\1/BROWSE/*/POI\2_FP3_\3_med.jpg',
                     r'diagrams/\1/BROWSE/*/POI\2_FP3_\3_small.jpg',
                     r'diagrams/\1/BROWSE/*/POI\2_FP3_\3_thumb.jpg',
                     r'diagrams/\1/BROWSE/*/POI\2_FP4_\3_full.jpg',
                     r'diagrams/\1/BROWSE/*/POI\2_FP4_\3_med.jpg',
                     r'diagrams/\1/BROWSE/*/POI\2_FP4_\3_small.jpg',
                     r'diagrams/\1/BROWSE/*/POI\2_FP4_\3_thumb.jpg',
                    ]),
    (r'volumes/(COCIRS_[56]xxx.*/COCIRS_[56]...)/DATA/GEODATA/GEO(\w+)_699.*', 0,
                    [r'diagrams/\1/BROWSE/SATURN/POI\2_FP1_full.jpg',
                     r'diagrams/\1/BROWSE/SATURN/POI\2_FP1_med.jpg',
                     r'diagrams/\1/BROWSE/SATURN/POI\2_FP1_small.jpg',
                     r'diagrams/\1/BROWSE/SATURN/POI\2_FP1_thumb.jpg',
                     r'diagrams/\1/BROWSE/SATURN/POI\2_FP3_full.jpg',
                     r'diagrams/\1/BROWSE/SATURN/POI\2_FP3_med.jpg',
                     r'diagrams/\1/BROWSE/SATURN/POI\2_FP3_small.jpg',
                     r'diagrams/\1/BROWSE/SATURN/POI\2_FP3_thumb.jpg',
                     r'diagrams/\1/BROWSE/SATURN/POI\2_FP4_full.jpg',
                     r'diagrams/\1/BROWSE/SATURN/POI\2_FP4_med.jpg',
                     r'diagrams/\1/BROWSE/SATURN/POI\2_FP4_small.jpg',
                     r'diagrams/\1/BROWSE/SATURN/POI\2_FP4_thumb.jpg',
                    ]),
    (r'volumes/(COCIRS_[56]xxx.*/COCIRS_[56]...)/DATA/\w+/(SPEC|ISPM|TAR|POI)(\d{10}_FP.)\..*', 0,
                    r'diagrams/\1/BROWSE/*/POI\3_*.jpg'),
    (r'volumes/(COCIRS_[56]xxx.*/COCIRS_[56]...)/DATA(|/[A-QS-Z]\w+)', 0,
                    r'diagrams/\1/BROWSE'),
    (r'volumes/(COCIRS_[56]xxx.*/COCIRS_[56]...)/DATA/RINDATA', 0,
                    r'diagrams/\1/BROWSE/S_RINGS'),
])

def test_associations_to_volumes():
    TESTS = [
        ( 1, 'volumes/COCIRS_5xxx/COCIRS_5512/BROWSE'),
        ( 1, 'volumes/COCIRS_5xxx/COCIRS_5512/BROWSE/DIONE'),
        (14, 'volumes/COCIRS_5xxx/COCIRS_5512/BROWSE/DIONE/POI0512240325_FP3_604.LBL'),
        (14, 'volumes/COCIRS_5xxx/COCIRS_5512/BROWSE/DIONE/POI0512240325_FP3_604.PNG'),
        (12, 'volumes/COCIRS_5xxx/COCIRS_5512/BROWSE/S_RINGS/RIN0512011549_FP3.PNG'),
        (12, 'volumes/COCIRS_5xxx/COCIRS_5512/BROWSE/S_RINGS/RIN0512011549_FP4.PNG'),
        (14, 'volumes/COCIRS_5xxx/COCIRS_5512/BROWSE/SATURN/POI0512010000_FP1.LBL'),
        (24, 'volumes/COCIRS_5xxx/COCIRS_5512/BROWSE/TARGETS/IMG0512010000_FP1.LBL'),
        ( 1, 'volumes/COCIRS_5xxx/COCIRS_5512/DATA'),
        ( 8, 'volumes/COCIRS_5xxx/COCIRS_5512/DATA/APODSPEC'),
        ( 8, 'volumes/COCIRS_5xxx/COCIRS_5512/DATA/GEODATA'),
        (24, 'volumes/COCIRS_5xxx/COCIRS_5512/DATA/APODSPEC/SPEC0512010000_FP1.DAT'),
        (26, 'volumes/COCIRS_5xxx/COCIRS_5512/DATA/GEODATA/GEO0512010000_601.LBL'),
        (24, 'volumes/COCIRS_5xxx/COCIRS_5512/DATA/ISPMDATA/ISPM0512010000_FP1.LBL'),
        (24, 'volumes/COCIRS_5xxx/COCIRS_5512/DATA/POIDATA/POI0512010000_FP1.LBL'),
        (10, 'volumes/COCIRS_5xxx/COCIRS_5512/DATA/RINDATA/RIN0512010000_FP3.LBL'),
        (24, 'volumes/COCIRS_5xxx/COCIRS_5512/DATA/TARDATA/TAR0512010000_FP1.LBL'),
        ( 1, 'diagrams/COCIRS_5xxx/COCIRS_5512/BROWSE'),
        ( 1, 'diagrams/COCIRS_5xxx/COCIRS_5512/BROWSE/S_RINGS'),
        (12, 'diagrams/COCIRS_5xxx/COCIRS_5912/BROWSE/S_RINGS/RIN0912010101_FP4_full.jpg'),
        (14, 'diagrams/COCIRS_5xxx/COCIRS_5912/BROWSE/SATURN/POI0912010101_FP1_thumb.jpg'),
        (32, 'diagrams/COCIRS_5xxx/COCIRS_5912/BROWSE/TARGETS/IMG0912010101_FP1_full.jpg'),
        (14, 'diagrams/COCIRS_5xxx/COCIRS_5912/BROWSE/TITAN/POI0912111106_FP1_606_small.jpg'),
    ]

    for (count, path) in TESTS:
        abspaths = pdsfile.rules.translate_all(associations_to_volumes, path)
        trimmed = [p.rpartition('holdings/')[-1] for p in abspaths]
        assert len(abspaths) == count, f'Miscount: {path} {len(abspaths)} {trimmed}'


def test_associations_to_diagrams():
    TESTS = [
        ( 1, 'volumes/COCIRS_5xxx/COCIRS_5512/BROWSE'),
        ( 1, 'volumes/COCIRS_5xxx/COCIRS_5512/BROWSE/DIONE'),
        ( 4, 'volumes/COCIRS_5xxx/COCIRS_5512/BROWSE/DIONE/POI0512240325_FP3_604.LBL'),
        ( 4, 'volumes/COCIRS_5xxx/COCIRS_5512/BROWSE/DIONE/POI0512240325_FP3_604.PNG'),
        ( 4, 'volumes/COCIRS_5xxx/COCIRS_5512/BROWSE/S_RINGS/RIN0512011549_FP3.PNG'),
        ( 4, 'volumes/COCIRS_5xxx/COCIRS_5512/BROWSE/S_RINGS/RIN0512011549_FP4.PNG'),
        ( 4, 'volumes/COCIRS_5xxx/COCIRS_5512/BROWSE/SATURN/POI0512010000_FP1.LBL'),
        ( 4, 'volumes/COCIRS_5xxx/COCIRS_5512/BROWSE/TARGETS/IMG0512010000_FP1.LBL'),
        ( 1, 'volumes/COCIRS_5xxx/COCIRS_5512/DATA'),
        ( 1, 'volumes/COCIRS_5xxx/COCIRS_5512/DATA/APODSPEC'),
        ( 1, 'volumes/COCIRS_5xxx/COCIRS_5512/DATA/GEODATA'),
        ( 1, 'volumes/COCIRS_5xxx/COCIRS_5512/DATA/RINDATA'),
        (12, 'volumes/COCIRS_5xxx/COCIRS_5512/DATA/APODSPEC/SPEC0512010000_FP1.DAT'),
        (12, 'volumes/COCIRS_5xxx/COCIRS_5512/DATA/GEODATA/GEO0512010000_601.LBL'),
        (12, 'volumes/COCIRS_5xxx/COCIRS_5512/DATA/ISPMDATA/ISPM0512010000_FP1.LBL'),
        (12, 'volumes/COCIRS_5xxx/COCIRS_5512/DATA/POIDATA/POI0512010000_FP1.LBL'),
        ( 8, 'volumes/COCIRS_5xxx/COCIRS_5512/DATA/RINDATA/RIN0512010000_FP3.LBL'),
        (12, 'volumes/COCIRS_5xxx/COCIRS_5512/DATA/TARDATA/TAR0512010000_FP1.LBL'),
        ( 0, 'diagrams/COCIRS_5xxx/COCIRS_5512/BROWSE'),
        ( 0, 'diagrams/COCIRS_5xxx/COCIRS_5512/BROWSE/S_RINGS'),
        (12, 'diagrams/COCIRS_5xxx/COCIRS_5912/BROWSE/S_RINGS/RIN0912010101_FP4_full.jpg'),
        ( 8, 'diagrams/COCIRS_5xxx/COCIRS_5912/BROWSE/SATURN/POI0912010101_FP1_thumb.jpg'),
        (12, 'diagrams/COCIRS_5xxx/COCIRS_5912/BROWSE/SATURN/POI0912010101_FP4_thumb.jpg'),
        ( 8, 'diagrams/COCIRS_5xxx/COCIRS_5912/BROWSE/TARGETS/IMG0912010101_FP1_full.jpg'),
        (12, 'diagrams/COCIRS_5xxx/COCIRS_5912/BROWSE/TARGETS/IMG0912010101_FP4_full.jpg'),
        ( 8, 'diagrams/COCIRS_5xxx/COCIRS_5912/BROWSE/TITAN/POI0912111106_FP1_606_small.jpg'),
        ( 8, 'diagrams/COCIRS_5xxx/COCIRS_5512/BROWSE/RHEA/POI0512231930_FP1_605.LBL'),
    ]

    for (count, path) in TESTS:
        abspaths = pdsfile.rules.translate_all(associations_to_diagrams, path)
        trimmed = [p.rpartition('holdings/')[-1] for p in abspaths]
        assert len(abspaths) == count, f'Miscount: {path} {len(abspaths)} {trimmed}'


####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl',  re.I, ''),

    (r'volumes/(COCIRS_[01].*)/DATA/CUBE/(\w+/\w+)\.tar\.gz',        0, r'previews/\1/DATA/CUBE/\2_*'),
    (r'volumes/(COCIRS_[01].*)/EXTRAS/CUBE_OVERVIEW/(\w+/\w+)\.JPG', 0, r'previews/\1/DATA/CUBE/\2_*'),

    (r'volumes/(COCIRS_[56].*)/BROWSE/(.*)_\w+\..*',                0,  r'diagrams/\1/BROWSE/\2*'),
    (r'volumes/(COCIRS_[56].*)/DATA/RINDATA/RIN(\w+)\..*',          0, (r'diagrams/\1/BROWSE/S_RINGS/RIN\2_*',
                                                                        r'diagrams/\1/BROWSE/TARGETS/IMG\2_*')),
    (r'volumes/(COCIRS_[56].*)/DATA/GEODATA/GEO(\w+)_(6..)\..*',    0, (r'diagrams/\1/BROWSE/*/POI\2_FP?_\3_*',
                                                                        r'diagrams/\1/BROWSE/TARGETS/IMG\2_FP?_*')),
    (r'volumes/(COCIRS_[56].*)/DATA/POIDATA/POI(\w+)\..*',          0, r'diagrams/\1/BROWSE/TARGETS/IMG\2_*'),
    (r'volumes/(COCIRS_[56].*)/DATA/APODSPEC/SPEC(\w+)\..*',        0, r'diagrams/\1/BROWSE/TARGETS/IMG\2_*'),
    (r'volumes/(COCIRS_[56].*)/DATA/ISPMDATA/ISPM(\w+)\..*',        0, r'diagrams/\1/BROWSE/TARGETS/IMG\2_*'),
    (r'volumes/(COCIRS_[56].*)/DATA/TARDATA/TAR(\w+)\..*',          0, r'diagrams/\1/BROWSE/TARGETS/IMG\2_*'),
])

s_rings_viewables = translator.TranslatorByRegex([
    (r'volumes/(COCIRS_[56].*)/DATA/\w+/(SPEC|ISPM|TAR)(\w+)\..*',  0, r'diagrams/\1/BROWSE/S_RINGS/RIN\2_*'),
    (r'volumes/(COCIRS_[56].*)/DATA/\w+/GEO(\w+)_699\..*',          0, r'diagrams/\1/BROWSE/S_RINGS/RIN\2_*'),
])

saturn_viewables = translator.TranslatorByRegex([
    (r'volumes/(COCIRS_[56].*)/DATA/\w+/(SPEC|ISPM|TAR|POI)(\w+)\..*', 0, r'diagrams/\1/BROWSE/SATURN/POI\2_*'),
    (r'volumes/(COCIRS_[56].*)/DATA/\w+/GEO(\w+)_699\..*',             0, r'diagrams/\1/BROWSE/SATURN/POI\2_*'),
])

spice_lookup = {
    601: 'Mimas',
    602: 'Enceladus',
    603: 'Tethys',
    604: 'Dione',
    605: 'Rhea',
    606: 'Titan',
    607: 'Hyperion',
    608: 'Iapetus',
    609: 'Phoebe',
    610: 'Janus',
    611: 'Epimetheus',
    612: 'Helene',
    613: 'Telesto',
    614: 'Calypso',
    615: 'Atlas',
    616: 'Prometheus',
    617: 'Pandora',
    618: 'Pan',
}

viewables = {}
for (id, name) in spice_lookup.items():
    viewables[name] = translator.TranslatorByRegex([
        (r'volumes/(COCIRS_[56].*)/DATA/\w+/(SPEC|ISPM|TAR|POI)(\w+)\..*', 0, (r'diagrams/\1/BROWSE/*/POI\2_%3d_*.jpg' % id,)),
        (r'volumes/(COCIRS_[56].*)/DATA/\w+/GEO(\w+)_%3d\..*' % id,        0, (r'diagrams/\1/BROWSE/*/POI\2_%3d_*.jpg' % id,)),
])

viewables['default'] = default_viewables
viewables['Rings'] = s_rings_viewables
viewables['Saturn'] = saturn_viewables

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews)/COCIRS_[01]xxx(|_.*)/\w+/DATA/CUBE/(|\w+)',         0, (True, True, True )),
    (r'volumes/COCIRS_[01]xxx(|_.*)/COCIRS_..../EXTRAS/CUBE_OVERVIEW/(|\w+)', 0, (True, True, True )),

    (r'(volumes|diagrams)/COCIRS_[56]xxx/\w+/DATA/\w+(|/\w+)',                0, (True, True, True )),
    (r'(volumes|diagrams)/COCIRS_[56]xxx/\w+/BROWSE/\w+(|/\w+)',              0, (True, True, True )),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'(volumes|diagrams)/COCIRS_[56]xxx(|_\w+)/\w+/(DATA|BROWSE)',              0, r'\1/COCIRS_[56]xxx\2/*/\3'),
    (r'(volumes|diagrams)/COCIRS_[56]xxx(|_\w+)/\w+/(DATA|BROWSE)/(\w+)',        0, r'\1/COCIRS_[56]xxx\2/*/\3/\4'),
    (r'(volumes|diagrams)/COCIRS_[56]xxx(|_\w+)/\w+/(DATA|BROWSE)/(\w+)/.*',     0, r'\1/COCIRS_[56]xxx\2/*/\3/\4/*'),

    (r'(volumes|previews)/COCIRS_[01]xxx(|_\w+)/\w+/(DATA|EXTRAS)',              0, r'\1/COCIRS_[01]xxx\2/*/\3'),
    (r'(volumes|previews)/COCIRS_[01]xxx(|_\w+)/\w+/(DATA|EXTRAS)/(\w+)',        0, r'\1/COCIRS_[01]xxx\2/*/\3/\4'),
    (r'(volumes|previews)/COCIRS_[01]xxx(|_\w+)/\w+/(DATA|EXTRAS)/(\w+/\w+)',    0, r'\1/COCIRS_[01]xxx\2/*/\3/\4'),
    (r'(volumes|previews)/COCIRS_[01]xxx(|_\w+)/\w+/(DATA|EXTRAS)/(\w+/\w+)/.*', 0, r'\1/COCIRS_[01]xxx\2/*/\3/\4/*'),
])

####################################################################################################################################
# SPLIT_RULES
####################################################################################################################################

split_rules = translator.TranslatorByRegex([
    (r'(.*)\.tar.gz', 0, (r'\1', '', '.tar.gz')),
])

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/.*/DATA/APODSPEC/SPEC.*', 0, ('Cassini CIRS',   0, 'cocirs_spec', 'Calibrated Interferograms',    True)),
    (r'volumes/.*/DATA/GEODATA/GEO.*',   0, ('Cassini CIRS', 110, 'cocirs_geo',  'System Geometry',              True)),
    (r'volumes/.*/DATA/ISPMDATA/ISPM.*', 0, ('Cassini CIRS', 120, 'cocirs_ispm', 'Observation Metadata',         True)),
    (r'volumes/.*/DATA/POIDATA/POI.*',   0, ('Cassini CIRS', 130, 'cocirs_poi',  'Footprint Geometry on Bodies', True)),
    (r'volumes/.*/DATA/RINDATA/RIN.*',   0, ('Cassini CIRS', 140, 'cocirs_rin',  'Footprint Geometry on Rings',  True)),
    (r'volumes/.*/DATA/TARDATA/TAR.*',   0, ('Cassini CIRS', 150, 'cocirs_tar',  'Target Body Identifications',  True)),

    (r'volumes/.*/BROWSE/TARGETS/IMG.*',  0, ('Cassini CIRS', 510, 'cocirs_browse_target',     'Extra Browse Diagram (Default)',    True)),
    (r'volumes/.*/BROWSE/SATURN/POI.*',   0, ('Cassini CIRS', 520, 'cocirs_browse_saturn',     'Extra Browse Diagram (Saturn)',     True)),
    (r'volumes/.*/BROWSE/S_RINGS/RIN.*',  0, ('Cassini CIRS', 530, 'cocirs_browse_rings',      'Extra Browse Diagram (Rings)',      True)),
    (r'volumes/.*/BROWSE/.*/POI.*_601.*', 0, ('Cassini CIRS', 601, 'cocirs_browse_mimas',      'Extra Browse Diagram (Mimas)',      True)),
    (r'volumes/.*/BROWSE/.*/POI.*_602.*', 0, ('Cassini CIRS', 602, 'cocirs_browse_enceladus',  'Extra Browse Diagram (Enceladus)',  True)),
    (r'volumes/.*/BROWSE/.*/POI.*_603.*', 0, ('Cassini CIRS', 603, 'cocirs_browse_tethys',     'Extra Browse Diagram (Tethys)',     True)),
    (r'volumes/.*/BROWSE/.*/POI.*_604.*', 0, ('Cassini CIRS', 604, 'cocirs_browse_dione',      'Extra Browse Diagram (Dione)',      True)),
    (r'volumes/.*/BROWSE/.*/POI.*_605.*', 0, ('Cassini CIRS', 605, 'cocirs_browse_rhea',       'Extra Browse Diagram (Rhea)',       True)),
    (r'volumes/.*/BROWSE/.*/POI.*_606.*', 0, ('Cassini CIRS', 606, 'cocirs_browse_titan',      'Extra Browse Diagram (Titan)',      True)),
    (r'volumes/.*/BROWSE/.*/POI.*_607.*', 0, ('Cassini CIRS', 607, 'cocirs_browse_hyperion',   'Extra Browse Diagram (Hyperion)',   True)),
    (r'volumes/.*/BROWSE/.*/POI.*_608.*', 0, ('Cassini CIRS', 608, 'cocirs_browse_iapetus',    'Extra Browse Diagram (Iapetus)',    True)),
    (r'volumes/.*/BROWSE/.*/POI.*_609.*', 0, ('Cassini CIRS', 609, 'cocirs_browse_phoebe',     'Extra Browse Diagram (Phoebe)',     True)),
    (r'volumes/.*/BROWSE/.*/POI.*_610.*', 0, ('Cassini CIRS', 610, 'cocirs_browse_janus',      'Extra Browse Diagram (Janus)',      True)),
    (r'volumes/.*/BROWSE/.*/POI.*_611.*', 0, ('Cassini CIRS', 611, 'cocirs_browse_epimetheus', 'Extra Browse Diagram (Epimetheus)', True)),
    (r'volumes/.*/BROWSE/.*/POI.*_612.*', 0, ('Cassini CIRS', 612, 'cocirs_browse_helene',     'Extra Browse Diagram (Helene)',     True)),
    (r'volumes/.*/BROWSE/.*/POI.*_613.*', 0, ('Cassini CIRS', 613, 'cocirs_browse_telesto',    'Extra Browse Diagram (Telesto)',    True)),
    (r'volumes/.*/BROWSE/.*/POI.*_614.*', 0, ('Cassini CIRS', 614, 'cocirs_browse_calypso',    'Extra Browse Diagram (Calypso)',    True)),
    (r'volumes/.*/BROWSE/.*/POI.*_615.*', 0, ('Cassini CIRS', 615, 'cocirs_browse_atlas',      'Extra Browse Diagram (Atlas)',      True)),
    (r'volumes/.*/BROWSE/.*/POI.*_616.*', 0, ('Cassini CIRS', 616, 'cocirs_browse_prometheus', 'Extra Browse Diagram (Prometheus)', True)),
    (r'volumes/.*/BROWSE/.*/POI.*_617.*', 0, ('Cassini CIRS', 617, 'cocirs_browse_pandora',    'Extra Browse Diagram (Pandora)',    True)),
    (r'volumes/.*/BROWSE/.*/POI.*_618.*', 0, ('Cassini CIRS', 618, 'cocirs_browse_pan',        'Extra Browse Diagram (Pan)',        True)),

    (r'diagrams/.*/TARGETS/.*_thumb\..*', 0, ('browse', 10, 'browse_thumb',  'Browse Image (thumbnail)', False)),
    (r'diagrams/.*/TARGETS/.*_small\..*', 0, ('browse', 20, 'browse_small',  'Browse Image (small)',     False)),
    (r'diagrams/.*/TARGETS/.*_med\..*',   0, ('browse', 30, 'browse_medium', 'Browse Image (medium)',    False)),
    (r'diagrams/.*/TARGETS/.*_full\..*',  0, ('browse', 40, 'browse_full',   'Browse Image (full)',      True)),
])

####################################################################################################################################
# OPUS_FORMAT
####################################################################################################################################

opus_format = translator.TranslatorByRegex([
    (r'.*\.DAT', 0, ('Binary', 'Table')),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

opus_products = translator.TranslatorByRegex([
    (r'.*/(COCIRS_[56]xxx)(|_v[0-9\.]+)/(COCIRS_[56]...)/DATA/\w+/[A-Z]+([0-9]{10})_(FP.).*', 0,
                [r'volumes/\1*/\3/DATA/APODSPEC/SPEC\4_\5.DAT',
                 r'volumes/\1*/\3/DATA/APODSPEC/SPEC\4_\5.LBL',
                 r'volumes/\1*/\3/DATA/GEODATA/GEO\4_6*',
                 r'volumes/\1*/\3/DATA/ISPMDATA/ISPM\4_\5.TAB',
                 r'volumes/\1*/\3/DATA/ISPMDATA/ISPM\4_\5.LBL',
                 r'volumes/\1*/\3/DATA/POIDATA/POI\4_\5.TAB',
                 r'volumes/\1*/\3/DATA/POIDATA/POI\4_\5.LBL',
                 r'volumes/\1*/\3/DATA/RINDATA/RIN\4_\5.TAB',
                 r'volumes/\1*/\3/DATA/RINDATA/RIN\4_\5.LBL',
                 r'volumes/\1*/\3/DATA/TARDATA/TAR\4_\5.TAB',
                 r'volumes/\1*/\3/DATA/TARDATA/TAR\4_\5.LBL',
                 r'volumes/\1*/\3/BROWSE/TARGETS/IMG\4_\5.PNG',
                 r'volumes/\1*/\3/BROWSE/TARGETS/IMG\4_\5.LBL',
                 r'volumes/\1*/\3/BROWSE/SATURN/POI\4_\5.PNG',
                 r'volumes/\1*/\3/BROWSE/SATURN/POI\4_\5.LBL',
                 r'volumes/\1*/\3/BROWSE/S_RINGS/RIN\4_\5.PNG',
                 r'volumes/\1*/\3/BROWSE/S_RINGS/RIN\4_\5.LBL',
                 r'volumes/\1*/\3/BROWSE/*/POI\4_\5_*',
                 r'diagrams/\1/\3/BROWSE/*/POI\4_\5_*',
                 r'diagrams/\1/\3/BROWSE/S_RINGS/RIN\4_\5_full.jpg',
                 r'diagrams/\1/\3/BROWSE/S_RINGS/RIN\4_\5_med.jpg',
                 r'diagrams/\1/\3/BROWSE/S_RINGS/RIN\4_\5_small.jpg',
                 r'diagrams/\1/\3/BROWSE/S_RINGS/RIN\4_\5_thumb.jpg',
                 r'diagrams/\1/\3/BROWSE/TARGETS/IMG\4_\5_full.jpg',
                 r'diagrams/\1/\3/BROWSE/TARGETS/IMG\4_\5_med.jpg',
                 r'diagrams/\1/\3/BROWSE/TARGETS/IMG\4_\5_small.jpg',
                 r'diagrams/\1/\3/BROWSE/TARGETS/IMG\4_\5_thumb.jpg',
                ]),
])

opus_support_products = translator.TranslatorByRegex([])

####################################################################################################################################
# OPUS_ID
####################################################################################################################################

opus_id = translator.TranslatorByRegex([
    (r'.*COCIRS_[56]xxx.*/(DATA|BROWSE)/\w+/[A-Z]+([0-9]{10})_FP(.).*', 0, r'co-cirs-\2-fp\3'),
])

####################################################################################################################################
# OPUS_ID_TO_PRIMARY_LOGICAL_PATH
####################################################################################################################################

opus_id_to_primary_logical_path = translator.TranslatorByRegex([
    (r'co-cirs-(.*)-fp(.)', 0, r'volumes/COCIRS_[56]xxx/COCIRS_[56]???/DATA/APODSPEC/SPEC\1_FP\2.DAT'),
])

####################################################################################################################################
# DATA_SET_ID
####################################################################################################################################

data_set_id = translator.TranslatorByRegex([
    (r'.*/COCIRS_0xxx/COCIRS_0[0-3].*'            , 0, 'CO-J-CIRS-2/3/4-TSDR-V2.0'),
    (r'.*/COCIRS_0xxx/COCIRS_0[4-9].*/DATA/TSDR.*', 0, 'CO-S-CIRS-2/3/4-TSDR-V4.0'),
    (r'.*/COCIRS_0xxx/COCIRS_0[4-9].*/DATA/CUBE.*', 0, 'CO-S-CIRS-5-CUBES-V2.0'   ),
    (r'.*/COCIRS_1xxx/.*/DATA/TSDR.*'             , 0, 'CO-S-CIRS-2/3/4-TSDR-V4.0'),
    (r'.*/COCIRS_1xxx/.*/DATA/CUBE.*'             , 0, 'CO-S-CIRS-5-CUBES-V2.0'   ),
    (r'.*/COCIRS_[01]xxx_v3/.*/DATA/TSDR.*'       , 0, 'CO-S-CIRS-2/3/4-TSDR-V3.2'),
    (r'.*/COCIRS_[01]xxx_v3/.*/DATA/CUBE.*'       , 0, 'CO-S-CIRS-5-CUBES-V1.0'   ),
    (r'.*/COCIRS_0xxx_v2/.*'                      , 0, 'CO-S-CIRS-2/3/4-TSDR-V2.0'),
    (r'.*/COCIRS_1xxx_v2/COCIRS_100[1-6].*'       , 0, 'CO-S-CIRS-2/3/4-TSDR-V2.0'),
    (r'.*/COCIRS_1xxx_v2/COCIRS_100[7-9].*'       , 0, 'CO-S-CIRS-2/3/4-TSDR-V3.1'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class COCIRS_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('COCIRS_[0156]xxx', re.I, 'COCIRS_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS
    SPLIT_RULES = split_rules + pdsfile.PdsFile.SPLIT_RULES

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_FORMAT = opus_format + pdsfile.PdsFile.OPUS_FORMAT
    OPUS_PRODUCTS = opus_products
    OPUS_ID = opus_id
    OPUS_ID_TO_PRIMARY_LOGICAL_PATH = opus_id_to_primary_logical_path

    VIEWABLES = viewables

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']  = associations_to_volumes
    ASSOCIATIONS['previews'] = associations_to_previews
    ASSOCIATIONS['diagrams'] = associations_to_diagrams

    DATA_SET_ID = data_set_id

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS = translator.TranslatorByRegex([(r'co-cirs-.*', 0, COCIRS_xxxx)]) + \
                                      pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COCIRS_xxxx'] = COCIRS_xxxx

####################################################################################################################################
