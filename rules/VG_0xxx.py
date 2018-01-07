####################################################################################################################################
# rules/VG_0xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

key_from_path = translator.TranslatorByRegex([
    (r'[-a-z]+/VG_0xxx(|_\w+)/VG_([0-9]{4})', re.I, r'VG_0xxx/VG_\2'),
    (r'[-a-z]+/VG_0xxx(|_\w+)',               re.I, r'VG_0xxx'),
])

description_and_icon_by_dict = translator.TranslatorByDict({
    'VG_0xxx'        : ('Voyager image collection, original release of compressed raw images',        'VOLDIR'),
    'VG_0xxx/VG_0001': ('Voyager 2 Uranus images, original release of compressed raw images',         'VOLUME'),
    'VG_0xxx/VG_0002': ('Voyager 2 Uranus images, original release of compressed raw images',         'VOLUME'),
    'VG_0xxx/VG_0003': ('Voyager 2 Uranus images, original release of compressed raw images',         'VOLUME'),
    'VG_0xxx/VG_0004': ('Selected Voyager Saturn images, original release of compressed raw images',  'VOLUME'),
    'VG_0xxx/VG_0005': ('Selected Voyager Saturn images, original release of compressed raw images',  'VOLUME'),
    'VG_0xxx/VG_0006': ('Selected Voyager Jupiter images, original release of compressed raw images', 'VOLUME'),
    'VG_0xxx/VG_0007': ('Selected Voyager Jupiter images, original release of compressed raw images', 'VOLUME'),
    'VG_0xxx/VG_0008': ('Selected Voyager Jupiter images, original release of compressed raw images', 'VOLUME'),
    'VG_0xxx/VG_0009': ('Voyager 2 Neptune images, original release of compressed raw images',        'VOLUME'),
    'VG_0xxx/VG_0010': ('Voyager 2 Neptune images, original release of compressed raw images',        'VOLUME'),
    'VG_0xxx/VG_0011': ('Voyager 2 Neptune images, original release of compressed raw images',        'VOLUME'),
    'VG_0xxx/VG_0012': ('Voyager 2 Neptune images, original release of compressed raw images',        'VOLUME'),
    'VG_0xxx/VG_0013': ('Voyager 1 Jupiter images, original release of compressed raw images',        'VOLUME'),
    'VG_0xxx/VG_0014': ('Voyager 1 Jupiter images, original release of compressed raw images',        'VOLUME'),
    'VG_0xxx/VG_0015': ('Voyager 1 Jupiter images, original release of compressed raw images',        'VOLUME'),
    'VG_0xxx/VG_0016': ('Voyager 1 Jupiter images, original release of compressed raw images',        'VOLUME'),
    'VG_0xxx/VG_0017': ('Voyager 1 Jupiter images, original release of compressed raw images',        'VOLUME'),
    'VG_0xxx/VG_0018': ('Voyager 1 Jupiter images, original release of compressed raw images',        'VOLUME'),
    'VG_0xxx/VG_0019': ('Voyager 1 Jupiter images, original release of compressed raw images',        'VOLUME'),
    'VG_0xxx/VG_0020': ('Voyager 1 and 2 Jupiter images, original release of compressed raw images',  'VOLUME'),
    'VG_0xxx/VG_0021': ('Voyager 2 Jupiter images, original release of compressed raw images',        'VOLUME'),
    'VG_0xxx/VG_0022': ('Voyager 2 Jupiter images, original release of compressed raw images',        'VOLUME'),
    'VG_0xxx/VG_0023': ('Voyager 2 Jupiter images, original release of compressed raw images',        'VOLUME'),
    'VG_0xxx/VG_0024': ('Voyager 2 Jupiter images, original release of compressed raw images',        'VOLUME'),
    'VG_0xxx/VG_0025': ('Voyager 2 Jupiter images, original release of compressed raw images',        'VOLUME'),
    'VG_0xxx/VG_0026': ('Voyager 1 Saturn images, original release of compressed raw images',         'VOLUME'),
    'VG_0xxx/VG_0027': ('Voyager 1 Saturn images, original release of compressed raw images',         'VOLUME'),
    'VG_0xxx/VG_0028': ('Voyager 1 Saturn images, original release of compressed raw images',         'VOLUME'),
    'VG_0xxx/VG_0029': ('Voyager 1 Saturn images, original release of compressed raw images',         'VOLUME'),
    'VG_0xxx/VG_0030': ('Voyager 1 Saturn images, original release of compressed raw images',         'VOLUME'),
    'VG_0xxx/VG_0031': ('Voyager 1 Saturn images, original release of compressed raw images',         'VOLUME'),
    'VG_0xxx/VG_0032': ('Voyager 1 Saturn images, original release of compressed raw images',         'VOLUME'),
    'VG_0xxx/VG_0033': ('Voyager 1 and 2 Saturn images, original release of compressed raw images',   'VOLUME'),
    'VG_0xxx/VG_0034': ('Voyager 2 Saturn images, original release of compressed raw images',         'VOLUME'),
    'VG_0xxx/VG_0035': ('Voyager 2 Saturn images, original release of compressed raw images',         'VOLUME'),
    'VG_0xxx/VG_0036': ('Voyager 2 Saturn images, original release of compressed raw images',         'VOLUME'),
    'VG_0xxx/VG_0037': ('Voyager 2 Saturn images, original release of compressed raw images',         'VOLUME'),
    'VG_0xxx/VG_0038': ('Voyager 2 Saturn images, original release of compressed raw images',         'VOLUME'),
}, key_from_path)

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*\.IBG',               re.I,   ('Compressed browse image',            'IMAGE'   )),
    (r'volumes/.*\.IMQ',               re.I,   ('Compressed raw image, VICAR',        'IMAGE'   )),
    (r'volumes/.*/BROWSE(|/w+)',       re.I,   ('Compressed browse images',           'IMAGEDIR')),
    (r'volumes/VG_0xxx/VG_0.../(?!DOCUMENT)(?!INDEX)(?!LABEL)(?!SOFTWARE).*/C[0-9]+X+',
                                       re.I,   ('Image files grouped by SC clock',    'IMAGEDIR')),
    (r'volumes/VG_0xxx/VG_0.../(?!DOCUMENT)(?!INDEX)(?!LABEL)(?!SOFTWARE)\w+',
                                       re.I,   ('Image files grouped by target',      'IMAGEDIR')),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'volumes/VG_0xxx/VG_000[1-3]/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)', 0,
                                                                (r'previews/VGISS_7xxx/VGISS_7???/DATA/\1XX/\1\2_thumb.jpg',
                                                                 r'previews/VGISS_7xxx/VGISS_7???/DATA/\1XX/\1\2_small.jpg',
                                                                 r'previews/VGISS_7xxx/VGISS_7???/DATA/\1XX/\1\2_med.jpg',
                                                                 r'previews/VGISS_7xxx/VGISS_7???/DATA/\1XX/\1\2_full.jpg')),
    (r'volumes/VG_0xxx/VG_000[45]/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)',
                                                               (r'previews/VGISS_6xxx/VGISS_6???/DATA/\1XX/\1\2_thumb.jpg',
                                                                r'previews/VGISS_6xxx/VGISS_6???/DATA/\1XX/\1\2_small.jpg',
                                                                r'previews/VGISS_6xxx/VGISS_6???/DATA/\1XX/\1\2_med.jpg',
                                                                r'previews/VGISS_6xxx/VGISS_6???/DATA/\1XX/\1\2_full.jpg')),
    (r'volumes/VG_0xxx/VG_000[6-8]/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)', 0,
                                                               (r'previews/VGISS_5xxx/VGISS_5???/DATA/\1XX/\1\2_thumb.jpg',
                                                                r'previews/VGISS_5xxx/VGISS_5???/DATA/\1XX/\1\2_small.jpg',
                                                                r'previews/VGISS_5xxx/VGISS_5???/DATA/\1XX/\1\2_med.jpg',
                                                                r'previews/VGISS_5xxx/VGISS_5???/DATA/\1XX/\1\2_full.jpg')),
    (r'volumes/VG_0xxx/VG_0009/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)',     0,
                                                               (r'previews/VGISS_8xxx/VGISS_8???/DATA/\1XX/\1\2_thumb.jpg',
                                                                r'previews/VGISS_8xxx/VGISS_8???/DATA/\1XX/\1\2_small.jpg',
                                                                r'previews/VGISS_8xxx/VGISS_8???/DATA/\1XX/\1\2_med.jpg',
                                                                r'previews/VGISS_8xxx/VGISS_8???/DATA/\1XX/\1\2_full.jpg')),
    (r'volumes/VG_0xxx/VG_001[0-2]/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)', 0,
                                                               (r'previews/VGISS_8xxx/VGISS_8???/DATA/\1XX/\1\2_thumb.jpg',
                                                                r'previews/VGISS_8xxx/VGISS_8???/DATA/\1XX/\1\2_small.jpg',
                                                                r'previews/VGISS_8xxx/VGISS_8???/DATA/\1XX/\1\2_med.jpg',
                                                                r'previews/VGISS_8xxx/VGISS_8???/DATA/\1XX/\1\2_full.jpg')),
    (r'volumes/VG_0xxx/VG_001[3-9]/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)', 0,
                                                               (r'previews/VGISS_5xxx/VGISS_51??/DATA/\1XX/\1\2_thumb.jpg',
                                                                r'previews/VGISS_5xxx/VGISS_51??/DATA/\1XX/\1\2_small.jpg',
                                                                r'previews/VGISS_5xxx/VGISS_51??/DATA/\1XX/\1\2_med.jpg',
                                                                r'previews/VGISS_5xxx/VGISS_51??/DATA/\1XX/\1\2_full.jpg')),
    (r'volumes/VG_0xxx/VG_0020/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)',     0,
                                                               (r'previews/VGISS_5xxx/VGISS_5???/DATA/\1XX/\1\2_thumb.jpg',
                                                                r'previews/VGISS_5xxx/VGISS_5???/DATA/\1XX/\1\2_small.jpg',
                                                                r'previews/VGISS_5xxx/VGISS_5???/DATA/\1XX/\1\2_med.jpg',
                                                                r'previews/VGISS_5xxx/VGISS_5???/DATA/\1XX/\1\2_full.jpg')),
    (r'volumes/VG_0xxx/VG_002[1-5]/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)', 0,
                                                               (r'previews/VGISS_5xxx/VGISS_52??/DATA/\1XX/\1\2_thumb.jpg',
                                                                r'previews/VGISS_5xxx/VGISS_52??/DATA/\1XX/\1\2_small.jpg',
                                                                r'previews/VGISS_5xxx/VGISS_52??/DATA/\1XX/\1\2_med.jpg',
                                                                r'previews/VGISS_5xxx/VGISS_52??/DATA/\1XX/\1\2_full.jpg')),
    (r'volumes/VG_0xxx/VG_002[6-9]/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)', 0,
                                                               (r'previews/VGISS_6xxx/VGISS_61??/DATA/\1XX/\1\2_thumb.jpg',
                                                                r'previews/VGISS_6xxx/VGISS_61??/DATA/\1XX/\1\2_small.jpg',
                                                                r'previews/VGISS_6xxx/VGISS_61??/DATA/\1XX/\1\2_med.jpg',
                                                                r'previews/VGISS_6xxx/VGISS_61??/DATA/\1XX/\1\2_full.jpg')),
    (r'volumes/VG_0xxx/VG_003[0-2]/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)', 0,
                                                               (r'previews/VGISS_6xxx/VGISS_61??/DATA/\1XX/\1\2_thumb.jpg',
                                                                r'previews/VGISS_6xxx/VGISS_61??/DATA/\1XX/\1\2_small.jpg',
                                                                r'previews/VGISS_6xxx/VGISS_61??/DATA/\1XX/\1\2_med.jpg',
                                                                r'previews/VGISS_6xxx/VGISS_61??/DATA/\1XX/\1\2_full.jpg')),
    (r'volumes/VG_0xxx/VG_0033/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)',     0,
                                                               (r'previews/VGISS_6xxx/VGISS_6???/DATA/\1XX/\1\2_thumb.jpg',
                                                                r'previews/VGISS_6xxx/VGISS_6???/DATA/\1XX/\1\2_small.jpg',
                                                                r'previews/VGISS_6xxx/VGISS_6???/DATA/\1XX/\1\2_med.jpg',
                                                                r'previews/VGISS_6xxx/VGISS_6???/DATA/\1XX/\1\2_full.jpg')),
    (r'volumes/VG_0xxx/VG_003[4-8]/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)', 0,
                                                                (r'previews/VGISS_6xxx/VGISS_62??/DATA/\1XX/\1\2_thumb.jpg',
                                                                 r'previews/VGISS_6xxx/VGISS_62??/DATA/\1XX/\1\2_small.jpg',
                                                                 r'previews/VGISS_6xxx/VGISS_62??/DATA/\1XX/\1\2_med.jpg',
                                                                 r'previews/VGISS_6xxx/VGISS_62??/DATA/\1XX/\1\2_full.jpg')),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

volumes_to_volumes = translator.TranslatorByRegex([
    (r'volumes/VG_0xxx/VG_000[1-3]/(.*)\.IMQ', 0, r'volumes/VG_0xxx/VG_0003/BROWSE/\1.IBG'),
    (r'volumes/VG_0xxx/VG_000[4-5]/(.*)\.IMQ', 0, r'volumes/VG_0xxx/VG_0005/BROWSE/\1.IBG'),
    (r'volumes/VG_0xxx/VG_000[6-8]/(.*)\.IMQ', 0, r'volumes/VG_0xxx/VG_0008/BROWSE/\1.IBG'),
    (r'volumes/VG_0xxx/(VG_00??)/(.*)\.IMQ',   0, r'volumes/VG_0xxx/\1/BROWSE/\2.IBG'),

    (r'volumes/VG_0xxx/VG_0003/BROWSE/(.*)\.IBG',   0, r'volumes/VG_0xxx/VG_000[123]/\1.IMQ'),
    (r'volumes/VG_0xxx/VG_0005/BROWSE/(.*)\.IBG',   0, r'volumes/VG_0xxx/VG_000[45]/\1.IMQ'),
    (r'volumes/VG_0xxx/VG_0008/BROWSE/(.*)\.IBG',   0, r'volumes/VG_0xxx/VG_000[678]/\1.IMQ'),
    (r'volumes/VG_0xxx/(VG_00??)/BROWSE/(.*)\.IBG', 0, r'volumes/VG_0xxx/\1/\2.IBG'),

    (r'volumes/VG_0xxx/VG_000[1-3]/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)', 0, r'volumes/VGISS_7xxx/VGISS_7???/DATA/\1XX/\1\2_*.*'),
    (r'volumes/VG_0xxx/VG_000[45]/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)',  0, r'volumes/VGISS_6xxx/VGISS_6???/DATA/\1XX/\1\2_*.*'),
    (r'volumes/VG_0xxx/VG_000[6-8]/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)', 0, r'volumes/VGISS_5xxx/VGISS_5???/DATA/\1XX/\1\2_*.*'),
    (r'volumes/VG_0xxx/VG_0009/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)',     0, r'volumes/VGISS_7xxx/VGISS_8???/DATA/\1XX/\1\2_*.*'),
    (r'volumes/VG_0xxx/VG_001[0-2]/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)', 0, r'volumes/VGISS_7xxx/VGISS_8???/DATA/\1XX/\1\2_*.*'),
    (r'volumes/VG_0xxx/VG_001[3-9]/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)', 0, r'volumes/VGISS_5xxx/VGISS_51??/DATA/\1XX/\1\2_*.*'),
    (r'volumes/VG_0xxx/VG_0020/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)',     0, r'volumes/VGISS_5xxx/VGISS_5???/DATA/\1XX/\1\2_*.*'),
    (r'volumes/VG_0xxx/VG_002[1-5]/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)', 0, r'volumes/VGISS_5xxx/VGISS_52??/DATA/\1XX/\1\2_*.*'),
    (r'volumes/VG_0xxx/VG_002[6-9]/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)', 0, r'volumes/VGISS_6xxx/VGISS_61??/DATA/\1XX/\1\2_*.*'),
    (r'volumes/VG_0xxx/VG_003[0-2]/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)', 0, r'volumes/VGISS_6xxx/VGISS_61??/DATA/\1XX/\1\2_*.*'),
    (r'volumes/VG_0xxx/VG_0033/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)',     0, r'volumes/VGISS_6xxx/VGISS_6???/DATA/\1XX/\1\2_*.*'),
    (r'volumes/VG_0xxx/VG_003[4-8]/.*/(C[0-9]{5})([0-9]{2})\.(IMQ|IBG)', 0, r'volumes/VGISS_6xxx/VGISS_62??/DATA/\1XX/\1\2_*.*'),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'volumes/VG_0xxx/VG_..../(?!DOCUMENT)(?!INDEX)(?!LABEL)(?!SOFTWARE)(.*)/C[0-9]{5}XX', re.I, (True, True, True)),
    (r'volumes/VG_0xxx/VG_..../(?!DOCUMENT)(?!INDEX)(?!LABEL)(?!SOFTWARE)\w+',              re.I, (True, True, True)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'volumes/VG_0xxx/\w+/(?!DOCUMENT)(?!INDEX)(?!LABEL)(?!SOFTWARE)(\w+)',             re.I, r'volumes/VG_0xxx/*/\1'),
    (r'volumes/VG_0xxx/\w+/(?!DOCUMENT)(?!INDEX)(?!LABEL)(?!SOFTWARE)(\w+)/C[0-9]{5}XX', re.I, r'volumes/VG_0xxx/*/\1/*'),
    (r'volumes/VG_0xxx/\w+/(?!DOCUMENT)(?!INDEX)(?!LABEL)(?!SOFTWARE)(\w+)/\w+',         re.I, r'volumes/VG_0xxx/*/\1/*'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class VG_0xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('VG_0xxx', re.I, 'VG_0xxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_dict + description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS

    VOLUMES_TO_ASSOCIATIONS = pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS.copy()
    VOLUMES_TO_ASSOCIATIONS['volumes'] = volumes_to_volumes + pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS['volumes']

    VIEWABLES = pdsfile.PdsFile.VIEWABLES.copy()
    VIEWABLES = {'default': default_viewables}

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['VG_0xxx'] = VG_0xxx

####################################################################################################################################
