####################################################################################################################################
# rules/CORSS_8xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

key_from_path = translator.TranslatorByRegex([
    (r'[-a-z]+/CORSS_8xxx(|_\w+)/CORSS_(8[0-9]{3})', re.I, r'CORSS_8xxx/CORSS_\2'),
    (r'[-a-z]+/CORSS_8xxx(|_\w+)',                   re.I, r'CORSS_8xxx'),
])

description_and_icon = translator.TranslatorByDict({
    'CORSS_8xxx'           : ('Cassini RSS radio occultation profiles of Saturn\'s rings', 'VOLDIR'),
    'CORSS_8xxx/CORSS_8001': ('Cassini RSS radio occultation profiles of Saturn\'s rings', 'VOLUME'),
}, key_from_path)

####################################################################################################################################
# INFO_FILE_BASENAMES
####################################################################################################################################

info_file_basenames = translator.TranslatorByRegex([
    (r'(.*_Summary.LBL)', 0, r'\1'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class CORSS_8xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('CORSS_8xxx', re.I, 'CORSS_8xxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    INFO_FILE_BASENAMES = info_file_basenames + pdsfile.PdsFile.INFO_FILE_BASENAMES

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['CORSS_8xxx'] = CORSS_8xxx

####################################################################################################################################
