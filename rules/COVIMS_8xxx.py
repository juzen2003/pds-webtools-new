####################################################################################################################################
# rules/COVIMS_8xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*_TAU_01KM\.TAB', 0, ('Occultation Profile (1 km)',  'SERIES')),
    (r'volumes/.*_TAU_10KM\.TAB', 0, ('Occultation Profile (10 km)', 'SERIES')),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl', re.I, ''),
    (r'volumes/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_8...)/(data|EASYDATA)/(\w+)_TAU_\d+KM\.TAB', 0,
                    (r'previews/COVIMS_8xxx/\2/data/\4_TAU_full.jpg',
                     r'previews/COVIMS_8xxx/\2/data/\4_TAU_med.jpg',
                     r'previews/COVIMS_8xxx/\2/data/\4_TAU_small.jpg',
                     r'previews/COVIMS_8xxx/\2/data/\4_TAU_thumb.jpg',
                    )),
    (r'volumes/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_8.../browse/.\w_+)\.PDF', 0,
                    (r'previews/COVIMS_8xxx/\2_full.jpg',
                     r'previews/COVIMS_8xxx/\2_med.jpg',
                     r'previews/COVIMS_8xxx/\2_small.jpg',
                     r'previews/COVIMS_8xxx/\2_thumb.jpg',
                    )),
])

diagrams_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl', re.I, ''),
    (r'volumes/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_8...)/(data|EASYDATA)/(\w+)_TAU_\d+KM\.TAB', 0,
                    (r'diagrams/COVIMS_8xxx/\2/data/\4_full.jpg',
                     r'diagrams/COVIMS_8xxx/\2/data/\4_med.jpg',
                     r'diagrams/COVIMS_8xxx/\2/data/\4_small.jpg',
                     r'previews/COVIMS_8xxx/\2/data/\4_thumb.jpg',
                    )),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'.*/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_8...)/(data|browse)', 0,
                    [r'volumes/COVIMS_8xxx\1/\2/data',
                     r'volumes/COVIMS_8xxx\1/\2/browse',
                    ]),
    (r'.*/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_8...)/(data|browse|EASYDATA)/(VIMS_.*)_(TAU.*|[a-z]\.jpg)', 0,
                    [r'volumes/COVIMS_8xxx\1/\2/data/\4_TAU_01KM.LBL',
                     r'volumes/COVIMS_8xxx\1/\2/data/\4_TAU_01KM.TAB',
                     r'volumes/COVIMS_8xxx\1/\2/data/\4_TAU_10KM.LBL',
                     r'volumes/COVIMS_8xxx\1/\2/data/\4_TAU_10KM.TAB',
                     r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_GEOMETRY_full.jpg',
                     r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_GEOMETRY_med.jpg',
                     r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_GEOMETRY_small.jpg',
                     r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_GEOMETRY_thumb.jpg',
                     r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_LIGHTCURVE_full.jpg',
                     r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_LIGHTCURVE_med.jpg',
                     r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_LIGHTCURVE_small.jpg',
                     r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_LIGHTCURVE_thumb.jpg',
                     r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_NPOLE_full.jpg',
                     r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_NPOLE_med.jpg',
                     r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_NPOLE_small.jpg',
                     r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_NPOLE_thumb.jpg',
                     r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_STAR_full.jpg',
                     r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_STAR_med.jpg',
                     r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_STAR_small.jpg',
                     r'volumes/COVIMS_8xxx\1/\2/browse/\4_TAU_STAR_thumb.jpg',
                    ]),
    (r'volumes/COVIMS_8xxx_v1/COVIMS_8001/EASYDATA', 0,
                    [r'volumes/COVIMS_8xxx/COVIMS_8001/data',
                     r'volumes/COVIMS_8xxx/COVIMS_8001/browse',
                    ]),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'.*/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_8...)/(data|browse|EASYDATA)', 0,
                    [r'previews/COVIMS_8xxx/\2/data',
                     r'previews/COVIMS_8xxx/\2/browse',
                    ]),
    (r'.*/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_8...)/(data|browse|EASYDATA)/(VIMS_.*)_(TAU.*|[a-z]\.jpg)', 0,
                    [r'previews/COVIMS_8xxx/\2/data/\4_TAU_full.jpg',
                     r'previews/COVIMS_8xxx/\2/data/\4_TAU_med.jpg',
                     r'previews/COVIMS_8xxx/\2/data/\4_TAU_small.jpg',
                     r'previews/COVIMS_8xxx/\2/data/\4_TAU_thumb.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_GEOMETRY_full.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_GEOMETRY_med.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_GEOMETRY_small.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_GEOMETRY_thumb.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_LIGHTCURVE_full.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_LIGHTCURVE_med.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_LIGHTCURVE_small.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_LIGHTCURVE_thumb.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_NPOLE_full.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_NPOLE_med.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_NPOLE_small.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_NPOLE_thumb.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_STAR_full.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_STAR_med.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_STAR_small.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_STAR_thumb.jpg',
                   ]),
])

associations_to_diagrams = translator.TranslatorByRegex([
    (r'.*/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_8...)/(data|browse|EASYDATA)', 0,
                    r'diagrams/COVIMS_8xxx/\2/data'),
    (r'.*/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_8...)/(data|EASYDATA)/(VIMS_.*)_(TAU.*|[a-z]\.jpg)', 0,
                    [r'diagrams/COVIMS_8xxx/\2/data/\3_full.jpg',
                     r'diagrams/COVIMS_8xxx/\2/data/\3_med.jpg',
                     r'diagrams/COVIMS_8xxx/\2/data/\3_small.jpg',
                     r'diagrams/COVIMS_8xxx/\2/data/\3_thumb.jpg',
                    ]),
])

associations_to_metadata = translator.TranslatorByRegex([
    (r'volumes/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_8...)/data/(VIMS_.*)_(TAU_\d+KM)\..*', 0,
                    [r'metadata/COVIMS_8xxx/\2/\2_index.tab/\3_\4',
                     r'metadata/COVIMS_8xxx/\2/\2_profile_index.tab/\3_TAU01',
                     r'metadata/COVIMS_8xxx/\2/\2_supplemental_index.tab/\3_TAU01',
                    ]),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews|diagrams)/COVIMS_8xxx.*/COVIMS_8.../(data|browse|EASYDATA)', 0, (True, False, False)),
])

####################################################################################################################################
# SPLIT_RULES
####################################################################################################################################

split_rules = translator.TranslatorByRegex([
    (r'(VIMS_...._..._\w+_[IE])_(TAU_\d\w+)\.(.*)', 0, (r'\1', r'_\2', r'.\3')),
])

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/.*_TAU_01KM\.(TAB|LBL)', 0, ('Cassini VIMS', 10, 'covims_occ_01', 'Occultation Profile (1 km)',  True)),
    (r'volumes/.*_TAU_10KM\.(TAB|LBL)', 0, ('Cassini VIMS', 20, 'covims_occ_10', 'Occultation Profile (10 km)', True)),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

# Use of explicit file names means we don't need to invoke glob.glob(); this goes much faster
opus_products = translator.TranslatorByRegex([
    (r'.*/COVIMS_8xxx(|_v[0-9\.]+)/(COVIMS_....)/(data|EASYDATA)/(VIMS_.*)_(TAU.*|[a-z]+)\..*', 0,
                    [r'volumes/COVIMS_8xxx*/\2/data/\4_TAU_01KM.LBL',
                     r'volumes/COVIMS_8xxx*/\2/data/\4_TAU_01KM.TAB',
                     r'volumes/COVIMS_8xxx*/\2/data/\4_TAU_10KM.LBL',
                     r'volumes/COVIMS_8xxx*/\2/data/\4_TAU_10KM.TAB',
                     r'volumes/COVIMS_8xxx*/\2/EASYDATA/\4_TAU_01KM.LBL',
                     r'volumes/COVIMS_8xxx*/\2/EASYDATA/\4_TAU_01KM.TAB',
                     r'volumes/COVIMS_8xxx*/\2/EASYDATA/\4_TAU_10KM.LBL',
                     r'volumes/COVIMS_8xxx*/\2/EASYDATA/\4_TAU_10KM.TAB',
                     r'previews/COVIMS_8xxx/\2/data/\4_TAU_full.jpg',
                     r'previews/COVIMS_8xxx/\2/data/\4_TAU_med.jpg',
                     r'previews/COVIMS_8xxx/\2/data/\4_TAU_small.jpg',
                     r'previews/COVIMS_8xxx/\2/data/\4_TAU_thumb.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_GEOMETRY_full.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_GEOMETRY_med.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_GEOMETRY_small.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_GEOMETRY_thumb.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_LIGHTCURVE_full.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_LIGHTCURVE_med.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_LIGHTCURVE_small.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_LIGHTCURVE_thumb.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_NPOLE_full.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_NPOLE_med.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_NPOLE_small.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_NPOLE_thumb.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_STAR_full.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_STAR_med.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_STAR_small.jpg',
                     r'previews/COVIMS_8xxx/\2/browse/\4_TAU_STAR_thumb.jpg',
                     r'diagrams/COVIMS_8xxx/\2/data/\4_full.jpg',
                     r'diagrams/COVIMS_8xxx/\2/data/\4_med.jpg',
                     r'diagrams/COVIMS_8xxx/\2/data/\4_small.jpg',
                     r'diagrams/COVIMS_8xxx/\2/data/\4_thumb.jpg',
                     r'metadata/COVIMS_8xxx/\2/\2_index.lbl',
                     r'metadata/COVIMS_8xxx/\2/\2_index.tab',
                     r'metadata/COVIMS_8xxx/\2/\2_profile_index.lbl',
                     r'metadata/COVIMS_8xxx/\2/\2_profile_index.tab',
                     r'metadata/COVIMS_8xxx/\2/\2_supplemental_index.lbl',
                     r'metadata/COVIMS_8xxx/\2/\2_supplemental_index.tab',
                    ]),
])

####################################################################################################################################
# OPUS_ID
####################################################################################################################################

opus_id = translator.TranslatorByRegex([
    (r'.*/COVIMS_8xxx.*/(data|EASYDATA)/VIMS_(\d{4})_(\d{3})_(\w+)_([IE]).*', 0, r'co-vims-occ-#LOWER#\2-\3-\4-\5'),
])

####################################################################################################################################
# OPUS_ID_TO_PRIMARY_LOGICAL_PATH
####################################################################################################################################

opus_id_to_primary_logical_path = translator.TranslatorByRegex([
    (r'co-vims-occ-(.*)', 0,  r'volumes/COVIMS_0xxx/COVIMS_8001/data/#UPPER#VIMS_\1_TAU01KM.TAB'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class COVIMS_8xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('COVIMS_8xxx', re.I, 'COVIMS_8xxx')]) + \
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
pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS = translator.TranslatorByRegex([(r'co-vims-occ-.*', 0, COVIMS_8xxx)]) + \
                                      pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COVIMS_8xxx'] = COVIMS_8xxx

####################################################################################################################################
