####################################################################################################################################
# rules/VG_20xx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

key_from_path = translator.TranslatorByRegex([
    (r'[-a-z]+/VG_20xx(|_\w+)/VG_(20[0-9]{2})', re.I, r'VG_20xx/VG_\2'),
    (r'[-a-z]+/VG_20xx(|_\w+)',                 re.I, r'VG_20xx'),
])

description_and_icon_by_dict = translator.TranslatorByDict({
    'VG_20xx'        : ('Selected Voyager IRIS thermal infrared data, original release', 'VOLDIR'),
    'VG_20xx/VG_2001': ('Selected Voyager IRIS thermal infrared data, original release', 'VOLUME'),
}, key_from_path)

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'.*/JUPITER', re.I, ('Jupiter data', 'DATADIR')),
    (r'.*/SATURN',  re.I, ('Saturn data',  'DATADIR')),
    (r'.*/URANUS',  re.I, ('Uranus data',  'DATADIR')),
    (r'.*/NEPTUNE', re.I, ('Neptune data', 'DATADIR')),

    (r'.*VG1_JUP\.DAT', re.I, ('Voyager 1 Jupiter data', 'DATA')),
    (r'.*VG2_JUP\.DAT', re.I, ('Voyager 2 Jupiter data', 'DATA')),
    (r'.*VG1_SAT\.DAT', re.I, ('Voyager 1 Saturn data',  'DATA')),
    (r'.*VG2_SAT\.DAT', re.I, ('Voyager 2 Saturn data',  'DATA')),
    (r'.*VG2_URA\.DAT', re.I, ('Voyager 2 Uranus data',  'DATA')),
    (r'.*VG2_NEP\.DAT', re.I, ('Voyager 2 Neptune data', 'DATA')),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class VG_20xx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('VG_20xx', re.I, 'VG_20xx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_dict + description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['VG_20xx'] = VG_20xx

####################################################################################################################################

