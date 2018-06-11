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

# def nh_file_types(filenames, prefix='RAW', suffix='IMAGE'):
#     """Given a list of LORRI or MVIC file names for the same clock count, return
#     the associated set of unique file types.
#     """
# 
#     # If there is just one filename, use the primary type
#     primary_type = prefix + '_' + suffix
# 
#     if len(filenames) == 1:
#         return [primary_type]
# 
#     # Sort the filenames by priority
#     sortable_priorities = []
#     for indx in range(len(filenames)):
#         filename = filenames[indx]
#         upperfile = filename.upper()
#         k = upperfile.index('0X')
#         code = upperfile[k:][2:5]
#         sortable_priorities.append((FILE_TYPE_PRIORITY[code], indx))
# 
#     sortable_priorities.sort()
# 
#     # Fill in the top-priority file type
#     (priority, indx) = sortable_priorities[0]
#     type_of_primary = FILE_TYPE_LOOKUP[priority]
#     primary_is_binned = BINNED_TYPE_LOOKUP[priority]
#     types_used = [primary_type]
#     sortable_types = [(indx, primary_type)]
# 
#     # Assign subsequent types based on priority
#     for (priority, indx) in sortable_priorities[1:]:
#         this_type = FILE_TYPE_LOOKUP[priority] + primary_type
# 
#         # If primary is not binned, always identify binned images
#         is_binned = BINNED_TYPE_LOOKUP[priority]
#         if is_binned and not primary_is_binned:
#             this_type = 'BINNED_' + this_type
# 
#         # A recurrence of a prior file type is a duplicate
#         if this_type in types_used:
#             duplicate_type = 'DUPLICATE_' + this_type
# 
#             if duplicate_type in types_used:
#                 raise ValueError('Non-unique file type ' + this_type +
#                                  ' for ' + filenames[indx])
# 
#             this_type = duplicate_type
# 
#         types_used.append(this_type)
#         sortable_types.append((indx, this_type))
# 
#     # Sort back to the original given order of filenames
#     sortable_types.sort()
# 
#     return [rec[1] for rec in sortable_types]

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
    (r'(volumes|previews)/(NHxx.._xxxx.*/NH...._[12])...',            0,    r'\1/\2*'),
    (r'(volumes|previews)/(NHxx.._xxxx.*/NH...._[12]).../data',       re.I, r'\1/\2*/data'),
    (r'(volumes|previews)/(NHxx.._xxxx.*/NH...._[12]).../data/(\w+)', re.I, r'\1/\2*/data/*'),
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

    # Orders volumes by LA, JU, PC, PE
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
    (r'previews/NHxx.._xxxx/NH...._2xxx/.*$', 0, ''),

    (r'volumes/NHxx.._xxxx/NH...._1.../data/.*eng\.(fit|lbl)$', 0, 'Raw Data'),
    (r'volumes/NHxx.._xxxx/NH...._2.../data/.*sci\.(fit|lbl)$', 0, 'Calibrated Data'),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

opus_products = translator.TranslatorByRegex([
    (r'.*volumes/(NH..LO_xxxx)/(NH..LO)_[12](...)/(.*)_(eng|sci)\.(fit|lbl)', 0, [r'volumes/\1/\2_1\3/\4_eng.fit',
                                                                                  r'volumes/\1/\2_1\3/\4_eng.lbl',
                                                                                  r'volumes/\1/\2_2\3/\4_sci.lbl',
                                                                                  r'volumes/\1/\2_2\3/\4_sci.fit',
                                                                                  r'previews/\1/\2_1\3/\4_eng_thumb.jpg',
                                                                                  r'previews/\1/\2_1\3/\4_eng_small.jpg',
                                                                                  r'previews/\1/\2_1\3/\4_eng_med.jpg',
                                                                                  r'previews/\1/\2_1\3/\4_eng_full.jpg',
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

    (r'.*volumes/(NH..MV_xxxx)/(NH..MV)_[12](...)/(.*)_(eng|sci)\.(fit|lbl)', 0, [r'volumes/\1/\2_1\3/\4_eng.fit',
                                                                                  r'volumes/\1/\2_1\3/\4_eng.lbl',
                                                                                  r'volumes/\1/\2_2\3/\4_sci.lbl',
                                                                                  r'volumes/\1/\2_2\3/\4_sci.lbl',
                                                                                  r'previews/\1/\2_1\3/\4_eng_thumb.jpg',
                                                                                  r'previews/\1/\2_1\3/\4_eng_small.jpg',
                                                                                  r'previews/\1/\2_1\3/\4_eng_med.jpg',
                                                                                  r'previews/\1/\2_1\3/\4_eng_full.jpg']),

])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class NHxxxx_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('NHxx.._xxxx', re.I, 'NHxxxx_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_PRODUCTS = opus_products

    VIEWABLES = {'default': default_viewables}

    VOLUMES_TO_ASSOCIATIONS = pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS.copy()
    VOLUMES_TO_ASSOCIATIONS['volumes'] = volumes_to_volumes + pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS['volumes']

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['NHxxxx_xxxx'] = NHxxxx_xxxx

####################################################################################################################################
