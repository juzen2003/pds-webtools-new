####################################################################################################################################
# rules/NHxxxx_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# Special procedure to define and prioritize OPUS_TYPES
####################################################################################################################################

# Define the priority among file types
FILE_CODE_PRIORITY = {

    # LORRI codes
    '630': 0,  #- LORRI High-res Lossless (CDH 1)/LOR
    '631': 2,  #- LORRI High-res Packetized (CDH 1)/LOR
    '632': 4,  #- LORRI High-res Lossy (CDH 1)/LOR
    '633': 6,  #- LORRI 4x4 Binned Lossless (CDH 1)/LOR
    '634': 8,  #- LORRI 4x4 Binned Packetized (CDH 1)/LOR
    '635': 10, #- LORRI 4x4 Binned Lossy (CDH 1)/LOR
    '636': 1,  #- LORRI High-res Lossless (CDH 2)/LOR
    '637': 3,  #- LORRI High-res Packetized (CDH 2)/LOR
    '638': 5,  #- LORRI High-res Lossy (CDH 2)/LOR
    '639': 7,  #- LORRI 4x4 Binned Lossless (CDH 2)/LOR
    '63A': 9,  #- LORRI 4x4 Binned Packetized (CDH 2)/LOR
    '63B': 11, #- LORRI 4x4 Binned Lossy (CDH 2)/LOR

    # MVIC codes
    '530': 12, #- MVIC Panchromatic TDI Lossless (CDH 1)/MP1,MP2
    '531': 18, #- MVIC Panchromatic TDI Packetized (CDH 1)/MP1,MP2
    '532': 24, #- MVIC Panchromatic TDI Lossy (CDH 1)/MP1,MP2

    '533': 30, #- MVIC Panchromatic TDI 3x3 Binned Lossless (CDH 1)/MP1,MP2
    '534': 32, #- MVIC Panchromatic TDI 3x3 Binned Packetized (CDH 1)/MP1,MP2
    '535': 34, #- MVIC Panchromatic TDI 3x3 Binned Lossy (CDH 1)/MP1,MP2

    '536': 13, #- MVIC Color TDI Lossless (CDH 1)/MC0,MC1,MC2,MC3
    '537': 19, #- MVIC Color TDI Packetized (CDH 1)/MC0,MC1,MC2,MC3
    '538': 25, #- MVIC Color TDI Lossy (CDH 1)/MC0,MC1,MC2,MC3

    '539': 14, #- MVIC Panchromatic Frame Transfer Lossless (CDH 1)/MPF
    '53A': 20, #- MVIC Panchromatic Frame Transfer Packetized (CDH 1)/MPF
    '53B': 26, #- MVIC Panchromatic Frame Transfer Lossy (CDH 1)/MPF

    '53F': 15, #- MVIC Panchromatic TDI Lossless (CDH 2)/MP1,MP2
    '540': 21, #- MVIC Panchromatic TDI Packetized (CDH 2)/MP1,MP2
    '541': 27, #- MVIC Panchromatic TDI Lossy (CDH 2)/MP1,MP2

    '542': 31, #- MVIC Panchromatic TDI 3x3 Binned Lossless (CDH 2)/MP1,MP2
    '543': 33, #- MVIC Panchromatic TDI 3x3 Binned Packetized (CDH 2)/MP1,MP2
    '544': 35, #- MVIC Panchromatic TDI 3x3 Binned Lossy (CDH 2)/MP1,MP2

    '545': 16, #- MVIC Color TDI Lossless (CDH 2)/MC0,MC1,MC2,MC3
    '546': 22, #- MVIC Color TDI Packetized (CDH 2)/MC0,MC1,MC2,MC3
    '547': 28, #- MVIC Color TDI Lossy (CDH 2)/MC0,MC1,MC2,MC3

    '548': 17, #- MVIC Panchromatic Frame Transfer Lossless (CDH 2)/MPF
    '549': 23, #- MVIC Panchromatic Frame Transfer Packetized (CDH 2)/MPF
    '54A': 29, #- MVIC Panchromatic Frame Transfer Lossy (CDH 2)/MPF
}

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/\w+/......_1.../data(|/[0-9_]+)', re.I, ('Raw images grouped by date',              'IMAGEDIR')),
    (r'volumes/\w+/......_2.../data(|/[0-9_]+)', re.I, ('Calibrated images grouped by date',       'IMAGEDIR')),
    (r'volumes/.*_eng(|_[0-9]+)\.fit',           re.I, ('Raw image, FITS',                         'IMAGE'   )),
    (r'volumes/.*_sci(|_[0-9]+)\.fit',           re.I, ('Calibrated image, FITS',                  'IMAGE'   )),
    (r'.*/catalog/NH.CAT',                       re.I, ('Mission description',                     'INFO'    )),
    (r'.*/catalog/NHSC.CAT',                     re.I, ('Spacecraft description',                  'INFO'    )),
    (r'.*/catalog/(LORRI|MVIC)\.CAT',            re.I, ('Instrument description',                  'INFO'    )),
    (r'.*/catalog/.*RELEASE\.CAT',               re.I, ('Release information',                     'INFO'    )),
    (r'.*/catalog/132524_apl\.cat',              re.I, ('Target information',                      'INFO'    )),
    (r'volumes/.*/data(|\w+)',                   re.I, ('Data files organized by date',            'IMAGEDIR')),
    (r'.*/NH...._1...\.tar\.gz',                 0,    ('Downloadable archive of raw data',        'TARBALL' )),
    (r'.*/NH...._2...\.tar\.gz',                 0,    ('Downloadable archive of calibrated data', 'TARBALL' )),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews)/NHxxLO_..../NH..LO_..../data(|/\w+)', re.I, (True, True, True)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'(volumes|previews)/(NHxx.._xxxx.*/NH)..(.._[12])...',            0,    r'\1/\2??\3*'),
    (r'(volumes|previews)/(NHxx.._xxxx.*/NH)..(.._[12]).../data',       re.I, (r'\1/\2??\3*/data',   r'\1/\2??\3*/DATA'  )),
    (r'(volumes|previews)/(NHxx.._xxxx.*/NH)..(.._[12]).../data/(\w+)', re.I, (r'\1/\2??\3*/data/*', r'\1/\2??\3*/DATA/*')),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl',  re.I, ''),

    (r'.*/(NHxx.._xxxx)(_v1)/(NH.*)/data/\w+/(\w{3}_[0-9]{10}).*',    0, r'previews/\1/\3/data/*/\4*'),
    (r'.*/(NHxx.._xxxx)(_v2)/(NH.*)/data/\w+/(\w{3}_[0-9]{10}).*',    0, r'previews/\1/\3/data/*/\4*'),
    (r'.*/(NHxx.._xxxx)(_v1)/(NH.*)/DATA/\w+/MC([0-9]_[0-9]{10}).*',  0, r'previews/\1/\3/data/*/mc\4_*'),
    (r'.*/(NHxx.._xxxx)(_v1)/(NH.*)/DATA/\w+/MP([0-9]_[0-9]{10}).*',  0, r'previews/\1/\3/data/*/mp\4_*'),
    (r'.*/(NHxx.._xxxx)(_v1)/(NH.*)/DATA/\w+/MPF([0-9]_[0-9]{10}).*', 0, r'previews/\1/\3/data/*/mpf\4_*'),

    (r'.*/(NHxx.._xxxx)(|_.*)/(NH.*/data/\w+/\w{3}_[0-9]{10}).*',     0, r'previews/\1/\3_*'),
    (r'.*/(NHxx.._xxxx)(|_.*)/(NH.*/data/\w+/\w{3}_[0-9]{10}).*',     0, r'previews/\1/\3_*'),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'.*/(NHxx.._xxxx)(|_v[2-9])/(NH....)_[12](...)/data/(\w+)/([a-z0-9]+_[0-9]{10}).*',
                                                                    0,    [r'volumes/\1\2/\3_1\4/data/\5/\6*',
                                                                           r'volumes/\1\2/\3_2\4/data/\5/\6*']),
    (r'.*/(NHxx.._xxxx)(|_v[2-9])/(NH....)_[12](...)/data/(\w+)$',  0,    [r'volumes/\1\2/\3_1\4/data/\5',
                                                                           r'volumes/\1\2/\3_2\4/data/\5']),
    (r'.*/(NHxx.._xxxx)(|_v[2-9])/(NH....)_[12](...)/data$',        0,    [r'volumes/\1\2/\3_1\4/data',
                                                                           r'volumes/\1\2/\3_2\4/data']),

    # Special rules to deal with one uppercase volume, NHJUMV_1001
    (r'.*/(NHxxMV_xxxx_v1/NHJUMV)_[12](001)/DATA/(\w+)/mc([0-9]_[0-9]{10}).*',
                                                                    re.I, [r'volumes/\1_1\2/DATA/\3/MC\4*',
                                                                           r'volumes/\1_2\2/data/\3/mc\4*']),
    (r'.*/(NHxxMV_xxxx_v1/NHJUMV)_[12](001)/DATA/(\w+)/mp([0-9]_[0-9]{10}).*',
                                                                    re.I, [r'volumes/\1_1\2/DATA/\3/MP\4*',
                                                                           r'volumes/\1_2\2/data/\3/mp\4*']),
    (r'.*/(NHxxMV_xxxx_v1/NHJUMV)_[12](001)/DATA/(\w+)/mpf(_[0-9]{10}).*',
                                                                    re.I, [r'volumes/\1_1\2/DATA/\3/MPF\4*',
                                                                           r'volumes/\1_2\2/data/\3/mpf\4*']),
    (r'.*/(NHxxMV_xxxx_v1/NHJUMV)_[12](001)/DATA/(\w+)$',           re.I, [r'volumes/\1_1\2/DATA/\3',
                                                                           r'volumes/\1_2\2/data/\3']),
    (r'.*/(NHxxMV_xxxx_v1/NHJUMV)_[12](001)/DATA$',                 re.I, [r'volumes/\1_1\2/DATA',
                                                                           r'volumes/\1_2\2/data']),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'.*/(NHxx.._xxxx)(|_v[2-9])/(NH....)_[12](.../data/\w+)/([a-z0-9]+_[0-9]{10}).*',
                                                                    0,    [r'previews/\1/\3_1\4/\5*',
                                                                           r'previews/\1/\3_2\4/\5*']),
    # Special rules to deal with one uppercase volume, NHJUMV_1001
    (r'.*/NHxxMV_xxxx_v1/NHJUMV_[12]001/DATA/(\w+)/MC([0-9]_[0-9]{10}).*',
                                                                    re.I, [r'previews/NHxxMV_xxxx/NHJUMV_1001/data/\1/mc\2*',
                                                                           r'previews/NHxxMV_xxxx/NHJUMV_2001/data/\1/mc\2*']),
    (r'.*/NHxxMV_xxxx_v1/NHJUMV_[12]001/DATA/(\w+)/MP([0-9]_[0-9]{10}).*',
                                                                    re.I, [r'previews/NHxxMV_xxxx/NHJUMV_1001/data/\1/mp\2*',
                                                                           r'previews/NHxxMV_xxxx/NHJUMV_2001/data/\1/mp\2*']),
    (r'.*/NHxxMV_xxxx_v1/NHJUMV_[12]001/DATA/(\w+)/MPF(_[0-9]{10}).*',
                                                                    re.I, [r'previews/NHxxMV_xxxx/NHJUMV_1001/data/\1/mpf\2*',
                                                                           r'previews/NHxxMV_xxxx/NHJUMV_2001/data/\1/mpf\2*']),

    (r'.*/(NHxx.._xxxx)(|_.*)/(NH....)_[12](.../data/\w+)$',        re.I, [r'previews/\1/\3_1\4',
                                                                           r'previews/\1/\3_2\4']),
    (r'.*/(NHxx.._xxxx)(|_.*)/(NH....)_[12](.../data)$',            re.I, [r'previews/\1/\3_1\4',
                                                                           r'previews/\1/\3_2\4']),
])

associations_to_metadata = translator.TranslatorByRegex([
    (r'.*/(NHxx.._xxxx)(|_.*)/(NH...._....)/data/\w+/([a-z0-9]+_[0-9]{10}).*',
                                                                    re.I, [r'metadata/\1/\3/\3_index.tab/\4',
                                                                           r'metadata/\1/\3/\3_supplemental_index.tab/\4',
                                                                           r'metadata/\1/\3/\3_moon_summary.tab/\4',
                                                                           r'metadata/\1/\3/\3_ring_summary.tab/\4',
                                                                           r'metadata/\1/\3/\3_charon_summary.tab/\4',
                                                                           r'metadata/\1/\3/\3_pluto_summary.tab/\4',
                                                                           r'metadata/\1/\3/\3_jupiter_summary.tab/\4',
                                                                           r'metadata/\1/\3']),
    (r'.*/(NHxx.._xxxx)(|_.*)/(NH...._....)/data/(|\w+)$',          re.I,  r'metadata/\1/\3'),
])

####################################################################################################################################
# SORT_KEY
####################################################################################################################################

sort_key = translator.TranslatorByRegex([

    # Order volumes by LA, JU, PC, PE
    (r'NHLA(.._[0-9]{4}.*)', 0, r'NH1LA\1'),
    (r'NHJU(.._[0-9]{4}.*)', 0, r'NH2JU\1'),
    (r'NHPC(.._[0-9]{4}.*)', 0, r'NH3PC\1'),
    (r'NHPE(.._[0-9]{4}.*)', 0, r'NH4PE\1'),
    (r'(\w{3})_([0-9]{10})(.*)', re.I, r'\2\1\3'),
])

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([

    # Hide calibrated previews because the raw previews are fine
    (r'previews/NHxx.._xxxx(|_v.+)/NH...._2xxx/.*$', 0, ''),

    (r'volumes/NHxx.._xxxx(|_v.+)/NH...._1.../data/.*_eng(|_[1-9])\.(fit|lbl)$', re.I,
                                            ('New Horizons',   0, 'nh_raw',   'Raw Image')),
    (r'volumes/NHxx.._xxxx(|_v.+)/NH...._2.../data/.*_sci(|_[1-9])\.(fit|lbl)$', re.I,
                                            ('New Horizons', 100, 'nh_calib', 'Calibrated Image'))
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

# NOTE: Entries supporting versions are commented out; nncomment when OPUS is ready to support version numbers in shopping carts

opus_products = translator.TranslatorByRegex([
    (r'.*volumes/(NH..LO_xxxx)(?:|_v.+)/(NH..LO)_[12](...)/(.*)_0x..._(eng|sci)(|_[1-9][0-9]*)\.(fit|lbl)', 0,
                                                                [r'volumes/\1/\2_1\3/\4_0x???_eng*.[fl][ib][tl]',
                                                                 r'volumes/\1_v*/\2_1\3/\4_0x???_eng*.[fl][ib][tl]',
                                                                 r'volumes/\1/\2_2\3/\4_0x???_sci*.[fl][ib][tl]',
                                                                 r'volumes/\1_v*/\2_2\3/\4_0x???_sci*.[fl][ib][tl]',
                                                                 r'previews/\1/\2_1\3/\4_0x???_eng*_thumb.jpg',
                                                                 r'previews/\1/\2_1\3/\4_0x???_eng*_small.jpg',
                                                                 r'previews/\1/\2_1\3/\4_0x???_eng*_med.jpg',
                                                                 r'previews/\1/\2_1\3/\4_0x???_eng*_full.jpg',
                                                                 r'metadata/\1/\2_1\3/\2_1\3_jupiter_summary.lbl',
                                                                 r'metadata/\1/\2_1\3/\2_1\3_jupiter_summary.tab',
                                                                 r'metadata/\1/\2_1\3/\2_1\3_pluto_summary.lbl',
                                                                 r'metadata/\1/\2_1\3/\2_1\3_pluto_summary.tab',
                                                                 r'metadata/\1/\2_1\3/\2_1\3_charon_summary.lbl',
                                                                 r'metadata/\1/\2_1\3/\2_1\3_charon_summary.tab',
                                                                 r'metadata/\1/\2_1\3/\2_1\3_moon_summary.lbl',
                                                                 r'metadata/\1/\2_1\3/\2_1\3_moon_summary.tab',
                                                                 r'metadata/\1/\2_1\3/\2_1\3_ring_summary.lbl',
                                                                 r'metadata/\1/\2_1\3/\2_1\3_ring_summary.tab',
                                                                 r'metadata/\1/\2_1\3/\2_1\3_inventory.lbl',
                                                                 r'metadata/\1/\2_1\3/\2_1\3_inventory.tab']),

    # These two entries are necessary because NHxxMV_xxxx_v1/NHJUMV_1001 uses uppercase file names
    (r'.*volumes/(NH..MV_xxxx)(?:|_v.+)/(NH..MV)_[12](...)/data/(.*)/mc(.*)_0x..._(eng|sci)(|_[1-9][0-9]*)\.(fit|lbl)', 0,
                                                                [r'volumes/\1/\2_1\3/data/\4/mc\5_0x???_eng*.[fl][ib][tl]',
                                                                 r'volumes/\1_v1/\2_1\3/DATA/\4/MC\5_0X???_ENG*.[FL][IB][TL]',
                                                                 r'volumes/\1_v*/\2_1\3/data/\4/mc\5_0x???_eng*.[fl][ib][tl]',
                                                                 r'volumes/\1/\2_2\3/data/\4/mc\5_0x???_sci*.[fl][ib][tl]',
                                                                 r'volumes/\1_v*/\2_2\3/data/\4/mc\5_0x???_sci*.[fl][ib][tl]',
                                                                 r'previews/\1/\2_1\3/data/\4/mc\5_0x???_eng*_thumb.jpg',
                                                                 r'previews/\1/\2_1\3/data/\4/mc\5_0x???_eng*_small.jpg',
                                                                 r'previews/\1/\2_1\3/data/\4/mc\5_0x???_eng*_med.jpg',
                                                                 r'previews/\1/\2_1\3/data/\4/mc\5_0x???_eng*_full.jpg']),

    (r'.*volumes/(NH..MV_xxxx)(?:|_v.+)/(NH..MV)_[12](...)/data/(.*)/mpf(.*)_0x..._(eng|sci)(|_[1-9][0-9]*)\.(fit|lbl)', 0,
                                                                [r'volumes/\1/\2_1\3/data/\4/mpf\5_0x???_eng*.[fl][ib][tl]',
                                                                 r'volumes/\1_v1/\2_1\3/DATA/\4/MPF\5_0X???_ENG*.[FL][IB][TL]',
                                                                 r'volumes/\1_v*/\2_1\3/data/\4/mpf\5_0x???_eng*.[fl][ib][tl]',
                                                                 r'volumes/\1/\2_2\3/data/\4/mpf\5_0x???_sci*.[fl][ib][tl]',
                                                                 r'volumes/\1_v*/\2_2\3/data/\4/mpf\5_0x???_sci*.[fl][ib][tl]',
                                                                 r'previews/\1/\2_1\3/data/\4/mpf\5_0x???_eng*_thumb.jpg',
                                                                 r'previews/\1/\2_1\3/data/\4/mpf\5_0x???_eng*_small.jpg',
                                                                 r'previews/\1/\2_1\3/data/\4/mpf\5_0x???_eng*_med.jpg',
                                                                 r'previews/\1/\2_1\3/data/\4/mpf\5_0x???_eng*_full.jpg']),

    (r'.*volumes/(NH..MV_xxxx)(?:|_v.+)/(NH..MV)_[12](...)/(.*)_0x..._(eng|sci)(|_[1-9][0-9]*)\.(fit|lbl)', 0,
                                                                [r'volumes/\1/\2_1\3/\4_0x???_eng*.[fl][ib][tl]',
                                                                 r'volumes/\1_v*/\2_1\3/\4_0x???_eng*.[fl][ib][tl]',
                                                                 r'volumes/\1/\2_2\3/\4_0x???_sci*.[fl][ib][tl]',
                                                                 r'volumes/\1_v*/\2_2\3/\4_0x???_sci*.[fl][ib][tl]',
                                                                 r'previews/\1/\2_1\3/\4_0x???_eng*_thumb.jpg',
                                                                 r'previews/\1/\2_1\3/\4_0x???_eng*_small.jpg',
                                                                 r'previews/\1/\2_1\3/\4_0x???_eng*_med.jpg',
                                                                 r'previews/\1/\2_1\3/\4_0x???_eng*_full.jpg']),
])

####################################################################################################################################
# FILESPEC_TO_OPUS_ID
####################################################################################################################################

# filespec_to_opus_id = translator.TranslatorByRegex([
#     # Raw and calibrated NH volumes (series *_1001 and *_2001) share common OPUS IDs.
#     (r'NHJULO_[12].*/data/\w+/(lor_[0-9]{10})_.*$', re.I, r'new_horizons.lorri.jupiter..\1'),
#     (r'NHPELO_[12].*/data/\w+/(lor_[0-9]{10})_.*$', 0,    r'new_horizons.lorri.pluto..\1'),
#     (r'NHPCLO_[12].*/data/\w+/(lor_[0-9]{10})_.*$', 0,    r'new_horizons.lorri.pluto_cruise..\1'),
#     (r'NHLULO_[12].*/data/\w+/(lor_[0-9]{10})_.*$', 0,    r'new_horizons.lorri.jupiter_cruise..\1'),
#
#     (r'NHJUMV_[12].*/data/\w+/(m.._[0-9]{10})_.*$', re.I, r'new_horizons.mvic.jupiter..\1'),
#     (r'NHPEMV_[12].*/data/\w+/(m.._[0-9]{10})_.*$', 0,    r'new_horizons.mvic.pluto..\1'),
#     (r'NHPCMV_[12].*/data/\w+/(m.._[0-9]{10})_.*$', 0,    r'new_horizons.mvic.pluto_cruise..\1'),
#     (r'NHLAMV_[12].*/data/\w+/(m.._[0-9]{10})_.*$', 0,    r'new_horizons.mvic.jupiter_cruise..\1'),
# ])

filespec_to_opus_id = translator.TranslatorByRegex([
    # Raw and calibrated NH volumes (series *_1001 and *_2001) share common OPUS IDs.
    (r'NH..LO_[12].*/data/\w+/(lor_[0-9]{10})_.*$', re.I, r'nh-lorri-\1'),
    (r'NH..MV_[12].*/data/\w+/(m.._[0-9]{10})_.*$', re.I, r'nh-mvic-\1'),
])

####################################################################################################################################
# OPUS_ID_TO_FILESPEC
####################################################################################################################################

# Organized giving priority to lossless, full-resolution
opus_id_to_filespec = translator.TranslatorByRegex([
    (r'nh-lorri-.*', 0, (re.compile('.*_0[xX]63[06]_(eng|ENG)\.(fit|FIT)$'),    # High-res lossless
                         re.compile('.*_0[xX]63[17]_(eng|ENG)\.(fit|FIT)$'),    # High-res packetized
                         re.compile('.*_0[xX]63[28]_(eng|ENG)\.(fit|FIT)$'),    # High-res lossy
                         re.compile('.*_0[xX]63[39]_(eng|ENG)\.(fit|FIT)$'),    # 4x4 lossless
                         re.compile('.*_0[xX]63[4aA]_(eng|ENG)\.(fit|FIT)$'),   # 4x4 packetized
                         re.compile('.*_0[xX]63[5bB]_(eng|ENG)\.(fit|FIT)$'))), # 4x4 lossy

    (r'nh-mvic-.*', 0,  (re.compile('.*_0[xX]5(30|36|3F|45|48)_(eng|ENG)\.(fit|FIT)$'), # High-res lossless
                         re.compile('.*_0[xX]5(31|37|40|46|49)_(eng|ENG)\.(fit|FIT)$'), # High-res packetized
                         re.compile('.*_0[xX]5(32|38|41|47|4A)_(eng|ENG)\.(fit|FIT)$'), # High-res lossy
                         re.compile('.*_0[xX]5(33|42)_(eng|ENG)\.(fit|FIT)$'),          # 3x3 lossless
                         re.compile('.*_0[xX]5(34|43)_(eng|ENG)\.(fit|FIT)$'),          # 3x3 packetized
                         re.compile('.*_0[xX]5(35|44)_(eng|ENG)\.(fit|FIT)$'))),        # 3x3 lossy
])

####################################################################################################################################
# FILESPEC_TO_LOGICAL_PATH
####################################################################################################################################

filespec_to_logical_path = translator.TranslatorByRegex([
    (r'NH(..)(..)_(.*_(thumb|small|med|full)\.jpg)', 0, r'previews/NHxx\2_xxxx/NH\1\2_\3'),
    (r'NH(..)(..)_(.*)$',                            0, r'volumes/NHxx\2_xxxx/NH\1\2_\3'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class NHxxxx_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('NHxx.._xxxx', re.I, 'NHxxxx_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS
    SORT_KEY = sort_key + pdsfile.PdsFile.SORT_KEY

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_PRODUCTS = opus_products
    FILESPEC_TO_OPUS_ID = filespec_to_opus_id

    VIEWABLES = {'default': default_viewables}

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']  = associations_to_volumes
    ASSOCIATIONS['previews'] = associations_to_previews
    ASSOCIATIONS['metadata'] = associations_to_metadata

    FILENAME_KEYLEN = 14    # trim off suffixes

    def opus_prioritizer(self, pdsfiles):
        """Prioritizes items that have been downlinked in multiple ways."""

        for header in list(pdsfiles.keys()): # We change pdsfiles in the loop!
            sublists = pdsfiles[header]
            if len(sublists) == 1: continue
            if header[0] != 'New Horizons': continue

            priority = []
            for sublist in sublists:
                code = (sublist[0].basename.replace('X','x')
                        .partition('_0x')[2][:3]).upper()
                rank = sublist[0].version_rank
                priority.append((FILE_CODE_PRIORITY[code],
                                code, -rank, sublist))

            priority.sort()
            code0 = priority[0][1]
            list0 = [priority[0][3]]

            for (prio, code, _, sublist) in priority[1:]:
                if code == code0:
                    list0.append(sublist)
                    continue

                new_header = ('New Horizons',
                              header[1]+50,
                              header[2]+'_alternate',
                              header[3]+' Alternate Downlink')
                if new_header not in pdsfiles:
                    pdsfiles[new_header] = []
                pdsfiles[new_header].append(sublist)
            pdsfiles[header] = list0

        return pdsfiles

# Global attributes shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_FILESPEC = opus_id_to_filespec + pdsfile.PdsFile.OPUS_ID_TO_FILESPEC
pdsfile.PdsFile.FILESPEC_TO_LOGICAL_PATH = filespec_to_logical_path + pdsfile.PdsFile.FILESPEC_TO_LOGICAL_PATH

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['NHxxxx_xxxx'] = NHxxxx_xxxx

####################################################################################################################################
