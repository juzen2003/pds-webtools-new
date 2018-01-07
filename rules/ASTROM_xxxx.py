####################################################################################################################################
# rules/ASTROM_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

key_from_path = translator.TranslatorByRegex([
    (r'[-a-z]+/ASTROM_xxxx(|_\w+)/ASTROM_([0-9]{4})', re.I, r'ASTROM_xxxx/ASTROM_\2'),
    (r'[-a-z]+/ASTROM_xxxx(|_\w+)',                   re.I, r'ASTROM_xxxx'),
])

description_and_icon = translator.TranslatorByDict({
    'ASTROM_xxxx'            : ('Satellite astrometry collection',                    'VOLDIR'),
    'ASTROM_xxxx/ASTROM_0001': ('HST WFPC2 astrometry of Saturn\'s moons, 1994-2002', 'VOLUME'),
    'ASTROM_xxxx/ASTROM_0101': ('HST WFPC2 astrometry of Saturn\'s moons, 1996-2005', 'VOLUME'),
}, key_from_path)

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class ASTROM_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('ASTROM_xxxx', re.I, 'ASTROM_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon + pdsfile.PdsFile.DESCRIPTION_AND_ICON

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['ASTROM_xxxx'] = ASTROM_xxxx

####################################################################################################################################
