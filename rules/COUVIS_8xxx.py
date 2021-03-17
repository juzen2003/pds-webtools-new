####################################################################################################################################
# rules/COUVIS_8xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*_TAU01KM\.TAB', 0, ('Occultation Profile (1 km)',  'SERIES')),
    (r'volumes/.*_TAU10KM\.TAB', 0, ('Occultation Profile (10 km)', 'SERIES')),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'volumes/COUVIS_8xxx(|_v[0-9\.]+)/(COUVIS_8...)/(data|DATA/EASYDATA)/(UVIS_HSP.*)_TAU_?\d+KM\.TAB', 0,
                    (r'previews/COUVIS_8xxx/\2/data/\4_full.jpg',
                     r'previews/COUVIS_8xxx/\2/data/\4_med.jpg',
                     r'previews/COUVIS_8xxx/\2/data/\4_small.jpg',
                     r'previews/COUVIS_8xxx/\2/data/\4_thumb.jpg',
                    )),
])

diagrams_viewables = translator.TranslatorByRegex([
    (r'volumes/COUVIS_8xxx(|_v[0-9\.]+)/(COUVIS_8...)/(data|DATA/EASYDATA)/(UVIS_HSP.*)_TAU_?\d+KM\.TAB', 0,
                    (r'diagrams/COUVIS_8xxx/\2/data/\4_full.jpg',
                     r'diagrams/COUVIS_8xxx/\2/data/\4_med.jpg',
                     r'diagrams/COUVIS_8xxx/\2/data/\4_small.jpg',
                     r'diagrams/COUVIS_8xxx/\2/data/\4_thumb.jpg',
                    )),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'.*/COUVIS_8xxx(|_v[0-9\.]+)/(COUVIS_8...)/(data|DATA/EASYDATA)/(UVIS_HSP.*)_(TAU\w+KM|[a-z]+)\..*', 0,
                    [r'volumes/COUVIS_8xxx\1/\2/\3/\4_TAU_01KM.LBL',
                     r'volumes/COUVIS_8xxx\1/\2/\3/\4_TAU_01KM.TAB',
                     r'volumes/COUVIS_8xxx\1/\2/\3/\4_TAU_10KM.LBL',
                     r'volumes/COUVIS_8xxx\1/\2/\3/\4_TAU_10KM.TAB',
                    ]),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'.*/COUVIS_8xxx(|_v[0-9\.]+)/(COUVIS_8...)/(data|DATA/EASYDATA)/(UVIS_HSP.*)_(TAU\w+KM|[a-z]+)\..*', 0,
                    [r'previews/COUVIS_8xxx/\2/data/\3_full.jpg',
                     r'previews/COUVIS_8xxx/\2/data/\3_med.jpg',
                     r'previews/COUVIS_8xxx/\2/data/\3_small.jpg',
                     r'previews/COUVIS_8xxx/\2/data/\3_thumb.jpg',
                    ]),
])

associations_to_diagrams = translator.TranslatorByRegex([
    (r'.*/COUVIS_8xxx(|_v[0-9\.]+)/(COUVIS_8...)/(data|DATA/EASYDATA)/(UVIS_HSP.*)_(TAU\w+KM|[a-z]+)\..*', 0,
                    [r'diagrams/COUVIS_8xxx/\2/data/\3_full.jpg',
                     r'diagrams/COUVIS_8xxx/\2/data/\3_med.jpg',
                     r'diagrams/COUVIS_8xxx/\2/data/\3_small.jpg',
                     r'diagrams/COUVIS_8xxx/\2/data/\3_thumb.jpg',
                    ]),
])

associations_to_metadata = translator.TranslatorByRegex([
    (r'volumes/COUVIS_8xxx(|_v[0-9\.]+)/(COUVIS_8...)/(data|DATA/EASYDATA)/(UVIS_HSP.*)_(TAU\w+KM)\..*', 0,
                    [r'metadata/COUVIS_8xxx/\2/\2_index.tab/\4_\5',
                     r'metadata/COUVIS_8xxx/\2/\2_profile_index.tab/\4_TAU01',
                     r'metadata/COUVIS_8xxx/\2/\2_supplemental_index.tab/\4_TAU01',
                    ]),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews|diagrams)/COUVIS_8xxx.*/COUVIS_8.../data', 0, (True, True, False)),
    (r'volumes/COUVIS_8xxx_v1/COUVIS_8001/DATA/EASYDATA',           0, (True, True, False)),
])

####################################################################################################################################
# SPLIT_RULES
####################################################################################################################################

split_rules = translator.TranslatorByRegex([
    (r'(UVIS_HSP_...._..._\w+_[IE])_(\w+)\.(.*)$', 0, (r'\1', r'_\2', r'.\3')),
])

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/.*_TAU01KM\.(TAB|LBL)', 0, ('Cassini UVIS', 10, 'couvis_occ_01', 'Occultation Profile (1 km)',  True)),
    (r'volumes/.*_TAU10KM\.(TAB|LBL)', 0, ('Cassini UVIS', 20, 'couvis_occ_10', 'Occultation Profile (10 km)', True)),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

# Use of explicit file names means we don't need to invoke glob.glob(); this goes much faster
opus_products = translator.TranslatorByRegex([
    (r'.*/COUVIS_8xxx(|_v[0-9\.]+)/(COUVIS_....)/(data|DATA/EASYDATA)/(UVIS_HSP.*)_(TAU.*|[a-z]+)\..*', 0,
                    [r'volumes/COUVIS_8xxx*/\2/\3/\4_TAU_01KM.LBL',
                     r'volumes/COUVIS_8xxx*/\2/\3/\4_TAU_01KM.TAB',
                     r'volumes/COUVIS_8xxx*/\2/\3/\4_TAU_10KM.LBL',
                     r'volumes/COUVIS_8xxx*/\2/\3/\4_TAU_10KM.TAB',
                     r'previews/COUVIS_8xxx/\2/data/\4_full.jpg',
                     r'previews/COUVIS_8xxx/\2/data/\4_med.jpg',
                     r'previews/COUVIS_8xxx/\2/data/\4_small.jpg',
                     r'previews/COUVIS_8xxx/\2/data/\4_thumb.jpg',
                     r'diagrams/COUVIS_8xxx/\2/data/\4_full.jpg',
                     r'diagrams/COUVIS_8xxx/\2/data/\4_med.jpg',
                     r'diagrams/COUVIS_8xxx/\2/data/\4_small.jpg',
                     r'diagrams/COUVIS_8xxx/\2/data/\4_thumb.jpg',
                     r'metadata/COUVIS_8xxx/\2/\2_index.lbl',
                     r'metadata/COUVIS_8xxx/\2/\2_index.tab',
                     r'metadata/COUVIS_8xxx/\2/\2_profile_index.lbl',
                     r'metadata/COUVIS_8xxx/\2/\2_profile_index.tab',
                     r'metadata/COUVIS_8xxx/\2/\2_supplemental_index.lbl',
                     r'metadata/COUVIS_8xxx/\2/\2_supplemental_index.tab',
                    ]),
])

####################################################################################################################################
# OPUS_ID
####################################################################################################################################

opus_id = translator.TranslatorByRegex([
    (r'.*/COUVIS_8xxx.*/(data|DATA/EASYDATA)/UVIS_HSP_(\d{4})_(\d{3})_(\w+)_([IE]).*', 0, r'co-uvis-occ-#LOWER#\2-\3-\4-\5'),
])

####################################################################################################################################
# OPUS_ID_TO_PRIMARY_LOGICAL_PATH
####################################################################################################################################

opus_id_to_primary_logical_path = translator.TranslatorByRegex([
    (r'co-uvis-occ-(.*)', 0,  r'volumes/COUVIS_8xxx/COUVIS_8001/data/#UPPER#UVIS_HSP_\1_TAU01KM.TAB'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class COUVIS_8xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('COUVIS_8xxx', re.I, 'COUVIS_8xxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    SPLIT_RULES = split_rules + pdsfile.PdsFile.SPLIT_RULES

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_PRODUCTS = opus_products
    OPUS_ID = opus_id
    OPUS_ID_TO_PRIMARY_LOGICAL_PATH = opus_id_to_primary_logical_path

    VIEWABLES = {
        'default': default_viewables,
        'diagram': diagrams_viewables,
    }

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']  = associations_to_volumes
    ASSOCIATIONS['previews'] = associations_to_previews
    ASSOCIATIONS['diagrams'] = associations_to_diagrams
    ASSOCIATIONS['metadata'] = associations_to_metadata

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS = translator.TranslatorByRegex([(r'co-uvis-occ.*', 0, COUVIS_8xxx)]) + \
                                      pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COUVIS_8xxx'] = COUVIS_8xxx

####################################################################################################################################
