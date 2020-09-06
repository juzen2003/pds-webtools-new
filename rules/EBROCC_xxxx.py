####################################################################################################################################
# rules/EBROCC_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*/data',         re.I, ('Data files by observatory',     'IMAGEDIR')),
    (r'volumes/.*/data/\w+',     re.I, ('Data files by observatory',     'IMAGEDIR')),
    (r'volumes/.*/geometry/\w+', re.I, ('Geometry files by observatory', 'GEOMDIR' )),
])

####################################################################################################################################
# OPUS_FORMAT
####################################################################################################################################

opus_format = translator.TranslatorByRegex([
    (r'.*\.TAB$',        0, ('Text', 'CSV')),
])

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/.*\.(TAB|LBL)$', 0, ('Ground Based', 0, 'gb_occ_profile', 'Occultation Profile', True)),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

# Use of explicit file names means we don't need to invoke glob.glob(); this goes much faster
opus_products = translator.TranslatorByRegex([
    (r'.*volumes/(EBROCC_..../.*)\.(TAB|LBL)', 0, [r'volumes/\1.TAB',
                                                   r'volumes/\1.LBL']),
    (r'.*volumes/(EBROCC_....)/(EBROCC_....)/DATA/.*/(\w+)_(EPD|IPD)\.(TAB|LBL)', 0,
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
    (r'EBROCC_0001/DATA/ESO1M/\w+_(I|E)\w+\..+$',  0, r'eso1m-apph-occ-1989-184-28sgr-\1'),
    (r'EBROCC_0001/DATA/ESO22M/\w+_(I|E)\w+\..+$', 0, r'eso22m-apph-occ-1989-184-28sgr-\1'),
    (r'EBROCC_0001/DATA/IRTF/\w+_(I|E).+$',        0, r'irtf-urac-occ-1989-184-28sgr-\1'),
    (r'EBROCC_0001/DATA/LICK1M/\w+_(I|E)\w+\..+$', 0, r'lick1m-ccdc-occ-1989-184-28sgr-\1'),
    (r'EBROCC_0001/DATA/MCD27M/\w+_(I|E)\w+\..+$', 0, r'mcd27m-iirar-occ-1989-184-28sgr-\1'),
    (r'EBROCC_0001/DATA/PAL200/\w+_(I|E)\w+\..+$', 0, r'pal200-circ-occ-1989-184-28sgr-\1')
])

####################################################################################################################################
# FILESPEC_TO_LOGICAL_PATH
####################################################################################################################################

filespec_to_logical_path = translator.TranslatorByRegex([
    (r'EBROCC(_..../.*_(thumb|small|med|full)\.(jpg|png))', 0, r'previews/EBROCC_xxxx/EBROCC\1'),
    (r'EBROCC(_..../.*)$',                                  0, r'volumes/EBROCC_xxxx/EBROCC\1'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class EBROCC_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('EBROCC_xxxx', re.I, 'EBROCC_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_FORMAT = opus_format + pdsfile.PdsFile.OPUS_FORMAT
    OPUS_PRODUCTS = opus_products
    FILESPEC_TO_OPUS_ID = filespec_to_opus_id

pdsfile.PdsFile.FILESPEC_TO_LOGICAL_PATH = filespec_to_logical_path + pdsfile.PdsFile.FILESPEC_TO_LOGICAL_PATH

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['EBROCC_xxxx'] = EBROCC_xxxx

####################################################################################################################################
