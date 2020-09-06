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
    (r'(\w+)(_RAW)\.(JPG|IMG)',        0, r'\1_1RAW.\3'    ),
    (r'(\w+)(_CLEANED)\.(JPG|IMG)',    0, r'\1_2CLEANED.\3'),
    (r'(\w+)(_CALIB)\.(JPG|IMG)',      0, r'\1_3CALIB.\3'  ),
    (r'(\w+)(_GEOMED)\.(JPG|IMG)',     0, r'\1_4GEOMED.\3' ),
    (r'(\w+)(_RESLOC)\.(DAT|TAB)',     0, r'\1_5RESLOC.\3' ),
    (r'(\w+)(_GEOMA)\.(DAT|TAB)',      0, r'\1_6GEOMA.\3'  ),

    (r'(\w+)(_RAW)\.LBL',        0, r'\1_1RAW.zLBL'    ),    # Label after matching file, not after everything
    (r'(\w+)(_CLEANED)\.LBL',    0, r'\1_2CLEANED.zLBL'),
    (r'(\w+)(_CALIB)\.LBL',      0, r'\1_3CALIB.zLBL'  ),
    (r'(\w+)(_GEOMED)\.LBL',     0, r'\1_4GEOMED.zLBL' ),
    (r'(\w+)(_RESLOC)\.LBL',     0, r'\1_5RESLOC.zLBL' ),
    (r'(\w+)(_GEOMA)\.LBL',      0, r'\1_6GEOMA.zLBL'  ),
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
    (r'.*/(VGISS_.xxx/VGISS_....)/(DATA|BROWSE)/(C.....XX/C[0-9]{7})_\w+\..*',
                                                                0,  [r'volumes/\1/DATA/\3_RAW.IMG',
                                                                     r'volumes/\1/DATA/\3_RAW.LBL',
                                                                     r'volumes/\1/DATA/\3_CLEANED.IMG',
                                                                     r'volumes/\1/DATA/\3_CLEANED.LBL',
                                                                     r'volumes/\1/DATA/\3_CALIB.IMG',
                                                                     r'volumes/\1/DATA/\3_CALIB.LBL',
                                                                     r'volumes/\1/DATA/\3_GEOMED.IMG',
                                                                     r'volumes/\1/DATA/\3_GEOMED.LBL',
                                                                     r'volumes/\1/DATA/\3_RESLOC.DAT',
                                                                     r'volumes/\1/DATA/\3_RESLOC.TAB',
                                                                     r'volumes/\1/DATA/\3_RESLOC.LBL',
                                                                     r'volumes/\1/DATA/\3_GEOMA.DAT',
                                                                     r'volumes/\1/DATA/\3_GEOMA.TAB',
                                                                     r'volumes/\1/DATA/\3_GEOMA.LBL',
                                                                     r'volumes/\1/BROWSE/\3_RAW.JPG',
                                                                     r'volumes/\1/BROWSE/\3_RAW.LBL',
                                                                     r'volumes/\1/BROWSE/\3_CLEANED.JPG',
                                                                     r'volumes/\1/BROWSE/\3_CLEANED.LBL',
                                                                     r'volumes/\1/BROWSE/\3_CALIB.JPG',
                                                                     r'volumes/\1/BROWSE/\3_CALIB.LBL',
                                                                     r'volumes/\1/BROWSE/\3_GEOMED.JPG',
                                                                     r'volumes/\1/BROWSE/\3_GEOMED.LBL']),

    (r'.*/(VGISS_.xxx/VGISS_....)/(DATA|BROWSE)/(C.....XX)',    0, [r'volumes/\1/DATA/\3',
                                                                    r'volumes/\1/BROWSE/\3']),
    (r'.*/(VGISS_.xxx/VGISS_....)/(DATA|BROWSE)$',              0, [r'volumes/\1/DATA',
                                                                    r'volumes/\1/BROWSE']),
    (r'metadata/(VGISS_.xxx/VGISS_....)/VGISS_...._index\..*',  0, [r'volumes/\1/INDEX/INDEX.TAB',
                                                                    r'volumes/\1/INDEX/INDEX.LBL']),
    (r'metadata/(VGISS_.)xxx/VGISS_.999/VGISS_...._index\..*',  0, [r'volumes/\1/INDEX/CUMINDEX.TAB',
                                                                    r'volumes/\1/INDEX/CUMINDEX.LBL']),

    # VG_0006 to VG_0008, selected Jupiter
    (r'.*/VGISS_5xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C[0-9]{7}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_000[6-8]/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_000[6-8]/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_000[6-8]/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_000[6-8]/*/*/*/*/\2*']),

    # VG_0013 to VG_0025, Jupiter
    (r'.*/VGISS_5xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C14[0-9]{5}|C15[0-4][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0013/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0013/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0013/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0013/*/*/*/*/\2*']),
    (r'.*/VGISS_5xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C15[45][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0014/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0014/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0014/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0014/*/*/*/*/\2*']),
    (r'.*/VGISS_5xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C15[5-9][0-9]{4}|C160[0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0015/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0015/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0015/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0015/*/*/*/*/\2*']),
    (r'.*/VGISS_5xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C16[0-2][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0016/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0016/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0016/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0016/*/*/*/*/\2*']),
    (r'.*/VGISS_5xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C16[23][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0017/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0017/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0017/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0017/*/*/*/*/\2*']),
    (r'.*/VGISS_5xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C16[34][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0018/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0018/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0018/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0018/*/*/*/*/\2*']),
    (r'.*/VGISS_5xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C16[4-9][0-9]{4}|C17[0-3][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0019/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0019/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0019/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0019/*/*/*/*/\2*']),

    (r'.*/VGISS_5xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C175[0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0020/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0020/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0020/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0020/*/*/*/*/\2*']),
    (r'.*/VGISS_5xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C18[0-9]{5}|C19[0-4][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0020/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0020/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0020/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0020/*/*/*/*/\2*']),
    (r'.*/VGISS_5xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C19[4-9][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0021/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0021/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0021/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0021/*/*/*/*/\2*']),
    (r'.*/VGISS_5xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C199[0-9]{4}|C20[0-3][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0022/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0022/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0022/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0022/*/*/*/*/\2*']),
    (r'.*/VGISS_5xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C20[34][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0023/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0023/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0023/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0023/*/*/*/*/\2*']),
    (r'.*/VGISS_5xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C20[4-6][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0024/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0024/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0024/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0024/*/*/*/*/\2*']),
    (r'.*/VGISS_5xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C20[67][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0025//*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0025//*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0025//*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0025//*/*/*/*/\2*']),

    # VG_0004 to VG_0005, selected Saturn
    (r'.*/VGISS_6xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C[0-9]{7}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_000[45]/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_000[45]/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_000[45]/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_000[45]/*/*/*/*/\2*']),

    # VG_0026 to VG_0038, Saturn
    (r'.*/VGISS_6xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C32[0-9]{5}|C33[0-5]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0026/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0026/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0026/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0026/*/*/*/*/\2*']),
    (r'.*/VGISS_6xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C33[5-9][0-9]{4}|C34[0-4][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0027/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0027/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0027/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0027/*/*/*/*/\2*']),
    (r'.*/VGISS_6xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C34[4-7][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0028/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0028/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0028/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0028/*/*/*/*/\2*']),
    (r'.*/VGISS_6xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C34[7-9][0-9]{4}|C350[0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0029/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0029/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0029/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0029/*/*/*/*/\2*']),
    (r'.*/VGISS_6xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C35[0-3][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0030/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0030/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0030/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0030/*/*/*/*/\2*']),
    (r'.*/VGISS_6xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C35[3-6][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0031/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0031/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0031/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0031/*/*/*/*/\2*']),
    (r'.*/VGISS_6xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C35[6-8][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0032/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0032/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0032/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0032/*/*/*/*/\2*']),
    (r'.*/VGISS_6xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C35[89][0-9]{4}|C41[0-9]{5}|C42[0-2][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0033/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0033/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0033/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0033/*/*/*/*/\2*']),
    (r'.*/VGISS_6xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C42[2-9][0-9]{4}|C43[0-2][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0034/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0034/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0034/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0034/*/*/*/*/\2*']),
    (r'.*/VGISS_6xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C43[2-5][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0035/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0035/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0035/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0035/*/*/*/*/\2*']),
    (r'.*/VGISS_6xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C43[5-8][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0036/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0036/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0036/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0036/*/*/*/*/\2*']),
    (r'.*/VGISS_6xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C43[89][0-9]{4}|C44[01][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0037/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0037/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0037/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0037/*/*/*/*/\2*']),
    (r'.*/VGISS_6xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C44[12][0-9]{4}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0038/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0038/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0038/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0038/*/*/*/*/\2*']),
    (r'.*/VGISS_6xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C4[23][0-9]{5}).*',
                                                                0,   r'volumes/VG_0xxx/VG_0038/FOUND/*/\2*'),
    (r'.*/VGISS_6xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C43[0-9]{5}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0038/BROWSE/CALIB/*/\2*']),

    # VG_0001 to VG_0003, Uranus
    (r'.*/VGISS_7xxx/VGISS_..../(DATA|BROWSE)/C.....XX/(C[0-9]{7}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_000[1-3]/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_000[1-3]/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_000[1-3]/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_000[1-3]/*/*/*/*/\2*']),

    # VG_0009 to VG_0012, Neptune
    (r'.*/VGISS_8xxx/VGISS_..../(DATA|BROWSE)/(C.....XX)/(C[0-9]{7}).*',
                                                                0,  [r'volumes/VG_0xxx/VG_0009/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0009/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0009/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_0009/*/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_001[0-2]/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_001[0-2]/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_001[0-2]/*/*/*/\2*',
                                                                     r'volumes/VG_0xxx/VG_001[0-2]/*/*/*/*/\2*']),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'.*/(VGISS_.xxx/VGISS_....)/(DATA|BROWSE)/(C.....XX/C[0-9]{7})_\w+\..*',
                                                                0, [r'previews/\1/DATA/\3_full.jpg',
                                                                    r'previews/\1/DATA/\3_thumb.jpg',
                                                                    r'previews/\1/DATA/\3_small.jpg',
                                                                    r'previews/\1/DATA/\3_med.jpg']),
    (r'.*/(VGISS_.xxx/VGISS_....)/(DATA|BROWSE)/(C.....XX)$',   0,  r'previews/\1/DATA/\3'),
    (r'.*/(VGISS_.xxx/VGISS_....)/BROWSE$',                     0,  r'previews/\1/DATA'),
])

associations_to_metadata = translator.TranslatorByRegex([
    (r'.*/(VGISS_.xxx)/(VGISS_....)/(DATA|BROWSE)/(C.....XX)/(C[0-9]{7})_\w+\..*',
                                                                0, [r'metadata/\1/\2/\2_index.tab/\5',
                                                                    r'metadata/\1/\2/\2_raw_image_index.tab/\5',
                                                                    r'metadata/\1/\2/\2_supplemental_index.tab/\5',
                                                                    r'metadata/\1/\2/\2_ring_summary.tab/\5',
                                                                    r'metadata/\1/\2/\2_moon_summary.tab/\5',
                                                                    r'metadata/\1/\2/\2_jupiter_summary.tab/\5',
                                                                    r'metadata/\1/\2/\2_saturn_summary.tab/\5',
                                                                    r'metadata/\1/\2/\2_uranus_summary.tab/\5',
                                                                    r'metadata/\1/\2/\2_neptune_summary.tab/\5',
                                                                    r'metadata/\1/\2']),
    (r'.*/(VGISS_.xxx)/(VGISS_....)/(DATA|BROWSE)/C.....XX$',   0,  r'metadata/\1/\2'),
    (r'.*/(VGISS_.xxx)/(VGISS_....)/(DATA|BROWSE)$',            0,  r'metadata/\1/\2'),
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
    (r'.*\.lbl',  re.I, ''),

    (r'volumes/(.*)/(DATA/\w+/.*)_(RAW|CLEANED|CALIB|GEOMED)\..*', 0, (r'previews/\1/\2_thumb.jpg',
                                                                       r'previews/\1/\2_small.jpg',
                                                                       r'previews/\1/\2_med.jpg',
                                                                       r'previews/\1/\2_full.jpg')),
])

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/.*/C[0-9]{7}_RAW\..*$',     0, ('Voyager ISS',  0, 'vgiss_raw',     'Raw Image',                     True)),
    (r'volumes/.*/C[0-9]{7}_CLEANED\..*$', 0, ('Voyager ISS', 10, 'vgiss_cleaned', 'Cleaned Image',                 True)),
    (r'volumes/.*/C[0-9]{7}_CALIB\..*$',   0, ('Voyager ISS', 20, 'vgiss_calib',   'Calibrated Image',              True)),
    (r'volumes/.*/C[0-9]{7}_GEOMED\..*$',  0, ('Voyager ISS', 30, 'vgiss_geomed',  'Geometrically Corrected Image', True)),
    (r'volumes/.*/C[0-9]{7}_RESLOC\..*$',  0, ('Voyager ISS', 40, 'vgiss_resloc',  'Reseau Table',                  True)),
    (r'volumes/.*/C[0-9]{7}_GEOMA\..*$',   0, ('Voyager ISS', 50, 'vgiss_geoma',   'Geometric Tiepoint Table',      True)),
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
    (r'.*volumes/(VGISS_[5-8]xxx)/(VGISS_[5-8]...)/(DATA/.*)_[A-Z]+\.(IMG|DAT|LBL|TAB)',
                                        0, [r'volumes/\1/\2/\3_RAW.IMG',
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
                                            r'metadata/\1/\2/\2_inventory.lbl',
                                            r'metadata/\1/\2/\2_index.lbl',
                                            r'metadata/\1/\2/\2_index.tab',
                                            r'metadata/\1/\2/\2_raw_image_index.lbl',
                                            r'metadata/\1/\2/\2_raw_image_index.tab',
                                            r'metadata/\1/\2/\2_supplemental_index.lbl',
                                            r'metadata/\1/\2/\2_supplemental_index.tab'])
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

    ASSOCIATIONS = pdsfile.PdsFile.ASSOCIATIONS.copy()
    ASSOCIATIONS['volumes']  = associations_to_volumes
    ASSOCIATIONS['previews'] = associations_to_previews
    ASSOCIATIONS['metadata'] = associations_to_metadata

    VIEWABLES = {'default': default_viewables}

    FILENAME_KEYLEN = 8     # trim off suffixes

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_FILESPEC = opus_id_to_filespec + pdsfile.PdsFile.OPUS_ID_TO_FILESPEC

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['VGISS_xxxx'] = VGISS_xxxx

####################################################################################################################################
