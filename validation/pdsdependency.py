#!/usr/bin/env python
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
################################################################################

TESTS = translator.TranslatorByRegex([
    ('.*',                         0,  'general'),
    ('.*/COCIRS_0[4-9]../.*',      0,  'cocirs01'),
    ('.*/COCIRS_1xxx/.*',          0,  'cocirs01'),
    ('.*/COCIRS_[56]xxx/.*',       0,  'cocirs56'),
    ('.*/COISS_[12]xxx/.*',        0, ['coiss12', 'cumindex', 'metadata']),
    ('.*/COISS_3xxx/.*',           0,  'coiss3'),
    ('.*/COUVIS_0xxx/.*',          0, ['couvis', 'cumindex', 'metadata']),
    ('.*/COVIMS_0xxx/COVIMS_0.*',  0, ['covims', 'cumindex', 'metadata']),
    ('.*/COVIMS_0xxx/COVIMS_UNKS', 0, ['covims', 'cumindex_unks', 'metadata']),
    ('.*/GO_xxxx/*',               0,  'go'),
    ('.*/HST.x_xxxx/.*',           0,  'hst'),
    ('.*/NH..(LO|MV)_xxxx/.*',     0, ['nh', 'metadata']),
    ('.*/VGISS_[5678]xxx/.*',      0, ['vgiss', 'cumindex', 'metadata']),
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

        if logger is None:
            logger = pdslogger.PdsLogger.get_logger(LOGNAME)

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

    Thing = thing[0].upper() + thing[1:]

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
# General metadata test
################################################################################

_ = PdsDependency(
    'Metadata index table is newer than index.tab',
    'volumes/$/$/index/index.tab',
    r'volumes/(.*?)/(.*?)/index/index.tab',
    r'metadata/\1/\2/\2_index.tab',
    suite='metadata', newer=True,
)

################################################################################
# Cumulative index tests
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
# Cumulative index tests for COVIMS_UNKS
################################################################################

_ = PdsDependency(
    'PDS3 label for every metadata table',
    'metadata/$/$/*.tab',
    r'metadata/(.*?)/(.*?)/(.*)\.tab',
    r'metadata/\1/\2/\3.lbl',
    suite='cumindex_unks', newer=False,
)

_ = PdsDependency(
    'Newer cumulative version for every metadata table',
    'metadata/$/$/COVIMS_UNKS*.tab',
    r'metadata/(.*?)/COVIMS_UNKS/COVIMS_UNKS(.*).tab',
    r'metadata/\1/COVIMS_0999/COVIMS_0999\2.tab',
    suite='cumindex_unks', newer=True,
)

################################################################################
# Preview tests
################################################################################

# For COCIRS_0xxx and COCIRS_1xxx
_ = PdsDependency(
    'Preview versions of every cube file',
    'volumes/$/$/EXTRAS/CUBE_OVERVIEW/*/*.tar.gz',
    r'volumes/(.*)/EXTRAS/CUBE_OVERVIEW/(.*)\.tar\.gz',
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
     r'previews/\1_full.jpg',
     r'calibrated/\1_CALIB.IMG'],
    suite='coiss12', newer=False,
)

# For COISS_3xxx
_ = PdsDependency(
    'Previews of every COISS derived map',
    'volumes/$/$/data/images/*.IMG',
    r'volumes/(.*?)/data/images/(.*)\.IMG',
    [r'previews/\1/data/images/\2_thumb.jpg',
     r'previews/\1/data/images/\2_small.jpg',
     r'previews/\1/data/images/\2_med.jpg',
     r'previews/\1/data/images/\2_full.jpg'],
    suite='coiss3', newer=True,
)

_ = PdsDependency(
    'Previews of every COISS derived map',
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
    'Newer supplemental index for every NH volume',
    'volumes/$/$/DATA/*/*.lbl',
    r'volumes/(\w+)/(\w+)/.*\.lbl',
    r'metadata/\1/\2/\2_supplemental_index.tab',
    suite='couvis', newer=True,
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
    r'volumes/(.*)\.LBL',
    [r'previews/\1_thumb.jpg',
     r'previews/\1_small.jpg',
     r'previews/\1_med.jpg',
     r'previews/\1_full.jpg'],
    suite='hst', newer=False,
)

# For NHxxLO_xxxx and NHxxMV_xxxx
_ = PdsDependency(
    'Previews of every NH image file',
    'volumes/$/$/data/*/*.fit',
    r'volumes/(.*)\.fit',
    [r'previews/\1_thumb.jpg',
     r'previews/\1_small.jpg',
     r'previews/\1_med.jpg',
     r'previews/\1_full.jpg'],
    suite='nh', newer=False,
)

_ = PdsDependency(
    'Newer supplemental index for every NH volume',
    'volumes/$/$/data/*/*.lbl',
    r'volumes/(\w+)/(\w+)/.*\.lbl',
    r'metadata/\1/\2/\2_supplemental_index.tab',
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

def test(pdsdir, logger=None):
    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)

    path = pdsdir.abspath
    for suite in TESTS.all(path):
        _ = PdsDependency.test_suite(suite, path, logger=logger)

################################################################################
################################################################################

if __name__ == '__main__':

    # Set up parser
    parser = argparse.ArgumentParser(
        description='pdsdependency: Check all required files associated with ' +
                    'with a volume, confirming that they exist and that '      +
                    'their creation dates are consistent.')

    parser.add_argument('volume', nargs='+', type=str,
                        help='The path to the root directory of a volume.')

    parser.add_argument('--log', '-l', type=str, default='',
                        help='Directory for the log files. If not specified, ' +
                             'log files are written to the "validation" '      +
                             'subdirectory of the path defined by '            +
                             'environment variable "%s". ' % LOGROOT_ENV       +
                             'If this is undefined, logs are written to the '  +
                             '"Logs" subdirectory of the current working '     +
                             'directory.')

    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Do not also log to the terminal.')

    # Parse and validate the command line
    args = parser.parse_args()

    status = 0

    # Define the logging directory
    if args.log:
        log_root = args.log
    else:
        try:
            log_root = os.path.join(os.environ[LOGROOT_ENV], 'validation')
        except KeyError:
            log_root = 'Logs'

    # Validate the paths
    for path in args.volume:
        path = os.path.abspath(path)
        pdsdir = pdsfile.PdsFile.from_abspath(path)
        if not pdsdir.is_volume_dir():
            print 'pdsdependency error: not a volume directory: ' + \
                  pdsdir.logical_path
            sys.exit(1)

    # Initialize logger and handler that writes to stdout
    pdsfile.PdsFile.set_log_root(log_root)
    log_path_ = os.path.join(log_root, 'dependency')

    LOGGER = pdslogger.PdsLogger(LOGNAME)

    if not args.quiet:
        LOGGER.add_handler(pdslogger.stdout_handler)

    warning_handler = pdslogger.warning_handler(log_path_)
    LOGGER.add_handler(warning_handler)

    error_handler = pdslogger.error_handler(log_path_)
    LOGGER.add_handler(error_handler)

    LOGGER.open(' '.join(sys.argv))
    try:

        # Loop through paths...
        for path in args.volume:

            path = os.path.abspath(path)
            pdsdir = pdsfile.PdsFile.from_abspath(path)
            logfile = pdsdir.log_path_for_volume('dependency', dir='dependency')
            path_handler = pdslogger.file_handler(logfile)

            LOGGER.open('Dependency tests', path, handler=path_handler)
            LOGGER.info('Log file', logfile)
            LOGGER.replace_root(pdsdir.root_)
            try:
                test(pdsdir, logger=LOGGER)

            except (Exception, KeyboardInterrupt) as e:
                LOGGER.exception(e)
                raise

            finally:
                _ = LOGGER.close()

    except (Exception, KeyboardInterrupt) as e:
        LOGGER.exception(e)
        status = 1
        raise

    finally:
        (fatal, errors, warnings, tests) = LOGGER.close()
        if fatal or errors: status = 1

    sys.exit(status)
