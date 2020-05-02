####################################################################################################################################
# rules/COUVIS_0xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*/DATA',          re.I, ('Data files grouped by date', 'CUBEDIR')),
    (r'volumes/.*/DATA/\w+',      re.I, ('Data files grouped by date', 'CUBEDIR')),
    (r'volumes/.*/HSP\w+\.DAT',   re.I, ('Time series data',           'DATA')),
    (r'volumes/.*/HDAC\w+\.DAT',  re.I, ('Binary data cube',           'DATA')),
    (r'volumes/.*/\w+\.DAT',      re.I, ('Spectral data cube',         'CUBE')),
    (r'volumes/.*\.txt_[0-9].*',  re.I, ('Text file',                  'INFO')),
    (r'volumes/.*OLD.DIR',        re.I, ('Directory',                  'FOLDER')),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'.*/((COUVIS_0xxx/COUVIS_0...)/DATA/(\w+)/([\w0-9\_]+))\..*', 0, [r'volumes/\1.DAT',
                                                                        r'volumes/\1.LBL',
                                                                        r'volumes/\2/CALIB/VERSION_*/\3/\4_CAL_*.DAT',
                                                                        r'volumes/\2/CALIB/VERSION_*/\3/\4_CAL_*.LBL']),
    (r'.*/((COUVIS_0xxx/COUVIS_0...)/CALIB/VERSION_\d+/(\w+)/([\w0-9\_]+)_CAL_\d+)\..*',
                                                                    0, [r'volumes/\2/DATA/\3/\4.DAT',
                                                                        r'volumes/\2/DATA/\3/\4.LBL',
                                                                        r'volumes/\2/CALIB/VERSION_*/\3/\4_CAL_*.DAT',
                                                                        r'volumes/\2/CALIB/VERSION_*/\3/\4_CAL_*.LBL']),
    (r'.*/(COUVIS_0xxx/COUVIS_0...)/DATA(|/\w+)/?',                 0,  [r'volumes/\1/DATA\2',
                                                                         r'volumes/\1/CALIB/VERSION_*\2']),
    (r'.*/(COUVIS_0xxx/COUVIS_0...)/CALIB/VERSION_\d+(|/\w+)/?',    0,  [r'volumes/\1/DATA\2',
                                                                         r'volumes/\1/CALIB/VERSION_*\2']),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'.*/(COUVIS_0xxx/COUVIS_0.../DATA/\w+/\w+[0-9])(|_\w+)\..*',  0, [r'previews/\1_full.png',
                                                                        r'previews/\1_thumb.png',
                                                                        r'previews/\1_small.png',
                                                                        r'previews/\1_med.png']),
    (r'.*/(COUVIS_0xxx/COUVIS_0.../DATA)(|/\w+)$',                  0,  r'previews/\1/\2'),
])

associations_to_metadata = translator.TranslatorByRegex([
    (r'.*/(COUVIS_0xxx)/(COUVIS_0...)/DATA/\w+/(\w+[0-9])(|_\w+)\..*',
                                                                    0, [r'metadata/\1/\2/\2_index.tab/\3',
                                                                        r'metadata/\1/\2/\2_supplemental_index.tab/\3',
                                                                        r'metadata/\1/\2/\2_ring_summary.tab/\3',
                                                                        r'metadata/\1/\2/\2_moon_summary.tab/\3',
                                                                        r'metadata/\1/\2/\2_saturn_summary.tab/\3',
                                                                        r'metadata/\1/\2']),
    (r'.*/(COUVIS_0xxx)/(COUVIS_0...)/DATA(|/\w+)$',                0,  r'metadata/\1/\2'),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews)/COUVIS_0xxx/COUVIS_..../DATA(|/\w+)', 0, (True, True, True)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'volumes/(\w+)/COUVIS_[0-9]{4}/DATA/(\w+)', 0, r'volumes/\1/*/DATA/*'),
    (r'volumes/(\w+)/COUVIS_[0-9]{4}/DATA',       0, r'volumes/\1/*/DATA'),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl',  re.I, ''),

    (r'volumes/(.*/DATA/\w+/.*)\.(\w+)', 0, (r'previews/\1_full.png',
                                             r'previews/\1_thumb.png',
                                             r'previews/\1_small.png',
                                             r'previews/\1_med.png')),
])

####################################################################################################################################
# SORT_KEY
####################################################################################################################################

sort_key = translator.TranslatorByRegex([
    (r'(EUV|FUV|HSP|HDAC)([0-9]{4}_[0-9]{3}_[0-9]{2}_[0-9]{2}.*)_full(\..*)',   0, r'\2\1_1full\3'),
    (r'(EUV|FUV|HSP|HDAC)([0-9]{4}_[0-9]{3}_[0-9]{2}_[0-9]{2}.*)_med(\..*)',    0, r'\2\1_2med\3'),
    (r'(EUV|FUV|HSP|HDAC)([0-9]{4}_[0-9]{3}_[0-9]{2}_[0-9]{2}.*)_small(\..*)',  0, r'\2\1_3small\3'),
    (r'(EUV|FUV|HSP|HDAC)([0-9]{4}_[0-9]{3}_[0-9]{2}_[0-9]{2}.*)_thumb(\..*)',  0, r'\2\1_4thumb\3'),
    (r'(EUV|FUV|HSP|HDAC)([0-9]{4}_[0-9]{3}_[0-9]{2}_[0-9]{2}.*)',              0, r'\2\1'),
])

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/.*/DATA/.*\.DAT',  0, ('Cassini UVIS', 10, 'couvis_raw', 'Raw Data')),
    (r'volumes/.*/CALIB/.*\.DAT', 0, ('Cassini UVIS', 20, 'couvis_calib_corr', 'Calibration Data')),
])

####################################################################################################################################
# OPUS_FORMAT
####################################################################################################################################

opus_format = translator.TranslatorByRegex([
    (r'.*\.DAT$', 0, ('Binary', 'Unformatted')),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

# Use of explicit file names means we don't need to invoke glob.glob(); this goes much faster
opus_products = translator.TranslatorByRegex([
    (r'.*volumes/(COUVIS_0xxx)/(COUVIS_0...)/(DATA)/(.*)\.(DAT|LBL)',
                                                                0, [r'volumes/\1/\2/\3/\4.DAT',
                                                                    r'volumes/\1/\2/\3/\4.LBL',
                                                                    r'volumes/\1/\2/CALIB/VERSION_*/\4_CAL_*.DAT',
                                                                    r'volumes/\1/\2/CALIB/VERSION_*/\4_CAL_*.LBL',
                                                                    r'previews/\1/\2/\3/\4_thumb.png',
                                                                    r'previews/\1/\2/\3/\4_small.png',
                                                                    r'previews/\1/\2/\3/\4_med.png',
                                                                    r'previews/\1/\2/\3/\4_full.png',
                                                                    r'metadata/\1/\2/\2_jupiter_summary.lbl',
                                                                    r'metadata/\1/\2/\2_jupiter_summary.tab',
                                                                    r'metadata/\1/\2/\2_saturn_summary.lbl',
                                                                    r'metadata/\1/\2/\2_saturn_summary.tab',
                                                                    r'metadata/\1/\2/\2_moon_summary.lbl',
                                                                    r'metadata/\1/\2/\2_moon_summary.tab',
                                                                    r'metadata/\1/\2/\2_ring_summary.lbl',
                                                                    r'metadata/\1/\2/\2_ring_summary.tab',
                                                                    r'metadata/\1/\2/\2_inventory.lbl',
                                                                    r'metadata/\1/\2/\2_inventory.tab']),
])

####################################################################################################################################
# FILESPEC_TO_OPUS_ID
####################################################################################################################################

# filespec_to_opus_id = translator.TranslatorByRegex([
#     (r'COUVIS_0001/DATA/w+/(\w+)\.(DAT|LBL)$',                0, r'cassini.uvis.jupiter_cruise..\1'),
#     (r'COUVIS_0002/DATA/D2001_00[0-9]/(\w+)\.(DAT|LBL)$',     0, r'cassini.uvis.jupiter_cruise..\1'),
#     (r'COUVIS_0002/DATA/D2001_01[0-3]/(\w+)\.(DAT|LBL)$',     0, r'cassini.uvis.jupiter_cruise..\1'),
#     (r'COUVIS_0002/DATA/D2001_01[4-9]/(\w+)\.(DAT|LBL)$',     0, r'cassini.uvis.jupiter..\1'),
#     (r'COUVIS_0002/DATA/D2001_0[2-9][0-9]/(\w+)\.(DAT|LBL)$', 0, r'cassini.uvis.jupiter..\1'),
#     (r'COUVIS_000[3-5]/DATA/\w+/(\w+)\.(DAT|LBL)$',           0, r'cassini.uvis.saturn_cruise..\1'),
#     (r'COUVIS_000[6-9]/DATA/\w+/(\w+)\.(DAT|LBL)$',           0, r'cassini.uvis.saturn..\1'),
#     (r'COUVIS_00[1-9]./DATA/\w+/(\w+)\.(DAT|LBL)$',           0, r'cassini.uvis.saturn../\1'),
# ])

filespec_to_opus_id = translator.TranslatorByRegex([
    (r'COUVIS_00../DATA/\w+/(\w+)\.(DAT|LBL)$',  0, r'co-uvis-\1'),
])

####################################################################################################################################
# OPUS_ID_TO_FILESPEC
####################################################################################################################################

opus_id_to_filespec = translator.TranslatorByRegex([
    (r'co-uvis-\.*', 0, re.compile(r'.*\.DAT$')),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class COUVIS_0xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('COUVIS_0xxx', re.I, 'COUVIS_0xxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS
    SORT_KEY = sort_key + pdsfile.PdsFile.SORT_KEY

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_FORMAT = opus_format + pdsfile.PdsFile.OPUS_FORMAT
    OPUS_PRODUCTS = opus_products
    FILESPEC_TO_OPUS_ID = filespec_to_opus_id

    VIEWABLES = {'default': default_viewables}

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']  = associations_to_volumes
    ASSOCIATIONS['previews'] = associations_to_previews
    ASSOCIATIONS['metadata'] = associations_to_metadata

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_FILESPEC = opus_id_to_filespec + pdsfile.PdsFile.OPUS_ID_TO_FILESPEC

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COUVIS_0xxx'] = COUVIS_0xxx

####################################################################################################################################
