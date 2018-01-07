####################################################################################################################################
# rules/GO_0xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

key_from_path = translator.TranslatorByRegex([
    (r'[-a-z]+/GO_0xxx(|_\w+)/GO_(0[0-9]{3})', re.I, r'GO_0xxx/GO_\2'),
    (r'[-a-z]+/GO_0xxx(|_\w+)',                 re.I, r'GO_0xxx'),
])

description_and_icon_by_dict = translator.TranslatorByDict({
    'GO_0xxx'        : ('Galileo image collection',                                              'VOLDIR'),
    'GO_0xxx/GO_0017': ('Galileo images 1996-06-03 to 1996-12-14T (SC clock 03464059-03740374)', 'VOLUME'),
    'GO_0xxx/GO_0018': ('Galileo images 1996-11-09 to 1997-04-05T (SC clock 03689769-03899239)', 'VOLUME'),
    'GO_0xxx/GO_0019': ('Galileo images 1996-11-04 to 1997-10-06T (SC clock 03683692-04161140)', 'VOLUME'),
    'GO_0xxx/GO_0020': ('Galileo images 1997-11-04 to 1998-09-26T (SC clock 04203615-04666849)', 'VOLUME'),
    'GO_0xxx/GO_0021': ('Galileo images 1998-12-10 to 1999-08-13T (SC clock 04774216-05124811)', 'VOLUME'),
    'GO_0xxx/GO_0022': ('Galileo images 1999-10-11 to 1999-11-26T (SC clock 05207927-05273656)', 'VOLUME'),
    'GO_0xxx/GO_0023': ('Galileo images 1997-11-04 to 2002-03-19T (SC clock 04203615-06475387)', 'VOLUME'),
}, key_from_path)

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

    DESCRIPTION_AND_ICON = description_and_icon_by_dict + description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS

    VIEWABLES = {'default': default_viewables}

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['GO_0xxx'] = GO_0xxx

####################################################################################################################################
