####################################################################################################################################
# rules/COUVIS_0xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*/DATA',          re.I, ('Data files grouped by date', 'CUBEDIR')),
    (r'volumes/.*/DATA/\w+',      re.I, ('Data files grouped by date', 'CUBEDIR')),
    (r'volumes/.*/HSP\w+\.DAT',   re.I, ('Time series data',           'DATA')),
    (r'volumes/.*/HDAC\w+\.DAT',  re.I, ('Binary data cube',           'DATA')),
    (r'volumes/.*/\w+\.DAT',      re.I, ('Spectral data cube',         'CUBE')),
    (r'volumes/.*\.txt_[0-9].*',  re.I, ('Text file',                  'INFO')),
    (r'volumes/.*OLD.DIR',        re.I, ('Directory',                  'FOLDER')),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'previews/(.*)_(\w+\.png)',    0, r'volumes/\1.*'),
    (r'previews/(\w+/\w+/DATA/\w+)', 0, r'volumes/\1'),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews)/COUVIS_0xxx/COUVIS_..../DATA(|/\w+)', 0, (True, True, True)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'volumes/(\w+)/COUVIS_[0-9]{4}/DATA/(\w+)', 0, r'volumes/\1/*/DATA/*'),
    (r'volumes/(\w+)/COUVIS_[0-9]{4}/DATA',       0, r'volumes/\1/*/DATA'),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'volumes/(.*/DATA/\w+/.*)\.(\w+)', 0, (r'previews/\1_thumb.png',
                                             r'previews/\1_small.png',
                                             r'previews/\1_med.png',
                                             r'previews/\1_full.png')),
])

####################################################################################################################################
# SORT_KEY
####################################################################################################################################

sort_key = translator.TranslatorByRegex([
    (r'^(EUV|FUV|HSP|HDAC)([0-9]{4}_[0-9]{3}_[0-9]{2}_[0-9]{2}.*)_thumb(\..*)', 0, r'\2\1_1thumb\3'),
    (r'^(EUV|FUV|HSP|HDAC)([0-9]{4}_[0-9]{3}_[0-9]{2}_[0-9]{2}.*)_small(\..*)', 0, r'\2\1_2small\3'),
    (r'^(EUV|FUV|HSP|HDAC)([0-9]{4}_[0-9]{3}_[0-9]{2}_[0-9]{2}.*)_med(\..*)',   0, r'\2\1_3med\3'),
    (r'^(EUV|FUV|HSP|HDAC)([0-9]{4}_[0-9]{3}_[0-9]{2}_[0-9]{2}.*)_full(\..*)',  0, r'\2\1_4full\3'),
    (r'^(EUV|FUV|HSP|HDAC)([0-9]{4}_[0-9]{3}_[0-9]{2}_[0-9]{2}.*)(\.DAT|LBL)',  0, r'\2\1\3'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class COUVIS_0xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('COUVIS_0xxx', re.I, 'COUVIS_0xxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS
    SORT_KEY = sort_key + pdsfile.PdsFile.SORT_KEY
    ASSOCIATIONS_TO_VOLUMES = associations_to_volumes + pdsfile.PdsFile.ASSOCIATIONS_TO_VOLUMES

    VIEWABLES = {'default': default_viewables}

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COUVIS_0xxx'] = COUVIS_0xxx

####################################################################################################################################
