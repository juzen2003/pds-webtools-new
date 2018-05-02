####################################################################################################################################
# rules/GO_0xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/\w+/\w+(|/REDO)/[CEGIJ][0-9]{1,2}',               re.I, ('Images grouped by orbit',        'IMAGEDIR')),
    (r'volumes/\w+/\w+(|/REDO)/[CEGIJ][0-9]{1,2}/\w+',           re.I, ('Images grouped by target',       'IMAGEDIR')),
    (r'volumes/\w+/\w+(|/REDO)/[CEGIJ][0-9]{1,2}/\w+/C[0-9]{6}', re.I, ('Images grouped by SC clock',     'IMAGEDIR')),
    (r'volumes/\w+/\w+/REDO',                                    re.I, ('Redone images grouped by orbit', 'IMAGEDIR')),
    (r'volumes/.*\.IMG',                                         re.I, ('Raw image, VICAR',               'IMAGE'   )),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews)/GO_0xxx/GO_....(|/BROWSE)/([CEGIJ][0-9]{1,2}|REDO)/.*/C[0-9]{6}', re.I, (True, True, False)),
    (r'(volumes|previews)/GO_0xxx/GO_....(|/BROWSE)/([CEGIJ][0-9]{1,2}|REDO)/.*',           re.I, (True, True, True)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'(volumes|previews)/GO_0xxx/\w+(|/REDO)/[CEGIJ][0-9]{1,2}',          0, (r'\1/GO_0xxx/*/[CEGIJ][0-9]*',
                                                                               r'\1/GO_0xxx/*/REDO/[CEGIJ][0-9]*')),
    (r'(volumes|previews)/GO_0xxx/\w+(|/REDO)/[CEGIJ][0-9]{1,2}/(\w+)',    0, (r'\1/GO_0xxx/*/[CEGIJ][0-9]*/\3',
                                                                               r'\1/GO_0xxx/*/REDO/[CEGIJ][0-9]*/\3')),
    (r'(volumes|previews)/GO_0xxx/\w+(|/REDO)/[CEGIJ][0-9]{1,2}/(\w+)/.*', 0, (r'\1/GO_0xxx/*/[CEGIJ][0-9]*/\3/*',
                                                                               r'\1/GO_0xxx/*/REDO/[CEGIJ][0-9]*/\3/*')),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'volumes/(.*/C[0-9]{6}/.*)\.(IMG|LBL)', 0, (r'previews/\1_thumb.jpg',
                                                  r'previews/\1_small.jpg',
                                                  r'previews/\1_med.jpg',
                                                  r'previews/\1_full.jpg')),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class GO_0xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('GO_0xxx', re.I, 'GO_0xxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS

    VIEWABLES = {'default': default_viewables}

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['GO_0xxx'] = GO_0xxx

####################################################################################################################################
