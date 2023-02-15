####################################################################################################################################
# rules/ASTROM_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# FILESPEC_TO_VOLSET
####################################################################################################################################

filespec_to_volset = translator.TranslatorByRegex([
    (r'ASTROM_\d{4}.*', 0, r'ASTROM_xxxx'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class ASTROM_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('ASTROM_xxxx', re.I, 'ASTROM_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

pdsfile.PdsFile.FILESPEC_TO_VOLSET = filespec_to_volset + pdsfile.PdsFile.FILESPEC_TO_VOLSET

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['ASTROM_xxxx'] = ASTROM_xxxx

####################################################################################################################################
