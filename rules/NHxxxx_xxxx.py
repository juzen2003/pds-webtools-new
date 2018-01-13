####################################################################################################################################
# rules/NHxxxx_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

key_from_path = translator.TranslatorByRegex([
    (r'[-a-z]+/NHxxLO_xxxx(|_.*)/NHLALO_([12])...', re.I, r'NHxxLO_xxxx/NHLALO_\g<2>001'),
    (r'[-a-z]+/NHxxLO_xxxx(|_.*)/NHJULO_([12])...', re.I, r'NHxxLO_xxxx/NHJULO_\g<2>001'),
    (r'[-a-z]+/NHxxLO_xxxx(|_.*)/NHPCLO_([12])...', re.I, r'NHxxLO_xxxx/NHPCLO_\g<2>001'),
    (r'[-a-z]+/NHxxLO_xxxx(|_.*)/NHPELO_([12])...', re.I, r'NHxxLO_xxxx/NHPELO_\g<2>001'),
    (r'[-a-z]+/NHxxLO_xxxx(|_.*)',                  re.I, r'NHxxLO_xxxx\1'),

    (r'[-a-z]+/NHxxMV_xxxx(|_.*)/NHLAMV_([12])...', re.I, r'NHxxMV_xxxx/NHLAMV_\g<2>001'),
    (r'[-a-z]+/NHxxMV_xxxx(|_.*)/NHJUMV_([12])...', re.I, r'NHxxMV_xxxx/NHJUMV_\g<2>001'),
    (r'[-a-z]+/NHxxMV_xxxx(|_.*)/NHPCMV_([12])...', re.I, r'NHxxMV_xxxx/NHPCMV_\g<2>001'),
    (r'[-a-z]+/NHxxMV_xxxx(|_.*)/NHPEMV_([12])...', re.I, r'NHxxMV_xxxx/NHPEMV_\g<2>001'),
    (r'[-a-z]+/NHxxMV_xxxx(|_.*)',                  re.I, r'NHxxMV_xxxx\1'),
])

description_and_icon_by_dict = translator.TranslatorByDict({
    'NHxxLO_xxxx'            : ('New Horizons LORRI image collection (2016-2017)',                                   'VOLDIR'),
    'NHxxLO_xxxx_v1'         : ('New Horizons LORRI image collection (2007)',                                        'VOLDIR'),
    'NHxxLO_xxxx_v1.1'       : ('New Horizons LORRI image collection (2008)',                                        'VOLDIR'),
    'NHxxLO_xxxx_v2'         : ('New Horizons LORRI image collection (2009)',                                        'VOLDIR'),
    'NHxxLO_xxxx_v3'         : ('New Horizons LORRI image collection (2014)',                                        'VOLDIR'),
    'NHxxLO_xxxx_v4'         : ('New Horizons LORRI image collection (2016)',                                        'VOLDIR'),
    'NHxxLO_xxxx/NHJULO_1001': ('New Horizons raw LORRI images, Jupiter flyby, 2007-01-08 to 2015-07-15',            'VOLUME'),
    'NHxxLO_xxxx/NHJULO_2001': ('New Horizons calibrated LORRI images, Jupiter flyby, 2007-01-08 to 2015-07-15',     'VOLUME'),
    'NHxxLO_xxxx/NHLALO_1001': ('New Horizons raw LORRI images, cruise to Jupiter, 2006-02-24 to 2015-07-15',        'VOLUME'),
    'NHxxLO_xxxx/NHLALO_2001': ('New Horizons calibrated LORRI images, cruise to Jupiter, 2006-02-24 to 2015-07-15', 'VOLUME'),
    'NHxxLO_xxxx/NHPCLO_1001': ('New Horizons raw LORRI images, cruise to Pluto, 2007-09-29 to 2015-07-15',          'VOLUME'),
    'NHxxLO_xxxx/NHPCLO_2001': ('New Horizons calibrated LORRI images, cruise to Pluto, 2007-09-29 to 2015-07-15',   'VOLUME'),
    'NHxxLO_xxxx/NHPELO_1001': ('New Horizons raw LORRI images, Pluto flyby, 2015-01-25 to 2015-11-02',              'VOLUME'),
    'NHxxLO_xxxx/NHPELO_2001': ('New Horizons calibrated LORRI images, Pluto flyby, 2015-01-25 to 2015-11-02',       'VOLUME'),

    'NHxxMV_xxxx'            : ('New Horizons MVIC image collection (2016-2017)',                                    'VOLDIR'),
    'NHxxMV_xxxx_v1'         : ('New Horizons MVIC image collection (2008)',                                         'VOLDIR'),
    'NHxxMV_xxxx_v2'         : ('New Horizons MVIC image collection (2016)',                                         'VOLDIR'),
    'NHxxMV_xxxx/NHJUMV_1001': ('New Horizons raw MVIC images, Jupiter flyby, 2007-01-08 to 2015-07-15',             'VOLUME'),
    'NHxxMV_xxxx/NHJUMV_2001': ('New Horizons calibrated MVIC images, Jupiter flyby, 2007-01-08 to 2015-07-15',      'VOLUME'),
    'NHxxMV_xxxx/NHLAMV_1001': ('New Horizons raw MVIC images, cruise to Jupiter, 2006-02-24 to 2015-07-15',         'VOLUME'),
    'NHxxMV_xxxx/NHLAMV_2001': ('New Horizons calibrated MVIC images, cruise to Jupiter, 2006-02-24 to 2015-07-15',  'VOLUME'),
    'NHxxMV_xxxx/NHPCMV_1001': ('New Horizons raw MVIC images, cruise to Pluto, 2007-09-29 to 2015-07-15',           'VOLUME'),
    'NHxxMV_xxxx/NHPCMV_2001': ('New Horizons calibrated MVIC images, cruise to Pluto, 2007-09-29 to 2015-07-15',    'VOLUME'),
    'NHxxMV_xxxx/NHPEMV_1001': ('New Horizons raw MVIC images, Pluto flyby, 2015-01-25 to 2015-11-02',               'VOLUME'),
    'NHxxMV_xxxx/NHPEMV_2001': ('New Horizons calibrated MVIC images, Pluto flyby, 2015-01-25 to 2015-11-02',        'VOLUME'),
}, key_from_path)

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

    DESCRIPTION_AND_ICON = description_and_icon_by_dict + description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
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
