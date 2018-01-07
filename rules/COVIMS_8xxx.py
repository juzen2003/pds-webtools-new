####################################################################################################################################
# rules/COVIMS_8xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

key_from_path = translator.TranslatorByRegex([
    (r'[-a-z]+/COVIMS_8xxx(|_\w+)/COVIMS_(8[0-9]{3})', re.I, r'COVIMS_8xxx/COVIMS_\2'),
    (r'[-a-z]+/COVIMS_8xxx(|_\w+)',                    re.I, r'COVIMS_8xxx'),
])

description_and_icon = translator.TranslatorByDict({
    'COVIMS_8xxx'             : ('Cassini VIMS occultation profiles of Saturn\'s rings', 'VOLDIR'),
    'COVIMS_8xxx/COVIMS_8001' : ('Cassini VIMS occultation profiles of Saturn\'s rings', 'VOLUME'),
}, key_from_path)

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class COVIMS_8xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('COVIMS_8xxx', re.I, 'COVIMS_8xxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon + pdsfile.PdsFile.DESCRIPTION_AND_ICON

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COVIMS_8xxx'] = COVIMS_8xxx

####################################################################################################################################
