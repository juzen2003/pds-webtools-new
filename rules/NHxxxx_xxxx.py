####################################################################################################################################
# rules/NHxxxx_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

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
# Subclass definition
####################################################################################################################################

class NHxxxx_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('NHxx.._xxxx', re.I, 'NHxxxx_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors

    VIEWABLES = {'default': default_viewables}

    VOLUMES_TO_ASSOCIATIONS = pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS.copy()
    VOLUMES_TO_ASSOCIATIONS['volumes'] = volumes_to_volumes + pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS['volumes']

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['NHxxxx_xxxx'] = NHxxxx_xxxx

####################################################################################################################################
