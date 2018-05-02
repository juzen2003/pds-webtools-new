####################################################################################################################################
# rules/VGISS_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*/data',             re.I, ('Images grouped by SC clock',        'IMAGEDIR')),
    (r'volumes/.*/data/C[0-9]+X+',   re.I, ('Images grouped by SC clock',        'IMAGEDIR')),
    (r'volumes/.*/browse',           re.I, ('Browse images grouped by SC clock', 'IMAGEDIR')),
    (r'volumes/.*/browse/C[0-9]+X+', re.I, ('Browse images grouped by SC clock', 'IMAGEDIR')),
    (r'volumes/.*_raw\.img',         re.I, ('Raw image, VICAR',                  'IMAGE'   )),
    (r'volumes/.*_cleaned\.img',     re.I, ('Cleaned raw image, VICAR',          'IMAGE'   )),
    (r'volumes/.*_calib\.img',       re.I, ('Calibrated image, VICAR',           'IMAGE'   )),
    (r'volumes/.*_geomed\.img',      re.I, ('Undistorted image, VICAR',          'IMAGE'   )),
    (r'volumes/.*_geoma\.tab',       re.I, ('ASCII distortion table',            'TABLE'   )),
    (r'volumes/.*_geoma\.dat',       re.I, ('Distortion file, VICAR',            'DATA'    )),
    (r'volumes/.*_resloc\.dat',      re.I, ('Reseau table, VICAR',               'DATA'    )),
    (r'volumes/.*_resloc\.tab',      re.I, ('ASCII Reseau table',                'TABLE'   )),
    (r'volumes/.*/MIPL/.*\.dat',     re.I, ('VICAR data file',                   'DATA'    )),
    (r'volumes/.*/DARKS/.*\.img',    re.I, ('Dark current image, VICAR',         'IMAGE'   )),
])

####################################################################################################################################
# SORT_KEY
####################################################################################################################################

sort_key = translator.TranslatorByRegex([

    # Sort data files into increasing level of processing
    (r'(.*)(_RAW)\.(JPG|IMG)',        0, r'\1_1RAW.\3'    ),
    (r'(.*)(_CLEANED)\.(JPG|IMG)',    0, r'\1_2CLEANED.\3'),
    (r'(.*)(_CALIB)\.(JPG|IMG)',      0, r'\1_3CALIB.\3'  ),
    (r'(.*)(_GEOMED)\.(JPG|IMG)',     0, r'\1_4GEOMED.\3' ),
    (r'(.*)(_RESLOC)\.(DAT|TAB)',     0, r'\1_5RESLOC.\3' ),
    (r'(.*)(_GEOMA)\.(DAT|TAB)',      0, r'\1_6GEOMA.\3'  ),

    (r'(.*)(_RAW)\.LBL',        0, r'\1_1RAW.zLBL'    ),    # Label after matching file, not after everything
    (r'(.*)(_CLEANED)\.LBL',    0, r'\1_2CLEANED.zLBL'),
    (r'(.*)(_CALIB)\.LBL',      0, r'\1_3CALIB.zLBL'  ),
    (r'(.*)(_GEOMED)\.LBL',     0, r'\1_4GEOMED.zLBL' ),
    (r'(.*)(_RESLOC)\.LBL',     0, r'\1_5RESLOC.zLBL' ),
    (r'(.*)(_GEOMA)\.LBL',      0, r'\1_6GEOMA.zLBL'  ),
])

####################################################################################################################################
# SPLIT_RULES
####################################################################################################################################

split_rules = translator.TranslatorByRegex([
    (r'(.*)_(RAW|CLEANED|CALIB|GEOMED|RESLOC|GEOMA)\.(.*)$', 0, (r'\1', r'_\2', r'.\3')),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'volumes/(.*)/DATA/(.*)(_[A-Z]+)\.(IMG|LBL|DAT|TAB)', 0, r'volumes/\1/BROWSE/\2\3.*'),
    (r'volumes/(.*)/BROWSE/(.*)\.(JPG|LBL)',                0, r'volumes/\1/DATA/\2.*'),
    (r'volumes/(.*)/DATA/(\w+)',                            0, r'volumes/\1/BROWSE/\2'),
    (r'volumes/(.*)/BROWSE/(\w+)',                          0, r'volumes/\1/DATA/\2'),
    (r'previews/(.*)_(thumb|small|med|full)\.jpg',          0, r'volumes/\1_*.*'),
])

volumes_to_previews = translator.TranslatorByRegex([
    (r'volumes/(.*)/(DATA/.*)_(RAW|CLEANED|CALIB|GEOMED)\..*', 0, [r'previews/\1/\2_thumb.jpg',
                                                                   r'previews/\1/\2_small.jpg',
                                                                   r'previews/\1/\2_med.jpg',
                                                                   r'previews/\1/\2_full.jpg']),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews)/VGISS_..../VGISS_..../(DATA|BROWSE)',     0, (True, True, True)),
    (r'(volumes|previews)/VGISS_..../VGISS_..../(DATA|BROWSE)/\w+', 0, (True, True, True)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'(volumes|previews)/(VGISS_..../VGISS_..)../(DATA|BROWSE)',     0, r'\1/\2*/\3'),
    (r'(volumes|previews)/(VGISS_..../VGISS_..)../(DATA|BROWSE)/\w+', 0, r'\1/\2*/\3/*'),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'volumes/(.*)/(DATA/\w+/.*)_(RAW|CLEANED|CALIB|GEOMED)\..*', 0, (r'previews/\1/\2_thumb.jpg',
                                                                       r'previews/\1/\2_small.jpg',
                                                                       r'previews/\1/\2_med.jpg',
                                                                       r'previews/\1/\2_full.jpg')),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class VGISS_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('VGISS_[5678]xxx', re.I, 'VGISS_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    SORT_KEY = sort_key + pdsfile.PdsFile.SORT_KEY
    SPLIT_RULES = split_rules + pdsfile.PdsFile.SPLIT_RULES
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS

    ASSOCIATIONS_TO_VOLUMES = associations_to_volumes + pdsfile.PdsFile.ASSOCIATIONS_TO_VOLUMES

    VOLUMES_TO_ASSOCIATIONS = pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS.copy()
    VOLUMES_TO_ASSOCIATIONS['previews'] = volumes_to_previews + pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS['previews']

    VIEWABLES = {'default': default_viewables}

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['VGISS_xxxx'] = VGISS_xxxx

####################################################################################################################################

