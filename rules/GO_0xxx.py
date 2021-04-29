####################################################################################################################################
# rules/GO_0xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/\w+/\w+(|/REDO)/[CEGIJ][0-9]{1,2}',               re.I, ('Images grouped by orbit',        'IMAGEDIR')),
    (r'volumes/\w+/\w+(|/REDO)/[CEGIJ][0-9]{1,2}/\w+',           re.I, ('Images grouped by target',       'IMAGEDIR')),
    (r'volumes/\w+/\w+(|/REDO)/[CEGIJ][0-9]{1,2}/\w+/C[0-9]{6}', re.I, ('Images grouped by SC clock',     'IMAGEDIR')),
    (r'volumes/\w+/\w+/REDO',                                    re.I, ('Redone images grouped by orbit', 'IMAGEDIR')),
    (r'volumes/.*\.IMG',                                         re.I, ('Raw image, VICAR',               'IMAGE'   )),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'.*\.lbl',  re.I, ''),
    (r'volumes/(.*/C[0-9]{10}[A-Z])\.(IMG|LBL)', 0,
            [r'previews/\1_full.jpg',
             r'previews/\1_med.jpg',
             r'previews/\1_small.jpg',
             r'previews/\1_thumb.jpg',
            ]),
    (r'volumes/(GO_0xxx_v1/.*/C[0-9]{6}/.*)\.(IMG|LBL)', 0,
            [r'previews/\1_full.jpg',
             r'previews/\1_med.jpg',
             r'previews/\1_small.jpg',
             r'previews/\1_thumb.jpg',
            ]),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'.*/(GO_0xxx/GO_..../.*/C[0-9]{10}[A-Z]).*', 0,
            [r'volumes/\1.IMG',
             r'volumes/\1.LBL',
            ]),
    (r'.*/GO_0xxx_v1/(GO_..../.*/C[0-9]{6})/([0-9]{4}[A-Z]).*', 0,
            [r'volumes/GO_0xxx_v1/\1/\2.IMG',
             r'volumes/GO_0xxx_v1/\1/\2.LBL',
             r'volumes/GO_0xxx/\1\2.IMG',
             r'volumes/GO_0xxx/\1\2.LBL'
            ]),
    (r'.*/previews/(GO_0..._v1/.*)_[a-z]+\.jpg', 0,
            [r'volumes/\1.IMG',
             r'volumes/\1.LBL',
            ]),
    (r'.*/metadata/GO_0xxx/GO_0999.*', 0,
            r'volumes/GO_0xxx'),
    (r'.*/metadata/GO_0xxx_v1/GO_0999.*', 0,
            r'volumes/GO_0xxx_v1'),
])

associations_to_previews = translator.TranslatorByRegex([
    (r'.*/(GO_0xxx/GO_..../.*/C[0-9]{10}[A-Z]).*', 0,
            [r'previews/\1_full.jpg',
             r'previews/\1_med.jpg',
             r'previews/\1_small.jpg',
             r'previews/\1_thumb.jpg',
            ]),
    (r'.*/GO_0xxx_v1/(GO_..../.*/C[0-9]{6})/([0-9]{4}[A-Z]).*', 0,
            [r'previews/GO_0xxx_v1/\1/\2_full.jpg',
             r'previews/GO_0xxx_v1/\1/\2_med.jpg',
             r'previews/GO_0xxx_v1/\1/\2_small.jpg',
             r'previews/GO_0xxx_v1/\1/\2_thumb.jpg',
             r'previews/GO_0xxx/\1\2_full.jpg',
             r'previews/GO_0xxx/\1\2_med.jpg',
             r'previews/GO_0xxx/\1\2_small.jpg',
             r'previews/GO_0xxx/\1\2_thumb.jpg',
            ]),
    (r'.*/metadata/GO_0xxx/GO_0999.*', 0,
            r'previews/GO_0xxx'),
    (r'.*/metadata/GO_0xxx_v1/GO_0999.*', 0,
            r'previews/GO_0xxx_v1'),
])

associations_to_metadata = translator.TranslatorByRegex([
    (r'volumes/(GO_0xxx)/(GO_....)/.*/(C[0-9]{10})[A-Z].*', 0,
            r'metadata/\1/\2/\2_index.tab/\3'),
    (r'volumes/(GO_0xxx_v1)/(GO_....).*', 0,
            r'metadata/\1/\2'),
    (r'metadata/GO_0xxx(|_v[\d\.]+)/GO_00..', 0,
            r'metadata/GO_0xxx/GO_0999'),
    (r'metadata/GO_0xxx(|_v[\d\.]+)/GO_00../GO_00.._(.*)\..*', 0,
            [r'metadata/GO_0xxx/GO_0999/GO_0999_\2.tab',
             r'metadata/GO_0xxx/GO_0999/GO_0999_\2.lbl',
            ]),
])

####################################################################################################################################
# VERSIONS
####################################################################################################################################

# File names are split in _v1, merged afterward
versions = translator.TranslatorByRegex([
    (r'volumes/GO_0xxx.*/(GO_0.../.*/C\d{6})/?(\d{4}[A-Z]\..*)', 0,
            [r'volumes/GO_0xxx/\1\2',
             r'volumes/GO_0xxx_v1/\1/\2',
            ]),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews)/GO_0xxx/GO_....(|/BROWSE)/([CEGIJ][0-9]{1,2}|REDO)/.*',               0, (True, True, True)),

    (r'(volumes|previews)/GO_0xxx_v1/GO_....(|/BROWSE)/([CEGIJ][0-9]{1,2}|REDO)/.*/C[0-9]{6}',  0, (True, True, False)),
    (r'(volumes|previews)/GO_0xxx_v1/GO_....(|/BROWSE)/([CEGIJ][0-9]{1,2}|REDO)/.*',            0, (True, True, True)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'(volumes|previews)/GO_0xxx(|_v[1-9])/\w+(|/REDO)/([CEGIJ][0-9]{1,2})', 0,
            [r'\1/GO_0xxx\2/*/\4',
             r'\1/GO_0xxx\2/*/REDO/\4'
            ]),
    (r'(volumes|previews)/GO_0xxx(|_v[1-9])/\w+(|/REDO)/[CEGIJ][0-9]{1,2}/(\w+)', 0,
            [r'\1/GO_0xxx\2/*/*/\4',
             r'\1/GO_0xxx\2/*/REDO/*/\4',
            ]),
    (r'(volumes|previews)/GO_0xxx(|_v[1-9])/\w+(|/REDO)/[CEGIJ][0-9]{1,2}/(\w+)/C\d{6}', 0, 
            [r'\1/GO_0xxx\2/*/*/\4/*',
             r'\1/GO_0xxx\2/*/REDO/*/\4/*',
            ]),
])

####################################################################################################################################
# SORT_KEY
####################################################################################################################################

sort_key = translator.TranslatorByRegex([

    # Puts encounters in chronological order, after AAREADME, in root directory
    (r'([CEGIJ])([0-9])',      0, r'AAZ0\2\1'),
    (r'([CEGIJ])([0-9][0-9])', 0, r'AAZ\2\1'),
    (r'(AAREADME.TXT)',        0, r'\1'),
    (r'(CATALOG)',             0, r'\1'),
    (r'(DOCUMENT)',            0, r'\1'),
    (r'(ERRATA.TXT)',          0, r'\1'),
    (r'(INDEX)',               0, r'\1'),
    (r'(LABEL)',               0, r'\1'),
    (r'(REDO)',                0, r'\1'),
    (r'(VOLDESC.CAT)',         0, r'\1'),
])

####################################################################################################################################
# OPUS_TYPE
####################################################################################################################################

opus_type = translator.TranslatorByRegex([
    (r'volumes/GO_0xxx/GO_0.../(?!CATALOG|DOCUMENT|INDEX|LABEL).*\.(IMG|LBL)', 0, ('Galileo SSI', 10, 'gossi_raw', 'Raw Image', True)),
    (r'volumes/GO_0xxx(|_v[1-9])/GO_0.../(?!CATALOG|DOCUMENT|INDEX|LABEL).*\.(IMG|LBL)', 0, ('Galileo SSI', 10, 'gossi_raw', 'Raw Image', True)),
])

####################################################################################################################################
# OPUS_FORMAT
####################################################################################################################################

opus_format = translator.TranslatorByRegex([
    (r'.*\.IMG', 0, ('Binary', 'VICAR')),
])

####################################################################################################################################
# OPUS_PRODUCTS
####################################################################################################################################

# NOTE: _v1 files have been intentionally removed
opus_products = translator.TranslatorByRegex([

    # Include REPAIRED for anything GARBLED
    (r'.*volumes/GO_0xxx/(GO_0.*)/GARBLED/(C\d{6})(\d{4})R\.(IMG|LBL)', 0,
            [r'volumes/GO_0xxx/\1/REPAIRED/\2\3S.IMG',
             r'volumes/GO_0xxx/\1/REPAIRED/\2\3S.LBL',
             r'previews/GO_0xxx/\1/REPAIRED/\2\3S_full.jpg',
             r'previews/GO_0xxx/\1/REPAIRED/\2\3S_med.jpg',
             r'previews/GO_0xxx/\1/REPAIRED/\2\3S_small.jpg',
             r'previews/GO_0xxx/\1/REPAIRED/\2\3S_thumb.jpg',
            ]),

    # Include TIRETRACK for GO_0020/E12/EUROPA
    (r'.*volumes/GO_0xxx/GO_0020/E12/EUROPA/(C\d{6})(\d{4})R\.(IMG|LBL)', 0,
            [r'volumes/GO_0xxx/GO_0020/E12/TIRETRACK/\1\2S.IMG',
             r'volumes/GO_0xxx/GO_0020/E12/TIRETRACK/\1\2S.LBL',
             r'previews/GO_0xxx/GO_0020/E12/TIRETRACK/\1\2S_full.jpg',
             r'previews/GO_0xxx/GO_0020/E12/TIRETRACK/\1\2S_med.jpg',
             r'previews/GO_0xxx/GO_0020/E12/TIRETRACK/\1\2S_small.jpg',
             r'previews/GO_0xxx/GO_0020/E12/TIRETRACK/\1\2S_thumb.jpg',
            ]),

    # Include GO_0023/REDO for GO_0020/E11/IO
    (r'.*volumes/GO_0xxx/GO_0020/(E11/IO/C\d{6})(\d{4}R)\.(IMG|LBL)', 0,
            [r'volumes/GO_0xxx/GO_0023/REDO/\1\2.IMG',
             r'volumes/GO_0xxx/GO_0023/REDO/\1\2.LBL',
             r'previews/GO_0xxx/GO_0023/REDO/\1\2_full.jpg',
             r'previews/GO_0xxx/GO_0023/REDO/\1\2_med.jpg',
             r'previews/GO_0xxx/GO_0023/REDO/\1\2_small.jpg',
             r'previews/GO_0xxx/GO_0023/REDO/\1\2_thumb.jpg',
            ]),

    # Check GO_0018/REDO for GO_0017/C3/JUPITER
    (r'.*volumes/GO_0xxx/GO_0017/(C3/JUPITER/C\d{6})(\d{4}R)\.(IMG|LBL)', 0,
            [r'volumes/GO_0xxx/GO_0018/REDO/\1\2.IMG',
             r'volumes/GO_0xxx/GO_0018/REDO/\1\2.LBL',
             r'previews/GO_0xxx/GO_0018/REDO/\1\2_full.jpg',
             r'previews/GO_0xxx/GO_0018/REDO/\1\2_med.jpg',
             r'previews/GO_0xxx/GO_0018/REDO/\1\2_small.jpg',
             r'previews/GO_0xxx/GO_0018/REDO/\1\2_thumb.jpg',
            ]),

    # Check GO_0019/REDO for anything on GO_0017 or GO_0018
    (r'.*volumes/GO_0xxx/GO_001[78]/(../\w+/C\d{6})(\d{4}R)\.(IMG|LBL)', 0,
            [r'volumes/GO_0xxx/GO_0019/REDO/\1\2.IMG',
             r'volumes/GO_0xxx/GO_0019/REDO/\1\2.LBL',
             r'previews/GO_0xxx/GO_0019/REDO/\1\2_full.jpg',
             r'previews/GO_0xxx/GO_0019/REDO/\1\2_med.jpg',
             r'previews/GO_0xxx/GO_0019/REDO/\1\2_small.jpg',
             r'previews/GO_0xxx/GO_0019/REDO/\1\2_thumb.jpg',
            ]),

    # Default handling of all product file paths
    (r'.*volumes/(GO_0xxx)/(GO_0...)/(.*/C[0-9]{6})([0-9]{4}[RS])\.(IMG|LBL)', 0,
            [r'volumes/\1/\2/\3\4.IMG',
             r'volumes/\1/\2/\3\4.LBL',
             r'previews/\1/\2/\3\4_full.jpg',
             r'previews/\1/\2/\3\4_med.jpg',
             r'previews/\1/\2/\3\4_small.jpg',
             r'previews/\1/\2/\3\4_thumb.jpg',
             r'metadata/\1/\2/\2_index.lbl',
             r'metadata/\1/\2/\2_index.tab',
            ]),

    # Original products for those designated "REDO"
    (r'.*volumes/GO_0xxx/GO_001[89]/REDO/C3/([A-Z]+/C[0-9]{6})([0-9]{4})R\.(IMG|LBL)', 0,
            [r'volumes/GO_0xxx/GO_0017/C3/\1\2R.IMG',
             r'volumes/GO_0xxx/GO_0017/C3/\1\2R.LBL',
             r'previews/GO_0xxx/GO_0017/C3/\1\2R_full.jpg',
             r'previews/GO_0xxx/GO_0017/C3/\1\2R_med.jpg',
             r'previews/GO_0xxx/GO_0017/C3/\1\2R_small.jpg',
             r'previews/GO_0xxx/GO_0017/C3/\1\2R_thumb.jpg',
            ]),
    (r'.*volumes/GO_0xxx/GO_0019/REDO/(E\d/[A-Z]+/C[0-9]{6})([0-9]{4})R\.(IMG|LBL)', 0,
            [r'volumes/GO_0xxx/GO_0018/\1\2R.IMG',
             r'volumes/GO_0xxx/GO_0018/\1\2R.LBL',
             r'previews/GO_0xxx/GO_0018/\1\2R_full.jpg',
             r'previews/GO_0xxx/GO_0018/\1\2R_med.jpg',
             r'previews/GO_0xxx/GO_0018/\1\2R_small.jpg',
             r'previews/GO_0xxx/GO_0018/\1\2R_thumb.jpg',
            ]),

    # Original products for "TIRETRACK"
    (r'.*volumes/GO_0xxx/GO_0020/E12/TIRETRACK/(C[0-9]{6})([0-9]{4})S\.(IMG|LBL)', 0,
            [r'volumes/GO_0xxx/GO_0020/E12/EUROPA/\1\2R.IMG',
             r'volumes/GO_0xxx/GO_0020/E12/EUROPA/\1\2R.LBL',
             r'previews/GO_0xxx/GO_0020/E12/EUROPA/\1\2R_full.jpg',
             r'previews/GO_0xxx/GO_0020/E12/EUROPA/\1\2R_med.jpg',
             r'previews/GO_0xxx/GO_0020/E12/EUROPA/\1\2R_small.jpg',
             r'previews/GO_0xxx/GO_0020/E12/EUROPA/\1\2R_thumb.jpg',
            ]),

    # Original products for "REPAIRED"
    (r'.*volumes/GO_0xxx/(GO_002[23]/...)(|/IO)/REPAIRED/(C[0-9]{6})([0-9]{4})S\.(IMG|LBL)', 0,
            [r'volumes/GO_0xxx/\1\2/GARBLED/\3\4R.IMG',
             r'volumes/GO_0xxx/\1\2/GARBLED/\3\4R.LBL',
             r'previews/GO_0xxx/\1/\2/GARBLED/\3\4R_full.jpg',
             r'previews/GO_0xxx/\1/\2/GARBLED/\3\4R_med.jpg',
             r'previews/GO_0xxx/\1/\2/GARBLED/\3\4R_small.jpg',
             r'previews/GO_0xxx/\1/\2/GARBLED/\3\4R_thumb.jpg',
            ]),
])

####################################################################################################################################
# OPUS_ID
####################################################################################################################################

opus_id = translator.TranslatorByRegex([
    (r'.*/GO_0xxx/GO_00../.*/C([0-9]{10})[A-Z]\.(IMG|LBL)', 0, r'go-ssi-c\1'),
])

####################################################################################################################################
# OPUS_ID_TO_PRIMARY_LOGICAL_PATH
####################################################################################################################################

# Note: Lists are sorted to make sure that the preferred REDO/REPAIRED/TIRETRACK match comes first
opus_id_to_primary_logical_path = translator.TranslatorByRegex([
    (r'go-ssi-c(03[4-5].*)', 0, [r'volumes/GO_0xxx/GO_0017/??/*/C\1R.IMG']),
    (r'go-ssi-c(036.*)'    , 0, [r'volumes/GO_0xxx/GO_0019/REDO/??/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0018/REDO/??/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0017/??/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0018/??/*/C\1R.IMG']),
    (r'go-ssi-c(037.*)'    , 0, [r'volumes/GO_0xxx/GO_0019/REDO/??/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0018/REDO/??/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0017/??/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0018/??/*/C\1R.IMG']),
    (r'go-ssi-c(038.*)'    , 0, [r'volumes/GO_0xxx/GO_0019/REDO/??/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0018/REDO/??/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0018/??/*/C\1R.IMG']),
    (r'go-ssi-c(039.*)'    , 0, [r'volumes/GO_0xxx/GO_0019/??/*/C\1R.IMG']),
    (r'go-ssi-c(040.*)'    , 0, [r'volumes/GO_0xxx/GO_0019/??/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0019/???/*/C\1R.IMG']),
    (r'go-ssi-c(041.*)'    , 0, [r'volumes/GO_0xxx/GO_0019/???/*/C\1R.IMG']),
    (r'go-ssi-c(04[2-6].*)', 0, [r'volumes/GO_0xxx/GO_0023/REDO/E11/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0020/???/TIRETRACK/C\1S.IMG',
                                 r'volumes/GO_0xxx/GO_0020/???/[A-SU-Z]*/C\1R.IMG']),
    (r'go-ssi-c(04[7-9].*)', 0, [r'volumes/GO_0xxx/GO_0021/???/*/C\1R.IMG']),
    (r'go-ssi-c(05[0-1].*)', 0, [r'volumes/GO_0xxx/GO_0021/???/*/C\1R.IMG']),
    (r'go-ssi-c(052.*)'    , 0, [r'volumes/GO_0xxx/GO_0022/???/*/REPAIRED/C\1S.IMG',
                                 r'volumes/GO_0xxx/GO_0022/???/*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0022/???/*/GARBLED/C\1R.IMG']),
    (r'go-ssi-c(05[3-9].*)', 0, [r'volumes/GO_0xxx/GO_0023/G28/REPAIRED/C\1S.IMG',
                                 r'volumes/GO_0xxx/GO_0023/???/*/C\1R.IMG']),
    (r'go-ssi-c(06.*)'     , 0, [r'volumes/GO_0xxx/GO_0023/???/REPAIRED/C\1S.IMG',
                                 r'volumes/GO_0xxx/GO_0023/???/[A-FH-QS-Z]*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0023/???/R[AIOU]*/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0023/???/GANYMEDE/C\1R.IMG',
                                 r'volumes/GO_0xxx/GO_0023/???/GARBLED/C\1R.IMG']),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class GO_0xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('GO_0xxx', re.I, 'GO_0xxx')]) + \
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
    ASSOCIATIONS['volumes']  += associations_to_volumes
    ASSOCIATIONS['previews'] += associations_to_previews
    ASSOCIATIONS['metadata'] += associations_to_metadata

    VERSIONS = versions + pdsfile.PdsFile.VERSIONS

    FILENAME_KEYLEN = 11    # trim off suffixes

    METADATA_PATH_TRANSLATOR = translator.TranslatorByRegex([
        (r'(.*metadata/GO_0xxx)(|_v[0-9\.]+)/(GO_00..)/\3_(.*)', 0, r'\1\2/$/$_\4')
    ])

    def opus_prioritizer(self, pdsfiles):
        """Prioritizes items that have gone through the pipeline more than once."""

        volumes_found = set()
        metadata_subdict = {}
        for header in list(pdsfiles.keys()): # We change pdsfiles in the loop!
            sublists = pdsfiles[header]

            for sublist in sublists:
                volumes_found.add(sublist[0].volname)   # track volumes used

            if header[0] == 'metadata':
                metadata_subdict[header] = sublists
                continue

            if len(sublists) == 1:
                continue

            if header == '' or not header[0].startswith('Galileo SSI'):
                continue

            # Sort items in each sublist by priority
            priority = []       # (negative version rank, priority from name,
                                #  sublist)
            for sublist in sublists:
                volumes_found.add(sublist[0].volname)   # track volumes used
                abspath = sublist[0].abspath
                prio = 0
                if 'TIRETRACK' in abspath: prio = 1
                if 'REPAIR' in abspath: prio = 1
                if 'REDO' in abspath: prio = 1

                rank = sublist[0].version_rank
                priority.append((-rank, -prio, sublist))

            priority.sort()

            # Select the best product
            prio0 = priority[0][1]
            list0 = [priority[0][2]]

            for (_, prio, sublist) in priority[1:]:
                if prio == prio0:
                    list0.append(sublist)
                    continue

                new_header = (header[0],
                              header[1] + 10,
                              header[2] + '_alternate',
                              header[3] + ' (Superseded Processing)',
                              True)
                if new_header not in pdsfiles:
                    pdsfiles[new_header] = []
                pdsfiles[new_header].append(sublist)

            pdsfiles[header] = list0

        # Add metadata indices for any missing volumes
        volumes_found = list(volumes_found)
        volumes_found.sort()
        for (header,sublists) in metadata_subdict.items():
            if len(sublists) == len(volumes_found):
                continue

            patterns = [pdsf.abspath for pdsf in sublists[0]]
            patterns = [GO_0xxx.METADATA_PATH_TRANSLATOR.first(p) for p in patterns]
            new_sublists = []
            for volume in volumes_found:
                sublist = []
                for pattern in patterns:
                    sublist.append(pdsfile.PdsFile.from_abspath(pattern.replace('$', volume)))
                new_sublists.append(sublist)

            pdsfiles[header] = new_sublists

        return pdsfiles

# Global attribute shared by all subclasses
pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS = translator.TranslatorByRegex([(r'go-ssi-.*', 0, GO_0xxx)]) + \
                                      pdsfile.PdsFile.OPUS_ID_TO_SUBCLASS

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['GO_0xxx'] = GO_0xxx

####################################################################################################################################
# Unit tests
####################################################################################################################################

import pytest
from .pytest_support import *

@pytest.mark.parametrize(
    'input_path,expected',
    [
        ('volumes/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R.IMG',
         {('Galileo SSI',
           10,
           'gossi_raw',
           'Raw Image',
           True): ['volumes/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R.IMG',
                   'volumes/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R.LBL',
                   'volumes/GO_0xxx/GO_0017/LABEL/RLINEPRX.FMT',
                   'volumes/GO_0xxx/GO_0017/LABEL/RTLMTAB.FMT'],
          ('browse',
           10,
           'browse_thumb',
           'Browse Image (thumbnail)',
           False): ['previews/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R_thumb.jpg'],
          ('browse',
           20,
           'browse_small',
           'Browse Image (small)',
           False): ['previews/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R_small.jpg'],
          ('browse',
           30,
           'browse_medium',
           'Browse Image (medium)',
           False): ['previews/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R_med.jpg'],
          ('browse',
           40,
           'browse_full',
           'Browse Image (full)',
           True): ['previews/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R_full.jpg'],
          ('metadata',
           5,
           'rms_index',
           'RMS Node Augmented Index',
           False): ['metadata/GO_0xxx/GO_0017/GO_0017_index.tab',
                    'metadata/GO_0xxx/GO_0017/GO_0017_index.lbl']}
        )
    ]
)
def test_opus_products(input_path, expected):
    opus_products_test(input_path, expected)

def test_opus_id_to_primary_logical_path():
    TESTS = [
        'volumes/GO_0xxx/GO_0017/C3/CALLISTO/C0368211900R.IMG',
        'volumes/GO_0xxx/GO_0017/C3/EUROPA/C0368639400R.IMG',
        'volumes/GO_0xxx/GO_0017/C3/IO/C0368558239R.IMG',
        'volumes/GO_0xxx/GO_0017/C3/JUPITER/C0368369200R.IMG',
        'volumes/GO_0xxx/GO_0017/C3/OPNAV/C0372343200R.IMG',
        'volumes/GO_0xxx/GO_0017/C3/RINGS/C0368974113R.IMG',
        'volumes/GO_0xxx/GO_0017/C3/SML_SATS/C0368495800R.IMG',
        'volumes/GO_0xxx/GO_0017/G1/EUROPA/C0349875100R.IMG',
        'volumes/GO_0xxx/GO_0017/G1/GANYMEDE/C0349632000R.IMG',
        'volumes/GO_0xxx/GO_0017/G1/IO/C0349542152R.IMG',
        'volumes/GO_0xxx/GO_0017/G1/IO/C0350013800R.IMG',
        'volumes/GO_0xxx/GO_0017/G1/JUPITER/C0349605600R.IMG',
        'volumes/GO_0xxx/GO_0017/G1/OPNAV/C0356000600R.IMG',
        'volumes/GO_0xxx/GO_0017/G2/CALLISTO/C0360198468R.IMG',
        'volumes/GO_0xxx/GO_0017/G2/EUROPA/C0360063900R.IMG',
        'volumes/GO_0xxx/GO_0017/G2/GANYMEDE/C0359942400R.IMG',
        'volumes/GO_0xxx/GO_0017/G2/IO/C0359402500R.IMG',
        'volumes/GO_0xxx/GO_0017/G2/JUPITER/C0359509200R.IMG',
        'volumes/GO_0xxx/GO_0017/G2/OPNAV/C0359251000R.IMG',
        'volumes/GO_0xxx/GO_0017/G2/OPNAV/C0364621700R.IMG',
        'volumes/GO_0xxx/GO_0017/G2/RAW_CAL/C0360361122R.IMG',
        'volumes/GO_0xxx/GO_0017/G2/SML_SATS/C0360025813R.IMG',
        'volumes/GO_0xxx/GO_0017/J0/OPNAV/C0346405900R.IMG',
        'volumes/GO_0xxx/GO_0018/E4/EUROPA/C0374649000R.IMG',
        'volumes/GO_0xxx/GO_0018/E4/IO/C0374478045R.IMG',
        'volumes/GO_0xxx/GO_0018/E4/JUPITER/C0374456522R.IMG',
        'volumes/GO_0xxx/GO_0018/E4/OPNAV/C0382058200R.IMG',
        'volumes/GO_0xxx/GO_0018/E4/SML_SATS/C0374546000R.IMG',
        'volumes/GO_0xxx/GO_0018/E6/CALLISTO/C0383944100R.IMG',
        'volumes/GO_0xxx/GO_0018/E6/EUROPA/C0383694600R.IMG',
        'volumes/GO_0xxx/GO_0018/E6/GANYMEDE/C0383768868R.IMG',
        'volumes/GO_0xxx/GO_0018/E6/IO/C0383490245R.IMG',
        'volumes/GO_0xxx/GO_0018/E6/JUPITER/C0383548622R.IMG',
        'volumes/GO_0xxx/GO_0018/E6/OPNAV/C0388834700R.IMG',
        'volumes/GO_0xxx/GO_0018/E6/SML_SATS/C0383612800R.IMG',
        'volumes/GO_0xxx/GO_0018/G7/CALLISTO/C0389556200R.IMG',
        'volumes/GO_0xxx/GO_0018/G7/EUROPA/C0389522100R.IMG',
        'volumes/GO_0xxx/GO_0018/G7/GANYMEDE/C0389917900R.IMG',
        'volumes/GO_0xxx/GO_0018/G7/IO/C0389608268R.IMG',
        'volumes/GO_0xxx/GO_0018/G7/JUPITER/C0389557000R.IMG',
        'volumes/GO_0xxx/GO_0018/G7/OPNAV/C0389266100R.IMG',
        'volumes/GO_0xxx/GO_0018/G7/SML_SATS/C0389705600R.IMG',
        'volumes/GO_0xxx/GO_0018/REDO/C3/JUPITER/C0368977800R.IMG',
        'volumes/GO_0xxx/GO_0019/C10/CALLISTO/C0413382800R.IMG',
        'volumes/GO_0xxx/GO_0019/C9/CALLISTO/C0401505300R.IMG',
        'volumes/GO_0xxx/GO_0019/C9/EUROPA/C0401727700R.IMG',
        'volumes/GO_0xxx/GO_0019/C9/GANYMEDE/C0401668900R.IMG',
        'volumes/GO_0xxx/GO_0019/C9/IO/C0401704700R.IMG',
        'volumes/GO_0xxx/GO_0019/C9/JUPITER/C0401571845R.IMG',
        'volumes/GO_0xxx/GO_0019/C9/RAW_CAL/C0404187800R.IMG',
        'volumes/GO_0xxx/GO_0019/C9/SML_SATS/C0401604400R.IMG',
        'volumes/GO_0xxx/GO_0019/G8/CALLISTO/C0394364268R.IMG',
        'volumes/GO_0xxx/GO_0019/G8/GANYMEDE/C0394517800R.IMG',
        'volumes/GO_0xxx/GO_0019/G8/IO/C0394394100R.IMG',
        'volumes/GO_0xxx/GO_0019/G8/JUPITER/C0394455245R.IMG',
        'volumes/GO_0xxx/GO_0019/G8/SML_SATS/C0394449168R.IMG',
        'volumes/GO_0xxx/GO_0019/REDO/C3/EUROPA/C0368976678R.IMG',
        'volumes/GO_0xxx/GO_0019/REDO/C3/JUPITER/C0368369268R.IMG',
        'volumes/GO_0xxx/GO_0019/REDO/E4/EUROPA/C0374667300R.IMG',
        'volumes/GO_0xxx/GO_0019/REDO/E6/IO/C0383655111R.IMG',
        'volumes/GO_0xxx/GO_0020/E11/CALLISTO/C0420426068R.IMG',
        'volumes/GO_0xxx/GO_0020/E11/EUROPA/C0420617200R.IMG',
        'volumes/GO_0xxx/GO_0020/E11/IO/C0420361523R.IMG',
        'volumes/GO_0xxx/GO_0020/E11/JUPITER/C0420458568R.IMG',
        'volumes/GO_0xxx/GO_0020/E11/RINGS/C0420809545R.IMG',
        'volumes/GO_0xxx/GO_0020/E11/SML_SATS/C0420644201R.IMG',
        'volumes/GO_0xxx/GO_0020/E12/EUROPA/C0426234600R.IMG',
        'volumes/GO_0xxx/GO_0020/E12/GANYMEDE/C0426117300R.IMG',
        'volumes/GO_0xxx/GO_0020/E12/IO/C0426152100R.IMG',
        'volumes/GO_0xxx/GO_0020/E12/TIRETRACK/C0426272849S.IMG',
        'volumes/GO_0xxx/GO_0020/E14/EUROPA/C0440948000R.IMG',
        'volumes/GO_0xxx/GO_0020/E14/GANYMEDE/C0441013078R.IMG',
        'volumes/GO_0xxx/GO_0020/E14/IO/C0440873539R.IMG',
        'volumes/GO_0xxx/GO_0020/E15/EUROPA/C0449961800R.IMG',
        'volumes/GO_0xxx/GO_0020/E15/IO/C0449841900R.IMG',
        'volumes/GO_0xxx/GO_0020/E15/IO/C0450095900R.IMG',
        'volumes/GO_0xxx/GO_0020/E17/EUROPA/C0466581865R.IMG',
        'volumes/GO_0xxx/GO_0020/E17/JUPITER/C0466580845R.IMG',
        'volumes/GO_0xxx/GO_0020/E17/RINGS/C0466612545R.IMG',
        'volumes/GO_0xxx/GO_0021/C20/CALLISTO/C0498206600R.IMG',
        'volumes/GO_0xxx/GO_0021/C21/CALLISTO/C0506142900R.IMG',
        'volumes/GO_0xxx/GO_0021/C22/IO/C0512323300R.IMG',
        'volumes/GO_0xxx/GO_0021/E18/RAW_CAL/C0477421600R.IMG',
        'volumes/GO_0xxx/GO_0021/E19/EUROPA/C0484864900R.IMG',
        'volumes/GO_0xxx/GO_0022/I24/IO/C0520792800R.IMG',
        'volumes/GO_0xxx/GO_0022/I24/IO/GARBLED/C0520792749R.IMG',
        'volumes/GO_0xxx/GO_0022/I24/IO/REPAIRED/C0520792767S.IMG',
        'volumes/GO_0xxx/GO_0022/I25/EUROPA/C0527272700R.IMG',
        'volumes/GO_0xxx/GO_0022/I25/IO/C0527345000R.IMG',
        'volumes/GO_0xxx/GO_0022/I25/SML_SATS/C0527365601R.IMG',
        'volumes/GO_0xxx/GO_0023/C30/CALLISTO/C0605145126R.IMG',
        'volumes/GO_0xxx/GO_0023/E26/EUROPA/C0532836239R.IMG',
        'volumes/GO_0xxx/GO_0023/E26/IO/C0532939900R.IMG',
        'volumes/GO_0xxx/GO_0023/E26/SML_SATS/C0532888100R.IMG',
        'volumes/GO_0xxx/GO_0023/G28/EUROPA/C0552809300R.IMG',
        'volumes/GO_0xxx/GO_0023/G28/GANYMEDE/C0552443500R.IMG',
        'volumes/GO_0xxx/GO_0023/G28/GARBLED/C0552447568R.IMG',
        'volumes/GO_0xxx/GO_0023/G28/JUPITER/C0552766100R.IMG',
        'volumes/GO_0xxx/GO_0023/G28/OPNAV/C0566856700R.IMG',
        'volumes/GO_0xxx/GO_0023/G28/REPAIRED/C0552447569S.IMG',
        'volumes/GO_0xxx/GO_0023/G28/RINGS/C0552599400R.IMG',
        'volumes/GO_0xxx/GO_0023/G29/GANYMEDE/C0584054600R.IMG',
        'volumes/GO_0xxx/GO_0023/G29/IO/C0584260700R.IMG',
        'volumes/GO_0xxx/GO_0023/G29/JUPITER/C0584478200R.IMG',
        'volumes/GO_0xxx/GO_0023/G29/RAW_CAL/C0600486513R.IMG',
        'volumes/GO_0xxx/GO_0023/G29/REPAIRED/C0600491113S.IMG',
        'volumes/GO_0xxx/GO_0023/G29/RINGS/C0584346700R.IMG',
        'volumes/GO_0xxx/GO_0023/I27/IO/C0539931265R.IMG',
        'volumes/GO_0xxx/GO_0023/I27/IO/C0540090500R.IMG',
        'volumes/GO_0xxx/GO_0023/I31/CALLISTO/C0615354300R.IMG',
        'volumes/GO_0xxx/GO_0023/I31/IO/C0615325145R.IMG',
        'volumes/GO_0xxx/GO_0023/I31/JUPITER/C0615698700R.IMG',
        'volumes/GO_0xxx/GO_0023/I31/OPNAV/C0624540800R.IMG',
        'volumes/GO_0xxx/GO_0023/I32/IO/C0625566400R.IMG',
        'volumes/GO_0xxx/GO_0023/I32/JUPITER/C0625967145R.IMG',
        'volumes/GO_0xxx/GO_0023/I32/OPNAV/C0625709200R.IMG',
        'volumes/GO_0xxx/GO_0023/I32/RINGS/C0626030645R.IMG',
        'volumes/GO_0xxx/GO_0023/I32/SML_SATS/C0625614500R.IMG',
        'volumes/GO_0xxx/GO_0023/I33/EUROPA/C0639063400R.IMG',
        'volumes/GO_0xxx/GO_0023/I33/JUPITER/C0639371300R.IMG',
        'volumes/GO_0xxx/GO_0023/I33/OPNAV/C0639004613R.IMG',
        'volumes/GO_0xxx/GO_0023/I33/RAW_CAL/C0647529700R.IMG',
        'volumes/GO_0xxx/GO_0023/REDO/E11/IO/C0420361500R.IMG',
    ]

    for logical_path in TESTS:
        test_pdsf = pdsfile.PdsFile.from_logical_path(logical_path)
        opus_id = test_pdsf.opus_id
        opus_id_pdsf = pdsfile.PdsFile.from_opus_id(opus_id)
        assert opus_id_pdsf.logical_path == logical_path

        # Make sure _v1 exists
        versions = test_pdsf.all_versions()
        assert 10000 in versions
        v1_path = versions[10000].abspath
        v1_path = v1_path.replace('_v1/', '/')
        parts = v1_path.rpartition('/')
        v1_path = parts[0] + parts[2]
        assert v1_path == test_pdsf.abspath

        # Gather all the associated OPUS products
        product_dict = test_pdsf.opus_products()
        product_pdsfiles = []
        for pdsf_lists in product_dict.values():
            for pdsf_list in pdsf_lists:
                product_pdsfiles += pdsf_list

        # Filter out the metadata products and format files
        product_pdsfiles = [pdsf for pdsf in product_pdsfiles
                                 if pdsf.voltype_ != 'metadata/']
        product_pdsfiles = [pdsf for pdsf in product_pdsfiles
                                 if pdsf.extension.lower() != '.fmt']

        # Gather the set of absolute paths
        opus_id_abspaths = set()
        for pdsf in product_pdsfiles:
            opus_id_abspaths.add(pdsf.abspath)

        for pdsf in product_pdsfiles:
            # Every viewset is in the product set
            for viewset in pdsf.all_viewsets.values():
                for viewable in viewset.viewables:
                    assert viewable.abspath in opus_id_abspaths

            # Every associated product is in the product set except metadata
            for category in ('volumes', 'previews'):
                for abspath in pdsf.associated_abspaths(category):
                    assert abspath in opus_id_abspaths

def test_duplicated_products():

    TESTS = [
        ('GO_0018/REDO/C3/JUPITER/C0368976900R.IMG', 'GO_0017/C3/JUPITER/C0368976900R.IMG'    ),
        ('GO_0019/REDO/C3/JUPITER/C0368441600R.IMG', 'GO_0017/C3/JUPITER/C0368441600R.IMG'    ),
        ('GO_0019/REDO/C3/JUPITER/C0368441600R.IMG', 'GO_0017/C3/JUPITER/C0368441600R.IMG'    ),
        ('GO_0019/REDO/E6/IO/C0383655111R.IMG'     , 'GO_0018/E6/IO/C0383655111R.IMG'         ),
        ('GO_0019/REDO/E6/IO/C0383655111R.IMG'     , 'GO_0018/E6/IO/C0383655111R.IMG'         ),
        ('GO_0020/E12/TIRETRACK/C0426272849S.IMG'  , 'GO_0020/E12/EUROPA/C0426272849R.IMG'    ),
        ('GO_0022/I24/IO/REPAIRED/C0520792949S.IMG', 'GO_0022/I24/IO/GARBLED/C0520792949R.IMG'),
    ]

    for (file1, file2) in TESTS:
        pdsf1 = pdsfile.PdsFile.from_logical_path('volumes/GO_0xxx/' + file1)
        pdsf2 = pdsfile.PdsFile.from_logical_path('volumes/GO_0xxx/' + file2)
        assert pdsf1.opus_id == pdsf2.opus_id

        test_pdsf = pdsfile.PdsFile.from_opus_id(pdsf1.opus_id)
        assert test_pdsf.abspath == pdsf1.abspath

        products1 = pdsf1.opus_products()
        products2 = pdsf2.opus_products()

        for key in products1:
            assert key in products2, 'Missing key in products2: ' + str(key)
        for key in products2:
            assert key in products1, 'Missing key in products1: ' + str(key)
        for (key,value1) in products1.items():
            value2 = products2[key]
            assert str(value1) == str(value2), \
                    'Mismatch at ' + str(key) + ': ' + str(value1) + '|||' +\
                    str(value2)

####################################################################################################################################
