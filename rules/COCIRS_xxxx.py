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
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    # COCIRS_[56]xxx, diagrams to volumes
    (r'diagrams/(COCIRS_[56].*)/BROWSE',                                0, [r'volumes/\1/BROWSE',
                                                                            r'volumes/\1/DATA']),
    (r'diagrams/(COCIRS_[56].*)/BROWSE/(\w+)',                          0, [r'volumes/\1/BROWSE/\2',
                                                                            r'volumes/\1/DATA']),
    (r'diagrams/(COCIRS_[56].*)/BROWSE/(\w+/\w+)_\w+\.jpg',             0,  r'volumes/\1/BROWSE/\2.*'),

    (r'diagrams/(COCIRS_[56].*)/BROWSE/\w+/RIN(\w+)_(FP.)\..*',         0, [r'volumes/\1/DATA/*/RIN\2_\3.*',
                                                                            r'volumes/\1/DATA/*/ISPM\2_\3.*',
                                                                            r'volumes/\1/DATA/*/SPEC\2_\3.*',
                                                                            r'volumes/\1/DATA/*/TAR\2_\3.*',
                                                                            r'volumes/\1/DATA/*/GEO\2_699.*']),

    (r'diagrams/(COCIRS_[56].*)/BROWSE/\w+/POI(\w+)_(FP.)_(6..)\..*',   0, [r'volumes/\1/DATA/*/GEO\2_\4.*',
                                                                            r'volumes/\1/DATA/*/ISPM\2_\3.*',
                                                                            r'volumes/\1/DATA/*/SPEC\2_\3.*',
                                                                            r'volumes/\1/DATA/*/TAR\2_\3.*',
                                                                            r'volumes/\1/DATA/*/POI\2_\3.*']),

    (r'diagrams/(COCIRS_[56].*)/BROWSE/\w+/IMG(\w+)_(FP.)\..*',         0, [r'volumes/\1/DATA/*/GEO\2_*.*',
                                                                            r'volumes/\1/DATA/*/ISPM\2_\3.*',
                                                                            r'volumes/\1/DATA/*/SPEC\2_\3.*',
                                                                            r'volumes/\1/DATA/*/TAR\2_\3.*',
                                                                            r'volumes/\1/DATA/*/POI\2_\3.*',
                                                                            r'volumes/\1/DATA/*/RIN\2_\3.*']),

    # COCIRS_[01]xxx, previews to volumes
    (r'previews/(COCIRS_[01].*)/DATA/CUBE',                             0, [r'volumes/\1/DATA/CUBE',
                                                                            r'volumes/\1/EXTRAS/CUBE_OVERVIEW']),
    (r'previews/(COCIRS_[01].*)/DATA/CUBE/(\w+)',                       0, [r'volumes/\1/DATA/CUBE/\2',
                                                                            r'volumes/\1/EXTRAS/CUBE_OVERVIEW/\2']),
    (r'previews/(COCIRS_[01].*)/DATA/CUBE/(\w+/\w+)_\w+.jpg',           0, [r'volumes/\1/DATA/CUBE/\2*',
                                                                            r'volumes/\1/EXTRAS/CUBE_OVERVIEW/\2*']),
])

volumes_to_volumes = translator.TranslatorByRegex([

    # COCIRS_[56]xxx, BROWSE directory to DATA directory
    (r'(volumes/COCIRS_[56].*)/BROWSE(|/\w+)',                              0,  r'\1/DATA'),
    (r'(volumes/COCIRS_[56].*)/BROWSE/\w+/[A-Z]+([0-9]+)(_FP.)\..*',        0, [r'\1/DATA/*/*\2\3*',
                                                                                r'\1/DATA/GEODATA/GEO\2*']),
    (r'(volumes/COCIRS_[56].*)/BROWSE/\w+/[A-Z]+([0-9]+)(_FP.)(_6..)\..*',  0, [r'\1/DATA/*/*\2\3*',
                                                                                r'\1/DATA/*/*/GEO\2\4*']),
    # COCIRS_[56]xxx, BROWSE directory to BROWSE directory
    (r'(volumes/COCIRS_[56].*)/BROWSE/\w+/[A-Z]+([0-9]+)(_FP.)(|_6..)\..*', 0, r'\1/BROWSE/*/*\2\3*.*'),

    # COCIRS_[56]xxx, DATA directory to DATA directory
    (r'(volumes/COCIRS_[56].*/DATA/\w+/[A-Z]+[0-9]+)_FP.(.*)',              0, r'\1_FP*'),                      # other focal planes
    (r'(volumes/COCIRS_[56].*/DATA)/\w+/[A-Z]+([0-9]+_FP.).*',              0, [r'\1/*/*\2*',                   # same FP, other file types
                                                                                r'\1/GEODATA/GEO\2_6??.*']),    # related GEO files
    (r'(volumes/COCIRS_[56].*/DATA)/\w+/GEO(\w+)_6.*',                      0, r'\1/*/*\2*.*'),                 # ignore FPs for GEO files

    # COCIRS_[56]xxx, DATA directory to BROWSE directory
    (r'(volumes/COCIRS_[56].*)/DATA(|/\w+)',                                0, r'\1/BROWSE'),
    (r'(volumes/COCIRS_[56].*)/DATA/\w+/[A-Z]+([0-9]+_FP.)\..*',            0, r'\1/BROWSE/*/*\2*'),
    (r'(volumes/COCIRS_[56].*)/DATA/\w+/[A-Z]+([0-9]+)_6..\..*',            0, r'\1/BROWSE/*/*\2*'),

    # COCIRS_[01]xxx, DATA to EXTRAS
    (r'(volumes/COCIRS_[01].*)/DATA/CUBE',                              0,  r'\1/EXTRAS/CUBE_OVERVIEW'),
    (r'(volumes/COCIRS_[01].*)/DATA/CUBE/(\w+)',                        0,  r'\1/EXTRAS/CUBE_OVERVIEW/\2'),
    (r'(volumes/COCIRS_[01].*)/DATA/CUBE/(\w+/\w+)\..*',                0,  r'\1/EXTRAS/CUBE_OVERVIEW/\2*.*'),

    # COCIRS_[01]xxx, EXTRAS to DATA
    (r'(volumes/COCIRS_[01].*)/EXTRAS/CUBE_OVERVIEW',                   0,  r'\1/DATA/CUBE'),
    (r'(volumes/COCIRS_[01].*)/EXTRAS/CUBE_OVERVIEW/(\w+)',             0,  r'\1/DATA/CUBE/\2'),
    (r'(volumes/COCIRS_[01].*)/EXTRAS/CUBE_OVERVIEW/(\w+/\w+)\..*',     0,  r'\1/DATA/CUBE/\2*.*'),
])

volumes_to_previews = translator.TranslatorByRegex([
    (r'volumes/(COCIRS_[01].*)/DATA/CUBE',                              0,  r'previews/\1/DATA/CUBE'),
    (r'volumes/(COCIRS_[01].*)/DATA/CUBE/(\w+)',                        0,  r'previews/\1/DATA/CUBE/\2'),
    (r'volumes/(COCIRS_[01].*)/DATA/CUBE/(\w+/\w+)\..*',                0,  r'previews/\1/DATA/CUBE/\2*.*'),

    (r'volumes/(COCIRS_[01].*)/EXTRAS/CUBE_OVERVIEW',                   0,  r'previews/\1/DATA/CUBE'),
    (r'volumes/(COCIRS_[01].*)/EXTRAS/CUBE_OVERVIEW/(\w+)',             0,  r'previews/\1/DATA/CUBE/\2'),
    (r'volumes/(COCIRS_[01].*)/EXTRAS/CUBE_OVERVIEW/(\w+/\w+)\..*',     0,  r'previews/\1/DATA/CUBE/\2*.*'),
])

volumes_to_diagrams = translator.TranslatorByRegex([
    (r'volumes/(COCIRS_[56].*)/BROWSE',                             0,  r'diagrams/\1/BROWSE'),
    (r'volumes/(COCIRS_[56].*)/BROWSE/(\w+)',                       0,  r'diagrams/\1/BROWSE/\2'),
    (r'volumes/(COCIRS_[56].*)/BROWSE/(.*)\..*',                    0,  r'diagrams/\1/BROWSE/\2*'),

    (r'volumes/(COCIRS_[56].*)/DATA(|\w+)',                         0,  r'diagrams/\1/BROWSE'),
    (r'volumes/(COCIRS_[56].*)/DATA/RINDATA/RIN(\w+).*',            0,  r'diagrams/\1/BROWSE/*/RIN\2*'),
    (r'volumes/(COCIRS_[56].*)/DATA/GEODATA/GEO(\w+)_(6..).*',      0,  r'diagrams/\1/BROWSE/*/POI\2_FP?_\3*'),
    (r'volumes/(COCIRS_[56].*)/DATA/GEODATA/GEO(\w+)_699.*',        0,  r'diagrams/\1/BROWSE/SATURN/POI\2_FP?*'),
    (r'volumes/(COCIRS_[56].*)/DATA/APODSPEC/SPEC(\w+).*',          0,  r'diagrams/\1/BROWSE/*/*\2*'),
    (r'volumes/(COCIRS_[56].*)/DATA/ISPMDATA/ISPM(\w+).*',          0,  r'diagrams/\1/BROWSE/*/*\2*'),
    (r'volumes/(COCIRS_[56].*)/DATA/TARDATA/TAR(\w+).*',            0,  r'diagrams/\1/BROWSE/*/*\2*'),
    (r'volumes/(COCIRS_[56].*)/DATA/POIDATA/POI(\w+).*',            0,  r'diagrams/\1/BROWSE/*/*\2*'),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
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
# Subclass definition
####################################################################################################################################

class COCIRS_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('COCIRS_[0156]xxx', re.I, 'COCIRS_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    ASSOCIATIONS_TO_VOLUMES = associations_to_volumes + pdsfile.PdsFile.ASSOCIATIONS_TO_VOLUMES
    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS
    SPLIT_RULES = split_rules + pdsfile.PdsFile.SPLIT_RULES

    VIEWABLES = viewables

    VOLUMES_TO_ASSOCIATIONS = pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS.copy()
    VOLUMES_TO_ASSOCIATIONS['volumes'] = volumes_to_volumes + pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS['volumes']
    VOLUMES_TO_ASSOCIATIONS['diagrams'] = volumes_to_diagrams + pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS['diagrams']
    VOLUMES_TO_ASSOCIATIONS['previews'] = volumes_to_previews + pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS['previews']

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COCIRS_xxxx'] = COCIRS_xxxx

####################################################################################################################################
