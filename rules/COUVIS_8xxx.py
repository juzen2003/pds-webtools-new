####################################################################################################################################
# rules/COUVIS_8xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/.*_TAU01KM\.(TAB|LBL)$', 0, ('Cassini UVIS', 10, 'couvis_occ_01', 'Occultation Profile (1km)',  True)),
    (r'volumes/.*_TAU10KM\.(TAB|LBL)$', 0, ('Cassini UVIS', 20, 'couvis_occ_10', 'Occultation Profile (10km)', True)),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

# Use of explicit file names means we don't need to invoke glob.glob(); this goes much faster
opus_products = translator.TranslatorByRegex([
    (r'.*volumes/COUVIS_8xxx/(COUVIS_....)/data/(.*)_TAU01KM\.(TAB|LBL)', 0,
                            [r'volumes/COUVIS_8xxx/\1/data/\2_TAU01KM.TAB',
                             r'volumes/COUVIS_8xxx/\1/data/\2_TAU01KM.LBL',
                             r'volumes/COUVIS_8xxx/\1/data/\2_TAU10KM.LBL',
                             r'volumes/COUVIS_8xxx/\1/data/\2_TAU10KM.TAB']),

    (r'.*volumes/(COUVIS_8xxx)/(COUVIS_8...)/data/(.*)_TAU01KM\.(TAB|LBL)', 0,
                            [r'metadata/\1/\2/\2_index.lbl',
                             r'metadata/\1/\2/\2_index.tab',
                             r'metadata/\1/\2/\2_profile_index.lbl',
                             r'metadata/\1/\2/\2_profile_index.tab',
                             r'metadata/\1/\2/\2_supplemental_index.lbl',
                             r'metadata/\1/\2/\2_supplemental_index.tab',
                             r'previews/\1/\2/data/\3_full.png',
                             r'previews/\1/\2/data/\3_thumb.png',
                             r'previews/\1/\2/data/\3_small.png',
                             r'previews/\1/\2/data/\3_med.png',
                             r'diagrams/\1/\2/data/\3_full.png',
                             r'diagrams/\1/\2/data/\3_thumb.png',
                             r'diagrams/\1/\2/data/\3_small.png',
                             r'diagrams/\1/\2/data/\3_med.png']),
])

####################################################################################################################################
# FILESPEC_TO_OPUS_ID
####################################################################################################################################

filespec_to_opus_id = translator.TranslatorByRegex([
    (r'COUVIS_8001/data/UVIS_HSP_(\d{4})_(\d{3})_(\w+)_(I|E)_TAU01KM\..+$', 0, r'co-uvis-occ-\1-\2-\3-\4'),
])

####################################################################################################################################
# FILESPEC_TO_LOGICAL_PATH
####################################################################################################################################

filespec_to_logical_path = translator.TranslatorByRegex([
    (r'COUVIS(_8.../.*_(thumb|small|med|full)\.(jpg|png))', 0, r'previews/COUVIS_8xxx/COUVIS\1'),
    (r'COUVIS(_8.../.*)$',                                  0, r'volumes/COUVIS_8xxx/COUVIS\1'),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl',  re.I, ''),

    (r'.*volumes/(COUVIS_8xxx)/(COUVIS_8...)/data/(.*)_TAU\d+KM\.\w+', 0,
                                                (r'previews/\1/\2/data/\3_full.png',
                                                 r'previews/\1/\2/data/\3_thumb.png',
                                                 r'previews/\1/\2/data/\3_small.png',
                                                 r'previews/\1/\2/data/\3_med.png')),
])

diagrams_viewables = translator.TranslatorByRegex([
    (r'.*volumes/(COUVIS_8xxx)/(COUVIS_8...)/data/(.*)_TAU\d+KM\.\w+', 0,
                                                (r'diagrams/\1/\2/data/\3_full.png',
                                                 r'diagrams/\1/\2/data/\3_thumb.png',
                                                 r'diagrams/\1/\2/data/\3_small.png',
                                                 r'diagrams/\1/\2/data/\3_med.png')),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################
associations_to_volumes = translator.TranslatorByRegex([
    (r'.*/(COUVIS_8xxx)/(COUVIS_8...)/data/(.*)_\w+\.\w+', 0, [r'volumes/\1/\2/data/\3_TAU*KM.TAB',
                                                               r'volumes/\1/\2/data/\3_TAU*KM.LBL']),

    (r'.*/(COUVIS_8xxx)/(COUVIS_8...)/data(|/\w+)/?',      0,  r'volumes/\1/\2/data'),
    (r'.*/(COUVIS_8xxx)/(COUVIS_8...)/\w+.\w+',            0,  r'volumes/\1/\2/data'),
    (r'.*/(COUVIS_8xxx)/(COUVIS_8...)',                    0,  r'volumes/\1/\2'),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'.*/(COUVIS_8xxx)/(COUVIS_8...)/data/(.*)_\w+\.\w+', 0, [r'previews/\1/\2/data/\3_full.png',
                                                               r'previews/\1/\2/data/\3_thumb.png',
                                                               r'previews/\1/\2/data/\3_small.png',
                                                               r'previews/\1/\2/data/\3_med.png']),
    (r'.*/(COUVIS_8xxx)/(COUVIS_8...)/data(|/\w+)$',       0,  r'previews/\1/\2/data'),
    (r'.*/(COUVIS_8xxx)/(COUVIS_8...)',                    0,  r'previews/\1/\2'),
])

associations_to_diagrams = translator.TranslatorByRegex([
    (r'.*/(COUVIS_8xxx)/(COUVIS_8...)/data/(.*)_\w+\.\w+', 0, [r'diagrams/\1/\2/data/\3_full.png',
                                                               r'diagrams/\1/\2/data/\3_thumb.png',
                                                               r'diagrams/\1/\2/data/\3_small.png',
                                                               r'diagrams/\1/\2/data/\3_med.png']),
    (r'.*/(COUVIS_8xxx)/(COUVIS_8...)/data(|/\w+)$',       0,  r'diagrams/\1/\2/data'),
    (r'.*/(COUVIS_8xxx)/(COUVIS_8...)',                    0,  r'diagrams/\1/\2'),
])

associations_to_metadata = translator.TranslatorByRegex([
    (r'.*volumes/(COUVIS_8xxx)/(COUVIS_8...)/data/(.*_TAU\d+KM)\.\w+',
                                                                    0, [r'metadata/\1/\2/\2_index.tab/\3',
                                                                        r'metadata/\1/\2']),
    (r'.*volumes/(COUVIS_8xxx)/(COUVIS_8...)/data/(.*_TAU01KM)\.\w+',
                                                                    0, [r'metadata/\1/\2/\2_profile_index.tab/\3',
                                                                        r'metadata/\1/\2/\2_supplemental_index.tab/\3',
                                                                        r'metadata/\1/\2']),
    (r'.*/(COUVIS_8xxx)/(COUVIS_8...)/data/(.*)_(full|med|small|thumb)\.\w+',
                                                                    0, [r'metadata/\1/\2/\2_profile_index.tab/\3_TAU01KM',
                                                                        r'metadata/\1/\2/\2_supplemental_index.tab/\3_TAU01KM',
                                                                        r'metadata/\1/\2/\2_index.tab/\3_TAU*KM',
                                                                        r'metadata/\1/\2']),
    (r'.*/(COUVIS_8xxx)/(COUVIS_8...)/data(|/\w+)$',                0,  r'metadata/\1/\2'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class COUVIS_8xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('COUVIS_8xxx', re.I, 'COUVIS_8xxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_PRODUCTS = opus_products
    FILESPEC_TO_OPUS_ID = filespec_to_opus_id

    VIEWABLES = {
        'default': default_viewables,
        'diagrams': diagrams_viewables,
    }

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']  = associations_to_volumes
    ASSOCIATIONS['previews'] = associations_to_previews
    ASSOCIATIONS['diagrams'] = associations_to_diagrams
    ASSOCIATIONS['metadata'] = associations_to_metadata

pdsfile.PdsFile.FILESPEC_TO_LOGICAL_PATH = filespec_to_logical_path + pdsfile.PdsFile.FILESPEC_TO_LOGICAL_PATH

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COUVIS_8xxx'] = COUVIS_8xxx

####################################################################################################################################
