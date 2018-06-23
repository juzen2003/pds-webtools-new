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
FILE_TYPE_PRIORITY = {

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

FILE_TYPE_LOOKUP = (2 * [''] + 2 * ['PACKETIZED_'] + 2 * ['LOSSY_'] +   # LORRI
                    2 * [''] + 2 * ['PACKETIZED_'] + 2 * ['LOSSY_'] +   # LORRI
                    6 * [''] + 6 * ['PACKETIZED_'] + 6 * ['LOSSY_'] +   # MVIC
                    2 * [''] + 2 * ['PACKETIZED_'] + 2 * ['LOSSY_'])    # MVIC

BINNED_TYPE_LOOKUP = 6 * [False] + 6 * [True] + 18 * [False] + 6 * [True]

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
    (r'volumes/(NHxx.._xxxx)(|_.*)/(NH.*/data/\w+/.*)\.(\w+)', 0, (r'previews/\1/\3_thumb.jpg',
                                                                   r'previews/\1/\3_small.jpg',
                                                                   r'previews/\1/\3_med.jpg',
                                                                   r'previews/\1/\3_full.jpg')),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

volumes_to_volumes = translator.TranslatorByRegex([
    (r'volumes/(\w+/NH...._)[12](.../.*)_(sci|eng).*\.fit', 0, r'volumes/\1?\2*.*'),
    (r'volumes/(\w+/NH...._)[12](...)',                     0, r'volumes/\1?\2'),
    (r'volumes/(\w+/NH...._)[12](.../data[^.]*)',           0, r'volumes/\1?\2'),
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
])

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([

    # Hide calibrated previews because the raw previews are fine
    (r'previews/NHxx.._xxxx(|_v[1-9][0-9]*)/NH...._2xxx/.*$', 0, ''),

    (r'volumes/NHxx.._xxxx(|_v[1-9][0-9]*)/NH...._1.../data/.*eng(|_[1-9])\.(fit|lbl)$', re.I, 'Raw Data'),
    (r'volumes/NHxx.._xxxx(|_v[1-9][0-9]*)/NH...._2.../data/.*sci(|_[1-9])\.(fit|lbl)$', 0, 'Calibrated Data'),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

# NOTE: Entries supporting versions are commented out; nncomment when OPUS is ready to support version numbers in shopping carts

opus_products = translator.TranslatorByRegex([
    (r'.*volumes/(NH..LO_xxxx)/(NH..LO)_[12](...)/(.*)_(eng|sci)(|_[1-9][0-9]*)\.(fit|lbl)', 0,
                                                                [r'volumes/\1/\2_1\3/\4_eng*.[fl][ib][tl]',
#                                                                  r'volumes/\1_v*/\2_1\3/\4_eng*.[fl][ib][tl]',
                                                                 r'volumes/\1/\2_2\3/\4_sci*.[fl][ib][tl]',
#                                                                  r'volumes/\1_v*/\2_2\3/\4_sci*.[fl][ib][tl]',
                                                                 r'previews/\1/\2_1\3/\4_eng*_thumb.jpg',
                                                                 r'previews/\1/\2_1\3/\4_eng*_small.jpg',
                                                                 r'previews/\1/\2_1\3/\4_eng*_med.jpg',
                                                                 r'previews/\1/\2_1\3/\4_eng*_full.jpg',
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
#     (r'.*volumes/(NH..MV_xxxx)/(NH..MV)_[12](...)/data/(.*)/mc(.*)_0x(...)_(eng|sci)(|_[1-9][0-9]*)\.(fit|lbl)', 0,
#                                                                 [r'volumes/\1/\2_1\3/data/\4/mc\5_0x\6_eng*.[fl][ib][tl]',
#                                                                  r'volumes/\1_v1/\2_1\3/DATA/\4/MC\5_0X\6_ENG*.[FL][IB][TL]',
#                                                                  r'volumes/\1_v*/\2_1\3/data/\4/mc\5_0x\6_eng*.[fl][ib][tl]',
#                                                                  r'volumes/\1/\2_2\3/data/\4/mc\5_0x\6_sci*.[fl][ib][tl]',
#                                                                  r'volumes/\1_v*/\2_2\3/data/\4/mc\5_0x\6_sci*.[fl][ib][tl]',
#                                                                  r'previews/\1/\2_1\3/data/\4/mc\5_0x\6_eng*_thumb.jpg',
#                                                                  r'previews/\1/\2_1\3/data/\4/mc\5_0x\6_eng*_small.jpg',
#                                                                  r'previews/\1/\2_1\3/data/\4/mc\5_0x\6_eng*_med.jpg',
#                                                                  r'previews/\1/\2_1\3/data/\4/mc\5_0x\6_eng*_full.jpg']),
# 
#     (r'.*volumes/(NH..MV_xxxx)/(NH..MV)_[12](...)/data/(.*)/mpf(.*)_0x(...)_(eng|sci)(|_[1-9][0-9]*)\.(fit|lbl)', 0,
#                                                                 [r'volumes/\1/\2_1\3/data/\4/mpf\5_0x\6_eng*.[fl][ib][tl]',
#                                                                  r'volumes/\1_v1/\2_1\3/DATA/\4/MPF\5_0X\6_ENG*.[FL][IB][TL]',
#                                                                  r'volumes/\1_v*/\2_1\3/data/\4/mpf\5_0x\6_eng*.[fl][ib][tl]',
#                                                                  r'volumes/\1/\2_2\3/data/\4/mpf\5_0x\6_sci*.[fl][ib][tl]',
#                                                                  r'volumes/\1_v*/\2_2\3/data/\4/mpf\5_0x\6_sci*.[fl][ib][tl]',
#                                                                  r'previews/\1/\2_1\3/data/\4/mpf\5_0x\6_eng*_thumb.jpg',
#                                                                  r'previews/\1/\2_1\3/data/\4/mpf\5_0x\6_eng*_small.jpg',
#                                                                  r'previews/\1/\2_1\3/data/\4/mpf\5_0x\6_eng*_med.jpg',
#                                                                  r'previews/\1/\2_1\3/data/\4/mpf\5_0x\6_eng*_full.jpg']),

    (r'.*volumes/(NH..MV_xxxx)/(NH..MV)_[12](...)/(.*)_(eng|sci)(|_[1-9][0-9]*)\.(fit|lbl)', 0,
                                                                [r'volumes/\1/\2_1\3/\4_eng*.[fl][ib][tl]',
#                                                                  r'volumes/\1_v*/\2_1\3/\4_eng*.[fl][ib][tl]',
                                                                 r'volumes/\1/\2_2\3/\4_sci*.[fl][ib][tl]',
#                                                                  r'volumes/\1_v*/\2_2\3/\4_sci*.[fl][ib][tl]',
                                                                 r'previews/\1/\2_1\3/\4_eng*_thumb.jpg',
                                                                 r'previews/\1/\2_1\3/\4_eng*_small.jpg',
                                                                 r'previews/\1/\2_1\3/\4_eng*_med.jpg',
                                                                 r'previews/\1/\2_1\3/\4_eng*_full.jpg']),

])

####################################################################################################################################
# OPUS_ID_TO_FILESPEC
####################################################################################################################################

opus_id_to_filespec = translator.TranslatorByRegex([
    # Raw and calibrated NH volumes share common OPUS IDs, where "x" replaces the leading "1" or "2" in the volume ID and
    # "eng" or "sci" at the end of the file name is removed. The filespec returned points to the raw file. Note that some
    # releases of the data set have a downlink number following "eng" or "sci"; others do not.
    (r'(NH....)_x(...)/(.*)$', 0, r'\1_1\2/data/\3_eng*.fit'),
])

####################################################################################################################################
# FILESPEC_TO_OPUS_ID
####################################################################################################################################

filespec_to_opus_id = translator.TranslatorByRegex([
    # Raw and calibrated NH volumes (series *_1001 and *_2001) share common OPUS IDs. The OPUS ID replaces the leading
    # "1" or "2" by "x" and removes the final "eng" or "sci". It strips away a downlink number if necessary.
    (r'(NH....)_[12](...)(|_v[1-9])/data/(.*)_(eng|sci)(|_[1-9][0-9]*).(fit|lbl)$', 0, r'\1_x\2/\4'),
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

    VOLUMES_TO_ASSOCIATIONS = pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS.copy()
    VOLUMES_TO_ASSOCIATIONS['volumes'] = volumes_to_volumes + pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS['volumes']

# Global attributes shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_FILESPEC = opus_id_to_filespec + pdsfile.PdsFile.OPUS_ID_TO_FILESPEC
pdsfile.PdsFile.FILESPEC_TO_LOGICAL_PATH = filespec_to_logical_path + pdsfile.PdsFile.FILESPEC_TO_LOGICAL_PATH

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['NHxxxx_xxxx'] = NHxxxx_xxxx

####################################################################################################################################
