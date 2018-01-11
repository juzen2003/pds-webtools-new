#!/usr/bin/env python
################################################################################
# pdschecksums.py library and main program
#
# Syntax:
#   pdschecksums.py --task path [path ...]
# 
# Enter the --help option to see more information.
################################################################################

import sys
import os
import hashlib
import shutil
import glob
import argparse

import pdslogger
import pdsfile

LOGNAME = 'pds.validation.checksums'
LOGROOT_ENV = 'PDS_LOG_ROOT'

################################################################################

# From http://stackoverflow.com/questions/3431825/-
#       generating-an-md5-checksum-of-a-file

def hashfile(fname, blocksize=65536):
    f = open(fname, 'rb')
    hasher = hashlib.md5()
    buf = f.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = f.read(blocksize)
    return hasher.hexdigest()

################################################################################

def generate_checksums(pdsdir, selection=None, oldpairs=[], regardless=True,
                       limits={'normal':-1}, logger=None):
    """Generate a list of tuples (abspath, checksum) recursively from the given
    directory tree.

    If a selection is specified, it is interpreted as the basename of a file,
    and only that file is processed.

    The optional oldpairs is a list of (abspath, checksum) pairs. For any file
    that already has a checksum in the shortcut list, the checksum is copied
    from this list rather than re-calculated. This list is merged with the
    selection if a selection is identified.

    If regardless is True, then the checksum of a selection is calculated
    regardless of whether it is already in abspairs.
    """

    dirpath = pdsdir.abspath

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)
        logger.replace_root(pdsdir.root_)

    logger.open('Generating MD5 checksums', dirpath, limits=limits)

    md5_dict = {}
    for (abspath, hex) in oldpairs:
        md5_dict[abspath] = hex

    try:
        newtuples = []
        for (path, dirs, files) in os.walk(dirpath):
            for file in files:
                abspath = os.path.join(path, file)

                if selection and file != selection:
                    continue

                if file == '.DS_Store':         # skip .DS_Store files
                    logger.ds_store('.DS_Store skipped', abspath)
                    continue

                if file.startswith('._'):       # skip dot-underscore files
                    logger.dot_underscore('._* file skipped', abspath)
                    continue

                if '/.' in abspath:             # flag invisible files
                    logger.invisible('Invisible file', abspath)

                if regardless and selection:
                    md5 = hashfile(abspath)
                    newtuples.append((abspath, md5, file))
                    logger.normal('Selected MD5=%s' % md5, abspath)

                elif abspath in md5_dict:
                    newtuples.append((abspath, md5_dict[abspath], file))
                    logger.debug('MD5 copied', abspath)
    
                else:
                    md5 = hashfile(abspath)
                    newtuples.append((abspath, md5, file))
                    logger.normal('MD5=%s' % md5, abspath)

        if selection:
            if len(newtuples) == 0:
                raise ValueError('File selection %s not found' % selection)
            if len(newtuples) > 1:
                raise ValueError('Multiple copies of file selection %s found' %
                                 selection)

        # Add new values to dictionary
        for (abspath, md5, _) in newtuples:
            md5_dict[abspath] = md5

        # Restore original order, old keys then new
        old_keys = [p[0] for p in oldpairs]

        newpairs = []
        for key in old_keys:
            newpairs.append((key, md5_dict[key]))
            del md5_dict[key]
 
        for (key, new_md5, new_file) in newtuples:
            if key in md5_dict:     # if not already copied to list of pairs
                newpairs.append((key, md5_dict[key]))

    except (Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        raise

    finally:
        _ = logger.close()

    return newpairs

################################################################################

def read_checksums(checkfile, selection=None, limits={'ds_store':-1},
                              logger=None):

    """Return a list of tuples (abspath, checksum) from a checksum file.

    If a selection is specified, then only the checksum with this file name
    is returned."""

    checkfile = os.path.abspath(checkfile)
    pdscheck = pdsfile.PdsFile.from_abspath(checkfile)

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)
        logger.replace_root(pdscheck.root_)

    logger.open('Reading MD5 checksums', checkfile, limits=limits)

    try:
        prefix_ = pdscheck.dirpath_and_prefix_for_checksum()[1]

        # Read the pairs
        abspairs = []
        try:
          with open(checkfile, 'r') as f:
            for rec in f:
                hexval = rec[:32]
                filepath = rec[34:].rstrip()

                if selection and os.path.basename(filepath) != selection:
                    continue

                basename = os.path.basename(filepath)
                if basename == '.DS_Store':
                    logger.ds_store('.DS_Store checksum ignored', filepath)
                    continue

                if basename.startswith('._'):
                    logger.dot_underscore('._* file skipped', filepath)
                    continue

                if basename[0] == '.':
                    logger.invisible('Checksum for invisible file', filepath)

                abspairs.append((prefix_ + filepath, hexval))
                logger.debug('Read', filepath)
        except IOError as e:
            logger.fatal('Unable to open MD5 checksum file', checkfile)
            sys.exit(1)

        if selection and len(abspairs) == 0:
            raise ValueError('File selection %s not found' % selection)

    except Exception as e:
        logger.exception(e)
        raise

    finally:
        _ = logger.close()

    return abspairs

################################################################################

def checksum_dict(dirpath, logger=None):

    dirpath = os.path.abspath(dirpath)
    pdsdir = pdsfile.PdsFile.from_abspath(dirpath)

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)

    logger.info('Loading checksums for', dirpath, force=True)

    checkfile = pdsdir.checksum_path_and_lskip()[0]
    abspairs = read_checksums(checkfile, logger=logger)

    pair_dict = {}
    for (abspath, checksum) in abspairs:
        pair_dict[abspath] = checksum

    logger.info('Checksum load completed', dirpath, force=True)
    return pair_dict

################################################################################

def write_checksums(checkfile, abspairs,
                    limits={'dot_':-1, 'ds_store':-1, 'invisible':100},
                    logger=None):
    """Write a checksum table containing the given pairs (abspath, checksum)."""

    checkfile = os.path.abspath(checkfile)
    pdscheck = pdsfile.PdsFile.from_abspath(checkfile)

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)
        logger.replace_root(pdscheck.root_)

    logger.open('Writing MD5 checksums', checkfile, limits=limits)

    try:
        # Create parent directory if necessary
        parent = os.path.split(checkfile)[0]
        if not os.path.exists(parent):
            logger.normal('Creating directory', parent)
            os.makedirs(parent)

        prefix_ = pdscheck.dirpath_and_prefix_for_checksum()[1]
        lskip = len(prefix_)

        # Write file
        f = open(checkfile, 'w')
        for pair in abspairs:
            (abspath, hex) = pair

            if abspath.endswith('/.DS_Store'):      # skip .DS_Store files
                logger.ds_store('.DS_Store skipped', abspath)
                continue

            if '/._' in abspath:                    # skip dot-underscore files
                logger.dot_underscore('._* file skipped', abspath)
                continue

            if '/.' in abspath:                     # flag invisible files
                logger.invisible('Invisible file', abspath)

            f.write('%s  %s\n' % (hex, abspath[lskip:]))
            logger.debug('Written', abspath)
    
        f.close()

    except (Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        raise

    finally:
        _ = logger.close()

################################################################################

def validate_pairs(pairs1, pairs2, selection=None, limits={}, logger=None):
    """Validate the first checksum list against the second.

    If a selection is specified, only a file with that basename is checked."""

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)

    logger.open('Validating checksums', limits=limits)

    try:
        checksum_dict = {}
        for (abspath, hex) in pairs2:
            checksum_dict[abspath] = hex

        for (abspath, hex) in pairs1:
            if selection and selection != os.path.basename(abspath):
                continue

            if abspath not in checksum_dict:
                logger.error('Missing checksum', abspath)

            elif hex != checksum_dict[abspath]:
                del checksum_dict[abspath]
                logger.error('Checksum mismatch', abspath)

            else:
                del checksum_dict[abspath]
                logger.normal('Validated', abspath)

        if not selection:
            abspaths = checksum_dict.keys()
            abspaths.sort()
            for abspath in abspaths:
                logger.error('Extra file', abspath)

    except (Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        raise

    finally:
        return logger.close()

################################################################################

def move_old_checksums(checkfile, logfile, logger=None):
    """Appends a version number to an existing checksum file and moves it to
    the associated log directory."""

    if not os.path.exists(checkfile): return

    if not logfile:
        logger.info('Checksum file not backed up', checkfile)

    check_basename = os.path.basename(checkfile)
    (check_prefix, check_ext) = os.path.splitext(check_basename)

    log_dir = os.path.split(logfile)[0]
    dest_template = log_dir + '/' + check_prefix + '_v???' + check_ext

    version_paths = glob.glob(dest_template)

    max_version = 0
    lskip = len(check_ext)
    for version_path in version_paths:
        version = int(version_path[-lskip-3:-lskip])
        max_version = max(max_version, version)

    new_version = max_version + 1
    dest = dest_template.replace('???', '%03d' % new_version)
    shutil.move(checkfile, dest)

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)

    logger.info('Checksum file moved from', checkfile)
    logger.info('Checksum file moved to', dest)

    return dest

################################################################################
# Simplified functions to perform tasks
################################################################################

def initialize(pdsdir, selection, logger=None):

    checkfile = pdsdir.checksum_path_and_lskip()[0]

    # Check selection
    if selection:
        if logger is None:
            logger = pdslogger.PdsLogger.get_logger(LOGNAME)

        logger.fatal('File selection is disallowed for task "initialize": ' +
                     selection)
        sys.exit(1)

    # Check destination
    if os.path.exists(checkfile):
        if logger is None:
            logger = pdslogger.PdsLogger.get_logger(LOGNAME)

        logger.fatal('Checksum file already exists: ' + checkfile)
        sys.exit(1)

    # Generate checksums
    pairs = generate_checksums(pdsdir, logger=logger)

    # Write new checksum file
    write_checksums(checkfile, pairs, logger=logger)

def reinitialize(pdsdir, selection, logfile=None, logger=None):

    checkfile = pdsdir.checksum_path_and_lskip()[0]

    # Re-initialize just the selection; preserve others
    if selection:
        oldpairs = read_checksums(checkfile, logger=logger)
    else:
        oldpairs = []

    # Generate new checksums
    pairs = generate_checksums(pdsdir, selection, oldpairs, regardless=True,
                                       logger=logger)

    # Write new checksum file
    move_old_checksums(checkfile, logfile, logger=logger)
    write_checksums(checkfile, pairs, logger=logger)

def validate(pdsdir, selection, logger=None):

    checkfile = pdsdir.checksum_path_and_lskip()[0]

    # Read checksum file
    md5pairs = read_checksums(checkfile, selection, logger=logger)

    # Generate checksums
    dirpairs = generate_checksums(pdsdir, selection, logger=logger)

    # Validate
    validate_pairs(dirpairs, md5pairs, selection, logger=logger)

def repair(pdsdir, selection, logfile=None, logger=None):

    checkfile = pdsdir.checksum_path_and_lskip()[0]

    # Read destination
    md5pairs = read_checksums(checkfile, logger=logger)

    # Generate checksums
    if selection:
        dirpairs = generate_checksums(pdsdir, selection, md5pairs,
                                              regardless=True, logger=logger)
    else:
        dirpairs = generate_checksums(pdsdir, logger=logger)

    # Compare checksums
    md5pairs.sort()
    dirpairs.sort()
    canceled = (dirpairs == md5pairs)
    if canceled:
        if logger is None:
            logger = pdslogger.PdsLogger.get_logger(LOGNAME)
        logger.info('!!! Checksums match; repair canceled', checkfile)
        return

    # Write checksum file
    move_old_checksums(checkfile, logfile, logger=logger)
    write_checksums(checkfile, dirpairs, logger=logger)

def update(pdsdir, selection, logfile=None, logger=None):

    checkfile = pdsdir.checksum_path_and_lskip()[0]

    # Read destination
    md5pairs = read_checksums(checkfile, logger=logger)

    # Generate checksums if necessary
    dirpairs = generate_checksums(pdsdir, selection, md5pairs, regardless=False,
                                          logger=logger)

    # Compare checksums
    md5pairs.sort()
    dirpairs.sort()
    canceled = (dirpairs == md5pairs)
    if canceled:
        if logger is None:
            logger = pdslogger.PdsLogger.get_logger(LOGNAME)
        logger.info('Checksums match; update canceled', checkfile)
        return

    # Write checksum file
    move_old_checksums(checkfile, logfile, logger=logger)
    write_checksums(checkfile, dirpairs, logger=logger)

################################################################################
# Executable program
################################################################################

if __name__ == '__main__':

    # Set up parser
    parser = argparse.ArgumentParser(
        description='pdschecksums: Create, maintain and validate MD5 '         +
                    'checksum files for PDS volumes and volume sets.')

    parser.add_argument('--initialize', const='initialize',
                        default='', action='store_const', dest='task',
                        help='Create an MD5 checksum file for a volume or '    +
                             'volume set. Abort if the checksum file '         +
                             'already exists.')

    parser.add_argument('--reinitialize', const='reinitialize',
                        default='', action='store_const', dest='task',
                        help='Create an MD5 checksum file for a volume or '    +
                             'volume set. Replace the checksum file if it '    +
                             'already exists. If a single file is specified, ' +
                             'such as one archive file in a volume set, only ' +
                             'single checksum is re-initialized.')

    parser.add_argument('--validate', const='validate',
                        default='', action='store_const', dest='task',
                        help='Validate every file in a volume directory tree ' +
                             'against its MD5 checksum. If a single file '     +
                             'is specified, such as one archive file in a '    +
                             'volume set, only that single checksum is '       +
                             'validated.')

    parser.add_argument('--repair', const='repair',
                        default='', action='store_const', dest='task',
                        help='Validate every file in a volume directory tree ' +
                             'against its MD5 checksum. If any disagreement '  +
                             'is found, the checksum file is replaced; '       +
                             'otherwise it is unchanged. If a single file is ' +
                             'specified, such as one archive file of a '       +
                             'volume set, then only that single checksum is '  +
                             'repaired.')

    parser.add_argument('--update', const='update',
                        default='', action='store_const', dest='task',
                        help='Search a directory for any new files and add '   +
                             'their MD5 checksums to the checksum file. '      +
                             'Checksums of pre-existing files are not checked.')

    parser.add_argument('volume', nargs='+', type=str,
                        help='The path to the root directory of a volume or '  +
                             'volume set. For a volume set, all the volume '   +
                             'directories inside it are handled in sequence. ' +
                             'Note that, for archive directories, checksums '  +
                             'are grouped into one file for the entire '       +
                             'volume set.')

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
        print 'pdschecksums error: Missing task'
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
    log_path_ = os.path.join(log_root, 'checksums')

    LOGGER = pdslogger.PdsLogger(LOGNAME)

    if not args.quiet:
        LOGGER.add_handler(pdslogger.stdout_handler)

    warning_handler = pdslogger.warning_handler(log_path_)
    LOGGER.add_handler(warning_handler)

    error_handler = pdslogger.error_handler(log_path_)
    LOGGER.add_handler(error_handler)

    LOGGER.open(' '.join(sys.argv))
    try:

        abspaths = []
        for path in args.volume:

            # Conver to a list of absolute paths that exist
            path = os.path.abspath(path)
            try:
                pdsf = pdsfile.PdsFile.from_abspath(path, exists=True)
                abspaths.append(pdsf.abspath)

            except (ValueError, IOError):
                # Allow a volume name to stand in for a .tar.gz archive
                (dir, basename) = os.path.split(path)
                pdsdir = pdsfile.PdsFile.from_abspath(dir)
                if pdsdir.archives_ and '.' not in basename:
                    if pdsdir.voltype_ == 'volumes/':
                        basename += '.tar.gz'
                    else:
                        basename += '_%s.tar.gz' % pdsdir.voltype_[:-1]

                    newpaths = glob.glob(os.path.join(dir, basename))
                    if len(newpaths) == 0:
                        raise

                    abspaths += newpaths
                    continue
                else:
                    raise

        # Generate a list of tuples (pdsfile, selection)
        info = []
        for path in abspaths:

            pdsf = pdsfile.PdsFile.from_abspath(path)
            if pdsf.checksums_:
                raise ValueError('No checksums for checksum files')

            if pdsf.is_volset_dir():
                # Archive directories are checksumed by volset
                if pdsf.archives_:
                    info.append((pdsf, None))
                # Others are checksumed by volume
                else:
                    info += [(pdsf.child(c), None) for c in pdsf.childnames]

            elif pdsf.is_volume_dir():
                # Checksum one volume
                info.append((pdsf, None))

            elif pdsf.isdir:
                raise ValueError('Invalid directory for checksumming: ' +
                                 pdsf.logical_path)

            else:
                pdsdir = pdsf.parent()
                if pdsf.is_volume_file():
                    # Checksum one archive file
                    info.append((pdsdir, pdsf.basename))
                elif pdsdir.is_volume_dir():
                    # Checksum one top-level file in volume
                    info.append((pdsdir, pdsf.basename))
                else:
                    raise ValueError('Invalid file for checksumming: ' +
                                     pdsf.logical_path)

        # Loop through tuples...
        for (pdsdir, selection) in info:
            path = pdsdir.abspath

            if selection:
                pdsf = pdsdir.child(os.path.basename(selection))
            else:
                pdsf = pdsdir

            checkfile = pdsdir.checksum_path_and_lskip()[0]

            if pdsf.volname:
                logfile = pdsf.log_path_for_volume(id='md5', task=args.task,
                                                   dir='checksums')
            else:
                logfile = pdsf.log_path_for_volset(id='md5', task=args.task,
                                                   dir='checksums')

            path_handler = pdslogger.file_handler(logfile)

            if selection:
                LOGGER.open('Task "' + args.task + '" for selection ' +
                            selection, path, handler=path_handler)
            else:
                LOGGER.open('Task "' + args.task + '" for', path,
                            handler=path_handler)

            LOGGER.info('Log file', logfile)
            LOGGER.replace_root(pdsdir.root_)
            try:
                if args.task == 'initialize':
                    initialize(pdsdir, selection)

                elif args.task == 'reinitialize':
                    reinitialize(pdsdir, selection, logfile)

                elif args.task == 'validate':
                    validate(pdsdir, selection)

                elif args.task == 'repair':
                    repair(pdsdir, selection, logfile)

                else:   # update
                    update(pdsdir, selection, logfile)

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

