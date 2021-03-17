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
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'volumes/(.*/DATA/VISIT_..)/([IJUON]\w{8})(|_\w+)\.(.*)', 0,
        (r'previews/\1/\2_full.jpg',
         r'previews/\1/\2_med.jpg',
         r'previews/\1/\2_small.jpg',
         r'previews/\1/\2_thumb.jpg',
        ),
    ),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'.*/(HST.._....)(|_.*)/(HST.._..../DATA/VISIT_../\w{9}).*',   0, r'volumes/\1/\3*'),
    (r'.*/(HST.._....)(|_.*)/(HST.._..../DATA/VISIT_..)',           0, r'volumes/\1/\3'),
    (r'.*/(HST.._....)(|_.*)/(HST.._..../DATA)',                    0, r'volumes/\1/\3'),
    (r'.*/(HST.)9_9999.*',                                          0, r'volumes/\1x_xxxx'),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'.*/(HST.._....)(|_.*)/(HST.._..../DATA/VISIT_../\w{9}).*',   0, [r'previews/\1/\3_full.jpg',
                                                                        r'previews/\1/\3_med.jpg',
                                                                        r'previews/\1/\3_small.jpg',
                                                                        r'previews/\1/\3_thumb.jpg']),
    (r'.*/(HST.._....)(|_.*)/(HST.._..../DATA/VISIT_..)',           0, r'previews/\1/\3'),
    (r'.*/(HST.._....)(|_.*)/(HST.._..../DATA)',                    0, r'previews/\1/\3'),
    (r'.*/(HST.)9_9999.*',                                          0, r'previews/\1x_xxxx'),
])

associations_to_metadata = translator.TranslatorByRegex([
    (r'.*/(HST.._....)(|_.*)/(HST.._....)/DATA/VISIT_../(\w{9}).*', 0, [r'metadata/\1/\3/\3_index.tab/\4',
                                                                        r'metadata/\1/\3/\3_hstfiles.tab/\4']),
    (r'.*/(HST.._....)(|_.*)/(HST.._....)/DATA/VISIT_..',           0,  r'metadata/\1/\3'),
    (r'.*/(HST.._....)(|_.*)/(HST.._....)/DATA',                    0,  r'metadata/\1/\3'),
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
    (r'volumes/.*\.ASC',                 0, ('HST',  10, 'hst_text',        'FITS Header Text',                           True)),
    (r'volumes/.*\.LBL',                 0, ('HST',  10, 'hst_label',       'HST Preview Products',                       True)),
    (r'volumes/.*\.TIF',                 0, ('HST',  20, 'hst_tiff',        'Raw Data Preview (lossless)',                True)),
    (r'volumes/.*_(RAW.*|D0M_...)\.JPG', 0, ('HST',  30, 'hst_raw',         'Raw Data Preview',                           True)),
    (r'volumes/.*_(FLT.*|CAL)\.JPG',     0, ('HST',  40, 'hst_calib',       'Calibrated Data Preview',                    True)),
    (r'volumes/.*_SFL\.JPG',             0, ('HST',  50, 'hst_summed',      'Calibrated Summed Preview',                  True)),
    (r'volumes/.*_CRJ\.JPG',             0, ('HST',  60, 'hst_cosmic_ray',  'Calibrated Cosmic Ray Cleaned Preview',      True)),
    (r'volumes/.*_DRZ\.JPG',             0, ('HST',  70, 'hst_drizzled',    'Calibrated Geometrically Corrected Preview', True)),
    (r'volumes/.*_IMA\.JPG',             0, ('HST',  80, 'hst_ima',         'Pre-mosaic Preview',                         True)),
    (r'volumes/.*_MOS\.JPG',             0, ('HST',  90, 'hst_mosaic',      'Mosaic Preview',                             True)),
    (r'volumes/.*_(X1D|SX1)\.JPG',       0, ('HST', 100, 'hst_1d_spectrum', '1-D Spectrum Preview',                       True)),
    (r'volumes/.*_(X2D|SX2)\.JPG',       0, ('HST', 110, 'hst_2d_spectrum', '2-D Spectrum Preview',                       True)),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

opus_products = translator.TranslatorByRegex([
    (r'.*volumes/(HST.x_xxxx)(|_v.+)/(HST.._....)/(DATA/VISIT_../.{9}).*', 0,
                    [r'volumes/\1*/\3/\4*',
                     r'previews/\1/\3/\4_full.jpg',
                     r'previews/\1/\3/\4_med.jpg',
                     r'previews/\1/\3/\4_small.jpg',
                     r'previews/\1/\3/\4_thumb.jpg',
                     r'metadata/\1/\3/\3_index.lbl',
                     r'metadata/\1/\3/\3_index.tab',
                     r'metadata/\1/\3/\3_hstfiles.lbl',
                     r'metadata/\1/\3/\3_hstfiles.tab',
                    ])
])

####################################################################################################################################
# OPUS_ID
####################################################################################################################################

opus_id = translator.TranslatorByRegex([
    # Associated HST products share an OPUS ID based on the first nine characters of the file's basename.
    (r'.*/HSTI(.)_(....)/DATA/VISIT_../(\w{9})\w*\..*', 0, r'hst-\1\2-wfc3-#LOWER#\3'),
    (r'.*/HSTJ(.)_(....)/DATA/VISIT_../(\w{9})\w*\..*', 0, r'hst-\1\2-acs-#LOWER#\3'),
    (r'.*/HSTN(.)_(....)/DATA/VISIT_../(\w{9})\w*\..*', 0, r'hst-\1\2-nicmos-#LOWER#\3'),
    (r'.*/HSTO(.)_(....)/DATA/VISIT_../(\w{9})\w*\..*', 0, r'hst-\1\2-stis-#LOWER#\3'),
    (r'.*/HSTU(.)_(....)/DATA/VISIT_../(\w{9})\w*\..*', 0, r'hst-\1\2-wfpc2-#LOWER#\3'),
])

####################################################################################################################################
# OPUS_ID_TO_PRIMARY_LOGICAL_PATH
####################################################################################################################################

opus_id_to_primary_logical_path = translator.TranslatorByRegex([
    # The logical path returned points to the combined-detached label.
    (r'hst-(.)(....)-wfc3-(....)(..)(.*)',   0, r'volumes/HSTIx_xxxx/HSTI\1_\2/DATA/VISIT_#UPPER#\4/\3\4\5.LBL'),
    (r'hst-(.)(....)-acs-(....)(..)(.*)',    0, r'volumes/HSTJx_xxxx/HSTJ\1_\2/DATA/VISIT_#UPPER#\4/\3\4\5.LBL'),
    (r'hst-(.)(....)-nicmos-(....)(..)(.*)', 0, r'volumes/HSTNx_xxxx/HSTN\1_\2/DATA/VISIT_#UPPER#\4/\3\4\5.LBL'),
    (r'hst-(.)(....)-stis-(....)(..)(.*)',   0, r'volumes/HSTOx_xxxx/HSTO\1_\2/DATA/VISIT_#UPPER#\4/\3\4\5.LBL'),
    (r'hst-(.)(....)-wfpc2-(....)(..)(.*)',  0, r'volumes/HSTUx_xxxx/HSTU\1_\2/DATA/VISIT_#UPPER#\4/\3\4\5.LBL'),
])

####################################################################################################################################
# FILESPEC_TO_VOLSET
####################################################################################################################################

filespec_to_volset = translator.TranslatorByRegex([
    (r'HST([A-Z])[01]_\d{4}.*', 0, r'HST\1x_xxxx'),
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
    OPUS_ID = opus_id
    OPUS_ID_TO_PRIMARY_LOGICAL_PATH = opus_id_to_primary_logical_path

    VIEWABLES = {'default': default_viewables}

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']  = associations_to_volumes
    ASSOCIATIONS['previews'] = associations_to_previews
    ASSOCIATIONS['metadata'] = associations_to_metadata

    FILENAME_KEYLEN = 9     # trim off suffixes

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS = translator.TranslatorByRegex([(r'hst-.*', 0, HSTxx_xxxx)]) + \
                                      pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS

pdsfile.PdsFile.FILESPEC_TO_VOLSET = filespec_to_volset + pdsfile.PdsFile.FILESPEC_TO_VOLSET

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['HSTxx_xxxx'] = HSTxx_xxxx

####################################################################################################################################
