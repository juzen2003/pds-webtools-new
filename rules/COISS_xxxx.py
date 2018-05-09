####################################################################################################################################
# rules/COISS_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'calibrated/COISS_1xxx'     , re.I, ('Cassini Jupiter image collection, CISSCAL 3.8', 'VOLDIR')),
    (r'calibrated/COISS_2xxx'     , re.I, ('Cassini Saturn  image collection, CISSCAL 3.8', 'VOLDIR')),
    (r'calibrated/COISS_1xxx_v1.0', re.I, ('Cassini Jupiter image collection, CISSCAL 3.6', 'VOLDIR')),
    (r'calibrated/COISS_2xxx_v1.0', re.I, ('Cassini Saturn  image collection, CISSCAL 3.6', 'VOLDIR')),

    (r'volumes/.*/data/.*/N[0-9_]+\.img',                     re.I, ('Narrow-angle image, VICAR',     'IMAGE'   )),
    (r'volumes/.*/data/.*/W[0-9_]+\.img',                     re.I, ('Wide-angle image, VICAR',       'IMAGE'   )),
    (r'volumes/.*/data/.*/extras(/\w+)*(|/)',                 re.I, ('Preview image collection',      'BROWDIR' )),
    (r'volumes/.*/data/.*/extras/.*\.(jpeg|jpeg_small|tiff)', re.I, ('Preview image',                 'BROWSE'  )),
    (r'volumes/.*/COISS_0011/document/.*/[0-9]+\.[0-9]+(|/)', re.I, ('Calibration report',            'INFODIR' )),
    (r'volumes/.*/data(|/\w*)',                               re.I, ('Images grouped by SC clock',    'IMAGEDIR')),

    (r'calibrated/.*_calib\.img',                             re.I, ('Calibrated image, VICAR',       'IMAGE'   )),
    (r'calibrated/.*/data(|/\w+)',                            re.I, ('Calibrated images by SC clock', 'IMAGEDIR')),
    (r'calibrated/\w+(|/\w+)',                                re.I, ('Calibrated image collection',   'IMAGEDIR')),

    (r'.*/thumbnail(/\w+)*',            re.I, ('Small browse images',           'BROWDIR' )),
    (r'.*/thumbnail/.*\.(gif|jpg|jpeg|jpeg_small|tif|tiff|png)', 
                                        re.I, ('Small browse image',            'BROWSE'  )),
    (r'.*/(tiff|full)(/\w+)*',          re.I, ('Full-size browse images',       'BROWDIR' )),
    (r'.*/(tiff|full)/.*\.(tif|tiff|png)', 
                                        re.I, ('Full-size browse image',        'BROWSE'  )),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'volumes/(.*/data/\w+/.*)\.(\w+)',  0, (r'previews/\1_thumb.*',
                                              r'previews/\1_small.*',
                                              r'previews/\1_med.*',
                                              r'previews/\1_full.*')),
    (r'calibrated/(COISS_....)(|_.*?)/(\w+/data/\w+/.*)_CALIB\.(\w+)', 0, (r'previews/\1/\3_thumb.*',
                                                                           r'previews/\1/\3_small.*',
                                                                           r'previews/\1/\3_med.*',
                                                                           r'previews/\1/\3_full.*')),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'previews/(.*)_(\w+\..*)',     0, r'volumes/\1.*'),
    (r'previews/(\w+/\w+/data/\w+)', 0, r'volumes/\1'),
    (r'previews/(\w+/\w+/data)',     0, r'volumes/\1'),
    (r'calibrated/(COISS_....)(|_.*?)/(\w+/data/\w+/\w+)_(CALIB\..*)', 0, r'volumes/\1/\3.*'),
    (r'calibrated/(COISS_....)(|_.*?)/(\w+/data/\w+)',                 0, r'volumes/\1/\3'),
    (r'calibrated/(COISS_....)(|_.*?)/(\w+/data)',                     0, r'volumes/\1/\3'),
    (r'calibrated/(COISS_....)(|_.*?)/(\w+)',                          0, r'volumes/\1/\3'),
    (r'calibrated/(COISS_....)(|_.*?)',                                0, r'volumes/\1'),
])

volumes_to_calibrated = translator.TranslatorByRegex([
    (r'volumes/(.*)\..*',             0, r'calibrated/\1_CALIB.*'),
    (r'volumes/(\w+/\w+/data)',       0, r'calibrated/\1'),
    (r'volumes/(\w+/\w+/data/\w+)',   0, r'calibrated/\1'),
    (r'volumes/(\w+)(/\w+/data)',     0, r'calibrated/\1_v1.0\2'),
    (r'volumes/(\w+)(/\w+/data/\w+)', 0, r'calibrated/\1_v1.0\2'),
])

volumes_to_previews = translator.TranslatorByRegex([
    (r'volumes/(.*)\..*',           0, r'previews/\1_*.*'),
    (r'volumes/(\w+/\w+/data)',     0, r'previews/\1'),
    (r'volumes/(\w+/\w+/data/\w+)', 0, r'previews/\1'),
])

volumes_to_volumes = translator.TranslatorByRegex([
    (r'(volumes/.*)/extras/\w+/(\w+)\.(.*)', 0, [r'\1/data/\2.*',
                                                 r'\1/extras/*/\2.*']),
    (r'(volumes/.*)/data/(\w+)\.(.*)',       0,  r'volumes/\1/extras/*/\2.*'),

    (r'(volumes/.*)/extras/\w+/(\w+)',       0, [r'\1/data/\2',
                                                 r'\1/extras/*/\2']),
    (r'(volumes/.*)/data/(\w+)',             0,  r'\1/extras/*/\2'),

    (r'(volumes/.*)/extras(|/\w+)',          0, [r'\1/data', r'\1/extras/*']),
    (r'(volumes/.*)/data',                   0,  r'\1/extras/*'),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews|calibrated)/COISS_[12]xxx(|_.*)/COISS_..../data(|/\w+)',       0, (True, True, True )),
    (r'(volumes|previews|calibrated)/COISS_[12]xxx(|_.*)/COISS_..../extras/\w+(|/\w+)', 0, (True, True, True )),
    (r'volumes/COISS_3xxx(|_.*)/COISS_..../data/(images|maps)',                         0, (True, True, False)),
    (r'volumes/COISS_3xxx(|_.*)/COISS_..../extras/\w+/images',                          0, (True, True, False)),
    (r'previews/COISS_3xxx(|_.*)/COISS_..../data/(images|maps)',                        0, (True, True, False)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'volumes/COISS_0xxx(|_\w+)/COISS_....',                    0, r'volumes/COISS_0xxx\1/*'),
    (r'volumes/COISS_0xxx(|_\w+)/COISS_..../data',               0, r'volumes/COISS_0xxx\1/*/data'),
    (r'volumes/COISS_0xxx(|_\w+)/COISS_..../data/(\w+)',         0, r'volumes/COISS_0xxx\1/*/data/\2'),
    (r'volumes/COISS_0xxx(|_\w+)/COISS_..../data/(\w+/\w+)',     0, r'volumes/COISS_0xxx\1/*/data/\2'),
    (r'volumes/COISS_0xxx(|_\w+)/COISS_..../data/(\w+/\w+)/\w+', 0, r'volumes/COISS_0xxx\1/*/data/\2/*'),

    (r'(volumes|previews)/COISS_3xxx(|_\w+)/COISS_....',                    0, r'\1/COISS_3xxx\2/*'),
    (r'(volumes|previews)/COISS_3xxx(|_\w+)/COISS_..../data',               0, r'\1/COISS_3xxx\2/*/data'),
    (r'(volumes|previews)/COISS_3xxx(|_\w+)/COISS_..../data/(\w+)',         0, r'\1/COISS_3xxx\2/*/data/\3'),
    (r'(volumes|previews)/COISS_3xxx(|_\w+)/COISS_..../extras',             0, r'\1/COISS_3xxx\2/*/extras'),
    (r'(volumes|previews)/COISS_3xxx(|_\w+)/COISS_..../extras/(\w+)',       0, r'\1/COISS_3xxx\2/*/extras/\3'),
    (r'(volumes|previews)/COISS_3xxx(|_\w+)/COISS_..../extras/(\w+)/\w+',   0, r'\1/COISS_3xxx\2/*/extras/\3/*'),

    (r'(volumes|previews|calibrated)/(COISS_[12]...)(|_.*?)/COISS_....',            0, r'\1/\2\3/*'),
    (r'(volumes|previews|calibrated)/(COISS_[12]...)(|_.*?)/COISS_..../data',       0, r'\1/\2\3/*/data'),
    (r'(volumes|previews|calibrated)/(COISS_[12]...)(|_.*?)/COISS_..../data/(\w+)', 0, r'\1/\2\3/*/data/*'),

    (r'volumes/(COISS_[12]xxx)/COISS_..../extras/(\w+)/\w+', 0, r'volumes/\1/*/extras/\2/*'),
    (r'volumes/(COISS_[12]xxx)/COISS_..../extras/(\w+)',     0, r'volumes/\1/*/extras/\2'),
    (r'volumes/(COISS_[12]xxx)/COISS_..../(\w+)',            0, r'volumes/\1/*/\2'),
])

####################################################################################################################################
# SORT_KEY
####################################################################################################################################

sort_key = translator.TranslatorByRegex([

    # Skips over N or W, placing files into chronological order
    (r'([NW])([0-9]{10}_[0-9]+(?:|_\w+))\.(.*)', 0, r'\2\1\3'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class COISS_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('COISS_[0123]xxx', re.I, 'COISS_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS
    SORT_KEY = sort_key + pdsfile.PdsFile.SORT_KEY
    ASSOCIATIONS_TO_VOLUMES = associations_to_volumes + pdsfile.PdsFile.ASSOCIATIONS_TO_VOLUMES

    VIEWABLES = {'default': default_viewables}

    VOLUMES_TO_ASSOCIATIONS = pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS.copy()
    VOLUMES_TO_ASSOCIATIONS['volumes'] = volumes_to_volumes + pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS['volumes']
    VOLUMES_TO_ASSOCIATIONS['calibrated'] = volumes_to_calibrated + pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS['calibrated']
    VOLUMES_TO_ASSOCIATIONS['previews'] = volumes_to_previews + pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS['previews']

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COISS_xxxx'] = COISS_xxxx

####################################################################################################################################
