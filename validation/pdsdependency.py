#!/usr/bin/env python3
################################################################################
# pdsdependency.py library and main program
#
# Syntax:
#   pdsdependency.py volume_path [volume_path ...]
#
# Enter the --help option to see more information.
################################################################################

import sys
import os
import glob
import re
import argparse

import pdslogger
import pdsfile
import translator

LOGNAME = 'pds.validation.dependencies'
LOGROOT_ENV = 'PDS_LOG_ROOT'

################################################################################
# Translator for tests to apply
#
# Each path to a volume is compared against each regular expression. For those
# regular expressions that match, the associated suite of tests is performed.
# Note that 'general' tests are performed for every volume.
################################################################################

TESTS = translator.TranslatorByRegex([
    ('.*',                          0, ['general']),
    ('.*/COCIRS_0xxx(|_v[3-9])/COCIRS_0[4-9].*',
                                    0, ['cocirs01']),
    ('.*/COCIRS_1xxx(|_v[3-9]).*',  0, ['cocirs01']),
    ('.*/COCIRS_[56]xxx.*',         0, ['cocirs56']),
    ('.*/COISS_[12]xxx.*',          0, ['coiss12', 'cumindex', 'metadata',
                                        'inventory', 'rings', 'moons']),
    ('.*/COISS_100[1-7].*',         0, ['jupiter']),
    ('.*/COISS_100[89].*',          0, ['saturn']),
    ('.*/COISS_2xxx.*',             0, ['saturn']),
    ('.*/COISS_3xxx.*',             0, ['coiss3']),
    ('.*/COUVIS_0xxx.*',            0, ['couvis', 'cumindex', 'metadata',
                                        'supplemental']),
    ('.*/COUVIS_0006.*',            0, ['saturn', 'rings']),
    ('.*/COUVIS_000[7-9].*',        0, ['saturn', 'rings', 'moons']),
    ('.*/COUVIS_00[1-9].*',         0, ['saturn', 'rings', 'moons']),
    ('.*/COVIMS_0.*',               0, ['covims', 'cumindex', 'metadata']),
    ('.*/COVIMS_000[4-9].*',        0, ['saturn', 'rings', 'moons']),
    ('.*/COVIMS_00[1-9].*',         0, ['saturn', 'rings', 'moons']),
    ('.*/CO.*_8xxx.*',              0, ['supplemental', 'profile']),
    ('.*/EBROCC.*',                 0, ['ebrocc']),
    ('.*/GO_0xxx.*',                0, ['go', 'metadata', 'cumindex']),
    ('.*/HST.x_xxxx/.*',            0, ['hst', 'metadata', 'cumindex99']),
    ('.*/NH..(LO|MV)_xxxx.*',       0, ['nh', 'metadata', 'supplemental']),
    ('.*/NH..LO_xxxx.*',            0, ['inventory', 'rings', 'moons']),
    ('.*/NH(JU|LA)MV_xxxx.*',       0, ['nhbrowse_vx', 'jupiter']),
    ('.*/NH(PC|PE)MV_xxxx.*',       0, ['nhbrowse', 'pluto']),
    ('.*/VGISS_[5678]xxx.*',        0, ['vgiss', 'cumindex', 'metadata',
                                        'raw_image', 'supplemental']),
    ('.*/VGISS_5(10[4-9]|20[5-9]|11|21).*',
                                    0, ['jupiter', 'inventory', 'rings',
                                        'moons']),
    ('.*/VGISS_6(10|11[0-5]|2).*',  0, ['saturn', 'inventory', 'rings',
                                        'moons']),
    ('.*/VGISS_7xxx.*',             0, ['uranus', 'inventory', 'rings',
                                        'moons']),
    ('.*/VGISS_8xxx.*',             0, ['neptune', 'inventory', 'rings',
                                        'moons']),
])

################################################################################
# Class definition
################################################################################

class PdsDependency(object):

    DEPENDENCY_SUITES = {}
    MODTIME_DICT = {}

    def __init__(self, title, glob_pattern, regex, sublist, suite=None,
                       newer=True, dir='holdings'):
        """Constructor for a PdsDependency.

        Inputs:
            title           a short description of the dependency.
            glob_pattern    a glob pattern for finding files.
            regex           a regular expression to match the files.
            sublist         a list of substitution strings returning paths to
                            files that must exist.
            suite           optional name of a test suite to which this
                            dependency belongs.
            newer           True if the file file must be newer; False to
                            suppress a check of the modification date.
            dir             root directory of required file.
        """

        self.glob_pattern = glob_pattern

        if type(regex) == str:
            self.regex = re.compile('^' + regex + '$')
        else:
            self.regex = regex

        self.regex_pattern = self.regex.pattern

        if type(sublist) == str:
            self.sublist = [sublist]
        else:
            self.sublist = list(sublist)

        self.title = title
        self.suite = suite
        self.newer = newer

        self.dir_ = dir.rstrip('/') + '/'

        if suite is not None:
            if suite not in PdsDependency.DEPENDENCY_SUITES:
                PdsDependency.DEPENDENCY_SUITES[suite] = []

            PdsDependency.DEPENDENCY_SUITES[suite].append(self)

    @staticmethod
    def purge_cache():
        PdsDependency.MODTIME_DICT = {}

    @staticmethod
    def get_modtime(abspath, logger):
        """Return the Unix-style modification time for a file, recursively for
        a directory. Cache results for directories."""

        if os.path.isfile(abspath):
            return os.path.getmtime(abspath)

        if abspath in PdsDependency.MODTIME_DICT:
            return PdsDependency.MODTIME_DICT[abspath]

        modtime = -1.e99
        files = os.listdir(abspath)
        for file in files:
            absfile = os.path.join(abspath, file)

            if file == '.DS_Store':     # log .DS_Store files; ignore dates
                logger.ds_store('.DS_Store ignored', absfile)
                continue

            if '/._' in absfile:        # log dot-underscore files; ignore dates
                logger.dot_underscore('._* file ignored', absfile)
                continue

            modtime = max(modtime, PdsDependency.get_modtime(absfile, logger))

        PdsDependency.MODTIME_DICT[abspath] = modtime
        return modtime

    def test1(self, dirpath, check_newer=True, limit=200, logger=None):
        """Perform one test and log the results."""

        dirpath = os.path.abspath(dirpath)
        pdsdir = pdsfile.PdsFile.from_abspath(dirpath)
        lskip_ = len(pdsdir.root_)

        if logger is None:
            logger = pdslogger.PdsLogger.get_logger(LOGNAME)

        logger.replace_root([pdsdir.root_, pdsdir.disk_])

        # Remove "Newer" at beginning of titile if check_newer is False
        if not check_newer and self.title.startswith('Newer '):
            logger.open(self.title[6:].capitalize(), dirpath)
        else:
            logger.open(self.title, dirpath)

        try:
            pattern = pdsdir.root_ + self.glob_pattern

            pattern = pattern.replace('$', pdsdir.volset_[:-1], 1)
            if '$' in pattern:
                pattern = pattern.replace('$', pdsdir.volname, 1)

            abspaths = glob.glob(pattern)

            if len(abspaths) == 0:
                logger.info('No files found')

            else:
              for sub in self.sublist:
                logger.open('%s >> %s' % (self.regex_pattern[1:-1], sub),
                            limits={'normal': limit})
                try:
                    for abspath in abspaths:
                        path = abspath[lskip_:]

                        (requirement, count) = self.regex.subn(sub, path)
                        absreq = (pdsdir.disk_ + self.dir_ + requirement)

                        if count == 0:
                            logger.error('Invalid file path', absreq)
                            continue

                        if not os.path.exists(absreq):
                            logger.error('Missing file', absreq)
                            continue

                        if self.newer and check_newer:
                            source_modtime = PdsDependency.get_modtime(abspath,
                                                                       logger)
                            requirement_modtime = \
                                            PdsDependency.get_modtime(absreq,
                                                                      logger)

                            if requirement_modtime < source_modtime:
                                logger.error('File out of date', absreq)
                                continue

                        logger.normal('Confirmed', absreq)

                except (Exception, KeyboardInterrupt) as e:
                    logger.exception(e)
                    raise

                finally:
                    logger.close()

        except (Exception, KeyboardInterrupt) as e:
            logger.exception(e)
            raise

        finally:
            (fatal, errors, warnings, tests) = logger.close()

        return (fatal, errors, warnings, tests)

    @staticmethod
    def test_suite(key, dirpath, check_newer=True, limit=200, logger=None):

        dirpath = os.path.abspath(dirpath)
        pdsdir = pdsfile.PdsFile.from_abspath(dirpath)

        if logger is None:
            logger = pdslogger.PdsLogger.get_logger(LOGNAME)

        logger.replace_root(pdsdir.root_)
        logger.open('Dependency test suite "%s"' % key, dirpath)

        try:
            for dep in PdsDependency.DEPENDENCY_SUITES[key]:
                dep.test1(dirpath, check_newer, limit=limit, logger=logger)

        except (Exception, KeyboardInterrupt) as e:
            logger.exception(e)
            raise

        finally:
            (fatal, errors, warnings, tests) = logger.close()

        return (fatal, errors, warnings, tests)

################################################################################
# General test suite
################################################################################

for thing in pdsfile.VOLTYPES:

    if thing == 'volumes':
        thing_ = ''
    else:
        thing_ = '_' + thing

    Thing = thing.capitalize()

    _ = PdsDependency(
        'Newer archive files for %s'            % thing,
        '%s/$/$'                                % thing,
        r'%s/(.*?)/(.*)'                        % thing,
        r'archives-%s/\1/\2%s.tar.gz'           % (thing, thing_),
        suite='general', newer=True,
    )

    _ = PdsDependency(
        'Newer checksum files for %s'           % thing,
        '%s/$/$'                                % thing,
        r'%s/(.*?)/(.*)'                        % thing,
        r'checksums-%s/\1/\2%s_md5.txt'         % (thing, thing_),
        suite='general', newer=True,
    )

    _ = PdsDependency(
        'Newer checksum files for archives-%s'  % thing,
        'archives-%s/$/$*'                      % thing,
        r'archives-%s/(.*?)/(.*)%s.tar.gz'      % (thing, thing_),
        r'checksums-archives-%s/\1%s_md5.txt'   % (thing, thing_),
        suite='general', newer=True,
    )

    _ = PdsDependency(
        'Newer info shelf files for %s'         % thing,
        '%s/$/$'                                % thing,
        r'%s/(.*?)/(.*)'                        % thing,
        [r'%s/\1/\2_info.shelf'                 % thing,
         r'%s/\1/\2_info.py'                    % thing],
        suite='general', newer=True, dir='shelves/info',
    )

    _ = PdsDependency(
        'Newer info shelf files for archives-%s' % thing,
        'archives-%s/$/$*'                       % thing,
        r'archives-%s/(.*?)/(.*)%s.tar.gz'       % (thing, thing_),
        [r'archives-%s/\1_info.shelf'            % thing,
         r'archives-%s/\1_info.py'               % thing],
        suite='general', newer=True, dir='shelves/info',
    )

for thing in ['volumes', 'metadata', 'calibrated']:

    _ = PdsDependency(
        'Newer link shelf files for %s'             % thing,
        '%s/$/$'                                    % thing,
        r'%s/(.*?)/(.*)'                            % thing,
        [r'%s/\1/\2_links.shelf'                    % thing,
         r'%s/\1/\2_links.py'                       % thing],
        suite='general', newer=True, dir='shelves/links',
    )

################################################################################
# Metadata tests
################################################################################

# General metadata test requiring volname + "_index.tab"
_ = PdsDependency(
    'Metadata index table is newer than index.tab',
    'volumes/$/$',
    r'volumes/([^/]+?)(|_v[0-9.]+)/(.*?)',
    r'metadata/\1/\3/\3_index.tab',
    suite='metadata', newer=False,
)

# More metadata
_ = PdsDependency(
    'Supplemental index table',
    'volumes/$/$',
    r'volumes/([^/]+?)(|_v[0-9.]+)/(.*?)',
    r'metadata/\1/\3/\3_supplemental_index.tab',
    suite='supplemental', newer=False,
)

_ = PdsDependency(
    'Inventory file',
    'volumes/$/$',
    r'volumes/([^/]+?)(|_v[0-9.]+)/(.*?)',
    r'metadata/\1/\3/\3_inventory.tab',
    suite='inventory', newer=False,
)

_ = PdsDependency(
    'Jupiter summary file',
    'volumes/$/$',
    r'volumes/([^/]+?)(|_v[0-9.]+)/(.*?)',
    r'metadata/\1/\3/\3_jupiter_summary.tab',
    suite='jupiter', newer=False,
)

_ = PdsDependency(
    'Saturn summary file',
    'volumes/$/$',
    r'volumes/([^/]+?)(|_v[0-9.]+)/(.*?)',
    r'metadata/\1/\3/\3_saturn_summary.tab',
    suite='saturn', newer=False,
)

_ = PdsDependency(
    'Uranus summary file',
    'volumes/$/$',
    r'volumes/([^/]+?)(|_v[0-9.]+)/(.*?)',
    r'metadata/\1/\3/\3_uranus_summary.tab',
    suite='uranus', newer=False,
)

_ = PdsDependency(
    'Neptune summary file',
    'volumes/$/$',
    r'volumes/([^/]+?)(|_v[0-9.]+)/(.*?)',
    r'metadata/\1/\3/\3_neptune_summary.tab',
    suite='neptune', newer=False,
)

_ = PdsDependency(
    'Pluto/Charon summary file',
    'volumes/$/$',
    r'volumes/([^/]+?)(|_v[0-9.]+)/(.*?)',
    [r'metadata/\1/\3/\3_pluto_summary.tab',
     r'metadata/\1/\3/\3_charon_summary.tab'],
    suite='pluto', newer=False,
)

_ = PdsDependency(
    'Ring summary file',
    'volumes/$/$',
    r'volumes/([^/]+?)(|_v[0-9.]+)/(.*?)',
    r'metadata/\1/\3/\3_ring_summary.tab',
    suite='rings', newer=False,
)

_ = PdsDependency(
    'Moon summary file',
    'volumes/$/$',
    r'volumes/([^/]+?)(|_v[0-9.]+)/(.*?)',
    r'metadata/\1/\3/\3_moon_summary.tab',
    suite='moons', newer=False,
)

_ = PdsDependency(
    'Raw image summary file',
    'volumes/$/$',
    r'volumes/([^/]+?)(|_v[0-9.]+)/(.*?)',
    r'metadata/\1/\3/\3_raw_image_index.tab',
    suite='raw_image', newer=False,
)

_ = PdsDependency(
    'Profile index file',
    'volumes/$/$',
    r'volumes/([^/]+?)(|_v[0-9.]+)/(.*?)',
    r'metadata/\1/\3/\3_profile_index.tab',
    suite='profile', newer=False,
)

_ = PdsDependency(
    'EBROCC index files',
    'volumes/$/$',
    r'volumes/([^/]+?)(|_v[0-9.]+)/(.*?)',
    [r'metadata/\1/\3/PAL_supplemental_index.tab',
     r'metadata/\1/\3/PAL_supplemental_index.lbl',
     r'metadata/\1/\3/PAL_profile_index.tab',
     r'metadata/\1/\3/PAL_profile_index.lbl',
     r'metadata/\1/\3/MCD_supplemental_index.tab',
     r'metadata/\1/\3/MCD_supplemental_index.lbl',
     r'metadata/\1/\3/MCD_profile_index.tab',
     r'metadata/\1/\3/MCD_profile_index.lbl',
     r'metadata/\1/\3/LIC_supplemental_index.tab',
     r'metadata/\1/\3/LIC_supplemental_index.lbl',
     r'metadata/\1/\3/LIC_profile_index.tab',
     r'metadata/\1/\3/IRT_supplemental_index.tab',
     r'metadata/\1/\3/LIC_profile_index.lbl',
     r'metadata/\1/\3/IRT_supplemental_index.lbl',
     r'metadata/\1/\3/IRT_profile_index.tab',
     r'metadata/\1/\3/ES2_supplemental_index.tab',
     r'metadata/\1/\3/IRT_profile_index.lbl',
     r'metadata/\1/\3/ES2_supplemental_index.lbl',
     r'metadata/\1/\3/ES2_profile_index.lbl',
     r'metadata/\1/\3/ES2_profile_index.tab',
     r'metadata/\1/\3/ES1_supplemental_index.tab',
     r'metadata/\1/\3/ES1_supplemental_index.lbl',
     r'metadata/\1/\3/ES1_profile_index.tab',
     r'metadata/\1/\3/ES1_profile_index.lbl'],
    suite='ebrocc', newer=False,
)

################################################################################
# Cumulative index tests where "_x999" is the suffix
################################################################################

_ = PdsDependency(
    'PDS3 label for every metadata table',
    'metadata/$/$/*.tab',
    r'metadata/(.*?)/(.*?)/(.*)\.tab',
    r'metadata/\1/\2/\3.lbl',
    suite='cumindex', newer=False,
)

_ = PdsDependency(
    'Newer cumulative version for every metadata table',
    'metadata/$/$/*.tab',
    r'metadata/(.*?)/(.*?).../(.*?_.)...(.*).tab',
    r'metadata/\1/\g<2>999/\g<3>999\4.tab',
    suite='cumindex', newer=True,
)

_ = PdsDependency(
    'Newer archives and checksums of every cumulative metadata table',
    'metadata/$/*999/*.tab',
    r'metadata/(.*?)/(.*?)/.*\.tab',
    [r'archives-metadata/\1/\2_metadata.tar.gz',
     r'checksums-metadata/\1/\2_metadata_md5.txt',
     r'checksums-archives-metadata/\1_metadata_md5.txt'],
    suite='cumindex', newer=True,
)

_ = PdsDependency(
    'Newer checksums of cumulative index archives',
    'archives-metadata/$/*999_metadata.tar.gz',
    r'archives-metadata/(.*?)/(.*?)999_metadata.tar.gz',
    r'checksums-archives-metadata/\g<2>xxx_metadata_md5.txt',
    suite='cumindex', newer=True,
)

_ = PdsDependency(
    'Newer info shelf files for every cumulative metadata checksum file',
    'metadata/$/*999/*.tab',
    r'metadata/(.*?)/(.*?)/(.*)\.tab',
    [r'metadata/\1/\2_info.shelf',
     r'metadata/\1/\2_info.py',
     r'archives-metadata/\1_info.shelf',
     r'archives-metadata/\1_info.py'],
    suite='cumindex', newer=True, dir='shelves/info'
)

_ = PdsDependency(
    'Newer info shelf files for every cumulative metadata archive',
    'checksums-archives-metadata/$_metadata_md5.txt',
    r'checksums-archives-metadata/(.*?)_metadata_md5.txt',
    [r'archives-metadata/\g<1>_info.shelf',
     r'archives-metadata/\g<1>_info.py'],
    suite='cumindex', newer=True, dir='shelves/info'
)

################################################################################
# Cumulative index tests where "9_9999" is the suffix
################################################################################

_ = PdsDependency(
    'PDS3 label for every metadata table',
    'metadata/$/$/*.tab',
    r'metadata/(.*?)/(.*?)/(.*)\.tab',
    r'metadata/\1/\2/\3.lbl',
    suite='cumindex99', newer=False,
)

_ = PdsDependency(
    'Newer cumulative version for every metadata table',
    'metadata/$/$/*.tab',
    r'metadata/(.*?)/(.*?)._..../(.*?)._....(.*).tab',
    r'metadata/\1/\g<2>9_9999/\g<3>9_9999\4.tab',
    suite='cumindex99', newer=True,
)

_ = PdsDependency(
    'Newer archives and checksums of every cumulative metadata table',
    'metadata/$/*9_9999/*.tab',
    r'metadata/(.*?)/(.*?)/.*\.tab',
    [r'archives-metadata/\1/\2_metadata.tar.gz',
     r'checksums-metadata/\1/\2_metadata_md5.txt',
     r'checksums-archives-metadata/\1_metadata_md5.txt'],
    suite='cumindex99', newer=True,
)

_ = PdsDependency(
    'Newer checksums of cumulative index archives',
    'archives-metadata/$/*9_9999_metadata.tar.gz',
    r'archives-metadata/(.*?)/(.*?)9_9999_metadata.tar.gz',
    r'checksums-archives-metadata/\g<2>x_xxxx_metadata_md5.txt',
    suite='cumindex99', newer=True,
)

_ = PdsDependency(
    'Newer info shelf files for every cumulative metadata checksum file',
    'metadata/$/*9_9999/*.tab',
    r'metadata/(.*?)/(.*?)/(.*)\.tab',
    [r'metadata/\1/\2_info.shelf',
     r'metadata/\1/\2_info.py',
     r'archives-metadata/\1_info.shelf',
     r'archives-metadata/\1_info.py'],
    suite='cumindex99', newer=True, dir='shelves/info'
)

_ = PdsDependency(
    'Newer info shelf files for every cumulative metadata archive',
    'checksums-archives-metadata/$_metadata_md5.txt',
    r'checksums-archives-metadata/(.*?)_metadata_md5.txt',
    [r'archives-metadata/\g<1>_info.shelf',
     r'archives-metadata/\g<1>_info.py'],
    suite='cumindex99', newer=True, dir='shelves/info'
)

################################################################################
# Preview tests
################################################################################

# For COCIRS_0xxx and COCIRS_1xxx
_ = PdsDependency(
    'Preview versions of every cube file',
    'volumes/$/$/EXTRAS/CUBE_OVERVIEW/*/*.JPG',
    r'volumes/(.*)/EXTRAS/CUBE_OVERVIEW/(.*)\.JPG',
    [r'previews/\1/DATA/CUBE/\2_thumb.jpg',
     r'previews/\1/DATA/CUBE/\2_small.jpg',
     r'previews/\1/DATA/CUBE/\2_med.jpg',
     r'previews/\1/DATA/CUBE/\2_full.jpg'],
    suite='cocirs01', newer=True,
)

# For COCIRS_5xxx and COCIRS_6xxx
_ = PdsDependency(
    'Diagrams for every interferogram file',
    'volumes/$/$/BROWSE/*/*.PNG',
    r'volumes/(.*)\.PNG',
    [r'diagrams/\1_thumb.jpg',
     r'diagrams/\1_small.jpg',
     r'diagrams/\1_med.jpg',
     r'diagrams/\1_full.jpg'],
    suite='cocirs56', newer=False,
)

# For COISS_1xxx and COISS_2xxx
_ = PdsDependency(
    'Previews and calibrated versions of every COISS image file',
    'volumes/$/$/data/*/*.IMG',
    r'volumes/(.*)\.IMG',
    [r'previews/\1_thumb.jpg',
     r'previews/\1_small.jpg',
     r'previews/\1_med.jpg',
     r'previews/\1_full.png',
     r'calibrated/\1_CALIB.IMG'],
    suite='coiss12', newer=False,
)

# For COISS_3xxx
_ = PdsDependency(
    'Previews of every COISS derived map image',
    'volumes/$/$/data/images/*.IMG',
    r'volumes/(.*?)/data/images/(.*)\.IMG',
    [r'previews/\1/data/images/\2_thumb.jpg',
     r'previews/\1/data/images/\2_small.jpg',
     r'previews/\1/data/images/\2_med.jpg',
     r'previews/\1/data/images/\2_full.jpg'],
    suite='coiss3', newer=True,
)

_ = PdsDependency(
    'Previews of every COISS derived map PDF',
    'volumes/$/$/data/maps/*.PDF',
    r'volumes/(.*?)/data/maps/(.*)\.PDF',
    [r'previews/\1/data/maps/\2_thumb.png',
     r'previews/\1/data/maps/\2_small.png',
     r'previews/\1/data/maps/\2_med.png',
     r'previews/\1/data/maps/\2_full.png'],
    suite='coiss3', newer=True,
)

# For COUVIS_0xxx
_ = PdsDependency(
    'Newer supplemental index for every COUVIS volume',
    'volumes/$/$/DATA/*/*.lbl',
    r'volumes/(\w+)/(\w+)/.*\.lbl',
    r'metadata/\1/\2/\2_supplemental_index.tab',
    suite='couvis', newer=True,
)

_ = PdsDependency(
    'Previews of every COUVIS data file',
    'volumes/$/$/DATA/*/*.DAT',
    r'volumes/(.*)\.DAT',
    [r'previews/\1_thumb.png',
     r'previews/\1_small.png',
     r'previews/\1_med.png',
     r'previews/\1_full.png'],
    suite='couvis', newer=False,
)

# For COVIMS_0xxx and COVIMS_UNKS
_ = PdsDependency(
    'Previews and calibrated versions of every COVIMS cube',
    'volumes/$/$/data/*/*.qub',
    r'volumes/(.*)\.qub',
    [r'previews/\1_thumb.png',
     r'previews/\1_small.png',
     r'previews/\1_med.png',
     r'previews/\1_full.png'],
    suite='covims', newer=False,
)

# For GO_xxxx
_ = PdsDependency(
    'Previews of every GO image file',
    'volumes/$/$/*/*/*.IMG',
    r'volumes/(.*)\.IMG',
    [r'previews/\1_thumb.jpg',
     r'previews/\1_small.jpg',
     r'previews/\1_med.jpg',
     r'previews/\1_full.jpg'],
    suite='go', newer=True,
)

_ = PdsDependency(
    'Previews of every GO image file',
    'volumes/$/$/*/*.IMG',
    r'volumes/(.*)\.IMG',
    [r'previews/\1_thumb.jpg',
     r'previews/\1_small.jpg',
     r'previews/\1_med.jpg',
     r'previews/\1_full.jpg'],
    suite='go', newer=True,
)

# For HST*x_xxxx
_ = PdsDependency(
    'Previews of every HST image label',
    'volumes/$/$/data/*/*.LBL',
    r'volumes/(HST.._....)(|_v[0-9.]+)/(HST.*)\.LBL',
    [r'previews/\1/\3_thumb.jpg',
     r'previews/\1/\3_small.jpg',
     r'previews/\1/\3_med.jpg',
     r'previews/\1/\3_full.jpg'],
    suite='hst', newer=False,
)

# For NHxxLO_xxxx and NHxxMV_xxxx browse, stripping version number
_ = PdsDependency(
    'Previews of every NH image file',
    'volumes/$/$/data/*/*.fit',
    r'volumes/(NHxx.._....)(|_v[0-9.]+)/(NH.*?)(|_[0-9]+).fit',
    [r'previews/\1/\3_thumb.jpg',
     r'previews/\1/\3_small.jpg',
     r'previews/\1/\3_med.jpg',
     r'previews/\1/\3_full.jpg'],
    suite='nhbrowse', newer=False,
)

# For NHxxLO_xxxx and NHxxMV_xxxx browse, without stripping version number
_ = PdsDependency(
    'Previews of every NH image file',
    'volumes/$/$/data/*/*.fit',
    r'volumes/(NHxx.._....)(|_v[0-9.]+)/(NH.*?).fit',
    [r'previews/\1/\3_thumb.jpg',
     r'previews/\1/\3_small.jpg',
     r'previews/\1/\3_med.jpg',
     r'previews/\1/\3_full.jpg'],
    suite='nhbrowse_vx', newer=False,
)

_ = PdsDependency(
    'Newer supplemental index for every NH volume',
    'volumes/$/$/data/*/*.lbl',
    r'volumes/(NHxx.._....)(|_v[0-9.]+)/(NH...._.00)(.)/.*\.lbl',
    r'metadata/\1/\g<3>1/\g<3>1_supplemental_index.tab',
    suite='nh', newer=True,
)

# For VGISS_[5678]xxx
_ = PdsDependency(
    'Previews of every VGISS image file',
    'volumes/$/$/data/*/*RAW.IMG',
    r'volumes/(.*)_RAW\.IMG',
    [r'previews/\1_thumb.jpg',
     r'previews/\1_small.jpg',
     r'previews/\1_med.jpg',
     r'previews/\1_full.jpg'],
    suite='vgiss', newer=True,
)

################################################################################
################################################################################

def test(pdsdir, logger=None, check_newer=True):
    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)

    path = pdsdir.abspath
    for suite in TESTS.all(path):
        _ = PdsDependency.test_suite(suite, path, check_newer=check_newer,
                                                  logger=logger)

################################################################################
################################################################################

if __name__ == '__main__':

    # Set up parser
    parser = argparse.ArgumentParser(
        description='pdsdependency: Check all required files associated with ' +
                    'with a volume, confirming that they exist and that '      +
                    'their creation dates are consistent.')

    parser.add_argument('volume', nargs='+', type=str,
                        help='The path to the root directory of a volume or '  +
                             'a volume set.')

    parser.add_argument('--log', '-l', type=str, default='',
                        help='Optional root directory for a duplicate of the ' +
                             'log files. If not specified, the value of '      +
                             'environment variable "%s" ' % LOGROOT_ENV        +
                             'is used. In addition, individual logs are '      +
                             'written into the "logs" directory parallel to '  +
                             '"holdings". Logs are created inside the '        +
                             '"pdsdependency" subdirectory of each log root '  +
                             'directory.'
                             )

    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Do not also log to the terminal.')

    # Parse and validate the command line
    args = parser.parse_args()

    status = 0

    # Define the logging directory
    if args.log == '':
        try:
            args.log = os.environ[LOGROOT_ENV]
        except KeyError:
            args.log = None

    # Validate the paths
    for path in args.volume:
        path = os.path.abspath(path)
        pdsdir = pdsfile.PdsFile.from_abspath(path)
        if not pdsdir.is_volume_dir() and not pdsdir.is_volset_dir():
          print('pdsdependency error: ' + \
                'not a volume or volume set directory: ' + pdsdir.logical_path)
          sys.exit(1)

        if pdsdir.category_ != 'volumes/':
          print('pdsdependency error: ' + \
                'not a volume or volume set directory: ' + pdsdir.logical_path)
          sys.exit(1)

    # Initialize the logger
    logger = pdslogger.PdsLogger(LOGNAME)
    pdsfile.PdsFile.set_log_root(args.log)

    if not args.quiet:
        logger.add_handler(pdslogger.stdout_handler)

    if args.log:
        path = os.path.join(args.log, 'pdsdependency')
        warning_handler = pdslogger.warning_handler(path)
        logger.add_handler(warning_handler)

        error_handler = pdslogger.error_handler(path)
        logger.add_handler(error_handler)

    # Generate a list of file paths before logging
    paths = []
    for path in args.volume:

        if not os.path.exists(path):
            print('No such file or directory: ' + path)
            sys.exit(1)

        path = os.path.abspath(path)
        pdsf = pdsfile.PdsFile.from_abspath(path)

        if pdsf.checksums_:
            print('No pdsdependency for checksum files: ' + path)
            sys.exit(1)

        if pdsf.archives_:
            print('No pdsdependency for archive files: ' + path)
            sys.exit(1)

        if pdsf.is_volset_dir():
            paths += [os.path.join(path, c) for c in pdsf.childnames]

        else:
            paths.append(os.path.abspath(path))

    # Loop through paths...
    logger.open(' '.join(sys.argv))
    try:
        for path in paths:

            pdsdir = pdsfile.PdsFile.from_abspath(path)

            # Save logs in up to two places
            logfiles = set([pdsdir.log_path_for_volume(id='dependency',
                                                       dir='pdsdependency'),
                            pdsdir.log_path_for_volume(id='dependency',
                                                       dir='pdsdependency',
                                                       place='parallel')])

            # Create all the handlers for this level in the logger
            local_handlers = []
            for logfile in logfiles:
                logfile = logfile.replace('/volumes/', '/')
                local_handlers.append(pdslogger.file_handler(logfile))
                logdir = os.path.split(logfile)[0]

                # These handlers are only used if they don't already exist
                warning_handler = pdslogger.warning_handler(logdir)
                error_handler = pdslogger.error_handler(logdir)
                local_handlers += [warning_handler, error_handler]

            # Open the next level of the log
            logger.open('Dependency tests', path, handler=local_handlers)

            try:
                for logfile in logfiles:
                    logger.info('Log file', logfile)

                test(pdsdir, logger=logger)

            except (Exception, KeyboardInterrupt) as e:
                logger.exception(e)
                raise

            finally:
                _ = logger.close()

    except (Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        status = 1
        raise

    finally:
        (fatal, errors, warnings, tests) = logger.close()
        if fatal or errors: status = 1

    sys.exit(status)
