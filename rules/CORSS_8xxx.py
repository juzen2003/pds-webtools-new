####################################################################################################################################
# rules/CORSS_8xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*/data/Rev(...)',               re.I, (r'Data for Cassini orbit \1',         'DATADIR')),
    (r'volumes/.*/data/Rev(...)/Rev\w+E',       re.I, (r'Data for Cassini orbit \1 egress',  'SERIESDIR')),
    (r'volumes/.*/data/Rev(...)/Rev\w+I',       re.I, (r'Data for Cassini orbit \1 ingress', 'SERIESDIR')),
    (r'volumes/.*/Rev\w+_([KSX])(\d\d)_[IE]',   re.I, (r'\1-band data from DSN ground station \2', 'SERIESDIR')),

    (r'volumes/.*/RSS\w+_CAL\.TAB',             re.I, ('Calibration parameters',      'TABLE')),
    (r'volumes/.*/RSS\w+_DLP_.*\.TAB',          re.I, ('Diffraction-limited profile', 'TABLE')),
    (r'volumes/.*/RSS\w+_GEO\.TAB',             re.I, ('Geometry table',              'TABLE')),
    (r'volumes/.*/RSS\w+_TAU.*\.TAB',           re.I, ('Optical depth profile',       'SERIES')),
    (r'volumes/.*/Rev\w+_Summary.*\.pdf',       re.I, ('Observation description',     'INFO')),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl', re.I, ''),
    (r'volumes/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/(browse|data)/(.*)\.pdf',
                            0,  r'previews/CORSS_8xxx/\2/\3/\4_*'),
    (r'volumes/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/(data/Rev.../Rev...C?[IE])',
                            0,  r'previews/CORSS_8xxx/\2/\3_*'),
    (r'volumes/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/(data/Rev.../Rev...C?[IE])/(Rev...C?[IE])_(RSS\w+)',
                            0,  r'previews/CORSS_8xxx/\2/\3/\4_\5/\5_GEO_*'),
    (r'volumes/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/(data/.*)_(TAU|GEO).*\.TAB',
                            0,  r'previews/CORSS_8xxx/\2/\3_\4_*'),

    (r'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev(..)(C?[IE])_RSS_(\w+)/(\w+)_(Summary|GEO|TAU)(\.pdf|\.TAB|_.*M\.TAB)',
                            0,  r'previews/CORSS_8xxx/CORSS_8001/data/Rev0\1/Rev0\1\2/Rev0\1\2_RSS_\3/\4_\5*'),
    (r'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev(..)(C?[IE])_RSS_(\w+)',
                            0,  r'previews/CORSS_8xxx/CORSS_8001/data/Rev0\1/Rev0\1\2/Rev0\1\2_RSS_\3'),
])

diagram_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl', re.I, ''),
    (r'volumes/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8.../data/Rev.../(Rev...C?[IE])_RSS\w+)(|/.*)',
                            0,  r'previews/CORSS_8xxx/\2_*'),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'.*/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/(data|browse)',
                                0, [r'volumes/CORSS_8xxx\1/\2/data',
                                    r'volumes/CORSS_8xxx\1/\2/browse']),
    (r'.*/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/(data|browse)/(Rev...)(|_OccTrack_Geometry.*|.*\.jpg)',
                                0, [r'volumes/CORSS_8xxx\1/\2/data/\4',
                                    r'volumes/CORSS_8xxx\1/\2/browse/\4_OccTrack_Geometry.LBL',
                                    r'volumes/CORSS_8xxx\1/\2/browse/\4_OccTrack_Geometry.pdf']),
    (r'.*/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/data/(Rev.../Rev...C?[IE])(|\w+\..*)',
                                0,  r'volumes/CORSS_8xxx\1/\2/data/\3'),
    (r'.*/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/data/(Rev.../Rev...C?[IE]/Rev...\w+)',
                                0,  r'volumes/CORSS_8xxx\1/\2/data/\3'),
    (r'.*/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/data/(Rev.../Rev...C?[IE]/Rev...\w+/\w+)_(Summary|GEO|TAU).*',
                                0, [r'volumes/CORSS_8xxx\1/\2/data/\3_\4.LBL',
                                    r'volumes/CORSS_8xxx\1/\2/data/\3_\4.pdf']),
])

associations_to_diagrams = translator.TranslatorByRegex([
    (r'.*/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/(data|browse|EASYDATA)',
                                0, r'diagrams/CORSS_8xxx/\2/data'),
    (r'.*/CORSS_8xxx(|_v[0-9\.]+)/(COISS_8...)/(data|browse)/(Rev...)(|_OccTrack_Geometry.*|.*\.jpg)',
                                0, r'diagrams/CORSS_8xxx/\2/data/\4'),
    (r'.*/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/data/(Rev.../Rev...C?[IE]).*',
                                0, r'diagrams/CORSS_8xxx/\2/data/\3_*'),

    (r'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev(..)(C?[IE])_RSS_(\w+)',
                                0, r'diagrams/CORSS_8xxx/CORSS_8001/data/Rev0\1/Rev0\1\2_RSS_\3_*'),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'.*/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/(data|browse)',
                                0, [r'previews/CORSS_8xxx/\2/data',
                                    r'previews/CORSS_8xxx/\2/browse']),
    (r'.*/CORSS_8xxx(|_v[0-9\.]+)/(COISS_8...)/(data|browse)/(Rev...)(|_OccTrack_Geometry.*|.*\.jpg)',
                                0, [r'previews/CORSS_8xxx/\2/data/\4',
                                    r'previews/CORSS_8xxx/\2/browse/\4_OccTrack_Geometry_*']),
    (r'.*/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/data/(Rev.../Rev...C?[IE])(|\w+\..*)',
                                0,  r'previews/CORSS_8xxx/\2/data/\3_*'),
    (r'.*/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/data/(Rev.../Rev...C?[IE]/Rev...\w+)',
                                0,  r'previews/CORSS_8xxx\1/\2/data/\3'),
    (r'.*/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/data/(Rev.../Rev...C?[IE]/Rev...\w+/\w+)_(Summary|GEO|TAU).*',
                                0,  r'previews/CORSS_8xxx\1/\2/data/\3_\4_*'),

    (r'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev(..)(C?[IE])_RSS_(\w+)',
                                0,  r'previews/CORSS_8xxx/CORSS_8001/data/Rev0\1/Rev0\1\2/Rev0\1\2_RSS_\3'),
    (r'volumes/CORSS_8xxx_v1/CORSS_8001/EASYDATA/Rev(..)(C?[IE])_RSS_(\w+)/(\w+)_(Summary|GEO|TAU).*',
                                0,  r'previews/CORSS_8xxx/CORSS_8001/data/Rev0\1/Rev0\1\2/Rev0\1\2_RSS_\3/\4_\5*'),

])

associations_to_metadata = translator.TranslatorByRegex([
    (r'volumes/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/data.*/(\w+)\..*',
                                0,  r'metadata/CORSS_8xxx/\2/\2_index.tab/\3.LBL'),
    (r'volumes/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/data.*/(\w+)_TAU.*',
                                0, [r'metadata/CORSS_8xxx/\2/\2_profile_index.tab/\3_TAU_01KM',
                                    r'metadata/CORSS_8xxx/\2/\2_profile_index.tab/\3_TAU_1400M',
                                    r'metadata/CORSS_8xxx/\2/\2_profile_index.tab/\3_TAU_1600M',
                                    r'metadata/CORSS_8xxx/\2/\2_profile_index.tab/\3_TAU_2400M',
                                    r'metadata/CORSS_8xxx/\2/\2_profile_index.tab/\3_TAU_3000M',
                                    r'metadata/CORSS_8xxx/\2/\2_profile_index.tab/\3_TAU_4000M',
                                    r'metadata/CORSS_8xxx/\2/\2_supplemental_index.tab/\3_TAU_01KM',
                                    r'metadata/CORSS_8xxx/\2/\2_supplemental_index.tab/\3_TAU_1400M',
                                    r'metadata/CORSS_8xxx/\2/\2_supplemental_index.tab/\3_TAU_1600M',
                                    r'metadata/CORSS_8xxx/\2/\2_supplemental_index.tab/\3_TAU_2400M',
                                    r'metadata/CORSS_8xxx/\2/\2_supplemental_index.tab/\3_TAU_3000M',
                                    r'metadata/CORSS_8xxx/\2/\2_supplemental_index.tab/\3_TAU_4000M']),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|diagrams|previews)/.*/(data|browse)/.*', 0, (True, True, True )),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'(.*)/Rev...',                    0, r'\1/Rev*'),
    (r'(.*)/Rev.../Rev...C?[IE]',       0, r'\1/Rev*/Rev*[IE]'),
    (r'(.*)/Rev.../Rev...C?[IE]/Rev.*', 0, r'\1/Rev*/Rev*/Rev*'),
    (r'(.*)/EASYDATA/Rev\w+',           0, r'\1/EASYDATA/*'),
])

####################################################################################################################################
# SPLIT_RULES
####################################################################################################################################

split_rules = translator.TranslatorByRegex([
    (r'(RSS_...._..._\w+_[IE])_(TAU\w+)\.(.*)', 0, (r'\1', r'_\2', r'.\3')),
])

####################################################################################################################################
# OPUS_TYPE
#
# Used for indicating the type of a data file as it will appear in OPUS, e.g., "Raw Data", "Calibrated Data", etc. The tuple
# returned is (category, rank, slug, title) where:
#   category is 'browse', 'diagram', or a meaningful header for special cases like 'Voyager ISS', 'Cassini CIRS'
#   rank is the sort order within the category
#   slug is a short string that will appear in URLs
#   title is a meaning title for product, e.g., 'Raw Data (when calibrated is unavailable)'
#
# These translations take a file's logical path and return a string indicating the file's OPUS_TYPE.
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/.*_TAU_01KM\.(TAB|LBL)',  0, ('Cassini RSS', 10, 'corss_occ_best_res', 'Occultation Profile (~1 km res)', True)),
    (r'volumes/.*_TAU_1400M\.(TAB|LBL)', 0, ('Cassini RSS', 10, 'corss_occ_best_res', 'Occultation Profile (~1 km res)', True)),
    (r'volumes/.*_TAU_1600M\.(TAB|LBL)', 0, ('Cassini RSS', 10, 'corss_occ_best_res', 'Occultation Profile (~1 km res)', True)),
    (r'volumes/.*_TAU_2400M\.(TAB|LBL)', 0, ('Cassini RSS', 10, 'corss_occ_best_res', 'Occultation Profile (~1 km res)', True)),
    (r'volumes/.*_TAU_3000M\.(TAB|LBL)', 0, ('Cassini RSS', 10, 'corss_occ_best_res', 'Occultation Profile (~1 km res)', True)),
    (r'volumes/.*_TAU_4000M\.(TAB|LBL)', 0, ('Cassini RSS', 10, 'corss_occ_best_res', 'Occultation Profile (~1 km res)', True)),
    (r'volumes/.*_TAU_10KM\.(TAB|LBL)',  0, ('Cassini RSS', 20, 'corss_occ_10km_res', 'Occultation Profile (10 km res)', True)),

    (r'volumes/.*_DLP_500M\.(TAB|LBL)',  0, ('Cassini RSS', 30, 'corss_occ_dlp', 'Diffraction-Ltd Occultation Profile', True)),
    (r'volumes/.*_CAL\.(TAB|LBL)',       0, ('Cassini RSS', 40, 'corss_occ_cal', 'Occultation Calibration Parameters',  True)),
    (r'volumes/.*_GEO\.(TAB|LBL)',       0, ('Cassini RSS', 50, 'corss_occ_geo', 'Occultation Geometry Parameters',     True)),

    (r'volumes/.*_(DSN_Elevation|TimeLine_Figure|TimeLine_Table|Summary|OccTrack_Geometry)\.(pdf|LBL)',
                                         0, ('Cassini RSS', 60, 'corss_occ_doc', 'Occultation Documentation', True)),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

opus_products = translator.TranslatorByRegex([
    (r'.*/CORSS_8xxx(|_v[0-9\.]+)/(CORSS_8...)/.*/(Rev...)(C?[IE])_(RSS_...._..._..._[EI]).*', 0,
                [r'volumes/CORSS_8xxx*/\2/data/\3/\3\4/\3\4_\5/*',
                 r'volumes/CORSS_8xxx*/\2/EASYDATA/\3\4_\5/*',
                 r'volumes/CORSS_8xxx*/\2/browse/\3_OccTrack_Geometry.LBL',
                 r'volumes/CORSS_8xxx*/\2/browse/\3_OccTrack_Geometry.pdf',
                 r'previews/CORSS_8xxx/\2/data/\3/\3\4/\3\4_\5/*',
                 r'metadata/CORSS_8xxx/\2/CORSS_8001_*index.*',
                 ]),
])

####################################################################################################################################
# OPUS_ID
####################################################################################################################################

opus_id = translator.TranslatorByRegex([
    (r'.*/CORSS_8xxx.*/CORSS_8.../(data|browse).*/(Rev...C?)[IE]_RSS_(....)_(...)_(...)_([IE]).*', 0,
                        r'co-rss-occ-\3-\4-#LOWER#\2-\5-\6'),
    (r'.*/CORSS_8xxx_v1/CORSS_8.../EASYDATA.*/Rev(\d\d)(C?)[IE]_RSS_(....)_(...)_(...)_([IE]).*', 0,
                        r'co-rss-occ-\3-\4-#LOWER#rev0\1\2-\5-\6'),
])

####################################################################################################################################
# OPUS_ID_TO_PRIMARY_LOGICAL_PATH
####################################################################################################################################

opus_id_to_primary_logical_path = translator.TranslatorByRegex([
  (r'co-rss-occ-rev(...)(c?)(i|e)-(\d{4})-(\d{3})-(\w{3})', 0,
    [r'volumes/CORSS_8xxx/CORSS_8001/data/Rev\1/Rev\1#UPPER#\2\3#MIXED#/Rev\1#UPPER#\2\3_RSS_\4_\5_\6_\3/RSS_\4_\5_\6_\3_TAU_01KM.TAB',
     r'volumes/CORSS_8xxx/CORSS_8001/data/Rev\1/Rev\1#UPPER#\2\3#MIXED#/Rev\1#UPPER#\2\3_RSS_\4_\5_\6_\3/RSS_\4_\5_\6_\3_TAU_*00M.TAB']),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class CORSS_8xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('CORSS_8xxx', re.I, 'CORSS_8xxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS
    SPLIT_RULES = split_rules + pdsfile.PdsFile.SPLIT_RULES

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_PRODUCTS = opus_products
    OPUS_ID = opus_id
    OPUS_ID_TO_PRIMARY_LOGICAL_PATH = opus_id_to_primary_logical_path

    VIEWABLES = {
        'default': default_viewables,
        'diagram': diagram_viewables,
    }

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']  = associations_to_volumes
    ASSOCIATIONS['previews'] = associations_to_previews
    ASSOCIATIONS['diagrams'] = associations_to_diagrams
    ASSOCIATIONS['metadata'] = associations_to_metadata

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS = translator.TranslatorByRegex([(r'co-rss-occ-.*', 0, CORSS_8xxx)]) + \
                                      pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['CORSS_8xxx'] = CORSS_8xxx

####################################################################################################################################
