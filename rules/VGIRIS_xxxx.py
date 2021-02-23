####################################################################################################################################
# rules/VGIRIS_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

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
# FILESPEC_TO_VOLSET
####################################################################################################################################

filespec_to_volset = translator.TranslatorByRegex([
    (r'VGIRIS_\d{4}.*', 0, 'VGIRIS_xxxx_peer_review'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class VGIRIS_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('VGIRIS_xxxx', re.I, 'VGIRIS_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON

pdsfile.PdsFile.FILESPEC_TO_VOLSET = filespec_to_volset + pdsfile.PdsFile.FILESPEC_TO_VOLSET

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['VGIRIS_xxxx'] = VGIRIS_xxxx

####################################################################################################################################
