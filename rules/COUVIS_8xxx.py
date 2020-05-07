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
    (r'volumes/.*_TAU01KM\.(TAB|LBL)$', 0, ('Cassini UVIS', 10, 'couvis_occ_01',  'Occultation Profile (1km)')),
    (r'volumes/.*_TAU10KM\.(TAB|LBL)$', 0, ('Cassini UVIS', 20, 'couvis_occ_10',  'Occultation Profile (10km)')),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

# Use of explicit file names means we don't need to invoke glob.glob(); this goes much faster
opus_products = translator.TranslatorByRegex([
    (r'.*volumes/COUVIS_8xxx/(COUVIS_....)/DATA/(.*)_TAU01KM\.(TAB|LBL)', 0,
                            [r'volumes/COUVIS_8xxx/\1/data/\2_TAU01KM.TAB',
                             r'volumes/COUVIS_8xxx/\1/data/\2_TAU01KM.LBL',
                             r'volumes/COUVIS_8xxx/\1/data/\2_TAU10KM.LBL',
                             r'volumes/COUVIS_8xxx/\1/data/\2_TAU10KM.TAB'])])

####################################################################################################################################
# FILESPEC_TO_OPUS_ID
####################################################################################################################################

filespec_to_opus_id = translator.TranslatorByRegex([
    (r'COUVIS_8001/DATA/UVIS_HSP_(\d{4})_(\d{3})_(\w+)_(I|E)_TAU01KM\..+$', 0, r'co-uvis-occ-\1-\2-\3-\4'),
])

####################################################################################################################################
# FILESPEC_TO_LOGICAL_PATH
####################################################################################################################################

filespec_to_logical_path = translator.TranslatorByRegex([
    (r'COUVIS(_8.../.*_(thumb|small|med|full)\.(jpg|png))', 0, r'previews/COUVIS_8xxx/COUVIS\1'),
    (r'COUVIS(_8.../.*)$',                                  0, r'volumes/COUVIS_8xxx/COUVIS\1'),
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

pdsfile.PdsFile.FILESPEC_TO_LOGICAL_PATH = filespec_to_logical_path + pdsfile.PdsFile.FILESPEC_TO_LOGICAL_PATH

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COUVIS_8xxx'] = COUVIS_8xxx

####################################################################################################################################
