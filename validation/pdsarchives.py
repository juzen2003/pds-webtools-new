#!/usr/bin/env python
################################################################################
# pdsarchives.py library and main program
#
# Syntax:
#   pdsarchives.py --task path [path ...]
# 
# Enter the --help option to see more information.
################################################################################

import sys
import os
import tarfile
import zlib
import argparse

import pdslogger
import pdsfile

LOGNAME = 'pds.validation.archives'
LOGROOT_ENV = 'PDS_LOG_ROOT'

################################################################################
# General tarfile functions
################################################################################

def load_directory_info(pdsdir, limits={'normal':100}, logger=None):
    """Generate a list of tuples (abspath, dirpath, bytes, mod time) recursively
    for the given directory tree.
    """

    dirpath = pdsdir.abspath

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)
        logger.replace_root(pdsdir.root_)

    logger.open('Generating file info', dirpath, limits)

    try:
        (tarpath, lskip) = pdsdir.archive_path_and_lskip()

        tuples = [(dirpath, dirpath[lskip:], 0, 0)]
        for (path, dirs, files) in os.walk(dirpath):

            # Load files
            for file in files:
                abspath = os.path.join(path, file)

                if file == '.DS_Store':         # skip .DS_Store files
                    logger.ds_store('.DS_Store skipped', abspath)
                    continue

                if file.startswith('._'):       # skip dot-underscore files
                    logger.dot_underscore('._* file skipped', abspath)
                    continue

                if '/.' in abspath:             # flag invisible files
                    logger.invisible('Invisible file', abspath)

                bytes = os.path.getsize(abspath)
                modtime = os.path.getmtime(abspath)
                logger.normal('File info generated', abspath)

                tuples.append((abspath, abspath[lskip:], bytes, modtime))

            # Load directories
            for dir in dirs:
                abspath = os.path.join(path, dir)

                if dir.startswith('._'):       # skip dot-underscore files
                    logger.dot_underscore('._* directory skipped', abspath)
                    continue

                if '/.' in abspath:             # flag invisible files
                    logger.invisible('Invisible directory', abspath)

                logger.normal('Directory info generated', abspath)

                tuples.append((abspath, abspath[lskip:], 0, 0))

    except (Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        raise

    finally:
        _ = logger.close()

    return tuples

################################################################################

def read_archive_info(tarpath, limits={'normal':100}, logger=None):
    """Return a list of tuples (abspath, dirpath, bytes, modtime) from a .tar.gz
    file."""

    tarpath = os.path.abspath(tarpath)
    pdstar = pdsfile.PdsFile.from_abspath(tarpath)

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)
        logger.replace_root(pdstar.root_)

    logger.open('Reading archive file', tarpath, limits=limits)

    try:
        (dirpath, prefix) = pdstar.dirpath_and_prefix_for_archive()

        tuples = []
        with tarfile.open(tarpath, 'r:gz') as f:

            members = f.getmembers()
            for member in members:
                abspath = os.path.join(prefix, member.name)

                if abspath.endswith('/.DS_Store'):  # skip .DS_Store files
                    logger.error('.DS_Store in tarfile', abspath)

                if '/._' in abspath:                # skip dot-underscore files
                    logger.error('._* file in tarfile', abspath)

                if '/.' in abspath:                 # flag invisible files
                    logger.invisible('Invisible file found', abspath)

                if member.isdir():
                    tuples.append((abspath, member.name, 0, 0))
                else:
                    tuples.append((abspath, member.name, member.size,
                                            member.mtime))

                logger.normal('Info read', abspath)

    except (zlib.error, Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        raise

    finally:
        _ = logger.close()

    return tuples

################################################################################

def write_archive(pdsdir, clobber=True, archive_invisible=True,
                           limits={'normal':-1, 'dot_':100}, logger=None):
    """Write an archive file containing all the files in the directory."""

    def archive_filter(member):
        """Internal function to filter filenames"""

        # Erase user info
        member.uid = member.gid = 0
        member.uname = member.gname = "root"

        # Check for valid file names
        basename = os.path.basename(member.name)
        if basename == '.DS_Store':
            logger.ds_store('.DS_Store file skipped', member.name)
            return None

        if basename.startswith('._') or '/._' in member.name:
            logger.dot_underscore('._* file skipped', member.name)
            return None

        if basename.startswith('.') or '/.' in member.name:
            if archive_invisibles:
                logger.invisible('Invisible file archived', member.name)
                return member
            else:
                logger.invisible('Invisible file skipped', member.name)
                return None

        logger.normal('File archived', member.name)
        return member

    #### Begin active code

    dirpath = pdsdir.abspath

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)
        logger.replace_root(pdsdir.root_)

    logger.open('Writing .tar.gz file for', dirpath, limits=limits)

    try:
        (tarpath, lskip) = pdsdir.archive_path_and_lskip()

        if not clobber and os.path.exists(tarpath):
            logger.fatal('Archive file already exists', tarpath)
            sys.exit(1)

        f = tarfile.open(tarpath, mode='w:gz')
        f.add(dirpath, arcname=dirpath[lskip:], recursive=True,
                      filter=archive_filter)
        logger.normal('Written', tarpath)
        f.close()

    except (Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        raise

    finally:
        _ = logger.close()

################################################################################

def validate_tuples(dir_tuples, tar_tuples, limits={'normal':100}, logger=None):
    """Validate the directory list of tuples against the list from the tarfile.
    """

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)

    logger.open('Validating file information', limits=limits)

    try:
        tardict = {}
        for (abspath, dirpath, bytes, modtime) in tar_tuples:
            tardict[abspath] = (dirpath, bytes, modtime)

        for (abspath, dirpath, bytes, modtime) in dir_tuples:
            if abspath not in tardict:
                logger.error('Missing from tar file', abspath)

            elif (dirpath, bytes, modtime) != tardict[abspath]:

                if bytes != tardict[abspath][1]:
                    logger.error('Byte count mismatch', abspath)

                if modtime != tardict[abspath][2]:
                    logger.error('Modification time mismatch', abspath)

                del tardict[abspath]

            else:
                logger.normal('Validated', dirpath)
                del tardict[abspath]

        keys = tardict.keys()
        keys.sort()
        for abspath in keys:
            logger.error('Missing from directory', abspath)

    except (Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        raise

    finally:
        return logger.close()

################################################################################
# Simplified functions to perform tasks
################################################################################

def initialize(pdsdir, logger=None):
    write_archive(pdsdir, clobber=False, logger=logger)

def reinitialize(pdsdir, logger=None):
    write_archive(pdsdir, clobber=True, logger=logger)

def validate(pdsdir, logger=None):

    dir_tuples = load_directory_info(pdsdir, logger=logger)

    tarpath = pdsdir.archive_path_and_lskip()[0]
    tar_tuples = read_archive_info(tarpath, logger=logger)

    validate_tuples(dir_tuples, tar_tuples, logger=logger)

def repair(pdsdir, logger=None):

    dir_tuples = load_directory_info(pdsdir, logger=logger)

    tarpath = pdsdir.archive_path_and_lskip()[0]
    tar_tuples = read_archive_info(tarpath, logger=logger)

    # Compare
    dir_tuples.sort()
    tar_tuples.sort()
    canceled = (dir_tuples == tar_tuples)
    if canceled:
        if logger is None:
            logger = pdslogger.PdsLogger.get_logger(LOGNAME)
        logger.info('!!! Files match; repair canceled', tarpath)
        return

    # Overwrite tar file if necessary
    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)

    logger.info('Discrepancies found; writing new file', tarpath)
    write_archive(pdsdir, clobber=True, logger=logger)

################################################################################
# Executable program
################################################################################

if __name__ == '__main__':

    # Set up parser
    parser = argparse.ArgumentParser(
        description='pdsarchives: Create, maintain and validate .tar.gz '      +
                    'archives of PDS volume directory trees.')

    parser.add_argument('--initialize', const='initialize',
                        default='', action='store_const', dest='task',
                        help='Create a .tar.gz archive for a volume. Abort '   +
                             'if the archive already exists.')

    parser.add_argument('--reinitialize', const='reinitialize',
                        default='', action='store_const', dest='task',
                        help='Create a .tar.gz archive for a volume. Replace ' +
                             'the archive if it already exists.')

    parser.add_argument('--validate', const='validate',
                        default='', action='store_const', dest='task',
                        help='Validate every file in a volume against the '    +
                             'contents of its .tar.gz archive. Files match '   +
                             'if they have identical byte counts and '         +
                             'modification dates; file contents are not '      +
                             'compared.')

    parser.add_argument('--repair', const='repair',
                        default='', action='store_const', dest='task',
                        help='Validate every file in a volume against the '    +
                             'contents of its .tar.gz archive. If any file '   +
                             'has changed, write a new archive.')

    parser.add_argument('volume', nargs='+', type=str,
                        help='The path to the root of the volume or volume '   +
                             'set. For a volume set, all the volume '          +
                             'directories inside it are handled in sequence.')

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

    if not args.task:
        print 'pdsarchives error: Missing task'
        sys.exit(1)

    status = 0

    # Define the logging directory
    if args.log:
        log_root = args.log
    else:
        try:
            log_root = os.path.join(os.environ[LOGROOT_ENV], 'validation')
        except KeyError:
            log_root = 'Logs'

    # Initialize the logger
    pdsfile.PdsFile.set_log_root(log_root)
    log_path_ = os.path.join(log_root, 'archives')

    LOGGER = pdslogger.PdsLogger(LOGNAME)

    if not args.quiet:
        LOGGER.add_handler(pdslogger.stdout_handler)

    warning_handler = pdslogger.warning_handler(log_path_)
    LOGGER.add_handler(warning_handler)

    error_handler = pdslogger.error_handler(log_path_)
    LOGGER.add_handler(error_handler)

    LOGGER.open(' '.join(sys.argv))
    try:

        # Generate a list of pdsfiles for volume directories
        pdsdirs = []
        for path in args.volume:

            path = os.path.abspath(path)
            pdsf = pdsfile.PdsFile.from_abspath(path)
            if pdsf.checksums_:
                raise ValueError('No archives for checksum files')

            if pdsf.archives_:
                raise ValueError('No archives for archive files')

            try:
                pdsdir = pdsf.volume_pdsdir()
                pdsdirs.append(pdsdir)
            except ValueError:
                pdsdir = pdsf.volset_pdsdir()
                pdsdirs += [pdsdir.child(c) for c in pdsdir.childnames]

        # Loop through pdsdirs...
        for pdsdir in pdsdirs:

            logfile = pdsdir.log_path_for_volume(id='targz', task=args.task,
                                                 dir='archives')
            path_handler = pdslogger.file_handler(logfile)

            LOGGER.open('Task %s for' % args.task, pdsdir.abspath,
                                                   handler=path_handler)
            LOGGER.info('Log file', logfile)
            LOGGER.replace_root(pdsdir.root_)
            try:

                if args.task == 'initialize':
                    initialize(pdsdir)

                elif args.task == 'reinitialize':
                    reinitialize(pdsdir)

                elif args.task == 'validate':
                    validate(pdsdir)

                else:
                    repair(pdsdir)

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
