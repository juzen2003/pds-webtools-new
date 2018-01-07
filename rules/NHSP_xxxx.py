####################################################################################################################################
# rules/NHSP_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

key_from_path = translator.TranslatorByRegex([
    (r'[-a-z]+/NHSP_xxxx(|_\w+)/NHSP_([0-9]{4})', re.I, r'NHSP_xxxx/NHSP_\2'),
    (r'[-a-z]+/NHSP_xxxx(|_\w+)',                 re.I, r'NHSP_xxxx'),
])

description_and_icon = translator.TranslatorByDict({
    'NHSP_xxxx'          : ('SPICE kernels for New Horizons',                   'VOLDIR'),
    'NHSP_xxxx/NHSP_1000': ('SPICE kernels for the New Horizons Jupiter flyby', 'VOLUME'),
}, key_from_path)

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class NHSP_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('NHSP_xxxx', re.I, 'NHSP_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon + pdsfile.PdsFile.DESCRIPTION_AND_ICON

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['NHSP_xxxx'] = NHSP_xxxx

####################################################################################################################################
