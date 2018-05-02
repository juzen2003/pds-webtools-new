####################################################################################################################################
# rules/HSTxx_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*/data/visit_..',                    re.I, ('Images grouped by visit',              'IMAGEDIR')),
    (r'volumes/.*/data/visit.*/.*\.TIF',             re.I, ('16-bit unscaled TIFF of raw image',    'IMAGE')   ),
    (r'volumes/.*/data/visit.*/.*DRZ\.JPG',          re.I, ('Preview of "drizzled" image',          'IMAGE')   ),
    (r'volumes/.*/data/visit.*/.*_(D0M|RAW).*\.JPG', re.I, ('Preview of raw image',                 'IMAGE')   ),
    (r'volumes/.*/data/visit.*/.*_X1D.*\.JPG',       re.I, ('Line plot of spectrum',                'DATA')    ),
    (r'volumes/.*/data/visit.*/.*_X2D.*\.JPG',       re.I, ('Preview of 2-D image',                 'IMAGE')   ),
    (r'volumes/.*/data/visit.*/.*_FLT.*\.JPG',       re.I, ('Preview of calibrated image',          'IMAGE')   ),
    (r'volumes/.*/data/visit.*/.*\.ASC',             re.I, ('Listing of FITS label info',           'INFO')    ),
    (r'volumes/.*/data/visit.*/.*\.LBL',             re.I, ('PDS label with download instructions', 'LABEL')   ),
])

####################################################################################################################################
# SPLIT_RULES
####################################################################################################################################

split_rules = translator.TranslatorByRegex([
    (r'([IJUO]\w{8})(|_\w+)\.(.*)', 0, (r'\1', r'\2', r'.\3')),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'previews/(.*)_(thumb|small|med|full)\.jpg', 0, r'volumes/\1_*.*'),
])

volumes_to_previews = translator.TranslatorByRegex([
    (r'volumes/(.*/DATA/VISIT_..)/([IJUO]\w{8})(|_\w+)\.(.*)', 0, [r'previews/\1/\2_thumb.jpg',
                                                                   r'previews/\1/\2_small.jpg',
                                                                   r'previews/\1/\2_med.jpg',
                                                                   r'previews/\1/\2_full.jpg']),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'volumes/(.*/DATA/VISIT_..)/([IJUO]\w{8})(|_\w+)\.(.*)', 0, (r'previews/\1/\2_thumb.jpg',
                                                                   r'previews/\1/\2_small.jpg',
                                                                   r'previews/\1/\2_med.jpg',
                                                                   r'previews/\1/\2_full.jpg')),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews)/HST.x_xxxx/HST.._..../DATA(|/VISIT_..)', 0, (True, True, True)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'(volumes|previews)/(HST.x_xxxx/HST.._..../DATA)',            re.I, r'\1/\2'),
    (r'(volumes|previews)/(HST.x_xxxx/HST.._..../DATA)/(VISIT_..)', re.I, r'\1/\2/*'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class HSTxx_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('HST.x_xxxx', re.I, 'HSTxx_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
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

pdsfile.PdsFile.SUBCLASSES['HSTxx_xxxx'] = HSTxx_xxxx

####################################################################################################################################
