####################################################################################################################################
# rules/COVIMS_0xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*/data',                                      re.I, ('Data files grouped by date', 'CUBEDIR')),
    (r'volumes/.*/dat/\w+',                                   re.I, ('Data files grouped by date', 'CUBEDIR')),
    (r'volumes/.*/extras',                                    re.I, ('Browse image collection',    'BROWDIR')),
    (r'volumes/.*/data/.*/extras/\w+',                        re.I, ('Browse image collection',    'BROWDIR')),
    (r'volumes/.*/data/.*/extras/.*\.(jpeg|jpeg_small|tiff)', re.I, ('Browse image',               'BROWSE' )),
    (r'volumes/.*/software.*cube_prep/cube_prep',             re.I, ('Program binary',             'CODE'   )),
    (r'volumes/.*/software.*/PPVL_report',                    re.I, ('Program binary',             'CODE'   )),

    (r'.*/thumbnail(/\w+)*',            re.I, ('Small browse images',           'BROWDIR' )),
    (r'.*/thumbnail/.*\.(gif|jpg|jpeg|jpeg_small|tif|tiff|png)',
                                        re.I, ('Small browse image',            'BROWSE'  )),
    (r'.*/tiff(/\w+)*',                 re.I, ('Full-size browse images',       'BROWDIR' )),
    (r'.*/tiff/.*\.(gif|jpg|jpeg|jpeg_small|tif|tiff|png)',
                                        re.I, ('Full-size browse image',        'BROWSE'  )),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl',  re.I, ''),

    (r'volumes/(.*/data/\w+/.*)\.(\w+)', 0, (r'previews/\1_thumb.png',
                                             r'previews/\1_small.png',
                                             r'previews/\1_med.png',
                                             r'previews/\1_full.png')),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'.*/(COVIMS_0xxx)/(COVIMS_....)/(data|extras/\w+)/(\w+/v[0-9]{10})_[0-9](|_[0-9]{3}).*',
                                                                        0, [r'volumes/\1/\2/data/\4_*\5.qub',
                                                                            r'volumes/\1/\2/data/\4_*\5.lbl',
                                                                            r'volumes/\1/\2/data/\4_?.qub',
                                                                            r'volumes/\1/\2/data/\4_?.lbl',
                                                                            r'volumes/\1/\2/data/\4_??.qub',
                                                                            r'volumes/\1/\2/data/\4_??.lbl',
                                                                            r'volumes/\1/\2/extras/thumbnail/\4_*\5.IMG.jpeg_small',
                                                                            r'volumes/\1/\2/extras/browse/\4_*\5.IMG.jpeg',
                                                                            r'volumes/\1/\2/extras/full/\4_*\5.IMG.png',
                                                                            r'volumes/\1/\2/extras/tiff/\4_*\5.IMG.tiff']),
    (r'.*/(COVIMS_0xxx)/(COVIMS_....)/(data|extras|extras/\w+)/(\w+)$', 0, [r'volumes/\1/\2/data/\4',
                                                                            r'volumes/\1/\2/extras/thumbnail/\4',
                                                                            r'volumes/\1/\2/extras/browse/\4',
                                                                            r'volumes/\1/\2/extras/full/\4',
                                                                            r'volumes/\1/\2/extras/tiff/\4']),
    (r'.*/(COVIMS_0xxx)/(COVIMS_....)/(data|extras/\w+)$',              0, [r'volumes/\1/\2/data',
                                                                            r'volumes/\1/\2/extras/thumbnail',
                                                                            r'volumes/\1/\2/extras/browse',
                                                                            r'volumes/\1/\2/extras/full',
                                                                            r'volumes/\1/\2/extras/tiff']),
    (r'.*/(COVIMS_0xxx)/(COVIMS_....)/extras$',                         0,  r'volumes/\1/\2/data'),
    (r'metadata/(COVIMS_0xxx/COVIMS_....)/COVIMS_...._index\.\w+$',     0, [r'volumes/\1/index/index.tab',
                                                                            r'volumes/\1/index/index.lbl']),
    (r'metadata/COVIMS_0xxx/COVIMS_0999/COVIMS_...._index\.\w+$',       0, [r'volumes/COVIMS_0xxx/COVIMS_0094/index/cumindex.tab',
                                                                            r'volumes/COVIMS_0xxx/COVIMS_0094/index/cumindex.lbl']),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'.*/(COVIMS_0xxx)/(COVIMS_....)/(data|extras/\w+)/(\w+/v[0-9]{10}_[0-9]+).*',
                                                                       0, [r'previews/\1/\2/data/\4_full.jpg',
                                                                           r'previews/\1/\2/data/\4_med.jpg',
                                                                           r'previews/\1/\2/data/\4_small.jpg',
                                                                           r'previews/\1/\2/data/\4_thumb.jpg']),
    (r'.*/(COVIMS_0xxx)/(COVIMS_....)/(data|extras/\w+)/(\w+)$',       0,  r'previews/\1/\2/data/\4'),
    (r'.*/(COVIMS_0xxx)/(COVIMS_....)/(data|extras|extras/\w+)$',      0,  r'previews/\1/\2/data'),
    (r'.*/(COVIMS_0xxx)/(COVIMS_....)',                                0,  r'previews/\1/\2'),
])

associations_to_metadata = translator.TranslatorByRegex([
    (r'.*/(COVIMS_0xxx)/(COVIMS_....)/(data|extras/\w+)/\w+/(v[0-9]{10}_[0-9]+).*',
                                                                       0, [r'metadata/\1/\2/\2_index.tab/\4',
                                                                           r'metadata/\1/\2/\2_ring_summary.tab/\4',
                                                                           r'metadata/\1/\2/\2_moon_summary.tab/\4',
                                                                           r'metadata/\1/\2/\2_saturn_summary.tab/\4',
                                                                           r'metadata/\1/\2/\2_jupiter_summary.tab/\4',
                                                                           r'metadata/\1/\2']),
    (r'.*/(COVIMS_0xxx)/(COVIMS_....)/(|data|extras|extras/\w+)$',     0,  r'metadata/\1/\2/'),
    (r'.*/(COVIMS_0xxx)/(COVIMS_....)/index/index\.\w+$',              0, [r'metadata/\1/\2/\2_index.tab',
                                                                           r'metadata/\1/\2/\2_index.lbl']),
    (r'.*/(COVIMS_0xxx)/(COVIMS_....)/index/cumindex\.\w+$',           0, [r'metadata/\1/COVIMS_0999/COVIMS_0999_index.tab',
                                                                           r'metadata/\1/COVIMS_0999/COVIMS_0999_index.lbl']),
    (r'metadata/(COVIMS_0xxx)/(COVIMS_....)/(\w+)\.\w+$',              0, [r'metadata/\1/COVIMS_0999/\3.tab',
                                                                           r'metadata/\1/COVIMS_0999/\3.lbl']),
    (r'metadata/(COVIMS_0xxx)/(COVIMS_....)$',                         0,  r'metadata/\1/COVIMS_0999'),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews)/\w+/\w+/data(|/\w+)',       0, (True, True, True)),
    (r'(volumes|previews)/\w+/\w+/extras/\w+(|/\w+)', 0, (True, True, True)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'(volumes|previews)/(\w+)/\w+/data/\w+', 0, r'\1/\2/*/data/*'),
    (r'(volumes|previews)/(\w+)/\w+/data',     0, r'\1/\2/*/data'),

    (r'volumes/(\w+)/\w+/extras/(\w+)/\w+', 0, r'volumes/\1/*/extras/\2/*'),
    (r'volumes/(\w+)/\w+/extras/(\w+)',     0, r'volumes/\1/*/extras/\2'),
])

####################################################################################################################################
# OPUS_FORMAT
####################################################################################################################################

opus_format = translator.TranslatorByRegex([
    (r'.*\.qub$',        0, ('Binary', 'ISIS2')),
    (r'.*\.jpeg_small$', 0, ('Binary', 'JPEG')),
])

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/.*\.(qub|lbl)$',                      0, ('Cassini VIMS',   0, 'covims_raw',    'Raw cube',                  True)),
    (r'volumes/.*/extras/thumbnail/.*\.jpeg_small$', 0, ('Cassini VIMS', 110, 'covims_thumb',  'Extra preview (thumbnail)', False)),
    (r'volumes/.*/extras/browse/.*\.jpeg$',          0, ('Cassini VIMS', 120, 'covims_medium', 'Extra preview (medium)',    False)),
    (r'volumes/.*/extras/(tiff|full)/.*\.\w+$',      0, ('Cassini VIMS', 130, 'covims_full',   'Extra preview (full)',      True)),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

PACKED_OPUS_TYPE = ('Cassini VIMS', 10, 'covims_packed', 'Packed version of unpacked raw data', True)

opus_products = translator.TranslatorByRegex([
    (r'.*volumes/(COVIMS_0xxx)/(COVIMS_0...)/data/(\w+/v[0-9]{10})_[0-9]+(|_[0-9]{3})\.(qub|lbl)', 0,
                                                                    [r'volumes/\1/\2/data/\3_*\4.qub',
                                                                     r'volumes/\1/\2/data/\3_*\4.lbl',
                                                                     r'volumes/\1/\2/extras/thumbnail/\3_*\4.qub.jpeg_small',
                                                                     r'volumes/\1/\2/extras/browse/\3_*\4.qub.jpeg',
                                                                     r'volumes/\1/\2/extras/full/\3_*\4.qub.png',
                                                                     r'volumes/\1/\2/extras/tiff/\3_*\4.qub.tiff',
                                                                     r'previews/\1/\2/data/\3_*\4_thumb.png',
                                                                     r'previews/\1/\2/data/\3_*\4_small.png',
                                                                     r'previews/\1/\2/data/\3_*\4_med.png',
                                                                     r'previews/\1/\2/data/\3_*\4_full.png',
                                                                     r'metadata/\1/\2/\2_saturn_summary.lbl',
                                                                     r'metadata/\1/\2/\2_saturn_summary.tab',
                                                                     r'metadata/\1/\2/\2_moon_summary.lbl',
                                                                     r'metadata/\1/\2/\2_moon_summary.tab',
                                                                     r'metadata/\1/\2/\2_ring_summary.lbl',
                                                                     r'metadata/\1/\2/\2_ring_summary.tab',
                                                                     r'metadata/\1/\2/\2_inventory.lbl',
                                                                     r'metadata/\1/\2/\2_inventory.tab',
                                                                     r'metadata/\1/\2/\2_index.lbl',
                                                                     r'metadata/\1/\2/\2_index.tab']),
    # packed versions of unpacked files
    (r'.*volumes/(COVIMS_0xxx)/(COVIMS_0...)/data/(\w+/v[0-9]{10})_[0-9]+_[0-9]{3}\.(qub|lbl)', 0,
                                                                    [(r'volumes/\1/\2/data/\3_?.qub', PACKED_OPUS_TYPE),
                                                                     (r'volumes/\1/\2/data/\3_?.lbl', PACKED_OPUS_TYPE),
                                                                     (r'volumes/\1/\2/data/\3_??.qub', PACKED_OPUS_TYPE),
                                                                     (r'volumes/\1/\2/data/\3_??.lbl', PACKED_OPUS_TYPE)]),
])

####################################################################################################################################
# FILESPEC_TO_OPUS_ID
####################################################################################################################################

# filespec_to_opus_id = translator.TranslatorByRegex([
#     # There are up to two OPUS IDs associated with each VIMS file, one for the VIS channel and one for the IR channel.
#     # This translator returns the OPUS ID without the suffix "_IR" or "_VIS" used by OPUS. That must be handled separately
#     (r'COVIMS_0001/(data|extras)/.*/(v[0-9]{10})_[0-9]+\..+$',  0, r'cassini.vims.jupiter_cruise..\2'),
#
#     (r'COVIMS_0002/(data|extras)/.*/(v135[0-7][0-9]{6})_[0-9]+\..+$',  0, r'cassini.vims.jupiter_cruise..\2'),
#     (r'COVIMS_0002/(data|extras)/.*/(v13580[0-9]{5})_[0-9]+\..+$',     0, r'cassini.vims.jupiter_cruise..\2'),
#     (r'COVIMS_0002/(data|extras)/.*/(v1358[1-9][0-9]{5})_[0-9]+\..+$', 0, r'cassini.vims.jupiter..\2'),
#     (r'COVIMS_0002/(data|extras)/.*/(v1359[0-9]{6})_[0-9]+\..+$',      0, r'cassini.vims.jupiter..\2'),
#     (r'COVIMS_0002/(data|extras)/.*/(v13[6-9]{8})_[0-9]+\..+$',        0, r'cassini.vims.jupiter..\2'),
#
#     (r'COVIMS_0003/(data|extras)/.*/(v13[6-9]{8})_[0-9]+\..+$',        0, r'cassini.vims.saturn_cruise..\2'),
#     (r'COVIMS_0003/(data|extras)/.*/(v14[0-4]{8})_[0-9]+\..+$',        0, r'cassini.vims.saturn_cruise..\2'),
#     (r'COVIMS_0003/(data|extras)/.*/(v145[0-4][0-9]{6})_[0-9]+\..+$',  0, r'cassini.vims.saturn_cruise..\2'),
#     (r'COVIMS_0003/(data|extras)/.*/(v145[5-9][0-9]{6})_[0-9]+\..+$',  0, r'cassini.vims.saturn..\2'),
#     (r'COVIMS_0003/(data|extras)/.*/(v14[6-9][0-9]{7})_[0-9]+\..+$',   0, r'cassini.vims.saturn..\2'),
#
#     (r'COVIMS_000[4-9]/(data|extras)/.*/(v[0-9]{10})_[0-9]+\..+$',     0, r'cassini.vims.saturn..\2'),
#     (r'COVIMS_00[1-9]./(data|extras)/.*/(v[0-9]{10})_[0-9]+\..+$',     0, r'cassini.vims.saturn..\2'),
# ])

filespec_to_opus_id = translator.TranslatorByRegex([
    # There are up to two OPUS IDs associated with each VIMS file, one for the VIS channel and one for the IR channel.
    # This translator returns the OPUS ID without the suffix "_IR" or "_VIS" used by OPUS. That must be handled separately
    (r'COVIMS_00../(data|extras)/.*/(v[0-9]{10})_[0-9]+(|_[0-9]{3})\..+$',  0, r'co-vims-\2\3'),
])

####################################################################################################################################
# OPUS_ID_TO_FILESPEC
####################################################################################################################################

opus_id_to_filespec = translator.TranslatorByRegex([
    (r'co-vims-(v[0-9]{10})(|_...)', 0, r'.*\1_[0-9]+\2\.qub$'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class COVIMS_0xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('COVIMS_0xxx', re.I, 'COVIMS_0xxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_FORMAT = opus_format + pdsfile.PdsFile.OPUS_FORMAT
    OPUS_PRODUCTS = opus_products
    FILESPEC_TO_OPUS_ID = filespec_to_opus_id

    VIEWABLES = {'default': default_viewables}

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']  = associations_to_volumes
    ASSOCIATIONS['previews'] = associations_to_previews
    ASSOCIATIONS['metadata'] = associations_to_metadata

    def FILENAME_KEYLEN(self):
        parts = self.basename.split('_')
        if len(parts) == 3:
            return 0
        else:
            return 11   # trim off suffixes at least without _nnn line number


# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_FILESPEC = opus_id_to_filespec + pdsfile.PdsFile.OPUS_ID_TO_FILESPEC

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COVIMS_0xxx'] = COVIMS_0xxx

####################################################################################################################################
