####################################################################################################################################
# rules/VGISS_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

key_from_path = translator.TranslatorByRegex([
    (r'[-a-z]+/VGISS_([5-8])xxx(|_\w+)/VGISS_([5-8][0-9]{3})', re.I, r'VGISS_\1xxx/VGISS_\3'),
    (r'[-a-z]+/VGISS_([5-8])xxx(|_\w+)',                       re.I, r'VGISS_\1xxx'),
])

description_and_icon_by_dict = translator.TranslatorByDict({
    'VGISS_5xxx'           : ('Voyager Jupiter image collection, raw and calibrated',                           'VOLDIR'),
    'VGISS_5xxx/VGISS_5101': ('Voyager 1 Jupiter images 1978-12-11 to 1979-01-18 (SC clock 13854.55-14998.31)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5102': ('Voyager 1 Jupiter images 1979-01-18 to 1979-01-24 (SC clock 15000.55-15199.30)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5103': ('Voyager 1 Jupiter images 1979-01-24 to 1979-01-31 (SC clock 15201.54-15399.57)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5104': ('Voyager 1 Jupiter images 1979-01-31 to 1979-02-02 (SC clock 15400.00-15449.57)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5105': ('Voyager 1 Jupiter images 1979-02-02 to 1979-02-03 (SC clock 15450.00-15498.37)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5106': ('Voyager 1 Jupiter images 1979-02-04 to 1979-02-07 (SC clock 15508.28-15598.26)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5107': ('Voyager 1 Jupiter images 1979-02-07 to 1979-02-10 (SC clock 15600.34-15699.57)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5108': ('Voyager 1 Jupiter images 1979-02-10 to 1979-02-13 (SC clock 15700.00-15799.25)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5109': ('Voyager 1 Jupiter images 1979-02-13 to 1979-02-17 (SC clock 15801.33-15898.41)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5110': ('Voyager 1 Jupiter images 1979-02-17 to 1979-02-20 (SC clock 15900.49-15997.56)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5111': ('Voyager 1 Jupiter images 1979-02-20 to 1979-02-23 (SC clock 16000.03-16099.33)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5112': ('Voyager 1 Jupiter images 1979-02-23 to 1979-02-27 (SC clock 16100.05-16199.57)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5113': ('Voyager 1 Jupiter images 1979-02-27 to 1979-02-28 (SC clock 16200.00-16249.24)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5114': ('Voyager 1 Jupiter images 1979-02-28 to 1979-03-02 (SC clock 16250.03-16299.58)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5115': ('Voyager 1 Jupiter images 1979-03-02 to 1979-03-04 (SC clock 16300.01-16349.54)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5116': ('Voyager 1 Jupiter images 1979-03-04 to 1979-03-05 (SC clock 16350.03-16399.58)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5117': ('Voyager 1 Jupiter images 1979-03-05 to 1979-03-07 (SC clock 16400.00-16447.59)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5118': ('Voyager 1 Jupiter images 1979-03-07 to 1979-03-09 (SC clock 16450.47-16495.23)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5119': ('Voyager 1 Jupiter images 1979-03-09 to 1979-03-25 (SC clock 16501.03-16983.04)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5120': ('Voyager 1 Jupiter images 1979-03-31 to 1979-04-14 (SC clock 17182.42-17574.26)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5201': ('Voyager 2 Jupiter images 1979-04-15 to 1979-05-08 (SC clock 18110.30-18798.51)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5202': ('Voyager 2 Jupiter images 1979-05-08 to 1979-05-22 (SC clock 18801.17-19198.23)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5203': ('Voyager 2 Jupiter images 1979-05-22 to 1979-05-28 (SC clock 19200.49-19399.58)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5204': ('Voyager 2 Jupiter images 1979-05-28 to 1979-06-04 (SC clock 19400.02-19594.51)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5205': ('Voyager 2 Jupiter images 1979-06-04 to 1979-06-11 (SC clock 19602.10-19798.24)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5206': ('Voyager 2 Jupiter images 1979-06-11 to 1979-06-17 (SC clock 19800.23-19999.25)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5207': ('Voyager 2 Jupiter images 1979-06-18 to 1979-06-24 (SC clock 20001.33-20195.56)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5208': ('Voyager 2 Jupiter images 1979-06-24 to 1979-06-27 (SC clock 20209.44-20292.28)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5209': ('Voyager 2 Jupiter images 1979-06-28 to 1979-07-01 (SC clock 20301.26-20399.56)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5210': ('Voyager 2 Jupiter images 1979-07-01 to 1979-07-04 (SC clock 20400.00-20498.02)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5211': ('Voyager 2 Jupiter images 1979-07-04 to 1979-07-06 (SC clock 20501.24-20549.58)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5212': ('Voyager 2 Jupiter images 1979-07-06 to 1979-07-07 (SC clock 20550.03-20593.53)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5213': ('Voyager 2 Jupiter images 1979-07-08 to 1979-07-09 (SC clock 20603.35-20649.57)', 'VOLUME'),
    'VGISS_5xxx/VGISS_5214': ('Voyager 2 Jupiter images 1979-07-09 to 1979-07-16 (SC clock 20650.01-20863.05)', 'VOLUME'),

    'VGISS_6xxx'           : ('Voyager Saturn image collection, raw and calibrated',                           'VOLDIR'),
    'VGISS_6xxx/VGISS_6101': ('Voyager 1 Saturn images 1980-08-23 to 1980-09-02 (SC clock 32499.21-32798.04)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6102': ('Voyager 1 Saturn images 1980-09-02 to 1980-09-09 (SC clock 32800.31-32998.16)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6103': ('Voyager 1 Saturn images 1980-09-09 to 1980-09-15 (SC clock 33000.43-33198.36)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6104': ('Voyager 1 Saturn images 1980-09-15 to 1980-09-25 (SC clock 33200.47-33498.54)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6105': ('Voyager 1 Saturn images 1980-09-25 to 1980-10-05 (SC clock 33501.05-33799.12)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6106': ('Voyager 1 Saturn images 1980-10-05 to 1980-10-15 (SC clock 33801.23-34099.58)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6107': ('Voyager 1 Saturn images 1980-10-15 to 1980-10-25 (SC clock 34100.05-34399.57)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6108': ('Voyager 1 Saturn images 1980-10-25 to 1980-10-29 (SC clock 34400.04-34499.54)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6109': ('Voyager 1 Saturn images 1980-10-29 to 1980-11-01 (SC clock 34500.01-34599.57)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6110': ('Voyager 1 Saturn images 1980-11-01 to 1980-11-04 (SC clock 34600.02-34699.58)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6111': ('Voyager 1 Saturn images 1980-11-04 to 1980-11-08 (SC clock 34700.02-34799.53)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6112': ('Voyager 1 Saturn images 1980-11-08 to 1980-11-11 (SC clock 34800.32-34899.50)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6113': ('Voyager 1 Saturn images 1980-11-11 to 1980-11-14 (SC clock 34900.02-34999.57)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6114': ('Voyager 1 Saturn images 1980-11-14 to 1980-11-18 (SC clock 35000.02-35099.58)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6115': ('Voyager 1 Saturn images 1980-11-18 to 1980-11-21 (SC clock 35100.05-35199.54)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6116': ('Voyager 1 Saturn images 1980-11-21 to 1980-11-28 (SC clock 35200.02-35395.14)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6117': ('Voyager 1 Saturn images 1980-11-28 to 1980-12-01 (SC clock 35409.04-35499.56)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6118': ('Voyager 1 Saturn images 1980-12-01 to 1980-12-04 (SC clock 35500.00-35599.55)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6119': ('Voyager 1 Saturn images 1980-12-04 to 1980-12-08 (SC clock 35600.03-35694.32)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6120': ('Voyager 1 Saturn images 1980-12-08 to 1980-12-11 (SC clock 35708.08-35799.56)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6121': ('Voyager 1 Saturn images 1980-12-11 to 1980-12-15 (SC clock 35800.00-35932.25)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6201': ('Voyager 2 Saturn images 1981-06-05 to 1981-06-10 (SC clock 41561.54-41698.02)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6202': ('Voyager 2 Saturn images 1981-06-10 to 1981-06-20 (SC clock 41700.34-41997.29)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6203': ('Voyager 2 Saturn images 1981-06-20 to 1981-06-30 (SC clock 42000.01-42299.35)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6204': ('Voyager 2 Saturn images 1981-06-30 to 1981-07-10 (SC clock 42302.07-42599.02)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6205': ('Voyager 2 Saturn images 1981-07-10 to 1981-07-20 (SC clock 42601.34-42898.29)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6206': ('Voyager 2 Saturn images 1981-07-20 to 1981-07-30 (SC clock 42901.01-43197.56)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6207': ('Voyager 2 Saturn images 1981-07-30 to 1981-08-05 (SC clock 43200.16-43399.39)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6208': ('Voyager 2 Saturn images 1981-08-05 to 1981-08-09 (SC clock 43401.01-43499.55)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6209': ('Voyager 2 Saturn images 1981-08-09 to 1981-08-12 (SC clock 43500.02-43599.57)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6210': ('Voyager 2 Saturn images 1981-08-12 to 1981-08-15 (SC clock 43600.01-43699.13)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6211': ('Voyager 2 Saturn images 1981-08-15 to 1981-08-19 (SC clock 43701.00-43799.49)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6212': ('Voyager 2 Saturn images 1981-08-19 to 1981-08-22 (SC clock 43800.00-43899.58)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6213': ('Voyager 2 Saturn images 1981-08-22 to 1981-08-25 (SC clock 43900.02-43999.56)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6214': ('Voyager 2 Saturn images 1981-08-25 to 1981-09-01 (SC clock 44000.01-44199.55)', 'VOLUME'),
    'VGISS_6xxx/VGISS_6215': ('Voyager 2 Saturn images 1981-09-01 to 1981-09-05 (SC clock 44200.02-44304.48)', 'VOLUME'),

    'VGISS_7xxx'           : ('Voyager Uranus image collection, raw and calibrated',                           'VOLDIR'),
    'VGISS_7xxx/VGISS_7201': ('Voyager 2 Uranus images 1985-11-06 to 1985-11-23 (SC clock 24476.54-24987.58)', 'VOLUME'),
    'VGISS_7xxx/VGISS_7202': ('Voyager 2 Uranus images 1985-11-25 to 1985-12-27 (SC clock 25027.59-25992.58)', 'VOLUME'),
    'VGISS_7xxx/VGISS_7203': ('Voyager 2 Uranus images 1985-12-22 to 1986-01-06 (SC clock 26002.27-26288.56)', 'VOLUME'),
    'VGISS_7xxx/VGISS_7204': ('Voyager 2 Uranus images 1986-01-06 to 1986-01-16 (SC clock 26302.41-26594.13)', 'VOLUME'),
    'VGISS_7xxx/VGISS_7205': ('Voyager 2 Uranus images 1986-01-16 to 1986-01-23 (SC clock 26602.52-26799.49)', 'VOLUME'),
    'VGISS_7xxx/VGISS_7206': ('Voyager 2 Uranus images 1986-01-23 to 1986-01-29 (SC clock 26800.06-26999.53)', 'VOLUME'),
    'VGISS_7xxx/VGISS_7207': ('Voyager 2 Uranus images 1986-01-29 to 1986-02-19 (SC clock 27000.00-27628.44)', 'VOLUME'),

    'VGISS_8xxx'           : ('Voyager Neptune image collection, raw and calibrated',                           'VOLDIR'),
    'VGISS_8xxx/VGISS_8201': ('Voyager 2 Neptune images 1989-06-05 to 1989-06-23 (SC clock 08966.31-09497.47)', 'VOLUME'),
    'VGISS_8xxx/VGISS_8202': ('Voyager 2 Neptune images 1989-06-23 to 1989-07-09 (SC clock 09505.56-09998.43)', 'VOLUME'),
    'VGISS_8xxx/VGISS_8203': ('Voyager 2 Neptune images 1989-07-09 to 1989-07-22 (SC clock 10002.47-10378.21)', 'VOLUME'),
    'VGISS_8xxx/VGISS_8204': ('Voyager 2 Neptune images 1989-07-23 to 1989-08-05 (SC clock 10404.40-10798.14)', 'VOLUME'),
    'VGISS_8xxx/VGISS_8205': ('Voyager 2 Neptune images 1989-08-06 to 1989-08-12 (SC clock 10826.20-10999.58)', 'VOLUME'),
    'VGISS_8xxx/VGISS_8206': ('Voyager 2 Neptune images 1989-08-12 to 1989-08-18 (SC clock 11000.05-11199.49)', 'VOLUME'),
    'VGISS_8xxx/VGISS_8207': ('Voyager 2 Neptune images 1989-08-18 to 1989-08-25 (SC clock 11200.00-11399.50)', 'VOLUME'),
    'VGISS_8xxx/VGISS_8208': ('Voyager 2 Neptune images 1989-08-25 to 1989-09-01 (SC clock 11400.02-11599.58)', 'VOLUME'),
    'VGISS_8xxx/VGISS_8209': ('Voyager 2 Neptune images 1989-09-01 to 1989-09-12 (SC clock 11600.06-11935.39)', 'VOLUME'),
    'VGISS_8xxx/VGISS_8210': ('Voyager 2 Neptune images 1989-09-14 to 1989-09-29 (SC clock 12009.27-12457.32)', 'VOLUME'),
}, key_from_path)

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*/data',             re.I, ('Images grouped by SC clock',        'IMAGEDIR')),
    (r'volumes/.*/data/C[0-9]+X+',   re.I, ('Images grouped by SC clock',        'IMAGEDIR')),
    (r'volumes/.*/browse',           re.I, ('Browse images grouped by SC clock', 'IMAGEDIR')),
    (r'volumes/.*/browse/C[0-9]+X+', re.I, ('Browse images grouped by SC clock', 'IMAGEDIR')),
    (r'volumes/.*_raw\.img',         re.I, ('Raw image, VICAR',                  'IMAGE'   )),
    (r'volumes/.*_cleaned\.img',     re.I, ('Cleaned raw image, VICAR',          'IMAGE'   )),
    (r'volumes/.*_calib\.img',       re.I, ('Calibrated image, VICAR',           'IMAGE'   )),
    (r'volumes/.*_geomed\.img',      re.I, ('Undistorted image, VICAR',          'IMAGE'   )),
    (r'volumes/.*_geoma\.tab',       re.I, ('ASCII distortion table',            'TABLE'   )),
    (r'volumes/.*_geoma\.dat',       re.I, ('Distortion file, VICAR',            'DATA'    )),
    (r'volumes/.*_resloc\.dat',      re.I, ('Reseau table, VICAR',               'DATA'    )),
    (r'volumes/.*_resloc\.tab',      re.I, ('ASCII Reseau table',                'TABLE'   )),
    (r'volumes/.*/MIPL/.*\.dat',     re.I, ('VICAR data file',                   'DATA'    )),
    (r'volumes/.*/DARKS/.*\.img',    re.I, ('Dark current image, VICAR',         'IMAGE'   )),
])

####################################################################################################################################
# SORT_KEY
####################################################################################################################################

sort_key = translator.TranslatorByRegex([

    # Sort data files into increasing level of processing
    (r'(.*)(_RAW)\.(JPG|IMG)',        0, r'\1_1RAW.\3'    ),
    (r'(.*)(_CLEANED)\.(JPG|IMG)',    0, r'\1_2CLEANED.\3'),
    (r'(.*)(_CALIB)\.(JPG|IMG)',      0, r'\1_3CALIB.\3'  ),
    (r'(.*)(_GEOMED)\.(JPG|IMG)',     0, r'\1_4GEOMED.\3' ),
    (r'(.*)(_RESLOC)\.(DAT|TAB)',     0, r'\1_5RESLOC.\3' ),
    (r'(.*)(_GEOMA)\.(DAT|TAB)',      0, r'\1_6GEOMA.\3'  ),

    (r'(.*)(_RAW)\.LBL',        0, r'\1_1RAW.zLBL'    ),    # Label after matching file, not after everything
    (r'(.*)(_CLEANED)\.LBL',    0, r'\1_2CLEANED.zLBL'),
    (r'(.*)(_CALIB)\.LBL',      0, r'\1_3CALIB.zLBL'  ),
    (r'(.*)(_GEOMED)\.LBL',     0, r'\1_4GEOMED.zLBL' ),
    (r'(.*)(_RESLOC)\.LBL',     0, r'\1_5RESLOC.zLBL' ),
    (r'(.*)(_GEOMA)\.LBL',      0, r'\1_6GEOMA.zLBL'  ),
])

####################################################################################################################################
# SPLIT_RULES
####################################################################################################################################

split_rules = translator.TranslatorByRegex([
    (r'(.*)_(RAW|CLEANED|CALIB|GEOMED|RESLOC|GEOMA)\.(.*)$', 0, (r'\1', r'_\2', r'.\3')),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'volumes/(.*)/DATA/(.*)(_[A-Z]+)\.(IMG|LBL|DAT|TAB)', 0, r'volumes/\1/BROWSE/\2\3.*'),
    (r'volumes/(.*)/BROWSE/(.*)\.(JPG|LBL)',                0, r'volumes/\1/DATA/\2.*'),
    (r'volumes/(.*)/DATA/(\w+)',                            0, r'volumes/\1/BROWSE/\2'),
    (r'volumes/(.*)/BROWSE/(\w+)',                          0, r'volumes/\1/DATA/\2'),
    (r'previews/(.*)_(thumb|small|med|full)\.jpg',          0, r'volumes/\1_*.*'),
])

volumes_to_previews = translator.TranslatorByRegex([
    (r'volumes/(.*)/(DATA/.*)_(RAW|CLEANED|CALIB|GEOMED)\..*', 0, [r'previews/\1/\2_thumb.jpg',
                                                                   r'previews/\1/\2_small.jpg',
                                                                   r'previews/\1/\2_med.jpg',
                                                                   r'previews/\1/\2_full.jpg']),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews)/VGISS_..../VGISS_..../(DATA|BROWSE)',     0, (True, True, True)),
    (r'(volumes|previews)/VGISS_..../VGISS_..../(DATA|BROWSE)/\w+', 0, (True, True, True)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'(volumes|previews)/(VGISS_..../VGISS_..)../(DATA|BROWSE)',     0, r'\1/\2*/\3'),
    (r'(volumes|previews)/(VGISS_..../VGISS_..)../(DATA|BROWSE)/\w+', 0, r'\1/\2*/\3/*'),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'volumes/(.*)/(DATA/\w+/.*)_(RAW|CLEANED|CALIB|GEOMED)\..*', 0, (r'previews/\1/\2_thumb.jpg',
                                                                       r'previews/\1/\2_small.jpg',
                                                                       r'previews/\1/\2_med.jpg',
                                                                       r'previews/\1/\2_full.jpg')),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class VGISS_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('VGISS_[5678]xxx', re.I, 'VGISS_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_dict + description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    SORT_KEY = sort_key + pdsfile.PdsFile.SORT_KEY
    SPLIT_RULES = split_rules + pdsfile.PdsFile.SPLIT_RULES
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS

    ASSOCIATIONS_TO_VOLUMES = associations_to_volumes + pdsfile.PdsFile.ASSOCIATIONS_TO_VOLUMES

    VOLUMES_TO_ASSOCIATIONS = pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS.copy()
    VOLUMES_TO_ASSOCIATIONS['previews'] = volumes_to_previews + pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS['previews']

    VIEWABLES = {'default': default_viewables}

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['VGISS_xxxx'] = VGISS_xxxx

####################################################################################################################################

