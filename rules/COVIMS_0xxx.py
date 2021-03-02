####################################################################################################################################
# rules/COVIMS_0xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*/data',                                         re.I, ('Data files grouped by date',  'CUBEDIR')),
    (r'volumes/.*/data/\w+',                                     re.I, ('Data files grouped by date',  'CUBEDIR')),
    (r'volumes/.*/data.*\.qub',                                  re.I, ('Spectral image cube (ISIS2)', 'CUBE')),
    (r'volumes/.*/extras',                                       re.I, ('Browse image collection',     'BROWDIR')),
    (r'volumes/.*/data/.*/extras/\w+',                           re.I, ('Browse image collection',     'BROWDIR')),
    (r'volumes/.*/data/.*/extras/.*\.(jpeg|jpeg_small|tiff)',    re.I, ('Browse image',                'BROWSE' )),
    (r'volumes/.*/software.*cube_prep/cube_prep',                re.I, ('Program binary',              'CODE'   )),
    (r'volumes/.*/software.*/PPVL_report',                       re.I, ('Program binary',              'CODE'   )),
    (r'.*/thumbnail(/\w+)*',                                     re.I, ('Small browse images',         'BROWDIR' )),
    (r'.*/thumbnail/.*\.(gif|jpg|jpeg|jpeg_small|tif|tiff|png)', re.I, ('Small browse image',          'BROWSE'  )),
    (r'.*/tiff(/\w+)*',                                          re.I, ('Full-size browse images',     'BROWDIR' )),
    (r'.*/tiff/.*\.(gif|jpg|jpeg|jpeg_small|tif|tiff|png)',      re.I, ('Full-size browse image',      'BROWSE'  )),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl',  re.I, ''),

    (r'volumes/(.*/data/\w+/.*)\.(\w+)', 0, (r'previews/\1_thumb.png',
                                             r'previews/\1_small.png',
                                             r'previews/\1_med.png',
                                             r'previews/\1_full.png')),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'.*/COVIMS_0xxx(|_v[0-9\.]+)/(COVIMS_....)/(data|extras/\w+)/(\w+/v[0-9]{10}_[0-9]+)(_0[0-6][0-9]|).*',
                            0,  [r'volumes/COVIMS_0xxx\1/\2/data/\4\5.qub',
                                 r'volumes/COVIMS_0xxx\1/\2/data/\4\5.lbl',
                                 r'volumes/COVIMS_0xxx\1/\2/extras/thumbnail/\4\5.IMG.jpeg_small',
                                 r'volumes/COVIMS_0xxx\1/\2/extras/browse/\4\5.IMG.jpeg',
                                 r'volumes/COVIMS_0xxx\1/\2/extras/full/\4\5.IMG.png',
                                 r'volumes/COVIMS_0xxx\1/\2/extras/tiff/\4\5.IMG.tiff']),
    (r'.*/COVIMS_0xxx(|_v[0-9\.]+)/(COVIMS_....)/(data|extras/\w+)(|/\w+)',
                            0,  [r'volumes/COVIMS_0xxx\1/\2/data\4',
                                 r'volumes/COVIMS_0xxx\1/\2/extras/thumbnail\4',
                                 r'volumes/COVIMS_0xxx\1/\2/extras/browse\4',
                                 r'volumes/COVIMS_0xxx\1/\2/extras/full\4',
                                 r'volumes/COVIMS_0xxx\1/\2/extras/tiff\4']),
    (r'.*/COVIMS_0xxx(|_v[0-9\.]+)/(COVIMS_....)/extras',
                            0,   r'volumes/COVIMS_0xxx\1/\2/data'),
    (r'.*/COVIMS_0999.*',   0,  r'volumes/COVIMS_0xxx'),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'.*/COVIMS_0xxx(|_v[0-9\.]+)/(COVIMS_....)/(data|extras/\w+)/(\w+/v[0-9]{10}_[0-9]+)(_0[0-6][0-9]|).*',
                                0,  r'previews/COVIMS_0xxx/\2/data/\4\5_*.png'),
    (r'.*/COVIMS_0xxx(|_v[0-9\.]+)/(COVIMS_....)/(data|extras/\w+)(|/\w+)',
                                0,  r'previews/COVIMS_0xxx/\2/data\3'),
    (r'.*/COVIMS_0xxx(|_v[0-9\.]+)/(COVIMS_....)/extras',
                                0,  r'previews/COVIMS_0xxx/\2/data'),
    (r'.*/COVIMS_0999.*',       0,  r'previews/COVIMS_0xxx'),
])

associations_to_metadata = translator.TranslatorByRegex([
    (r'.*/COVIMS_0xxx(|_v[0-9\.]+)/(COVIMS_....)/(data|extras/\w+)/\w+/(v[0-9]{10}_[0-9]+)(_0[0-6][0-9]|).*',
                                0, [r'metadata/COVIMS_0xxx/\2/\2_index.tab/\4\5',
                                    r'metadata/COVIMS_0xxx/\2/\2_supplemental_index.tab/\4\5',
                                    r'metadata/COVIMS_0xxx/\2/\2_ring_summary.tab/\4\5',
                                    r'metadata/COVIMS_0xxx/\2/\2_moon_summary.tab/\4\5',
                                    r'metadata/COVIMS_0xxx/\2/\2_saturn_summary.tab/\4\5',
                                    r'metadata/COVIMS_0xxx/\2/\2_jupiter_summary.tab/\4\5']),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'.*/COVIMS_0.../(data|extras/w+)(|/.*)', 0, (True, True, True)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'(.*/COVIMS_0xxx.*)/(COVIMS_0...)/(data|extras/w+)/\w+', 0, r'\1/*/\3/*'),
    (r'(.*/COVIMS_0xxx.*)/(COVIMS_0...)/(data|extras/w+)',     0, r'\1/*/\3'),
])

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/.*\.(qub|lbl)$',                      0, ('Cassini VIMS',   0, 'covims_raw',    'Raw cube',                  True)),
    (r'volumes/.*/extras/thumbnail/.*\.jpeg_small$', 0, ('Cassini VIMS', 110, 'covims_thumb',  'Extra preview (thumbnail)', False)),
    (r'volumes/.*/extras/browse/.*\.jpeg$',          0, ('Cassini VIMS', 120, 'covims_medium', 'Extra preview (medium)',    False)),
    (r'volumes/.*/extras/(tiff|full)/.*\.\w+$',      0, ('Cassini VIMS', 130, 'covims_full',   'Extra preview (full)',      True)),
])

####################################################################################################################################
# OPUS_FORMAT
####################################################################################################################################

opus_format = translator.TranslatorByRegex([
    (r'.*\.qub$',        0, ('Binary', 'ISIS2')),
    (r'.*\.jpeg_small$', 0, ('Binary', 'JPEG')),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

opus_products = translator.TranslatorByRegex([
    (r'.*/COVIMS_0xxx(|_v[0-9\.]+)/(COVIMS_0...)/(data|extras/\w+)/(\w+/v[0-9]{10}_[0-9]+)(_0[0-6][0-9]|)\..*', 0,
            [r'volumes/COVIMS_0xxx*/\2/data/\4.qub',
             r'volumes/COVIMS_0xxx*/\2/data/\4.lbl',
             r'volumes/COVIMS_0xxx*/\2/extras/thumbnail/\4.qub.jpeg_small',
             r'volumes/COVIMS_0xxx*/\2/extras/browse/\4.qub.jpeg',
             r'volumes/COVIMS_0xxx*/\2/extras/full/\4.qub.png',
             r'volumes/COVIMS_0xxx*/\2/extras/tiff/\4.qub.tiff',
             r'previews/COVIMS_0xxx/\2/data/\4_*.png',
             r'metadata/COVIMS_0xxx/\2/\2_*summary.*',
             r'metadata/COVIMS_0xxx/\2/\2_inventory.*',
             r'metadata/COVIMS_0xxx/\2/\2_*index.*'
             ]),
])

####################################################################################################################################
# OPUS_ID
####################################################################################################################################

opus_id = translator.TranslatorByRegex([
    # There are up to two OPUS IDs associated with each VIMS file, one for the VIS channel and one for the IR channel.
    # This translator returns the OPUS ID without the suffix "_IR" or "_VIS" used by OPUS. That must be handled separately
    (r'.*/COVIMS_0xxx.*/(v[0-9]{10})_[0-9]+(|_[0-9]{3})\..*', 0, r'co-vims-\1\2'),
])

####################################################################################################################################
# OPUS_ID_TO_PRIMARY_LOGICAL_PATH
####################################################################################################################################

# By identifying the first three digits of the spacecraft clock with a range of volumes, we speed things up quite a bit
opus_id_to_primary_logical_path = translator.TranslatorByRegex([
    (r'co-vims-(v188.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_009[3-4]/data/*/\1_*\2.qub'),
    (r'co-vims-(v187.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_009[0-3]/data/*/\1_*\2.qub'),
    (r'co-vims-(v186.{7})(|_.{3})',     0, [r'volumes/COVIMS_0xxx/COVIMS_008[5-9]/data/*/\1_*\2.qub',
                                            r'volumes/COVIMS_0xxx/COVIMS_0090/data/*/\1_*\2.qub']),
    (r'co-vims-(v185.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_008[1-5]/data/*/\1_*\2.qub'),
    (r'co-vims-(v184.{7})(|_.{3})',     0, [r'volumes/COVIMS_0xxx/COVIMS_0079/data/*/\1_*\2.qub',
                                            r'volumes/COVIMS_0xxx/COVIMS_008[0-1]/data/*/\1_*\2.qub']),
    (r'co-vims-(v183.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_007[7-9]/data/*/\1_*\2.qub'),
    (r'co-vims-(v182.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_007[6-7]/data/*/\1_*\2.qub'),
    (r'co-vims-(v181.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_007[4-6]/data/*/\1_*\2.qub'),
    (r'co-vims-(v180.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_007[2-4]/data/*/\1_*\2.qub'),
    (r'co-vims-(v179.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_007[0-2]/data/*/\1_*\2.qub'),
    (r'co-vims-(v178.{7})(|_.{3})',     0, [r'volumes/COVIMS_0xxx/COVIMS_006[7-9]/data/*/\1_*\2.qub',
                                            r'volumes/COVIMS_0xxx/COVIMS_0070/data/*/\1_*\2.qub']),
    (r'co-vims-(v177.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_006[5-7]/data/*/\1_*\2.qub'),
    (r'co-vims-(v176.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_006[3-5]/data/*/\1_*\2.qub'),
    (r'co-vims-(v175.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_006[0-3]/data/*/\1_*\2.qub'),
    (r'co-vims-(v174.{7})(|_.{3})',     0, [r'volumes/COVIMS_0xxx/COVIMS_005[7-9]/data/*/\1_*\2.qub',
                                            r'volumes/COVIMS_0xxx/COVIMS_0060/data/*/\1_*\2.qub']),
    (r'co-vims-(v173.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_005[4-7]/data/*/\1_*\2.qub'),
    (r'co-vims-(v172.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_005[3-4]/data/*/\1_*\2.qub'),
    (r'co-vims-(v171.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_005[1-3]/data/*/\1_*\2.qub'),
    (r'co-vims-(v170.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_005[0-1]/data/*/\1_*\2.qub'),
    (r'co-vims-(v169.{7})(|_.{3})',     0, [r'volumes/COVIMS_0xxx/COVIMS_004[8-9]/data/*/\1_*\2.qub',
                                            r'volumes/COVIMS_0xxx/COVIMS_0050/data/*/\1_*\2.qub']),
    (r'co-vims-(v168.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_004[6-8]/data/*/\1_*\2.qub'),
    (r'co-vims-(v167.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_004[4-6]/data/*/\1_*\2.qub'),
    (r'co-vims-(v166.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_004[3-4]/data/*/\1_*\2.qub'),
    (r'co-vims-(v165.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_004[2-3]/data/*/\1_*\2.qub'),
    (r'co-vims-(v164.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_004[0-2]/data/*/\1_*\2.qub'),
    (r'co-vims-(v163.{7})(|_.{3})',     0, [r'volumes/COVIMS_0xxx/COVIMS_003[7-9]/data/*/\1_*\2.qub',
                                            r'volumes/COVIMS_0xxx/COVIMS_0040/data/*/\1_*\2.qub']),
    (r'co-vims-(v162.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_003[6-7]/data/*/\1_*\2.qub'),
    (r'co-vims-(v161.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_003[3-6]/data/*/\1_*\2.qub'),
    (r'co-vims-(v160.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_003[0-3]/data/*/\1_*\2.qub'),
    (r'co-vims-(v159.{7})(|_.{3})',     0, [r'volumes/COVIMS_0xxx/COVIMS_002[7-9]/data/*/\1_*\2.qub',
                                            r'volumes/COVIMS_0xxx/COVIMS_0030/data/*/\1_*\2.qub']),
    (r'co-vims-(v158.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_002[4-7]/data/*/\1_*\2.qub'),
    (r'co-vims-(v157.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_002[3-4]/data/*/\1_*\2.qub'),
    (r'co-vims-(v156.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_002[0-3]/data/*/\1_*\2.qub'),
    (r'co-vims-(v155.{7})(|_.{3})',     0, [r'volumes/COVIMS_0xxx/COVIMS_001[6-9]/data/*/\1_*\2.qub',
                                            r'volumes/COVIMS_0xxx/COVIMS_0020/data/*/\1_*\2.qub']),
    (r'co-vims-(v154.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_001[4-6]/data/*/\1_*\2.qub'),
    (r'co-vims-(v153.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_001[2-4]/data/*/\1_*\2.qub'),
    (r'co-vims-(v152.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_001[1-2]/data/*/\1_*\2.qub'),
    (r'co-vims-(v151.{7})(|_.{3})',     0, [r'volumes/COVIMS_0xxx/COVIMS_0009/data/*/\1_*\2.qub',
                                            r'volumes/COVIMS_0xxx/COVIMS_001[0-1]/data/*/\1_*\2.qub']),
    (r'co-vims-(v150.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_000[8-9]/data/*/\1_*\2.qub'),
    (r'co-vims-(v149.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_000[6-8]/data/*/\1_*\2.qub'),
    (r'co-vims-(v148.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_000[5-6]/data/*/\1_*\2.qub'),
    (r'co-vims-(v147.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_000[4-5]/data/*/\1_*\2.qub'),
    (r'co-vims-(v146.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_000[3-4]/data/*/\1_*\2.qub'),
    (r'co-vims-(v14[0-6].{7})(|_.{3})', 0,  r'volumes/COVIMS_0xxx/COVIMS_0003/data/*/\1_*\2.qub'),
    (r'co-vims-(v13[7-9].{7})(|_.{3})', 0,  r'volumes/COVIMS_0xxx/COVIMS_0003/data/*/\1_*\2.qub'),
    (r'co-vims-(v136.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_000[2-3]/data/*/\1_*\2.qub'),
    (r'co-vims-(v135.{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_0002/data/*/\1_*\2.qub'),
    (r'co-vims-(v13[0-4].{7})(|_.{3})', 0,  r'volumes/COVIMS_0xxx/COVIMS_0001/data/*/\1_*\2.qub'),
    (r'co-vims-(v12..{7})(|_.{3})',     0,  r'volumes/COVIMS_0xxx/COVIMS_0001/data/*/\1_*\2.qub'),
]),

####################################################################################################################################
# Subclass definition
####################################################################################################################################

BASENAME_REGEX = re.compile('(v?\d{10}_\d+)(_0[0-6][0-9]|).*')

class COVIMS_0xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('COVIMS_0xxx', re.I, 'COVIMS_0xxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS

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

    def FILENAME_KEYLEN(self):
        match = BASENAME_REGEX.match(self.basename)
        if match:
            return len(match.group(1) + match.group(2))
        else:
            return 0

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS = translator.TranslatorByRegex([(r'co-vims-v.*', 0, COVIMS_0xxx)]) + \
                                      pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COVIMS_0xxx'] = COVIMS_0xxx

####################################################################################################################################
