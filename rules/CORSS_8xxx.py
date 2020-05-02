####################################################################################################################################
# rules/CORSS_8xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/.*_TAU_01KM\.(TAB|LBL)$', 0, ('Cassini RSS', 10, 'corss_occ_01',  'Occultation Profile (1km)')),
    (r'volumes/.*_TAU_10KM\.(TAB|LBL)$', 0, ('Cassini RSS', 20, 'corss_occ_10',  'Occultation Profile (10km)')),
    (r'volumes/.*_DLP_500M\.(TAB|LBL)$', 0, ('Cassini RSS', 30, 'corss_occ_dlp', 'Diffraction-Ltd Occultation Profile')),
    (r'volumes/.*_CAL\.(TAB|LBL)$',      0, ('Cassini RSS', 40, 'corss_occ_cal', 'Occultation Calibration Parameters')),
    (r'volumes/.*_GEO\.(TAB|LBL)$',      0, ('Cassini RSS', 50, 'corss_occ_geo', 'Occultation Geometry Parameters')),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

# Use of explicit file names means we don't need to invoke glob.glob(); this goes much faster
opus_products = translator.TranslatorByRegex([
    (r'.*volumes/(CORSS_8xxx/.*)_TAU_01KM\.(TAB|LBL)', 0, [r'volumes/\1_TAU_01KM.TAB',
                                                           r'volumes/\1_TAU_01KM.LBL',
                                                           r'volumes/\1_TAU_10KM.TAB',
                                                           r'volumes/\1_TAU_10KM.LBL',
                                                           r'volumes/\1_DLP_500M.TAB',
                                                           r'volumes/\1_DLP_500M.LBL',
                                                           r'volumes/\1_CAL.TAB',
                                                           r'volumes/\1_CAL.LBL',
                                                           r'volumes/\1_GEO.TAB',
                                                           r'volumes/\1_GEO.LBL']),
])

####################################################################################################################################
# FILESPEC_TO_OPUS_ID
####################################################################################################################################

filespec_to_opus_id = translator.TranslatorByRegex([
    (r'CORSS_8001/data/Rev\w+/Rev\w+/\w+/RSS_(\d{4})_(\d{3})_(\w{3})_(I|E)_TAU_01KM\..+$', 0, r'co-rss-occ-\1-\2-\3-\4'),
])

####################################################################################################################################
# FILESPEC_TO_LOGICAL_PATH
####################################################################################################################################

filespec_to_logical_path = translator.TranslatorByRegex([
    (r'CORSS(_..../.*_(thumb|small|med|full)\.(jpg|png))', 0, r'previews/CORSS_8xxx/CORSS\1'),
    (r'CORSS(_..../.*)$',                                  0, r'volumes/CORSS_8xxx/CORSS\1'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class CORSS_8xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('CORSS_8xxx', re.I, 'CORSS_8xxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_PRODUCTS = opus_products
    FILESPEC_TO_OPUS_ID = filespec_to_opus_id

pdsfile.PdsFile.FILESPEC_TO_LOGICAL_PATH = filespec_to_logical_path + pdsfile.PdsFile.FILESPEC_TO_LOGICAL_PATH

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['CORSS_8xxx'] = CORSS_8xxx

####################################################################################################################################
