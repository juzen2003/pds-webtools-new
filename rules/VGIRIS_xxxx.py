####################################################################################################################################
# rules/VGIRIS_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

key_from_path = translator.TranslatorByRegex([
 (r'[-a-z]+/VGIRIS_xxxx(|_\w+)/VGIRIS_([0-9]{4})',  re.I, r'VGIRIS_xxxx/VGIRIS_\2'),
 (r'[-a-z]+/VGIRIS_xxxx(|_\w+)',                    re.I, r'VGIRIS_xxxx'),
])

description_and_icon_by_dict = translator.TranslatorByDict({
    'VGIRIS_xxxx'            : ('Voyager IRIS thermal infrared data, extended collection from original tapes',  'VOLDIR'),
    'VGIRIS_xxxx/VGIRIS_0001': ('Voyager IRIS thermal infrared extended data set from original tapes, Jupiter', 'VOLUME'),
    'VGIRIS_xxxx/VGIRIS_0002': ('Voyager IRIS thermal infrared extended data set from original tapes, Saturn',  'VOLUME'),

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

class VGIRIS_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('VGIRIS_xxxx', re.I, 'VGIRIS_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_dict + description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['VGIRIS_xxxx'] = VGIRIS_xxxx

####################################################################################################################################
