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
    (r'volumes/.*/data/cube',                re.I, ('Derived spectral image cubes', 'CUBEDIR')),
    (r'volumes/.*/data/cube/[^/]',           re.I, ('Image cubes by projection',    'CUBEDIR')),
    (r'volumes/.*/data/tsdr',                re.I, ('Data files',                   'DATADIR')),
    (r'volumes/.*/data/.*apodspec',          re.I, ('Calibrated spectra',           'DATADIR')),
    (r'volumes/.*/data/.*hsk_data',          re.I, ('Housekeeping data',            'DATADIR')),
    (r'volumes/.*/data/.*nav_data',          re.I, ('Geometry data',                'GEOMDIR')),
    (r'volumes/.*/data/.*uncalibr',          re.I, ('Uncalibrated data',            'DATADIR')),
    (r'volumes/.*/cube*/equirectangular',    re.I, ('Synthesized surface maps',     'DATADIR')),
    (r'volumes/.*/cube*/point_perspective',  re.I, ('Synthesized images',           'DATADIR')),
    (r'volumes/.*/cube*/ring_polar',         re.I, ('Synthesized ring maps',        'DATADIR')),

    (r'volumes/.*/extras/cube_overview/equirectangular',   re.I, ('JPEGs of synthesized surface maps', 'BROWDIR')),
    (r'volumes/.*/extras/cube_overview/point_perspective', re.I, ('JPEGs of synthesized images',       'BROWDIR')),
    (r'volumes/.*/extras/cube_overview/ring_polar',        re.I, ('JPEGs of synthesized ring maps',    'BROWDIR')),

    (r'volumes/COCIRS_[56].*\.png',          re.I, ('Browse diagram',               'DIAGRAM' )),
    (r'diagrams/COCIRS_[56].*\.png',         re.I, ('Observation diagram',          'DIAGRAM' )),
    (r'volumes/COCIRS_[56].*/BROWSE',        re.I, ('Observation diagrams',         'DIAGDIR' )),
    (r'diagrams/COCIRS_[56].*/BROWSE',       re.I, ('Observation diagrams',         'DIAGDIR' )),

    (r'volumes/.*/data/geodata/.*',          re.I, ('System geometry index',        'INDEX')),
    (r'volumes/.*/data/ispmdata/.*',         re.I, ('Interferogram metadata index', 'INDEX')),
    (r'volumes/.*/data/poidata/.*',          re.I, ('Surface geometry index',       'INDEX')),
    (r'volumes/.*/data/rindata/.*',          re.I, ('Ring geometry index',          'INDEX')),
    (r'volumes/.*/data/tardata/.*',          re.I, ('Target body index',            'INDEX')),

    (r'volumes/.*/data/geodat*',             re.I, ('System geometry metadata',     'GEOMDIR')),
    (r'volumes/.*/data/ispmdat*',            re.I, ('Interferogram metadata',       'INDEXDIR')),
    (r'volumes/.*/data/poidata',             re.I, ('Surface intercept geometry',   'GEOMDIR')),
    (r'volumes/.*/data/rindata',             re.I, ('Ring intercept geometry',      'GEOMDIR')),
    (r'volumes/.*/data/tardata',             re.I, ('Target indentifications',      'GEOMDIR')),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    # COCIRS_[56]xxx, volumes/DATA to volumes/DATA and volumes/BROWSE
    (r'volumes/(COCIRS_[56]xxx/COCIRS_[56].*)/DATA/(\w+/[A-Z]+)([0-9]+)_(FP.).*',
                                                                            0, [r'volumes/\1/DATA/GEODATA/GEO\3_*',
                                                                                r'volumes/\1/DATA/APODSPEC/SPEC\3_\4.DAT',
                                                                                r'volumes/\1/DATA/APODSPEC/SPEC\3_\4.LBL',
                                                                                r'volumes/\1/DATA/ISPMDATA/ISPM\3_\4.TAB',
                                                                                r'volumes/\1/DATA/ISPMDATA/ISPM\3_\4.LBL',
                                                                                r'volumes/\1/DATA/POIDATA/POI\3_\4.TAB',
                                                                                r'volumes/\1/DATA/POIDATA/POI\3_\4.LBL',
                                                                                r'volumes/\1/DATA/RINDATA/RIN\3_\4.TAB',
                                                                                r'volumes/\1/DATA/RINDATA/RIN\3_\4.LBL',
                                                                                r'volumes/\1/DATA/TARDATA/TAR\3_\4.TAB',
                                                                                r'volumes/\1/DATA/TARDATA/TAR\3_\4.LBL',
                                                                                r'volumes/\1/BROWSE/*/*\3_\4*']),

    (r'volumes/(COCIRS_[56]xxx/COCIRS_[56].*)/DATA/(\w+/[A-Z]+)([0-9]+)_(6..).*',
                                                                            0, [r'volumes/\1/DATA/GEODATA/GEO\3_\4.TAB',
                                                                                r'volumes/\1/DATA/GEODATA/GEO\3_\4.LBL',
                                                                                r'volumes/\1/DATA/*/*\3_FP*',
                                                                                r'volumes/\1/BROWSE/*/*\3_FP?_\4.*']),

    (r'volumes/(COCIRS_[56]xxx/COCIRS_[56].*)/DATA/(\w+/[A-Z]+)([0-9]+)_699.*',
                                                                            0,  r'volumes/\1/BROWSE/*/*\3_FP?.*'),

    (r'volumes/(COCIRS_[56]xxx/COCIRS_[56].*)/DATA/(|\w+)$',                0,  r'volumes/\1/BROWSE'),

    # COCIRS_[56]xxx, diagrams and volumes/BROWSE to volumes/DATA and volumes/BROWSE
    (r'.*/(COCIRS_[56]xxx/COCIRS_[56].*)/BROWSE/\w+/[A-Z]+([0-9]+)_(FP.).*',
                                                                            0, [r'volumes/\1/DATA/APODSPEC/SPEC\2_\3.DAT',
                                                                                r'volumes/\1/DATA/APODSPEC/SPEC\2_\3.LBL',
                                                                                r'volumes/\1/DATA/ISPMDATA/ISPM\2_\3.TAB',
                                                                                r'volumes/\1/DATA/ISPMDATA/ISPM\2_\3.LBL',
                                                                                r'volumes/\1/DATA/TARDATA/TAR\2_\3.TAB',
                                                                                r'volumes/\1/DATA/TARDATA/TAR\2_\3.LBL']),

    (r'.*/(COCIRS_[56]xxx/COCIRS_[56].*)/BROWSE/\w+/[A-Z]+([0-9]+)_(FP.)_(6..).*',
                                                                            0, [r'volumes/\1/DATA/GEODATA/GEO\2_\4.TAB',
                                                                                r'volumes/\1/DATA/GEODATA/GEO\2_\4.LBL',
                                                                                r'volumes/\1/DATA/POIDATA/POI\2_\3.TAB',
                                                                                r'volumes/\1/DATA/POIDATA/POI\2_\3.LBL',
                                                                                r'volumes/\1/BROWSE/*/*\2_\3_\4.PNG',
                                                                                r'volumes/\1/BROWSE/*/*\2_\3_\4.LBL']),

    (r'.*/(COCIRS_[56]xxx/COCIRS_[56].*)/BROWSE/TARGET/[A-Z]+([0-9]+)_(FP.).*',
                                                                            0, [r'volumes/\1/DATA/GEODATA/GEO\2_*',
                                                                                r'volumes/\1/DATA/POIDATA/POI\2_\3.TAB',
                                                                                r'volumes/\1/DATA/POIDATA/POI\2_\3.LBL',
                                                                                r'volumes/\1/DATA/RINDATA/RIN\2_\3.TAB',
                                                                                r'volumes/\1/DATA/RINDATA/RIN\2_\3.LBL',
                                                                                r'volumes/\1/BROWSE/*/*\2_\3*']),

    (r'.*/(COCIRS_[56]xxx/COCIRS_[56].*)/BROWSE/SATURN/POI([0-9]+)_(FP.).*',
                                                                            0, [r'volumes/\1/DATA/GEODATA/GEO\2_699.TAB',
                                                                                r'volumes/\1/DATA/GEODATA/GEO\2_699.LBL',
                                                                                r'volumes/\1/DATA/POIDATA/POI\2_\3.TAB',
                                                                                r'volumes/\1/DATA/POIDATA/POI\2_\3.LBL',
                                                                                r'volumes/\1/BROWSE/SATURN/POI\2_\3.PNG',
                                                                                r'volumes/\1/BROWSE/SATURN/POI\2_\3.LBL']),

    (r'.*/(COCIRS_[56]xxx/COCIRS_[56].*)/BROWSE/S_RINGS/RIN([0-9]+)_(FP.).*',
                                                                            0, [r'volumes/\1/DATA/GEODATA/GEO\2_699.TAB',
                                                                                r'volumes/\1/DATA/GEODATA/GEO\2_699.LBL',
                                                                                r'volumes/\1/DATA/RINDATA/RIN\2_\3.TAB',
                                                                                r'volumes/\1/DATA/RINDATA/RIN\2_\3.LBL',
                                                                                r'volumes/\1/BROWSE/S_RINGS/RIN\2_\3.PNG',
                                                                                r'volumes/\1/BROWSE/S_RINGS/RIN\2_\3.LBL']),

    (r'.*/(COCIRS_[56]xxx/COCIRS_[56].*)/BROWSE(|/\w+)$',                   0, [r'volumes/\1/DATA',
                                                                                r'volumes/\1/BROWSE\2']),

    # COCIRS_[01]xxx, previews to volumes/DATA and volumes/EXTRAS
    (r'previews/(COCIRS_[01]xxx.*/COCIRS_....)/DATA/CUBE/(\w+/\w+_F[134]_[^_\.]+).*',
                                                                            0, [r'volumes/\1/DATA/CUBE/\2.tar.gz',
                                                                                r'volumes/\1/DATA/CUBE/\2.lbl',
                                                                                r'volumes/\1/EXTRAS/CUBE_OVERVIEW/\2.JPG',
                                                                                r'volumes/\1/EXTRAS/CUBE_OVERVIEW/\2.LBL']),
    (r'previews/(COCIRS_[01]xxx.*/COCIRS_....)/DATA/CUBE/(\w+)$',           0, [r'volumes/\1/DATA/CUBE/\2',
                                                                                r'volumes/\1/EXTRAS/CUBE_OVERVIEW/\2']),
    (r'previews/(COCIRS_[01]xxx.*/COCIRS_....)/DATA/CUBE$',                 0, [r'volumes/\1/DATA/CUBE',
                                                                                r'volumes/\1/EXTRAS/CUBE_OVERVIEW']),

    # COCIRS_[01]xxx, volumes/DATA to volumes/DATA and volumes/EXTRAS
    (r'(volumes/COCIRS_[01]xxx.*/COCIRS_....)/DATA/CUBE/\w+/(\w+_F[134]).*',
                                                                            0, [r'\1/DATA/CUBE/*/\2*',
                                                                                r'\1/DATA/EXTRAS/*/\2*']),
    (r'(volumes/COCIRS_[01]xxx.*/COCIRS_....)/DATA/CUBE/(\w+/\w+)\..*',     0, [r'\1/EXTRAS/CUBE_OVERVIEW/\2.JPG',
                                                                                r'\1/EXTRAS/CUBE_OVERVIEW/\2.LBL']),
    (r'(volumes/COCIRS_[01]xxx.*/COCIRS_....)/DATA/CUBE/(\w+)$',            0,  r'\1/EXTRAS/CUBE_OVERVIEW/\2'),
    (r'(volumes/COCIRS_[01]xxx.*/COCIRS_....)/DATA/CUBE$',                  0,  r'\1/EXTRAS/CUBE_OVERVIEW'),

    # COCIRS_[01]xxx, volumes/EXTRAS to volumes/DATA and volumes/EXTRAS
    (r'(volumes/COCIRS_[01]xxx.*/COCIRS_....)/EXTRAS/CUBE_OVERVIEW/\w+/(\w+_F[134]).*',
                                                                            0, [r'\1/DATA/CUBE/*/\2*',
                                                                                r'\1/EXTRAS/CUBE_OVERVIEW/*/\2*']),
    (r'(volumes/COCIRS_[01]xxx.*/COCIRS_....)/EXTRAS/CUBE_OVERVIEW/(\w+)$', 0,  r'\1/DATA/CUBE/\2'),
    (r'(volumes/COCIRS_[01]xxx.*/COCIRS_....)/EXTRAS/CUBE_OVERVIEW$',       0,  r'\1/DATA/CUBE'),
    (r'(volumes/COCIRS_[01]xxx.*/COCIRS_....)/EXTRAS$',                     0,  r'\1/DATA'),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'.*/(COCIRS_[01]xxx)(|_v2)/(COCIRS_[01]...)/(DATA/CUBE|EXTRAS/CUBE_OVERVIEW)/(\w+/\w+_F[134]_\w+).*',
                                                                            0, [r'previews/\1/\3/DATA/CUBE/\5_full.jpg',
                                                                                r'previews/\1/\3/DATA/CUBE/\5_med.jpg',
                                                                                r'previews/\1/\3/DATA/CUBE/\5_small.jpg',
                                                                                r'previews/\1/\3/DATA/CUBE/\5_thumb.jpg']),
    (r'.*/(COCIRS_[01]xxx_v3/COCIRS_[01]...)/(DATA/CUBE|EXTRAS/CUBE_OVERVIEW)/(\w+/\w+_F[134]_\w+).*',
                                                                            0, [r'previews/\1/DATA/CUBE/\3_full.jpg',
                                                                                r'previews/\1/DATA/CUBE/\3_med.jpg',
                                                                                r'previews/\1/DATA/CUBE/\3_small.jpg',
                                                                                r'previews/\1/DATA/CUBE/\3_thumb.jpg']),
    (r'.*/(COCIRS_[01]xxx)(|v2)/(COCIRS_[01]...)/(DATA/CUBE|EXTRAS/CUBE_OVERVIEW)/(\w+)$',
                                                                            0,  r'previews/\1/\3/DATA/CUBE/\5'),
    (r'.*/(COCIRS_[01]xxx_v3/COCIRS_[01]...)/(DATA/CUBE|EXTRAS/CUBE_OVERVIEW)/(\w+)$',
                                                                            0,  r'previews/\1/DATA/CUBE/\3'),
    (r'.*/(COCIRS_[01]xxx)(|v2)/(COCIRS_[01]...)/(DATA/CUBE|EXTRAS/CUBE_OVERVIEW)$',
                                                                            0,  r'previews/\1/\3/DATA/CUBE'),
    (r'.*/(COCIRS_[01]xxx_v3/COCIRS_[01]...)/(DATA/CUBE|EXTRAS/CUBE_OVERVIEW)$',
                                                                            0,  r'previews/\1/DATA/CUBE'),
])

associations_to_diagrams = translator.TranslatorByRegex([
    (r'.*/(COCIRS_[56]xxx.*/COCIRS_[56].*)/BROWSE/(\w+/[A-Z]+[0-9]{10}_FP._6..).*',
                                                                            0, [r'diagrams/\1/BROWSE/\2_full.jpg',
                                                                                r'diagrams/\1/BROWSE/\2_thumb.jpg',
                                                                                r'diagrams/\1/BROWSE/\2_small.jpg',
                                                                                r'diagrams/\1/BROWSE/\2_med.jpg']),
    (r'.*/(COCIRS_[56]xxx.*/COCIRS_[56].*)/BROWSE/(\w+/[A-Z]+[0-9]{10}_FP.).*',
                                                                            0, [r'diagrams/\1/BROWSE/\2_full.jpg',
                                                                                r'diagrams/\1/BROWSE/\2_thumb.jpg',
                                                                                r'diagrams/\1/BROWSE/\2_small.jpg',
                                                                                r'diagrams/\1/BROWSE/\2_med.jpg']),
    (r'.*/(COCIRS_[56]xxx.*/COCIRS_[56].*)/BROWSE/(\w+)$',                  0,  r'diagrams/\1/BROWSE/\2'),
    (r'.*/(COCIRS_[56]xxx.*/COCIRS_[56].*)/BROWSE$',                        0,  r'diagrams/\1/BROWSE'),

    (r'.*/(COCIRS_[56]xxx.*/COCIRS_[56].*)/DATA/RINDATA/RIN(\w+)\..*',      0, [r'diagrams/\1/BROWSE/S_RINGS/RIN\2_full.jpg',
                                                                                r'diagrams/\1/BROWSE/S_RINGS/RIN\2_thumb.jpg',
                                                                                r'diagrams/\1/BROWSE/S_RINGS/RIN\2_small.jpg',
                                                                                r'diagrams/\1/BROWSE/S_RINGS/RIN\2_med.jpg']),
    (r'.*/(COCIRS_[56]xxx.*/COCIRS_[56].*)/DATA/GEODATA/GEO(\w+)_(6[^9].)\..*',
                                                                            0,  r'diagrams/\1/BROWSE/*/POI\2_FP?_\3*'),
    (r'.*/(COCIRS_[56]xxx.*/COCIRS_[56].*)/DATA/GEODATA/GEO(\w+)_699.*',    0,  r'diagrams/\1/BROWSE/SATURN/POI\2_FP?*'),
    (r'.*/(COCIRS_[56]xxx.*/COCIRS_[56].*)/DATA/APODSPEC/SPEC(\w+).*',      0,  r'diagrams/\1/BROWSE/*/*\2*'),
    (r'.*/(COCIRS_[56]xxx.*/COCIRS_[56].*)/DATA/ISPMDATA/ISPM(\w+).*',      0,  r'diagrams/\1/BROWSE/*/*\2*'),
    (r'.*/(COCIRS_[56]xxx.*/COCIRS_[56].*)/DATA/TARDATA/TAR(\w+).*',        0,  r'diagrams/\1/BROWSE/*/*\2*'),
    (r'.*/(COCIRS_[56]xxx.*/COCIRS_[56].*)/DATA/POIDATA/POI(\w+).*',        0,  r'diagrams/\1/BROWSE/*/*\2*'),
    (r'.*/(COCIRS_[56]xxx.*/COCIRS_[56].*)/DATA(|/\w+)$',                   0,  r'diagrams/\1/BROWSE'),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl',  re.I, ''),

    (r'volumes/(COCIRS_[01].*)/DATA/CUBE/(\w+/\w+)\.tar\.gz',        0, r'previews/\1/DATA/CUBE/\2_*.jpg'),
    (r'volumes/(COCIRS_[01].*)/EXTRAS/CUBE_OVERVIEW/(\w+/\w+)\.JPG', 0, r'previews/\1/DATA/CUBE/\2_*.jpg'),

    (r'volumes/(COCIRS_[56].*)/BROWSE/(.*)_\w+\..*',                0,  r'diagrams/\1/BROWSE/\2*.jpg'),
    (r'volumes/(COCIRS_[56].*)/DATA/RINDATA/RIN(\w+)\..*',          0, (r'diagrams/\1/BROWSE/S_RINGS/RIN\2_*.jpg',
                                                                        r'diagrams/\1/BROWSE/TARGETS/IMG\2_*.jpg')),
    (r'volumes/(COCIRS_[56].*)/DATA/GEODATA/GEO(\w+)_(6..)\..*',    0, (r'diagrams/\1/BROWSE/*/POI\2_FP?_\3_*.jpg',
                                                                        r'diagrams/\1/BROWSE/TARGETS/IMG\2_FP?_*.jpg')),
    (r'volumes/(COCIRS_[56].*)/DATA/POIDATA/POI(\w+)\..*',          0, r'diagrams/\1/BROWSE/TARGETS/IMG\2_*.jpg'),
    (r'volumes/(COCIRS_[56].*)/DATA/APODSPEC/SPEC(\w+)\..*',        0, r'diagrams/\1/BROWSE/TARGETS/IMG\2_*.jpg'),
    (r'volumes/(COCIRS_[56].*)/DATA/ISPMDATA/ISPM(\w+)\..*',        0, r'diagrams/\1/BROWSE/TARGETS/IMG\2_*.jpg'),
    (r'volumes/(COCIRS_[56].*)/DATA/TARDATA/TAR(\w+)\..*',          0, r'diagrams/\1/BROWSE/TARGETS/IMG\2_*.jpg'),
])

s_rings_viewables = translator.TranslatorByRegex([
    (r'volumes/(COCIRS_[56].*)/DATA/\w+/(SPEC|ISPM|TAR)(\w+)\..*',  0, r'diagrams/\1/BROWSE/S_RINGS/RIN\2_*.jpg'),
    (r'volumes/(COCIRS_[56].*)/DATA/\w+/GEO(\w+)_699\..*',          0, r'diagrams/\1/BROWSE/S_RINGS/RIN\2_*.jpg'),
])

saturn_viewables = translator.TranslatorByRegex([
    (r'volumes/(COCIRS_[56].*)/DATA/\w+/(SPEC|ISPM|TAR|POI)(\w+)\..*', 0, r'diagrams/\1/BROWSE/SATURN/POI\2_*.jpg'),
    (r'volumes/(COCIRS_[56].*)/DATA/\w+/GEO(\w+)_699\..*',             0, r'diagrams/\1/BROWSE/SATURN/POI\2_*.jpg'),
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
    (r'.*\.DAT$', 0, ('Binary', 'Table')),
    (r'.*\.TAB$', 0, ('ASCII', 'Table')),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

opus_products = translator.TranslatorByRegex([
    (r'.*volumes/(COCIRS_[56]xxx/COCIRS_[56]...)/DATA/.\w+/[A-Z]+([0-9]{10})_(FP.)\.(TAB|DAT|LBL)', 0,
            [r'volumes/\1/DATA/APODSPEC/SPEC\2_\3.DAT',
             r'volumes/\1/DATA/APODSPEC/SPEC\2_\3.LBL',
             r'volumes/\1/DATA/GEODATA/GEO\2_6*',
             r'volumes/\1/DATA/POIDATA/POI\2_\3.*',
             r'volumes/\1/DATA/RINDATA/RIN\2_\3.*',
             r'volumes/\1/DATA/TARDATA/TAR\2_\3.*',
             r'volumes/\1/BROWSE/TARGETS/IMG\2_\3.*',
             r'volumes/\1/BROWSE/SATURN/POI\2_\3.*',
             r'volumes/\1/BROWSE/S_RINGS/RIN\2_\3.*',
             r'volumes/\1/BROWSE/*/POI\2_\3_*.*',
             r'diagrams/\1/BROWSE/*/POI\2_\3_*.jpg',
             r'diagrams/\1/BROWSE/S_RINGS/RIN\2_\3_*.jpg',
             r'diagrams/\1/BROWSE/TARGETS/IMG\2_\3*.jpg']),
])

####################################################################################################################################
# FILESPEC_TO_OPUS_ID
####################################################################################################################################

filespec_to_opus_id = translator.TranslatorByRegex([
    (r'COCIRS_[56].../DATA/\w+/[A-Z]+([0-9]{10})_FP(.)\.(DAT|TAB|LBL)$', 0, r'co-cirs-\1-fp\2'),
])

####################################################################################################################################
# OPUS_ID_TO_FILESPEC
####################################################################################################################################

opus_id_to_filespec = translator.TranslatorByRegex([
    (r'co-cirs-.*', 0, re.compile(r'.*ISPM[0-9]{10}_FP.\.LBL')),
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
    FILESPEC_TO_OPUS_ID = filespec_to_opus_id

    VIEWABLES = viewables

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']  = associations_to_volumes
    ASSOCIATIONS['previews'] = associations_to_previews
    ASSOCIATIONS['diagrams'] = associations_to_diagrams

pdsfile.PdsFile.OPUS_ID_TO_FILESPEC = opus_id_to_filespec + pdsfile.PdsFile.OPUS_ID_TO_FILESPEC

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COCIRS_xxxx'] = COCIRS_xxxx

####################################################################################################################################
