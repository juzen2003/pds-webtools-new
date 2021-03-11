####################################################################################################################################
# rules/EBROCC_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*/DATA',         re.I, ('Data files by observatory',      'SERIESDIR')),
    (r'volumes/.*/DATA/\w+',     re.I, ('Data files by observatory',      'SERIESDIR')),
    (r'volumes/.*/GEOMETRY/\w+', re.I, ('Geometry files by observatory',  'GEOMDIR' )),
    (r'volumes/.*/BROWSE/\w+',   re.I, ('Browse diagrams by observatory', 'BROWDIR' )),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl', re.I, ''),
    (r'volumes/EBROCC_xxxx(|_v[0-9\.]+)/(EBROCC_....)/(DATA|BROWSE)/(\w+/\w+)\.TAB',
                            0,  (r'previews/EBROCC_xxxx/\2/\3/\4_full.jpg',
                                 r'previews/EBROCC_xxxx/\2/\3/\4_med.jpg',
                                 r'previews/EBROCC_xxxx/\2/\3/\4_small.jpg',
                                 r'previews/EBROCC_xxxx/\2/\3/\4_thumb.jpg')),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'.*/EBROCC_xxxx(|_v[0-9\.]+)/(EBROCC_....)/(DATA|BROWSE|SORCDATA|GEOMETRY)(|/\w+)',
                            0,  [r'volumes/EBROCC_xxxx\1/\2/DATA\4',
                                 r'volumes/EBROCC_xxxx\1/\2/BROWSE\4',
                                 r'volumes/EBROCC_xxxx\1/\2/GEOMETRY\4',
                                 r'volumes/EBROCC_xxxx\1/\2/SORCDATA\4']),
    (r'.*/EBROCC_xxxx(|_v[0-9\.]+)/(EBROCC_....)/(DATA|BROWSE|SORCDATA|GEOMETRY)/(\w+/\w{3}_[EI]).*',
                            0,  [r'volumes/EBROCC_xxxx\1/\2/DATA\4PD.*',
                                 r'volumes/EBROCC_xxxx\1/\2/BROWSE\4GB.*',
                                 r'volumes/EBROCC_xxxx\1/\2/GEOMETRY\4GD.*',
                                 r'volumes/EBROCC_xxxx\1/\2/SORCDATA\4*']),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'.*/EBROCC_xxxx(|_v[0-9\.]+)/(EBROCC_....)/(DATA|BROWSE|SORCDATA|GEOMETRY)(|/\w+)',
                            0,  [r'previews/EBROCC_xxxx/\2/DATA\4',
                                 r'previews/EBROCC_xxxx/\2/BROWSE\4',
                                 r'previews/EBROCC_xxxx/\2/GEOMETRY\4',
                                 r'previews/EBROCC_xxxx/\2/SORCDATA\4']),
    (r'.*/EBROCC_xxxx(|_v[0-9\.]+)/(EBROCC_....)/(DATA|BROWSE|SORCDATA|GEOMETRY)/(\w+/\w{3}_[EI]).*',
                            0,  [r'previews/EBROCC_xxxx/\2/DATA\4PD_*.jpg',
                                 r'previews/EBROCC_xxxx/\2/BROWSE\4GB_*.jpg']),
])

associations_to_metadata = translator.TranslatorByRegex([
    (r'volumes/EBROCC_xxxx(|_v[0-9\.]+)/(EBROCC_....)/(DATA|BROWSE|SORCDATA|GEOMETRY)/\w+/(\w+)\.\w+',
                            0,   r'metadata/EBROCC_xxxx/\2/\2_index.tab/\4'),
    (r'volumes/EBROCC_xxxx(|_v[0-9\.]+)/(EBROCC_....)/DATA/\w+/(\w+)\.\w+',
                            0,  [r'metadata/EBROCC_xxxx/\2/\2_profile_index.tab/\4',
                                 r'metadata/EBROCC_xxxx/\2/\2_supplemental_index.tab/\4']),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews)/EBROCC_xxxx.*/(DATA|BROWSE|SORCDATA|GEOMETRY)/.*', 0, (True, True, False)),
])

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/EBROCC_xxxx.*/EBROCC_..../DATA/\w+/\w+\.(TAB|LBL)',          0, ('Earth-based Occultations',  0, 'ebro_profile', 'Radial Profile',   True)),
    (r'volumes/EBROCC_xxxx.*/EBROCC_..../GEOMETRY/\w+/\w+\.(TAB|LBL)',      0, ('Earth-based Occultations', 10, 'ebro_geom',    'Geometry Table',   True)),
    (r'volumes/EBROCC_xxxx.*/EBROCC_..../BROWSE/\w+/\w+PB\.(PDF|PS|LBL)',   0, ('Earth-based Occultations', 20, 'ebro_preview', 'Preview Plot',     True)),
    (r'volumes/EBROCC_xxxx.*/EBROCC_..../BROWSE/\w+/\w+GB\.(PDF|PS|LBL)',   0, ('Earth-based Occultations', 30, 'ebro_diagram', 'Geometry Diagram', False)),
    (r'volumes/EBROCC_xxxx.*/EBROCC_..../SORCDATA/\w+/\w+_GEOMETRY\..*',    0, ('Earth-based Occultations', 40, 'ebro_source',  'Source Data',      False)),
    (r'volumes/EBROCC_xxxx.*/EBROCC_..../SORCDATA/\w+/\w+GRESS\.(OUT|LBL)', 0, ('Earth-based Occultations', 40, 'ebro_source',  'Source Data',      False)),
])

####################################################################################################################################
# OPUS_FORMAT
####################################################################################################################################

opus_format = translator.TranslatorByRegex([
    (r'.*\_GEOMETRY.DAT',    0, ('ASCII', 'Text')),
    (r'.*\_(E|IN)GRESS.OUT', 0, ('ASCII', 'Text')),
    (r'.*\.jpeg_small$',     0, ('Binary', 'JPEG')),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

opus_products = translator.TranslatorByRegex([
    (r'.*/EBROCC_xxxx(|_v[0-9\.]+)/(EBROCC_....)/(DATA|BROWSE|SORCDATA|GEOMETRY)/(\w+/\w{3}_[EI]).*', 0,
                    [r'volumes/EBROCC_xxxx*/\2/DATA/\4PD.LBL',
                     r'volumes/EBROCC_xxxx*/\2/DATA/\4PD.TAB',
                     r'volumes/EBROCC_xxxx*/\2/BROWSE/\4GB.*',
                     r'volumes/EBROCC_xxxx*/\2/BROWSE/\4PB.*',
                     r'volumes/EBROCC_xxxx*/\2/GEOMETRY/\4GD.*',
                     r'volumes/EBROCC_xxxx*/\2/SORCDATA/\4*',
                     r'previews/EBROCC_xxxx/\2/DATA/\4PD_*.jpg',
                     r'previews/EBROCC_xxxx/\2/BROWSE/\4GB_*.jpg',
                     r'metadata/EBROCC_xxxx/\2_*index.*',
                     ]),
])

####################################################################################################################################
# OPUS_ID
####################################################################################################################################

opus_id = translator.TranslatorByRegex([
    (r'.*/EBROCC_xxxx.*/\w+/ESO1M/ES1_(I|E).*',  0, r'eso1m-apph-occ-1989-184-28sgr-#LOWER#\1'),
    (r'.*/EBROCC_xxxx.*/\w+/ESO22M/ES2_(I|E).*', 0, r'eso22m-apph-occ-1989-184-28sgr-#LOWER#\1'),
    (r'.*/EBROCC_xxxx.*/\w+/IRTF/IRT_(I|E).*',   0, r'irtf-urac-occ-1989-184-28sgr-#LOWER#\1'),
    (r'.*/EBROCC_xxxx.*/\w+/LICK1M/LIC_(I|E).*', 0, r'lick1m-ccdc-occ-1989-184-28sgr-#LOWER#\1'),
    (r'.*/EBROCC_xxxx.*/\w+/MCD27M/MCD_(I|E).*', 0, r'mcd27m-iirar-occ-1989-184-28sgr-#LOWER#\1'),
    (r'.*/EBROCC_xxxx.*/\w+/PAL200/PAL_(I|E).*', 0, r'pal200-circ-occ-1989-184-28sgr-#LOWER#\1')
])

####################################################################################################################################
# OPUS_ID_TO_PRIMARY_LOGICAL_PATH
####################################################################################################################################

opus_id_to_primary_logical_path = translator.TranslatorByRegex([
    (r'eso1m-apph-occ-1989-184-28sgr-(.*)',   0, r'volumes/EBROCC_xxxx/EBROCC_0001/DATA/ESO1M/ES1_#UPPER#\1PD.TAB'),
    (r'eso22m-apph-occ-1989-184-28sgr-(.*)',  0, r'volumes/EBROCC_xxxx/EBROCC_0001/DATA/ESO22M/ES2_#UPPER#\1PD\.TAB'),
    (r'irtf-urac-occ-1989-184-28sgr-(.*)',    0, r'volumes/EBROCC_xxxx/EBROCC_0001/DATA/IRTF/IRT_#UPPER#\1PD\.TAB'),
    (r'lick1m-ccdc-occ-1989-184-28sgr-(.*)',  0, r'volumes/EBROCC_xxxx/EBROCC_0001/DATA/LICK1M/LIC_#UPPER#\1PD\.TAB'),
    (r'mcd27m-iirar-occ-1989-184-28sgr-(.*)', 0, r'volumes/EBROCC_xxxx/EBROCC_0001/DATA/MCD27M/MCD_#UPPER#\1PD\.TAB'),
    (r'pal200-circ-occ-1989-184-28sgr-(.*)',  0, r'volumes/EBROCC_xxxx/EBROCC_0001/DATA/PAL200/PAL_#UPPER#\1PD\.TAB'),
])

####################################################################################################################################
# DATA_SET_ID
####################################################################################################################################

data_set_id = translator.TranslatorByRegex([
    (r'.*volumes/EBROCC_xxxx/EBROCC_0001.*/(ES1|ESO1M).*',  0, r'ESO1M-SR-APPH-4-OCC-V1.0'),
    (r'.*volumes/EBROCC_xxxx/EBROCC_0001.*/(ES2|ESO22M).*', 0, r'ESO22M-SR-APPH-4-OCC-V1.0'),
    (r'.*volumes/EBROCC_xxxx/EBROCC_0001.*/IRT.*',          0, r'IRTF-SR-URAC-4-OCC-V1.0'),
    (r'.*volumes/EBROCC_xxxx/EBROCC_0001.*/LIC.*',          0, r'LICK1M-SR-CCDC-4-OCC-V1.0'),
    (r'.*volumes/EBROCC_xxxx/EBROCC_0001.*/MCD.*',          0, r'MCD27M-SR-IIRAR-4-OCC-V1.0'),
    (r'.*volumes/EBROCC_xxxx/EBROCC_0001.*/PAL.*',          0, r'PAL200-SR-CIRC-4-OCC-V1.0')
])

####################################################################################################################################
# FILESPEC_TO_VOLSET
####################################################################################################################################

filespec_to_volset = translator.TranslatorByRegex([
    (r'EBROCC_0001.*', 0, r'EBROCC_xxxx'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class EBROCC_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('EBROCC_xxxx', re.I, 'EBROCC_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS

    OPUS_TYPE = opus_type + pdsfile.PdsFile.OPUS_TYPE
    OPUS_FORMAT = opus_format + pdsfile.PdsFile.OPUS_FORMAT
    OPUS_PRODUCTS = opus_products
    OPUS_ID = opus_id
    OPUS_ID_TO_PRIMARY_LOGICAL_PATH = opus_id_to_primary_logical_path

    DATA_SET_ID = data_set_id

    VIEWABLES = {'default': default_viewables}

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']  = associations_to_volumes
    ASSOCIATIONS['previews'] = associations_to_previews
    ASSOCIATIONS['metadata'] = associations_to_metadata

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS = translator.TranslatorByRegex([(r'.*-28sgr-.*', 0, EBROCC_xxxx)]) + \
                                      pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS

pdsfile.PdsFile.FILESPEC_TO_VOLSET = filespec_to_volset + pdsfile.PdsFile.FILESPEC_TO_VOLSET

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['EBROCC_xxxx'] = EBROCC_xxxx

####################################################################################################################################
