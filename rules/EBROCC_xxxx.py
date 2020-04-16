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
    (r'volumes/.*\.(tab|lbl)$',                      0, ('Earth-based',   0, 'eb_data',    'Occultation profile')),
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
    FILESPEC_TO_OPUS_ID = filespec_to_opus_id

pdsfile.PdsFile.FILESPEC_TO_LOGICAL_PATH = filespec_to_logical_path + pdsfile.PdsFile.FILESPEC_TO_LOGICAL_PATH

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['EBROCC_xxxx'] = EBROCC_xxxx

####################################################################################################################################
