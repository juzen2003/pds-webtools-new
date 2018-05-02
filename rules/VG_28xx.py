####################################################################################################################################
# rules/VG_28xx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'.*/EDITDATA', re.I, ('Edited data',                   'DATADIR')),
    (r'.*/FOVMAPS',  re.I, ('Field-of-view maps',            'IMAGEDIR')),
    (r'.*/IMAGES',   re.I, ('Star reference image files',    'IMAGEDIR')),
    (r'.*/JITTER',   re.I, ('Pointing data',                 'GEOMDIR')),
    (r'.*/NOISDATA', re.I, ('Noise data',                    'DATADIR')),
    (r'.*/RAWDATA',  re.I, ('Raw data',                      'DATADIR')),
    (r'.*/TRAJECT',  re.I, ('Trajectory data',               'GEOMDIR')),
    (r'.*/VECTORS',  re.I, ('Pointing data',                 'GEOMDIR')),
    (r'.*/S_RINGS',  re.I, ('Saturn ring occultation data',  'DATADIR')),
    (r'.*/U_RINGS',  re.I, ('Uranian ring occultation data', 'DATADIR')),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

# view_options = translator.TranslatorByRegex([
#     (r'volumes/VG_28xx(|/\w+)/VG_28../IMAGES', 0, (True, False, False)),
# ])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class VG_28xx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('VG_28xxx', re.I, 'VG_28xx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
#     VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['VG_28xx'] = VG_28xx

####################################################################################################################################
