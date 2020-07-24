####################################################################################################################################
# rules/COISS_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'calibrated/COISS_1xxx'     , re.I, ('Cassini Jupiter image collection, CISSCAL 3.8', 'VOLDIR')),
    (r'calibrated/COISS_2xxx'     , re.I, ('Cassini Saturn  image collection, CISSCAL 3.8', 'VOLDIR')),
    (r'calibrated/COISS_1xxx_v1.0', re.I, ('Cassini Jupiter image collection, CISSCAL 3.6', 'VOLDIR')),
    (r'calibrated/COISS_2xxx_v1.0', re.I, ('Cassini Saturn  image collection, CISSCAL 3.6', 'VOLDIR')),

    (r'volumes/.*/data/.*/N[0-9_]+\.img',                     re.I, ('Narrow-angle image, VICAR',     'IMAGE'   )),
    (r'volumes/.*/data/.*/W[0-9_]+\.img',                     re.I, ('Wide-angle image, VICAR',       'IMAGE'   )),
    (r'volumes/.*/data/.*/extras(/\w+)*(|/)',                 re.I, ('Preview image collection',      'BROWDIR' )),
    (r'volumes/.*/data/.*/extras/.*\.(jpeg|jpeg_small|tiff)', re.I, ('Preview image',                 'BROWSE'  )),
    (r'volumes/.*/COISS_0011/document/.*/[0-9]+\.[0-9]+(|/)', re.I, ('Calibration report',            'INFODIR' )),
    (r'volumes/.*/data(|/\w*)',                               re.I, ('Images grouped by SC clock',    'IMAGEDIR')),

    (r'calibrated/.*_calib\.img',                             re.I, ('Calibrated image, VICAR',       'IMAGE'   )),
    (r'calibrated/.*/data(|/\w+)',                            re.I, ('Calibrated images by SC clock', 'IMAGEDIR')),
    (r'calibrated/\w+(|/\w+)',                                re.I, ('Calibrated image collection',   'IMAGEDIR')),

    (r'.*/thumbnail(/\w+)*',            re.I, ('Small browse images',           'BROWDIR' )),
    (r'.*/thumbnail/.*\.(gif|jpg|jpeg|jpeg_small|tif|tiff|png)',
                                        re.I, ('Small browse image',            'BROWSE'  )),
    (r'.*/(tiff|full)(/\w+)*',          re.I, ('Full-size browse images',       'BROWDIR' )),
    (r'.*/(tiff|full)/.*\.(tif|tiff|png)',
                                        re.I, ('Full-size browse image',        'BROWSE'  )),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl',  re.I, ''),

    (r'\w+/(.*/data/images/[^\.]+)\.\w+',  0, (r'previews/\1_full.png',
                                               r'previews/\1_thumb.jpg',
                                               r'previews/\1_small.jpg',
                                               r'previews/\1_med.jpg')),

    (r'\w+/(.*/data/maps/[^\.]+)\.\w+',    0, (r'previews/\1_full.png',
                                               r'previews/\1_thumb.png',
                                               r'previews/\1_small.png',
                                               r'previews/\1_med.png')),

    (r'\w+/(.*)/extras/\w+/(\w+/[^\.]+)\.\w+',  0, (r'previews/\1/data/\2_full.png',
                                                    r'previews/\1/data/\2_thumb.jpg',
                                                    r'previews/\1/data/\2_small.jpg',
                                                    r'previews/\1/data/\2_med.jpg')),

    (r'volumes/(COISS_....)/(\w+/data/\w+/[^\.]+)\.\w+', 0, (r'previews/\1/\2_full.png',
                                                             r'previews/\1/\2_thumb.jpg',
                                                             r'previews/\1/\2_small.jpg',
                                                             r'previews/\1/\2_med.jpg')),

    (r'calibrated/(COISS_....)(|_.*?)/(\w+/data/\w+/[^\.]+)_CALIB\.\w+', 0, (r'previews/\1/\3_full.png',
                                                                             r'previews/\1/\3_thumb.jpg',
                                                                             r'previews/\1/\3_small.jpg',
                                                                             r'previews/\1/\3_med.jpg')),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'.*/(COISS_[12]xxx)(|_.*?)/(COISS_....)/(data|extras/\w+)/(\w+/[NW][0-9]{10}_[0-9]+).*',
                                                                                0, [r'volumes/\1/\3/data/\5.IMG',
                                                                                    r'volumes/\1/\3/data/\5.LBL',
                                                                                    r'volumes/\1/\3/extras/thumbnail/\5.IMG.jpeg_small',
                                                                                    r'volumes/\1/\3/extras/browse/\5.IMG.jpeg',
                                                                                    r'volumes/\1/\3/extras/full/\5.IMG.png',
                                                                                    r'volumes/\1/\3/extras/tiff/\5.IMG.tiff']),
    (r'.*/(COISS_[12]xxx)(|_.*?)/(COISS_....)/(data|extras|extras/\w+)/(\w+)$', 0, [r'volumes/\1/\3/data/\5',
                                                                                    r'volumes/\1/\3/extras/thumbnail/\5',
                                                                                    r'volumes/\1/\3/extras/browse/\5',
                                                                                    r'volumes/\1/\3/extras/full/\5',
                                                                                    r'volumes/\1/\3/extras/tiff/\5']),
    (r'.*/(COISS_[12]xxx)(|_.*?)/(COISS_....)/(data|extras/\w+)$',              0, [r'volumes/\1/\3/data',
                                                                                    r'volumes/\1/\3/extras/thumbnail',
                                                                                    r'volumes/\1/\3/extras/browse',
                                                                                    r'volumes/\1/\3/extras/full',
                                                                                    r'volumes/\1/\3/extras/tiff']),
    (r'.*/(COISS_[12]xxx)(|_.*?)/(COISS_....)/extras$',                         0, [r'volumes/\1/\3/data',
                                                                                    r'volumes/\1/\3/extras']),
    (r'.*/(COISS_[12]xxx)(|_.*?)/(COISS_....)$',                                0,  r'volumes/\1/\3'),
    (r'metadata/(COISS_.xxx/COISS_....)/COISS_...._index\..*',                  0, [r'volumes/\1/INDEX/INDEX.TAB',
                                                                                    r'volumes/\1/INDEX/INDEX.LBL']),
    (r'metadata/COISS_1xxx/COISS_1999/COISS_...._index\..*',                    0, [r'volumes/COISS_1xxx/COISS_1009/INDEX/CUMINDEX.TAB',
                                                                                    r'volumes/COISS_1xxx/COISS_1009/INDEX/CUMINDEX.LBL']),
    (r'metadata/COISS_2xxx/COISS_2999/COISS_...._index\..*',                    0, [r'volumes/COISS_2xxx/COISS_2116/INDEX/CUMINDEX.TAB',
                                                                                    r'volumes/COISS_2xxx/COISS_2116/INDEX/CUMINDEX.LBL']),

    (r'.*/(COISS_3xxx.*)/(COISS_30..)/.*/images/(SM_[^\.]+)\..*',               0, [r'volumes/\1/\2/data/images/\3.IMG',
                                                                                    r'volumes/\1/\2/data/full/images/\3.IMG.png',
                                                                                    r'volumes/\1/\2/extras/browse/images/\3.IMG.jpeg',
                                                                                    r'volumes/\1/\2/extras/full/images/\3.IMG.png',
                                                                                    r'volumes/\1/\2/img_index.tab/\3']),

    (r'.*/(COISS_3xxx.*)/(COISS_30..)/.*/maps/(SM_[^\.]+)\..*',                 0, [r'volumes/\1/\2/data/maps/\3.PDF',
                                                                                    r'volumes/\1/\2/data/maps/\3.lbl',
                                                                                    r'volumes/\1/\2/data/full/maps/\3.PDF.png',
                                                                                    r'volumes/\1/\2/extras/browse/maps/\3.PDF.jpeg',
                                                                                    r'volumes/\1/\2/extras/full/maps/\3.PDF.png',
                                                                                    r'volumes/\1/\2/img_index.tab/\3']),

    (r'.*/(COISS_3xxx.*)/(COISS_30..)/.*/images$',                              0, [r'volumes/\1/\2/data/images',
                                                                                    r'volumes/\1/\2/extras/browse/images',
                                                                                    r'volumes/\1/\2/extras/full/images']),

    (r'.*/(COISS_3xxx.*)/(COISS_30..)/.*/maps$',                                0, [r'volumes/\1/\2/data/maps',
                                                                                    r'volumes/\1/\2/extras/browse/maps',
                                                                                    r'volumes/\1/\2/extras/full/maps']),
])

associations_to_calibrated = translator.TranslatorByRegex([
    (r'.*/(COISS_[12]xxx)(|_.*?)/(COISS_....)/(data|extras/\w+)/(\w+/[NW][0-9]{10}_[0-9]+).*',
                                                                                0, [r'calibrated/\1/\3/data/\5_CALIB.IMG',
                                                                                    r'calibrated/\1/\3/data/\5_CALIB.LBL']),
    (r'.*/(COISS_[12]xxx)(|_.*?)/(COISS_....)/(data|extras/\w+)(\w+)$',         0,  r'calibrated/\1/\3/data/\5'),
    (r'.*/(COISS_[12]xxx)(|_.*?)/(COISS_....)/(data|extras|extras/\w+)$',       0,  r'calibrated/\1/\3/data'),
    (r'.*/(COISS_[12]xxx)(|_.*?)/(COISS_....)$',                                0,  r'calibrated/\1/\3'),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'.*/(COISS_[12]xxx)(|_.*?)/(COISS_....)/(data|extras/\w+)/(\w+/[NW][0-9]{10}_[0-9]+).*',
                                                                                0, [r'previews/\1/\3/data/\5_full.png',
                                                                                    r'previews/\1/\3/data/\5_med.jpg',
                                                                                    r'previews/\1/\3/data/\5_small.jpg',
                                                                                    r'previews/\1/\3/data/\5_thumb.jpg']),
    (r'.*/(COISS_[12]xxx)(|_.*?)/(COISS_....)/(data|extras/\w+)/(\w+)$',        0,  r'previews/\1/\3/data/\5'),
    (r'.*/(COISS_[12]xxx)(|_.*?)/(COISS_....)/(data|extras|extras/\w+)$',       0,  r'previews/\1/\3/data'),
    (r'.*/(COISS_[12]xxx)(|_.*?)/(COISS_....)$',                                0,  r'previews/\1/\3'),

    (r'.*/(COISS_3xxx.*)/(COISS_30..)/.*/images/(SM_[^\.]+)\..*',               0, [r'previews/\1/\2/data/images/\3_full.png',
                                                                                    r'previews/\1/\2/data/images/\3_thumb.jpg',
                                                                                    r'previews/\1/\2/data/images/\3_small.jpg',
                                                                                    r'previews/\1/\2/data/images/\3_med.jpg']),

    (r'.*/(COISS_3xxx.*)/(COISS_30..)/.*/maps/(SM_[^\.]+)\..*',                 0, [r'previews/\1/\2/data/maps/\3_full.png',
                                                                                    r'previews/\1/\2/data/maps/\3_thumb.png',
                                                                                    r'previews/\1/\2/data/maps/\3_small.png',
                                                                                    r'previews/\1/\2/data/maps/\3_med.png']),

    (r'.*/(COISS_3xxx.*)/(COISS_30..)/.*/images$',                              0,  r'previews/\1/\2/data/images'),

    (r'.*/(COISS_3xxx.*)/(COISS_30..)/.*/maps$',                                0,  r'previews/\1/\2/data/maps'),

    (r'.*/(COISS_3xxx.*)/(COISS_30..)/.*/browse$',                                0,  r'previews/\1/\2/data'),
])

associations_to_metadata = translator.TranslatorByRegex([
    (r'.*/(COISS_[12]xxx)(|_.*?)/(COISS_....)/(data|extras/w+)/\w+/([NW][0-9]{10}_[0-9]+).*',
                                                                                0, [r'metadata/\1/\3/\3_index.tab/\5',
                                                                                    r'metadata/\1/\3/\3_ring_summary.tab/\5',
                                                                                    r'metadata/\1/\3/\3_moon_summary.tab/\5',
                                                                                    r'metadata/\1/\3/\3_saturn_summary.tab/\5',
                                                                                    r'metadata/\1/\3/\3_jupiter_summary.tab/\5',
                                                                                    r'metadata/\1/\3/']),
    (r'.*/(COISS_[12]xxx)(|_.*?)/(COISS_....)/(|data|extras|extras/\w+)(|/\w+)$',
                                                                                0,  r'metadata/\1/\3'),
    (r'.*/(COISS_[12]xxx)/(COISS_....)/index/index\..*',                        0, [r'metadata/\1/\2/\2_index.tab',
                                                                                    r'metadata/\1/\2/\2_index.lbl']),
    (r'.*/(COISS_1xxx)/(COISS_1...)/index/cumindex\..*',                        0, [r'metadata/\1/COISS_1999/COISS_1999_index.tab',
                                                                                    r'metadata/\1/COISS_1999/COISS_1999_index.lbl']),
    (r'.*/(COISS_2xxx)/(COISS_2...)/index/cumindex\..*',                        0, [r'metadata/\1/COISS_2999/COISS_2999_index.tab',
                                                                                    r'metadata/\1/COISS_2999/COISS_2999_index.lbl']),
    (r'metadata/(COISS_1xxx)/(COISS_....)/(COISS_....)_(\w+)\..*',              0, [r'metadata/\1/COISS_1999/COISS_1999_\4.tab',
                                                                                    r'metadata/\1/COISS_1999/COISS_1999_\4.lbl']),
    (r'metadata/(COISS_2xxx)/(COISS_....)/(COISS_....)_(\w+)\..*',              0, [r'metadata/\1/COISS_2999/COISS_2999_\4.tab',
                                                                                    r'metadata/\1/COISS_2999/COISS_2999_\4.lbl']),
    (r'metadata/(COISS_1xxx)/(COISS_....)$',                                    0,  r'metadata/\1/COISS_1999'),
    (r'metadata/(COISS_2xxx)/(COISS_....)$',                                    0,  r'metadata/\1/COISS_2999'),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews|calibrated)/COISS_[12]xxx(|_.*)/COISS_..../data(|/\w+)',       0, (True, True, True )),
    (r'(volumes|previews|calibrated)/COISS_[12]xxx(|_.*)/COISS_..../extras/\w+(|/\w+)', 0, (True, True, True )),
    (r'volumes/COISS_3xxx(|_.*)/COISS_..../data/(images|maps)',                         0, (True, True, False)),
    (r'volumes/COISS_3xxx(|_.*)/COISS_..../extras/\w+/images',                          0, (True, True, False)),
    (r'previews/COISS_3xxx(|_.*)/COISS_..../data/(images|maps)',                        0, (True, True, False)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'volumes/COISS_0xxx(|_\w+)/COISS_..../data',               0, r'volumes/COISS_0xxx\1/*/data'),
    (r'volumes/COISS_0xxx(|_\w+)/COISS_..../data/(\w+)',         0, r'volumes/COISS_0xxx\1/*/data/\2'),
    (r'volumes/COISS_0xxx(|_\w+)/COISS_..../data/(\w+/\w+)',     0, r'volumes/COISS_0xxx\1/*/data/\2'),
    (r'volumes/COISS_0xxx(|_\w+)/COISS_..../data/(\w+/\w+)/\w+', 0, r'volumes/COISS_0xxx\1/*/data/\2/*'),

    (r'(volumes|previews)/COISS_3xxx(|_\w+)/COISS_..../data',               0, r'\1/COISS_3xxx\2/*/data'),
    (r'(volumes|previews)/COISS_3xxx(|_\w+)/COISS_..../data/(\w+)',         0, r'\1/COISS_3xxx\2/*/data/\3'),
    (r'(volumes|previews)/COISS_3xxx(|_\w+)/COISS_..../extras',             0, r'\1/COISS_3xxx\2/*/extras'),
    (r'(volumes|previews)/COISS_3xxx(|_\w+)/COISS_..../extras/(\w+)',       0, r'\1/COISS_3xxx\2/*/extras/\3'),
    (r'(volumes|previews)/COISS_3xxx(|_\w+)/COISS_..../extras/(\w+)/\w+',   0, r'\1/COISS_3xxx\2/*/extras/\3/*'),

    (r'(volumes|previews|calibrated)/(COISS_[12]...)(|_.*?)/COISS_..../data',     0, r'\1/\2\3/*/data'),
    (r'(volumes|previews|calibrated)/(COISS_[12]...)(|_.*?)/COISS_..../data/\w+', 0, r'\1/\2\3/*/data/*'),

    (r'volumes/(COISS_[12]xxx)/COISS_..../extras/(\w+)/\w+',     0, r'volumes/\1/*/extras/\2/*'),
    (r'volumes/(COISS_[12]xxx)/COISS_..../extras/(\w+)',         0, r'volumes/\1/*/extras/\2'),
    (r'volumes/(COISS_[12]xxx)/COISS_..../(\w+)',                0, r'volumes/\1/*/\2'),

    (r'metadata/(COISS_[12]xxx)/(COISS_....)/(COISS_....)(_.*)', 0, r'metadata/\1/*/*\4'),
])

####################################################################################################################################
# SORT_KEY
####################################################################################################################################

sort_key = translator.TranslatorByRegex([

    # Skips over N or W, placing files into chronological order
    (r'([NW])([0-9]{10})(.*)_full.png', 0, r'\2\1\3_1full.jpg'),
    (r'([NW])([0-9]{10})(.*)_med.jpg', 0, r'\2\1\3_2med.jpg'),
    (r'([NW])([0-9]{10})(.*)_small.jpg', 0, r'\2\1\3_3small.jpg'),
    (r'([NW])([0-9]{10})(.*)_thumb.jpg', 0, r'\2\1\3_4thumb.jpg'),
    (r'([NW])([0-9]{10})(.*)', 0, r'\2\1\3'),
])

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/.*\.(IMG|LBL)$',                      0, ('Cassini ISS',   0, 'coiss_raw',    'Raw image')),
    (r'calibrated/.*_CALIB\.(IMG|LBL)$',             0, ('Cassini ISS',  10, 'coiss_calib',  'Calibrated image')),
    (r'volumes/.*/extras/thumbnail/.*\.jpeg_small$', 0, ('Cassini ISS', 110, 'coiss_thumb',  'Extra preview (thumbnail)')),
    (r'volumes/.*/extras/browse/.*\.jpeg$',          0, ('Cassini ISS', 120, 'coiss_medium', 'Extra preview (medium)')),
    (r'volumes/.*/extras/(tiff|full)/.*\.\w+$',      0, ('Cassini ISS', 130, 'coiss_full',   'Extra preview (full)')),
])

####################################################################################################################################
# OPUS_FORMAT
####################################################################################################################################

opus_format = translator.TranslatorByRegex([
    (r'.*\.IMG$',        0, ('Binary', 'VICAR')),
    (r'.*\.jpeg_small$', 0, ('Binary', 'JPEG')),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

opus_products = translator.TranslatorByRegex([
    (r'.*volumes/(COISS_[12]xxx)/(COISS_[12]...)/data/(\w+/[NW][0-9]{10})_[0-9]+\.(IMG|LBL)', 0,
                                                                    [r'volumes/\1/\2/data/\3_*.IMG',
                                                                     r'volumes/\1/\2/data/\3_*.LBL',
                                                                     r'volumes/\1/\2/extras/thumbnail/\3_*.IMG.jpeg_small',
                                                                     r'volumes/\1/\2/extras/browse/\3_*.IMG.jpeg',
                                                                     r'volumes/\1/\2/extras/full/\3_*.IMG.png',
                                                                     r'volumes/\1/\2/extras/tiff/\3_*.IMG.tiff',
                                                                     r'calibrated/\1/\2/data/\3_*_CALIB.IMG',
                                                                     r'calibrated/\1_v*/\2/data/\3_*_CALIB.IMG',
                                                                     r'calibrated/\1/\2/data/\3_*_CALIB.LBL',
                                                                     r'calibrated/\1_v*/\2/data/\3_*_CALIB.LBL',
                                                                     r'previews/\1/\2/data/\3_*_thumb.jpg',
                                                                     r'previews/\1/\2/data/\3_*_small.jpg',
                                                                     r'previews/\1/\2/data/\3_*_med.jpg',
                                                                     r'previews/\1/\2/data/\3_*_full.png',
                                                                     r'metadata/\1/\2/\2_jupiter_summary.lbl',
                                                                     r'metadata/\1/\2/\2_jupiter_summary.tab',
                                                                     r'metadata/\1/\2/\2_saturn_summary.lbl',
                                                                     r'metadata/\1/\2/\2_saturn_summary.tab',
                                                                     r'metadata/\1/\2/\2_moon_summary.lbl',
                                                                     r'metadata/\1/\2/\2_moon_summary.tab',
                                                                     r'metadata/\1/\2/\2_ring_summary.lbl',
                                                                     r'metadata/\1/\2/\2_ring_summary.tab',
                                                                     r'metadata/\1/\2/\2_inventory.lbl',
                                                                     r'metadata/\1/\2/\2_inventory.tab']),
])

####################################################################################################################################
# FILESPEC_TO_OPUS_ID
####################################################################################################################################

# filespec_to_opus_id = translator.TranslatorByRegex([
#     (r'COISS_100[0-4]/.*/([NW][0-9]{10})_[0-9]+\..+$',      0, r'cassini.iss.jupiter_cruise..\1'),
#     (r'COISS_1005/.*/([NW]1357[0-9]{6})_[0-9]+\..+$',       0, r'cassini.iss.jupiter_cruise..\1'),
#     (r'COISS_1005/.*/([NW]1358[0-1][0-9]{5})_[0-9]+\..+$',  0, r'cassini.iss.jupiter_cruise..\1'),
#     (r'COISS_1005/.*/([NW]1358[2-9][0-9]{5})_[0-9]+\..+$',  0, r'cassini.iss.jupiter..\1'),
#     (r'COISS_1005/.*/([NW]1359[0-9]{6})_[0-9]+\..+$',       0, r'cassini.iss.jupiter..\1'),
#     (r'COISS_1006/.*/([NW]1359[0-9]{6})_[0-9]+\..+$',       0, r'cassini.iss.jupiter..\1'),
#     (r'COISS_1006/.*/([NW]136[0-2][0-9]{6})_[0-9]+\..+$',   0, r'cassini.iss.jupiter..\1'),
#     (r'COISS_1006/.*/([NW]13630[0-7][0-9]{4})_[0-9]+\..+$', 0, r'cassini.iss.jupiter..\1'),
#     (r'COISS_1006/.*/([NW]13630[8-9][0-9]{4})_[0-9]+\..+$', 0, r'cassini.iss.saturn_cruise..\1'),
#     (r'COISS_1006/.*/([NW]1363[1-9][0-9]{5})_[0-9]+\..+$',  0, r'cassini.iss.saturn_cruise..\1'),
#     (r'COISS_100[7-9]/.*/([NW][0-9]{10})_[0-9]+\..+$',      0, r'cassini.iss.saturn_cruise..\1'),
#     (r'COISS_2.../.*/([NW][0-9]{10})_[0-9]+\..+$',          0, r'cassini.iss.saturn..\1'),
# ])

filespec_to_opus_id = translator.TranslatorByRegex([
    (r'COISS_[12][10]../(data|extras)/.*/([NW][0-9]{10})_[0-9]+\..+$', 0, r'co-iss-\2'),
])

####################################################################################################################################
# OPUS_ID_TO_FILESPEC
####################################################################################################################################

opus_id_to_filespec = translator.TranslatorByRegex([
    (r'co-iss-[nw][0-9]{10}', 0, re.compile(r'.*_[0-9]+\.IMG$')),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class COISS_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('COISS_[0123]xxx', re.I, 'COISS_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS
    SORT_KEY = sort_key + pdsfile.PdsFile.SORT_KEY

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_FORMAT = opus_format + pdsfile.PdsFile.OPUS_FORMAT
    OPUS_PRODUCTS = opus_products
    FILESPEC_TO_OPUS_ID = filespec_to_opus_id

    VIEWABLES = {'default': default_viewables}

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']    = associations_to_volumes
    ASSOCIATIONS['calibrated'] = associations_to_calibrated
    ASSOCIATIONS['previews']   = associations_to_previews
    ASSOCIATIONS['metadata']   = associations_to_metadata

    def FILENAME_KEYLEN(self):
        if self.volset[:10] == 'COISS_3xxx':
            return 0
        else:
            return 11   # trim off suffixes

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_FILESPEC = opus_id_to_filespec + pdsfile.PdsFile.OPUS_ID_TO_FILESPEC

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COISS_xxxx'] = COISS_xxxx

####################################################################################################################################
