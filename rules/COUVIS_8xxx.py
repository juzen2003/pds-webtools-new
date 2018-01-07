####################################################################################################################################
# rules/COUVIS_8xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

key_from_path = translator.TranslatorByRegex([
    (r'[-a-z]+/COUVIS_8xxx(|_\w+)/COUVIS_(8[0-9]{3})', re.I, r'COUVIS_8xxx/COUVIS_\2'),
    (r'[-a-z]+/COUVIS_8xxx(|_\w+)',                    re.I, r'COUVIS_8xxx'),
])

description_and_icon = translator.TranslatorByDict({
    'COUVIS_8xxx'             : ('Cassini UVIS occultation profiles of Saturn\'s rings', 'VOLDIR'),
    'COUVIS_8xxx/COUVIS_8001' : ('Cassini UVIS occultation profiles of Saturn\'s rings', 'VOLUME'),
}, key_from_path)

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class COUVIS_8xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('COUVIS_8xxx', re.I, 'COUVIS_8xxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon + pdsfile.PdsFile.DESCRIPTION_AND_ICON

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COUVIS_8xxx'] = COUVIS_8xxx

####################################################################################################################################
