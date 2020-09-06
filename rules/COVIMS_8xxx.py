####################################################################################################################################
# rules/COVIMS_8xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/.*_TAU_01KM\.(TAB|LBL)$', 0, ('Cassini VIMS', 10, 'covims_occ_01', 'Occultation Profile (1km)',  True)),
    (r'volumes/.*_TAU_10KM\.(TAB|LBL)$', 0, ('Cassini VIMS', 20, 'covims_occ_10', 'Occultation Profile (10km)', True)),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

# Use of explicit file names means we don't need to invoke glob.glob(); this goes much faster
opus_products = translator.TranslatorByRegex([
    (r'.*volumes/COVIMS_8xxx/(COVIMS_....)/data/(.*)_TAU_01KM\.(TAB|LBL)', 0,
                            [r'volumes/COVIMS_8xxx/\1/data/\2_TAU_01KM.TAB',
                             r'volumes/COVIMS_8xxx/\1/data/\2_TAU_01KM.LBL',
                             r'volumes/COVIMS_8xxx/\1/data/\2_TAU_10KM.LBL',
                             r'volumes/COVIMS_8xxx/\1/data/\2_TAU_10KM.TAB']),

    (r'.*volumes/(COVIMS_8xxx)/(COVIMS_8...)/data/.*_TAU_01KM\.(TAB|LBL)', 0,
                            [r'metadata/\1/\2/\2_index.lbl',
                             r'metadata/\1/\2/\2_index.tab',
                             r'metadata/\1/\2/\2_profile_index.lbl',
                             r'metadata/\1/\2/\2_profile_index.tab',
                             r'metadata/\1/\2/\2_supplemental_index.lbl',
                             r'metadata/\1/\2/\2_supplemental_index.tab']),

])

####################################################################################################################################
# FILESPEC_TO_OPUS_ID
####################################################################################################################################

filespec_to_opus_id = translator.TranslatorByRegex([
    (r'COVIMS_8001/data/VIMS_(\d{4})_(\d{3})_(\w+)_(I|E)_TAU_01KM\..+$', 0, r'co-vims-occ-\1-\2-\3-\4'),
])

####################################################################################################################################
# FILESPEC_TO_LOGICAL_PATH
####################################################################################################################################

filespec_to_logical_path = translator.TranslatorByRegex([
    (r'COVIMS(_8.../.*_(thumb|small|med|full)\.(jpg|png))', 0, r'previews/COVIMS_8xxx/COVIMS\1'),
    (r'COVIMS(_8.../.*)$',                                  0, r'volumes/COVIMS_8xxx/COVIMS\1'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class COVIMS_8xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('COVIMS_8xxx', re.I, 'COVIMS_8xxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_PRODUCTS = opus_products
    FILESPEC_TO_OPUS_ID = filespec_to_opus_id

pdsfile.PdsFile.FILESPEC_TO_LOGICAL_PATH = filespec_to_logical_path + pdsfile.PdsFile.FILESPEC_TO_LOGICAL_PATH

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COVIMS_8xxx'] = COVIMS_8xxx

####################################################################################################################################
