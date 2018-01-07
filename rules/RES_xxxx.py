####################################################################################################################################
# rules/RES_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

key_from_path = translator.TranslatorByRegex([
    (r'[-a-z]+/RES_xxxx(|_\w+)/RES_([0-9]{4})', re.I, r'RES_xxxx/RES_\2'),
    (r'[-a-z]+/RES_xxxx(|_\w+)',                re.I, r'RES_xxxx'),
])

description_and_icon = translator.TranslatorByDict({
    'RES_xxxx'         : ('Resonance calculations',                       'VOLDIR'),
    'RES_xxxx/RES_0001': ('Resonance calculations for the Saturn system', 'VOLUME'),

}, key_from_path)

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class RES_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('RES_xxxx', re.I, 'RES_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon + pdsfile.PdsFile.DESCRIPTION_AND_ICON

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['RES_xxxx'] = RES_xxxx

####################################################################################################################################
