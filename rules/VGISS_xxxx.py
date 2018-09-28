####################################################################################################################################
# rules/VGISS_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

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
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/.*/C[0-9]{7}_RAW\..*$',     0, ('standard',   0, 'raw',   'Raw Data')),
    (r'volumes/.*/C[0-9]{7}_CALIB\..*$',   0, ('standard', 100, 'calib', 'Calibrated Data')),

    (r'volumes/.*/C[0-9]{7}_CLEANED\..*$', 0, ('Voyager ISS', 10, 'vgiss-cleaned', 'Cleaned Data')),
    (r'volumes/.*/C[0-9]{7}_GEOMED\..*$',  0, ('Voyager ISS', 20, 'vgiss-geomed',  'Geometrically Corrected Data')),
    (r'volumes/.*/C[0-9]{7}_RESLOC\..*$',  0, ('Voyager ISS', 30, 'vgiss-resloc',  'Reseau Table')),
    (r'volumes/.*/C[0-9]{7}_GEOMA\..*$',   0, ('Voyager ISS', 40, 'vgiss-geoma',   'Geometric Tiepoint Table')),

    (r'volumes/.*/C[0-9]{7}\.IMQ$',        0, ('Voyager ISS', 110, 'vgiss-imq', 'Compressed Raw (IMQ)')),
    (r'volumes/.*/C[0-9]{7}\.IBQ$',        0, ('Voyager ISS', 120, 'vgiss-ibq', 'Small Preview (IBQ)')),
])

####################################################################################################################################
# OPUS_FORMAT
####################################################################################################################################

opus_format = translator.TranslatorByRegex([
    (r'.*\.IMG$', 0, ('Binary', 'VICAR')),
    (r'.*\.DAT$', 0, ('Binary', 'VICAR')),
    (r'.*\.IMQ$', 0, ('Binary', 'Compressed EDR')),
    (r'.*\.IBQ$', 0, ('Binary', 'PDS1 Attached Label')),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

opus_products = translator.TranslatorByRegex([
    (r'.*volumes/(VGISS_[5-8]xxx)/(VGISS_[5-8]...)/(DATA/.*)_[A-Z]+\.(IMG|DAT|LBL|TAB)', 0, [r'volumes/\1/\2/\3_RAW.IMG',
                                                                                             r'volumes/\1/\2/\3_RAW.LBL',
                                                                                             r'volumes/\1/\2/\3_CLEANED.IMG',
                                                                                             r'volumes/\1/\2/\3_CLEANED.LBL',
                                                                                             r'volumes/\1/\2/\3_CALIB.IMG',
                                                                                             r'volumes/\1/\2/\3_CALIB.LBL',
                                                                                             r'volumes/\1/\2/\3_GEOMED.IMG',
                                                                                             r'volumes/\1/\2/\3_GEOMED.LBL',
                                                                                             r'volumes/\1/\2/\3_RESLOC.DAT',
                                                                                             r'volumes/\1/\2/\3_RESLOC.TAB',
                                                                                             r'volumes/\1/\2/\3_RESLOC.LBL',
                                                                                             r'volumes/\1/\2/\3_GEOMA.DAT',
                                                                                             r'volumes/\1/\2/\3_GEOMA.TAB',
                                                                                             r'volumes/\1/\2/\3_GEOMA.LBL',
                                                                                             r'previews/\1/\2/\3_thumb.jpg',
                                                                                             r'previews/\1/\2/\3_small.jpg',
                                                                                             r'previews/\1/\2/\3_med.jpg',
                                                                                             r'previews/\1/\2/\3_full.jpg',
                                                                                             r'metadata/\1/\2/\2_jupiter_summary.tab',
                                                                                             r'metadata/\1/\2/\2_jupiter_summary.lbl',
                                                                                             r'metadata/\1/\2/\2_saturn_summary.tab',
                                                                                             r'metadata/\1/\2/\2_saturn_summary.lbl',
                                                                                             r'metadata/\1/\2/\2_uranus_summary.tab',
                                                                                             r'metadata/\1/\2/\2_uranus_summary.lbl',
                                                                                             r'metadata/\1/\2/\2_neptune_summary.tab',
                                                                                             r'metadata/\1/\2/\2_neptune_summary.lbl',
                                                                                             r'metadata/\1/\2/\2_moon_summary.tab',
                                                                                             r'metadata/\1/\2/\2_moon_summary.lbl',
                                                                                             r'metadata/\1/\2/\2_ring_summary.tab',
                                                                                             r'metadata/\1/\2/\2_ring_summary.lbl',
                                                                                             r'metadata/\1/\2/\2_inventory.tab',
                                                                                             r'metadata/\1/\2/\2_inventory.lbl'])
])

####################################################################################################################################
# FILESPEC_TO_OPUS_ID
####################################################################################################################################

filespec_to_opus_id = translator.TranslatorByRegex([
    (r'VGISS_5([12])../DATA/C.....XX/(C[0-9]{7})_[A-Z]+\....$', 0, r'vg-iss-\1-j-\2'),
    (r'VGISS_6([12])../DATA/C.....XX/(C[0-9]{7})_[A-Z]+\....$', 0, r'vg-iss-\1-s-\2'),
    (r'VGISS_7.../DATA/C.....XX/(C[0-9]{7})_[A-Z]+\....$',      0, r'vg-iss-2-u-\1'),
    (r'VGISS_8.../DATA/C.....XX/(C[0-9]{7})_[A-Z]+\....$',      0, r'vg-iss-2-n-\1'),
])

####################################################################################################################################
# OPUS_ID_TO_FILESPEC
####################################################################################################################################

# Return a regular expression that selects the primary data product associated with an OPUS ID
opus_id_to_filespec = translator.TranslatorByRegex([
    (r'vg-iss-.*', 0, re.compile('.*_RAW\.IMG$')),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class VGISS_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('VGISS_[5678]xxx', re.I, 'VGISS_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    SORT_KEY = sort_key + pdsfile.PdsFile.SORT_KEY
    SPLIT_RULES = split_rules + pdsfile.PdsFile.SPLIT_RULES
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_FORMAT = opus_format + pdsfile.PdsFile.OPUS_FORMAT
    OPUS_PRODUCTS = opus_products
    FILESPEC_TO_OPUS_ID = filespec_to_opus_id

    ASSOCIATIONS_TO_VOLUMES = associations_to_volumes + pdsfile.PdsFile.ASSOCIATIONS_TO_VOLUMES

    VOLUMES_TO_ASSOCIATIONS = pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS.copy()
    VOLUMES_TO_ASSOCIATIONS['previews'] = volumes_to_previews + pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS['previews']

    VIEWABLES = {'default': default_viewables}

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_FILESPEC = opus_id_to_filespec + pdsfile.PdsFile.OPUS_ID_TO_FILESPEC

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['VGISS_xxxx'] = VGISS_xxxx

####################################################################################################################################

