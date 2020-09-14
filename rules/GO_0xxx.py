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
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'.*/(GO_0xxx/GO_..../.*/C[0-9]{10}[A-Z]).*',              0, [r'volumes/\1.IMG',
                                                                    r'volumes/\1.LBL']),
    (r'.*/(GO_0xxx_v1/GO_..../.*/C[0-9]{6}/[0-9]{4}[A-Z]).*',   0, [r'volumes/\1.IMG',
                                                                    r'volumes/\1.LBL']),
    (r'metadata/(GO_0xxx)/(GO_00..)/.*_index\..*',              0, [r'volumes/\1/\2/INDEX/IMGINDEX.TAB',
                                                                    r'volumes/\1/\2/INDEX/IMGINDEX.LBL']),
    (r'metadata/(GO_0xxx)/(GO_0999)/.*_index\..*',              0, [r'volumes/\1/GO_0023/INDEX/CUMINDEX.TAB',
                                                                    r'volumes/\1/GO_0023/INDEX/CUMINDEX.LBL']),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'.*/(GO_0xxx/GO_..../.*/C[0-9]{10}[A-Z]).*',              0, [r'previews/\1_full.jpg',
                                                                    r'previews/\1_thumb.jpg',
                                                                    r'previews/\1_small.jpg',
                                                                    r'previews/\1_med.jpg']),
    (r'.*/(GO_0xxx_v1/GO_..../.*/C[0-9]{6}/[0-9]{4}[A-Z]).*',   0, [r'previews/\1_full.jpg',
                                                                    r'previews/\1_thumb.jpg',
                                                                    r'previews/\1_small.jpg',
                                                                    r'previews/\1_med.jpg']),
])

associations_to_metadata = translator.TranslatorByRegex([
    (r'.*/(GO_0xxx)/(GO_....)/.*/(C[0-9]{10})[A-Z].*',      0,  r'metadata/\1/\2/\2_index.tab/\3'),
    (r'.*/(GO_0xxx_v1)/(GO_....).*',                        0,  r'metadata/\1/\2'),
    ('volumes/(GO_0xxx.*/GO_....)/INDEX/IMGINDEX\..*',      0, [r'metadata/\1/\2/\2_index.tab',
                                                                r'metadata/\1/\2/\2_index.lbl']),
    ('volumes/(GO_0xxx.*/GO_....)/INDEX/CUMINDEX\..*',      0, [r'metadata/\1/GO_0999/GO_0999_index.tab',
                                                                r'metadata/\1/GO_0999/GO_0999_index.lbl']),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews)/GO_0xxx/GO_....(|/BROWSE)/([CEGIJ][0-9]{1,2}|REDO)/.*',               0, (True, True, True)),

    (r'(volumes|previews)/GO_0xxx_v1/GO_....(|/BROWSE)/([CEGIJ][0-9]{1,2}|REDO)/.*/C[0-9]{6}$', 0, (True, True, False)),
    (r'(volumes|previews)/GO_0xxx_v1/GO_....(|/BROWSE)/([CEGIJ][0-9]{1,2}|REDO)/.*',            0, (True, True, True)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'(volumes|previews)/GO_0xxx(|_v[1-9])/\w+(|/REDO)/[CEGIJ][0-9]{1,2}$',          0,  r'\1/GO_0xxx\2/*\3/[A-Z][0-9]*'),
    (r'(volumes|previews)/GO_0xxx(|_v[1-9])/\w+(|/REDO)/[CEGIJ][0-9]{1,2}/(\w+)$',    0,  r'\1/GO_0xxx\2/*\3/[A-Z][0-9]*/\4'),
    (r'(volumes|previews)/GO_0xxx(|_v[1-9])/\w+(|/REDO)/[CEGIJ][0-9]{1,2}/(\w+)/.*',  0,  r'\1/GO_0xxx\2/*\3/\[A-Z][0-9]*/\4/*'),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl',  re.I, ''),

    (r'volumes/(.*/C[0-9]{10}[A-Z])\.(IMG|LBL)', 0, (r'previews/\1_thumb.jpg',
                                                     r'previews/\1_small.jpg',
                                                     r'previews/\1_med.jpg',
                                                     r'previews/\1_full.jpg')),

    (r'volumes/(GO_0xxx_v1/.*/C[0-9]{6}/.*)\.(IMG|LBL)', 0, (r'previews/\1_thumb.jpg',
                                                             r'previews/\1_small.jpg',
                                                             r'previews/\1_med.jpg',
                                                             r'previews/\1_full.jpg')),
])

####################################################################################################################################
# SORT_KEY
####################################################################################################################################

sort_key = translator.TranslatorByRegex([

    # Puts encounters in chronological order, after AAREADME
    (r'([CEGIJ])([0-9])$',      0, r'AAZ0\2\1'),
    (r'([CEGIJ])([0-9][0-9])$', 0, r'AAZ\2\1'),
    (r'(AAREADME.TXT)$',        0, r'\1'),
    (r'(CATALOG)$',             0, r'\1'),
    (r'(DOCUMENT)$',            0, r'\1'),
    (r'(ERRATA.TXT)$',          0, r'\1'),
    (r'(INDEX)$',               0, r'\1'),
    (r'(LABEL)$',               0, r'\1'),
    (r'(REDO)$',                0, r'\1'),
    (r'(VOLDESC.CAT)$',         0, r'\1'),
])

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/GO_0xxx(|_v[1-9])/GO_0.../(?!CATALOG|DOCUMENT|INDEX|LABEL).*\.(IMG|LBL)', 0, ('Galileo SSI', 10, 'gossi_raw', 'Raw Image', True)),
])

####################################################################################################################################
# OPUS_FORMAT
####################################################################################################################################

opus_format = translator.TranslatorByRegex([
    (r'.*\.IMG$', 0, ('Binary', 'VICAR')),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

opus_products = translator.TranslatorByRegex([
    (r'.*volumes/(GO_0xxx)/(GO_0...)/(.*/C[0-9]{6})([0-9]{4}[A-Z])\.(IMG|LBL)', 0, [r'volumes/\1/\2/\3\4.IMG',
                                                                           r'volumes/\1/\2/\3\4.LBL',
                                                                           r'volumes/\1_v1/\2/\3/\4.IMG',
                                                                           r'volumes/\1_v1/\2/\3/\4.LBL',
                                                                           r'previews/\1/\2/\3\4_thumb.jpg',
                                                                           r'previews/\1/\2/\3\4_small.jpg',
                                                                           r'previews/\1/\2/\3\4_med.jpg',
                                                                           r'previews/\1/\2/\3\4_full.jpg',
                                                                           r'previews/\1_v1/\2/\3/\4_thumb.jpg',
                                                                           r'previews/\1_v1/\2/\3/\4_small.jpg',
                                                                           r'previews/\1_v1/\2/\3/\4_med.jpg',
                                                                           r'previews/\1_v1/\2/\3/\4_full.jpg',
                                                                           r'metadata/\1/\2/\2_index.lbl',
                                                                           r'metadata/\1/\2/\2_index.tab']),
])

####################################################################################################################################
# FILESPEC_TO_OPUS_ID
####################################################################################################################################

filespec_to_opus_id = translator.TranslatorByRegex([
    (r'GO_00../.*/(C[0-9]{10}).*', 0, r'go-ssi-\1'),
])

####################################################################################################################################
# OPUS_ID_TO_FILESPEC
####################################################################################################################################

opus_id_to_filespec = translator.TranslatorByRegex([
    (r'go-ssi-.*', 0, re.compile(r'.*\.IMG$')),
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
    SORT_KEY = sort_key + pdsfile.PdsFile.SORT_KEY

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_FORMAT = opus_format + pdsfile.PdsFile.OPUS_FORMAT
    OPUS_PRODUCTS = opus_products
    FILESPEC_TO_OPUS_ID = filespec_to_opus_id

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']  = associations_to_volumes
    ASSOCIATIONS['previews'] = associations_to_previews
    ASSOCIATIONS['metadata'] = associations_to_metadata

    FILENAME_KEYLEN = 11    # trim off suffixes

    VIEWABLES = {'default': default_viewables}

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_FILESPEC = opus_id_to_filespec + pdsfile.PdsFile.OPUS_ID_TO_FILESPEC

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['GO_0xxx'] = GO_0xxx

####################################################################################################################################
