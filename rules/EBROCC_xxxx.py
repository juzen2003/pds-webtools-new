####################################################################################################################################
# rules/EBROCC_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

key_from_path = translator.TranslatorByRegex([
    (r'[-a-z]+/EBROCC_xxxx(|_\w+)/EBROCC_([0-9]{4})', re.I, r'EBROCC_xxxx/EBROCC_\2'),
    (r'[-a-z]+/EBROCC_xxxx(|_\w+)',                   re.I, r'EBROCC_xxxx'),
])

description_and_icon_by_dict = translator.TranslatorByDict({
    'EBROCC_xxxx'            : ('Earth-based ring occultation data',                          'VOLDIR'),
    'EBROCC_xxxx/EBROCC_0001': ('Earth-based data from 28 Sgr occultation of Saturn\'s ring', 'VOLUME'),
}, key_from_path)

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*/data',         re.I, ('Data files by observatory',     'IMAGEDIR')),
    (r'volumes/.*/data/\w+',     re.I, ('Data files by observatory',     'IMAGEDIR')),
    (r'volumes/.*/geometry/\w+', re.I, ('Geometry files by observatory', 'GEOMDIR' )),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class EBROCC_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('EBROCC_xxxx', re.I, 'EBROCC_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_dict + description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['EBROCC_xxxx'] = EBROCC_xxxx

####################################################################################################################################
