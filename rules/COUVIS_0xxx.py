####################################################################################################################################
# rules/COUVIS_0xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*/DATA',          re.I, ('Data files grouped by date', 'CUBEDIR')),
    (r'volumes/.*/DATA/\w+',      re.I, ('Data files grouped by date', 'CUBEDIR')),
    (r'volumes/.*/HSP\w+\.DAT',   re.I, ('Time series data',           'DATA')),
    (r'volumes/.*/HDAC\w+\.DAT',  re.I, ('Binary data cube',           'DATA')),
    (r'volumes/.*/\w+\.DAT',      re.I, ('Spectral data cube',         'CUBE')),
    (r'volumes/.*\.txt_[0-9].*',  re.I, ('Text file',                  'INFO')),
    (r'volumes/.*OLD.DIR',        re.I, ('Directory',                  'FOLDER')),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl', re.I, ''),
    (r'volumes/COUVIS_0xxx(|_v[0-9\.]+)/(COUVIS_0.../DATA/\w+/\w+).*',
                            0,  r'previews/COUVIS_0xxx/\2_*'),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'volumes/COUVIS_0xxx(.*/COUVIS_0...)/(DATA|CALIB/VERSION_.)/(\w+)/(.*_\d\d)(|_CAL_.)\..*', 0,
            [r'volumes/COUVIS_0xxx\1/DATA/\3/\4.DAT',
             r'volumes/COUVIS_0xxx\1/DATA/\3/\4.LBL',
             r'volumes/COUVIS_0xxx\1/CALIB/VERSION_3/\3/\4_CAL_3.DAT',
             r'volumes/COUVIS_0xxx\1/CALIB/VERSION_3/\3/\4_CAL_3.LBL',
             r'volumes/COUVIS_0xxx\1/CALIB/VERSION_4/\3/\4_CAL_4.DAT',
             r'volumes/COUVIS_0xxx\1/CALIB/VERSION_4/\3/\4_CAL_4.LBL',
             r'volumes/COUVIS_0xxx\1/CALIB/VERSION_5/\3/\4_CAL_5.DAT',
             r'volumes/COUVIS_0xxx\1/CALIB/VERSION_5/\3/\4_CAL_5.LBL',
            ]),
    (r'volumes/COUVIS_0xxx(.*/COUVIS_0...)/(DATA|CALIB/VERSION_.)(|/\w+)', 0,
            [r'volumes/COUVIS_0xxx\1/DATA\3',
             r'volumes/COUVIS_0xxx\1/CALIB/VERSION_3\3',
             r'volumes/COUVIS_0xxx\1/CALIB/VERSION_4\3',
             r'volumes/COUVIS_0xxx\1/CALIB/VERSION_5\3',
            ]),
    (r'previews/COUVIS_0xxx(|_v[0-9\.]+)/(COUVIS_0...)/DATA(|/\w+)', 0,
            r'volumes/COUVIS_0xxx/\2/DATA\3'),
    (r'previews/COUVIS_0xxx(|_v[0-9\.]+)/(COUVIS_0.../DATA/\w+/\w+)_[a-z]+\.png', 0,
            [r'volumes/COUVIS_0xxx/\2.DAT',
             r'volumes/COUVIS_0xxx/\2.LBL',
            ]),
    (r'.*/COUVIS_0999.*', 0,
            r'volumes/COUVIS_0xxx'),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'volumes/COUVIS_0xxx(|_v[0-9\.]+)/(COUVIS_0.../DATA/\w+/\w+)\..*',
                            0,  [r'previews/COUVIS_0xxx/\2_full.png',
                                 r'previews/COUVIS_0xxx/\2_med.png',
                                 r'previews/COUVIS_0xxx/\2_small.png',
                                 r'previews/COUVIS_0xxx/\2_thumb.png',
                                ]),
    (r'volumes/COUVIS_0xxx(|_v[0-9\.]+)/(COUVIS_0.../DATA/\w+)',
                            0,  r'previews/COUVIS_0xxx/\2'),
    (r'.*/COUVIS_0999.*',   0,  r'previews/COUVIS_0xxx'),
])

associations_to_metadata = translator.TranslatorByRegex([
    (r'volumes/COUVIS_0xxx(|_v[0-9\.]+)/(COUVIS_0...)/DATA/\w+/(\w+)\..*',
                            0,  [r'metadata/COUVIS_0xxx/\2/\2_index.tab/\3',
                                 r'metadata/COUVIS_0xxx/\2/\2_supplemental_index.tab/\3',
                                 r'metadata/COUVIS_0xxx/\2/\2_ring_summary.tab/\3',
                                 r'metadata/COUVIS_0xxx/\2/\2_moon_summary.tab/\3',
                                 r'metadata/COUVIS_0xxx/\2/\2_jupiter_summary.tab/\3']),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews)/COUVIS_0xxx(|_v[0-9\.]+)/COUVIS_0.../DATA(|/\w+)', 0, (True, True, True)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'(volumes|previews)/COUVIS_0xxx(|_v[0-9\.]+)/COUVIS_..../DATA',     0, r'\1/COUVIS_0xxx\2/*/DATA'),
    (r'(volumes|previews)/COUVIS_0xxx(|_v[0-9\.]+)/COUVIS_..../DATA/\w+', 0, r'\1/COUVIS_0xxx\2/*/DATA/*'),
    (r'volumes/COUVIS_0xxx(|_v[0-9\.]+)/COUVIS_.../CALIB/VERSION_.',      0, r'volumes/COUVIS_0xxx\1/CALIB/VERSION*'),
    (r'volumes/COUVIS_0xxx(|_v[0-9\.]+)/COUVIS_.../CALIB/VERSION_./\w+',  0, r'volumes/COUVIS_0xxx\1/CALIB/VERSION*/*'),
])

####################################################################################################################################
# SORT_KEY
####################################################################################################################################

sort_key = translator.TranslatorByRegex([
    (r'(EUV|FUV|HSP|HDAC)([0-9]{4}_[0-9]{3}_[0-9]{2}_[0-9]{2}.*)_full(\..*)',   0, r'\2\1_1full\3'),
    (r'(EUV|FUV|HSP|HDAC)([0-9]{4}_[0-9]{3}_[0-9]{2}_[0-9]{2}.*)_med(\..*)',    0, r'\2\1_2med\3'),
    (r'(EUV|FUV|HSP|HDAC)([0-9]{4}_[0-9]{3}_[0-9]{2}_[0-9]{2}.*)_small(\..*)',  0, r'\2\1_3small\3'),
    (r'(EUV|FUV|HSP|HDAC)([0-9]{4}_[0-9]{3}_[0-9]{2}_[0-9]{2}.*)_thumb(\..*)',  0, r'\2\1_4thumb\3'),
    (r'(EUV|FUV|HSP|HDAC)([0-9]{4}_[0-9]{3}_[0-9]{2}_[0-9]{2}.*)',              0, r'\2\1'),
])

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/.*/DATA/.*\.DAT',  0, ('Cassini UVIS', 10, 'couvis_raw',        'Raw Data',         True)),
    (r'volumes/.*/CALIB/.*\.DAT', 0, ('Cassini UVIS', 20, 'couvis_calib_corr', 'Calibration Data', True)),
])

####################################################################################################################################
# OPUS_FORMAT
####################################################################################################################################

opus_format = translator.TranslatorByRegex([
    (r'.*\.DAT', 0, ('Binary', 'Unformatted')),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

opus_products = translator.TranslatorByRegex([
    (r'.*/COUVIS_0xxx(|_v[0-9\.]+)/(COUVIS_0...)/DATA/(\w+/\w+[0-9])(|_CAL.*|_[a-z]+)\..*', 0,
                    [r'volumes/COUVIS_0xxx*/\2/DATA/\3.DAT',
                     r'volumes/COUVIS_0xxx*/\2/DATA/\3.LBL',
                     r'volumes/COUVIS_0xxx*/\2/CALIB/VERSION_3/\3_CAL_3.DAT',
                     r'volumes/COUVIS_0xxx*/\2/CALIB/VERSION_3/\3_CAL_3.LBL',
                     r'volumes/COUVIS_0xxx*/\2/CALIB/VERSION_4/\3_CAL_4.DAT',
                     r'volumes/COUVIS_0xxx*/\2/CALIB/VERSION_4/\3_CAL_4.LBL',
                     r'volumes/COUVIS_0xxx*/\2/CALIB/VERSION_5/\3_CAL_5.DAT',
                     r'volumes/COUVIS_0xxx*/\2/CALIB/VERSION_5/\3_CAL_5.LBL',
                     r'previews/COUVIS_0xxx/\2/DATA/\3_full.png',
                     r'previews/COUVIS_0xxx/\2/DATA/\3_med.png',
                     r'previews/COUVIS_0xxx/\2/DATA/\3_small.png',
                     r'previews/COUVIS_0xxx/\2/DATA/\3_thumb.png',
                     r'metadata/COUVIS_0xxx/\2/\2_moon_summary.tab',
                     r'metadata/COUVIS_0xxx/\2/\2_moon_summary.lbl',
                     r'metadata/COUVIS_0xxx/\2/\2_ring_summary.tab',
                     r'metadata/COUVIS_0xxx/\2/\2_ring_summary.lbl',
                     r'metadata/COUVIS_0xxx/\2/\2_saturn_summary.tab',
                     r'metadata/COUVIS_0xxx/\2/\2_saturn_summary.lbl',
                     r'metadata/COUVIS_0xxx/\2/\2_index.tab',
                     r'metadata/COUVIS_0xxx/\2/\2_index.lbl',
                     r'metadata/COUVIS_0xxx/\2/\2_supplemental_index.tab',
                     r'metadata/COUVIS_0xxx/\2/\2_supplemental_index.lbl',
                    ]),
])

####################################################################################################################################
# OPUS_ID
####################################################################################################################################

opus_id = translator.TranslatorByRegex([
    (r'.*/COUVIS_0.*/(EUV|FUV|HDAC|HSP)(\d{4}_\d{3}_\d\d_\d\d)(|_\d\d)(|_CAL_\d|_[a-z]+)\..*',  0, r'co-uvis-#LOWER#\1\2\3'),
])

####################################################################################################################################
# OPUS_ID_TO_PRIMARY_LOGICAL_PATH
####################################################################################################################################

opus_id_to_primary_logical_path = translator.TranslatorByRegex([
    (r'co-uvis-(euv|fuv|hdac|hsp)(19.._...)_(.*)', 0,  r'volumes/COUVIS_0xxx/COUVIS_0001/DATA/D\2/#UPPER#\1\2_\3.DAT'),
    (r'co-uvis-(euv|fuv|hdac|hsp)(2000_...)_(.*)', 0,  r'volumes/COUVIS_0xxx/COUVIS_0001/DATA/D\2/#UPPER#\1\2_\3.DAT'),
    (r'co-uvis-(euv|fuv|hdac|hsp)(2001_...)_(.*)', 0,  r'volumes/COUVIS_0xxx/COUVIS_000[23]/DATA/D\2/#UPPER#\1\2_\3.DAT'),
    (r'co-uvis-(euv|fuv|hdac|hsp)(2002_...)_(.*)', 0,  r'volumes/COUVIS_0xxx/COUVIS_0004/DATA/D\2/#UPPER#\1\2_\3.DAT'),
    (r'co-uvis-(euv|fuv|hdac|hsp)(2003_...)_(.*)', 0,  r'volumes/COUVIS_0xxx/COUVIS_000[56]/DATA/D\2/#UPPER#\1\2_\3.DAT'),
    (r'co-uvis-(euv|fuv|hdac|hsp)(2004_...)_(.*)', 0, [r'volumes/COUVIS_0xxx/COUVIS_000[6-9]/DATA/D\2/#UPPER#\1\2_\3.DAT',
                                                       r'volumes/COUVIS_0xxx/COUVIS_0010/DATA/D\2/#UPPER#\1\2_\3.DAT']),
    (r'co-uvis-(euv|fuv|hdac|hsp)(2005_...)_(.*)', 0,  r'volumes/COUVIS_0xxx/COUVIS_001[0-3]/DATA/D\2/#UPPER#\1\2_\3.DAT'),
    (r'co-uvis-(euv|fuv|hdac|hsp)(2006_...)_(.*)', 0,  r'volumes/COUVIS_0xxx/COUVIS_001[4-7]/DATA/D\2/#UPPER#\1\2_\3.DAT'),
    (r'co-uvis-(euv|fuv|hdac|hsp)(2007_...)_(.*)', 0, [r'volumes/COUVIS_0xxx/COUVIS_001[8-9]/DATA/D\2/#UPPER#\1\2_\3.DAT',
                                                       r'volumes/COUVIS_0xxx/COUVIS_002[0-1]/DATA/D\2/#UPPER#\1\2_\3.DAT']),
    (r'co-uvis-(euv|fuv|hdac|hsp)(2008_...)_(.*)', 0,  r'volumes/COUVIS_0xxx/COUVIS_002[2-5]/DATA/D\2/#UPPER#\1\2_\3.DAT'),
    (r'co-uvis-(euv|fuv|hdac|hsp)(2009_...)_(.*)', 0,  r'volumes/COUVIS_0xxx/COUVIS_002[6-9]/DATA/D\2/#UPPER#\1\2_\3.DAT'),
    (r'co-uvis-(euv|fuv|hdac|hsp)(2010_...)_(.*)', 0,  r'volumes/COUVIS_0xxx/COUVIS_003[0-3]/DATA/D\2/#UPPER#\1\2_\3.DAT'),
    (r'co-uvis-(euv|fuv|hdac|hsp)(2011_...)_(.*)', 0,  r'volumes/COUVIS_0xxx/COUVIS_003[4-7]/DATA/D\2/#UPPER#\1\2_\3.DAT'),
    (r'co-uvis-(euv|fuv|hdac|hsp)(2012_...)_(.*)', 0, [r'volumes/COUVIS_0xxx/COUVIS_003[8-9]/DATA/D\2/#UPPER#\1\2_\3.DAT',
                                                       r'volumes/COUVIS_0xxx/COUVIS_004[0-1]/DATA/D\2/#UPPER#\1\2_\3.DAT']),
    (r'co-uvis-(euv|fuv|hdac|hsp)(2013_...)_(.*)', 0,  r'volumes/COUVIS_0xxx/COUVIS_004[2-5]/DATA/D\2/#UPPER#\1\2_\3.DAT'),
    (r'co-uvis-(euv|fuv|hdac|hsp)(2014_...)_(.*)', 0,  r'volumes/COUVIS_0xxx/COUVIS_004[6-9]/DATA/D\2/#UPPER#\1\2_\3.DAT'),
    (r'co-uvis-(euv|fuv|hdac|hsp)(2015_...)_(.*)', 0,  r'volumes/COUVIS_0xxx/COUVIS_005[0-3]/DATA/D\2/#UPPER#\1\2_\3.DAT'),
    (r'co-uvis-(euv|fuv|hdac|hsp)(2016_...)_(.*)', 0,  r'volumes/COUVIS_0xxx/COUVIS_005[4-7]/DATA/D\2/#UPPER#\1\2_\3.DAT'),
    (r'co-uvis-(euv|fuv|hdac|hsp)(2017_...)_(.*)', 0, [r'volumes/COUVIS_0xxx/COUVIS_005[8-9]/DATA/D\2/#UPPER#\1\2_\3.DAT',
                                                       r'volumes/COUVIS_0xxx/COUVIS_0060/DATA/D\2/#UPPER#\1\2_\3.DAT']),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class COUVIS_0xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('COUVIS_0xxx', re.I, 'COUVIS_0xxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS
    SORT_KEY = sort_key + pdsfile.PdsFile.SORT_KEY

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_FORMAT = opus_format + pdsfile.PdsFile.OPUS_FORMAT
    OPUS_PRODUCTS = opus_products
    OPUS_ID = opus_id
    OPUS_ID_TO_PRIMARY_LOGICAL_PATH = opus_id_to_primary_logical_path

    VIEWABLES = {'default': default_viewables}

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']  = associations_to_volumes
    ASSOCIATIONS['previews'] = associations_to_previews
    ASSOCIATIONS['metadata'] = associations_to_metadata

    ############################################################################
    # DATA_SET_ID is defined as a function rather than a translator
    ############################################################################

    VERSIONS_PATH_AND_KEY = translator.TranslatorByRegex([
        (r'volumes/COUVIS_0xxx(|_v\d)/(COUVIS_0...)/(.*)/(\w+)\.(DAT|LBL)', 0,
                    (r'metadata/COUVIS_0xxx/\2/\2\1_versions.tab', r'\4.LBL'))
    ])

    def DATA_SET_ID(self):
        """Look up the ID of this product using one of the "versions" indices in
        the metadata tree."""

        result = COUVIS_0xxx.VERSIONS_PATH_AND_KEY.first(self.logical_path)
        if not result:
            return ''

        (versions_path, key) = result
        versions_table = pdsfile.PdsFile.from_logical_path(versions_path)
        row = versions_table.child_of_index(key)
        if not row.exists:
            return ''

        return row.row_dicts[0].get('DATA_SET_ID', '')

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS = translator.TranslatorByRegex([(r'co-uvis-[efh].*', 0, COUVIS_0xxx)]) + \
                                      pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COUVIS_0xxx'] = COUVIS_0xxx

####################################################################################################################################
