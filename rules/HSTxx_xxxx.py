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
    (r'volumes/.*/data/visit_..',                    re.I, ('Images grouped by visit',                  'IMAGEDIR')),
    (r'volumes/.*/data/visit.*/.*\.TIF',             re.I, ('16-bit unscaled TIFF of raw image',        'IMAGE')   ),
    (r'volumes/.*/data/visit.*/.*DRZ\.JPG',          re.I, ('Preview of "drizzled" image',              'IMAGE')   ),
    (r'volumes/.*/data/visit.*/.*_(D0M|RAW).*\.JPG', re.I, ('Preview of raw image',                     'IMAGE')   ),
    (r'volumes/.*/data/visit.*/.*_X1D.*\.JPG',       re.I, ('Line plot of spectrum',                    'DATA')    ),
    (r'volumes/.*/data/visit.*/.*_X2D.*\.JPG',       re.I, ('Preview of 2-D image',                     'IMAGE')   ),
    (r'volumes/.*/data/visit.*/.*_FLT.*\.JPG',       re.I, ('Preview of calibrated image',              'IMAGE')   ),
    (r'volumes/.*/data/visit.*/.*\.ASC',             re.I, ('Listing of FITS label info',               'INFO')    ),
    (r'volumes/.*/data/visit.*/.*\.LBL',             re.I, ('PDS label with download instructions',     'LABEL')   ),
    (r'volumes/.*/index/hstfiles\..*',               re.I, ('Index of associations between data files', 'INDEX')   ),
    (r'metadata/.*hstfiles\..*',                     re.I, ('Index of associations between data files', 'INDEX')   ),
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
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/.*\.ASC$',               0, 'HST FITS Header Text'),
    (r'volumes/.*\.TIF$',               0, 'HST Raw Data Preview (lossless)'),
    (r'volumes/.*_(RAW|D0M_...)\.JPG$', 0, 'HST Raw Data Preview'),
    (r'volumes/.*_(FLT|CAL)\.JPG$',     0, 'HST Calibrated Data Preview'),
    (r'volumes/.*_(DRZ|MOS|IMA)\.JPG$', 0, 'HST Preview of Line Spectrum'),
    (r'volumes/.*_X2D\.JPG$',           0, 'HST Preview of 2-D Spectrum'),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

opus_products = translator.TranslatorByRegex([
    (r'.*volumes/(HST.x_xxxx)/(HST.._....)/(DATA/VISIT_../.{9}).*', 0, [r'volumes/\1/\2/\3*',
                                                                        r'previews/\1/\2/\3_thumb.jpg',
                                                                        r'previews/\1/\2/\3_small.jpg',
                                                                        r'previews/\1/\2/\3_med.jpg',
                                                                        r'previews/\1/\2/\3_full.jpg'])
])

####################################################################################################################################
# OPUS_ID_TO_FILESPEC
####################################################################################################################################

opus_id_to_filespec = translator.TranslatorByRegex([
    # Associated HST products share an OPUS ID based on the first nine characters of the file's basename. The filespec returned
    # points to the combined-detached label.
    (r'(HST[A-Z]._....)/V(.*)$', 0,  r'\1/DATA/VISIT_\2.LBL'),
])

####################################################################################################################################
# FILESPEC_TO_OPUS_ID
####################################################################################################################################

filespec_to_opus_id = translator.TranslatorByRegex([
    # Associated HST products share an OPUS ID based on the first nine characters of the file's basename.
    (r'(HST[A-Z]._....)/DATA/VISIT_(../\w{9})\w*\....',  0, r'\1/V\2'),
])

####################################################################################################################################
# FILESPEC_TO_LOGICAL_PATH
####################################################################################################################################

filespec_to_logical_path = translator.TranslatorByRegex([
    (r'HST(.)(._..../.*_(thumb|small|med|full)\.(jpg|png))', 0, r'previews/HST\1x_xxxx/HST\1\2'),
    (r'HST(.)(._..../.*)$',                                  0, r'volumes/HST\1x_xxxx/HST\1\2'),
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

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_PRODUCTS = opus_products
    FILESPEC_TO_OPUS_ID = filespec_to_opus_id

    VOLUMES_TO_ASSOCIATIONS = pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS.copy()
    VOLUMES_TO_ASSOCIATIONS['previews'] = volumes_to_previews + pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS['previews']

    VIEWABLES = {'default': default_viewables}

    FILENAME_KEYLEN = 9     # trim off suffixes

# Global attributes shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_FILESPEC = opus_id_to_filespec + pdsfile.PdsFile.OPUS_ID_TO_FILESPEC
pdsfile.PdsFile.FILESPEC_TO_LOGICAL_PATH = filespec_to_logical_path + pdsfile.PdsFile.FILESPEC_TO_LOGICAL_PATH

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['HSTxx_xxxx'] = HSTxx_xxxx

####################################################################################################################################
