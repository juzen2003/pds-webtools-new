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
    (r'([IJUON]\w{8})(|_\w+)\.(.*)', 0, (r'\1', r'\2', r'.\3')),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'.*/(HST.._....)(|_.*)/(HST.._..../DATA/VISIT_../\w{9}).*',   0, r'volumes/\1/\3*'),
    (r'.*/(HST.._....)(|_.*)/(HST.._..../DATA/VISIT_..)$',          0, r'volumes/\1/\3'),
    (r'.*/(HST.._....)(|_.*)/(HST.._..../DATA)$',                   0, r'volumes/\1/\3'),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'.*/(HST.._....)(|_.*)/(HST.._..../DATA/VISIT_../\w{9}).*',   0, [r'previews/\1/\3_full.jpg',
                                                                        r'previews/\1/\3_thumb.jpg',
                                                                        r'previews/\1/\3_small.jpg',
                                                                        r'previews/\1/\3_med.jpg']),
    (r'.*/(HST.._....)(|_.*)/(HST.._..../DATA/VISIT_..)$',          0,  r'previews/\1/\3'),
    (r'.*/(HST.._....)(|_.*)/(HST.._..../DATA)$',                   0,  r'previews/\1/\3'),
])

associations_to_metadata = translator.TranslatorByRegex([
    (r'.*/(HST.._....)(|_.*)/(HST.._....)/DATA/VISIT_../(\w{9}).*', 0, [r'metadata/\1/\3/\3_index.tab/\4',
                                                                        r'metadata/\1/\3/\3_hstfiles.tab/\4',
                                                                        r'metadata/\1/\3']),
    (r'.*/(HST.._....)(|_.*)/(HST.._....)/DATA/VISIT_..$',          0,  r'metadata/\1/\3'),
    (r'.*/(HST.._....)(|_.*)/(HST.._....)/DATA$',                   0,  r'metadata/\1/\3'),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'volumes/(.*/DATA/VISIT_..)/([IJUON]\w{8})(|_\w+)\.(.*)', 0, (r'previews/\1/\2_thumb.jpg',
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
    (r'volumes/.*\.ASC$',                 0, ('HST',  10, 'hst-text',        'FITS Header Text')),
    (r'volumes/.*\.LBL$',                 0, ('HST',  10, 'hst-label',       'HST Preview Products')),
    (r'volumes/.*\.TIF$',                 0, ('HST',  20, 'hst-tiff',        'Raw Data Preview (lossless)')),
    (r'volumes/.*_(RAW.*|D0M_...)\.JPG$', 0, ('HST',  30, 'hst-raw',         'Raw Data Preview')),
    (r'volumes/.*_(FLT.*|CAL)\.JPG$',     0, ('HST',  40, 'hst-calib',       'Calibrated Data Preview')),
    (r'volumes/.*_SFL\.JPG$',             0, ('HST',  50, 'hst-summed',      'Calibrated Summed Preview')),
    (r'volumes/.*_CRJ\.JPG$',             0, ('HST',  60, 'hst-cosmic-ray',  'Calibrated Cosmic Ray Cleaned Preview')),
    (r'volumes/.*_DRZ\.JPG$',             0, ('HST',  70, 'hst-drizzled',    'Calibrated Geometrically Corrected Preview')),
    (r'volumes/.*_IMA\.JPG$',             0, ('HST',  80, 'hst-ima',         'Pre-mosaic Preview')),
    (r'volumes/.*_MOS\.JPG$',             0, ('HST',  90, 'hst-mosaic',      'Mosaic Preview')),
    (r'volumes/.*_(X1D|SX1)\.JPG$',       0, ('HST', 100, 'hst-1d-spectrum', '1-D Spectrum Preview')),
    (r'volumes/.*_(X2D|SX2)\.JPG$',       0, ('HST', 110, 'hst-2d-spectrum', '2-D Spectrum Preview')),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

opus_products = translator.TranslatorByRegex([
    (r'.*volumes/(HST.x_xxxx)(|_v.+)/(HST.._....)/(DATA/VISIT_../.{9}).*', 0, [r'volumes/\1/\3/\4*',
                                                                               r'volumes/\1_v*/\3/\4*',
                                                                               r'previews/\1/\3/\4_thumb.jpg',
                                                                               r'previews/\1/\3/\4_small.jpg',
                                                                               r'previews/\1/\3/\4_med.jpg',
                                                                               r'previews/\1/\3/\4_full.jpg'])
])

####################################################################################################################################
# FILESPEC_TO_OPUS_ID
####################################################################################################################################

filespec_to_opus_id = translator.TranslatorByRegex([
    # Associated HST products share an OPUS ID based on the first nine characters of the file's basename.
    (r'HSTI(.)_(....)(|_v.+)/DATA/VISIT_../(\w{8}).*',  0, r'hst-\1\2-wfc3-\4'),
    (r'HSTJ(.)_(....)(|_v.+)/DATA/VISIT_../(\w{8}).*',  0, r'hst-\1\2-acs-\4'),
    (r'HSTN(.)_(....)(|_v.+)/DATA/VISIT_../(\w{8}).*',  0, r'hst-\1\2-nicmos-\4'),
    (r'HSTO(.)_(....)(|_v.+)/DATA/VISIT_../(\w{8}).*',  0, r'hst-\1\2-stis-\4'),
    (r'HSTU(.)_(....)(|_v.+)/DATA/VISIT_../(\w{8}).*',  0, r'hst-\1\2-wfpc2-\4'),
])

####################################################################################################################################
# OPUS_ID_TO_FILESPEC
####################################################################################################################################

opus_id_to_filespec = translator.TranslatorByRegex([
    # The filespec returned points to the combined-detached label.
    (r'hst-.*', 0,  re.compile(r'.*\.LBL$')),
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

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_PRODUCTS = opus_products
    FILESPEC_TO_OPUS_ID = filespec_to_opus_id

    VIEWABLES = {'default': default_viewables}

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']  = associations_to_volumes
    ASSOCIATIONS['previews'] = associations_to_previews
    ASSOCIATIONS['metadata'] = associations_to_metadata

    FILENAME_KEYLEN = 9     # trim off suffixes

# Global attributes shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_FILESPEC = opus_id_to_filespec + pdsfile.PdsFile.OPUS_ID_TO_FILESPEC
pdsfile.PdsFile.FILESPEC_TO_LOGICAL_PATH = filespec_to_logical_path + pdsfile.PdsFile.FILESPEC_TO_LOGICAL_PATH

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['HSTxx_xxxx'] = HSTxx_xxxx

####################################################################################################################################
