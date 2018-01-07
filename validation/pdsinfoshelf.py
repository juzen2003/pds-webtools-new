#!/usr/bin/env python
################################################################################
# pdsinfoshelf.py library and main program
#
# Syntax:
#   pdsinfoshelf.py --task path [path ...]
# 
# Enter the --help option to see more information.
################################################################################

import sys
import os
import shelve
import shutil
import glob
import datetime
import argparse
from PIL import Image

import pdslogger
import pdsfile
import pdschecksums

LOGNAME = 'pds.validation.fileinfo'
LOGROOT_ENV = 'PDS_LOG_ROOT'

PREVIEW_EXTS = set(['.jpg', '.png', '.gif', '.tif', '.tiff',
                    '.jpeg', '.jpeg_small'])

################################################################################

def generate_infodict(pdsdir, selection, old_infodict={},
                               limits={'normal':-1}, logger=None):
    """Generate a dictionary keyed by absolute file path for each file in the
    directory tree. Value returned is a tuple (bytes, child_count, modtime,
    checksum, preview size).

    If a selection is specified, it is interpreted as the basename of a file,
    and only that file is processed.

    The optional old_infodict overrides information found in the directory.
    This dictionary is merged with the new information assembled. However, if
    a selection is specified, information about the selection is always updated.
    """

    def get_info(abspath, infodict, checkdict):

        if os.path.isdir(abspath):
            bytes = 0
            children = 0
            modtime = ''
            checksum = ''
            size = (0,0)

            files = os.listdir(abspath)
            for file in files:
                absfile = os.path.join(abspath, file)

                if file == '.DS_Store':         # skip .DS_Store files
                    logger.ds_store('.DS_Store skipped', absfile)
                    continue

                if file.startswith('._'):       # skip dot-underscore files
                    logger.dot_underscore('._* file skipped', absfile)
                    continue

                if '/.' in abspath:             # flag invisible files
                    logger.invisible('Invisible file', absfile)

                info = get_info(absfile, infodict, checkdict)
                bytes += info[0]
                children += 1
                modtime = max(modtime, info[2])

        else:
            bytes = os.path.getsize(abspath)
            children = 0
            dt = datetime.datetime.fromtimestamp(os.path.getmtime(abspath))
            modtime = dt.strftime('%Y-%m-%d %H:%M:%S.%f')
            try:
                checksum = checkdict[abspath]
            except KeyError:
                logger.fatal('Missing checksum', abspath)
                sys.exit(1)

            size = (0,0)
            ext = os.path.splitext(abspath)[1]
            if ext.lower() in PREVIEW_EXTS:
                try:
                    im = Image.open(abspath)
                    size = im.size
                except Exception:
                    logger.error('Preview size not found', abspath)

        logger.normal('File info generated', abspath, force=True)
        info = (bytes, children, modtime, checksum, size)
        infodict[abspath] = info

        return info

    ################################
    # Begin executable code
    ################################

    dirpath = pdsdir.abspath

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)
        logger.replace_root(pdsdir.root_)

    if selection:
        logger.open('Generating file info for selection "%s"' % selection,
                    dirpath, limits)
    else:
        logger.open('Generating file info', dirpath, limits)

    found = False
    try:
        # Load checksum dictionary
        checkdict = pdschecksums.checksum_dict(dirpath, logger=logger)

        # Generate info recursively
        infodict = {}
        if selection:
            root = os.path.join(dirpath, selection)
        else:
            root = pdsdir.abspath

        _ = get_info(root, infodict, checkdict)

        # Merge dictionaries
        merged = old_infodict.copy()

        if selection:
            merged[root] = infodict[root]

        else:
            for (key, value) in infodict.iteritems():
                if key not in merged:
                    merged[key] = infodict[key]

        return merged

    except (Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        raise

    finally:
        _ = logger.close()

################################################################################

def shelve_infodict(pdsdir, infodict, limits={}, logger=None):
    """Write a new info shelf file for a directory tree."""

    # Initialize
    dirpath = pdsdir.abspath

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)
        logger.open('Shelving file info for', dirpath, limits=limits)

    logger.replace_root(pdsdir.root_)

    try:
        (shelf_path, lskip) = pdsdir.shelf_path_and_lskip(id='info')
        logger.info('Shelf file', shelf_path)

        # Write the shelf
        shelf = shelve.open(shelf_path, flag='n')

        for (key, values) in infodict.iteritems():
            shelf[key[lskip:]] = values

        shelf.close()

    except (Exception, KeyboardInterrupt), e:
        logger.exception(e)
        raise

    finally:
        _ = logger.close()

    logger.open('Writing Python dictionary', dirpath, limits=limits)
    try:
        # Determine the maximum length of the file path
        len_path = 0
        for (abspath, values) in infodict.iteritems():
            len_path = max(len_path, len(abspath))

        len_path -= lskip

        # Write the python dictionary version
        python_path = shelf_path[:-5] + 'py'
        name = os.path.basename(python_path)
        parts = name.split('_')
        name = '_'.join(parts[:2]) + '_info'
        abspaths = infodict.keys()
        abspaths.sort()

        with open(python_path, 'w') as f:
            f.write(name + ' = {\n')
            for abspath in abspaths:
                path = abspath[lskip:]
                (bytes, children, modtime, checksum, size) = infodict[abspath]
                f.write('    "%s: ' % (path + '"' + (len_path-len(path)) * ' '))
                f.write('(%11d, %3d, ' % (bytes, children))
                f.write('"%s", ' % modtime)
                f.write('"%-33s, ' % (checksum + '"'))
                f.write('(%4d,%4d)),\n' % size)

            f.write('}\n\n')

    except (Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        raise

    finally:
        _ = logger.close()

################################################################################

def load_infodict(pdsdir, logger=None):

    dirpath = pdsdir.abspath
    dirpath_ = dirpath.rstrip('/') + '/'

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)
        logger.replace_root(pdsdir.root_)

    logger.open('Reading info file for', dirpath_[:-1])

    try:
        (shelf_path, lskip) = pdsdir.shelf_path_and_lskip(id='info')
        logger.info('Shelf file', shelf_path)

        if not os.path.exists(shelf_path):
            raise IOError('File not found: ' + shelf_path)

        shelf = shelve.open(shelf_path, flag='r')

        infodict = {}
        for key in shelf.keys():
            if key == '':
                infodict[dirpath_[:-1]] = shelf[key]
            else:
                infodict[dirpath_[:lskip] + key] = shelf[key]

        shelf.close()
        return infodict

    except (Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        raise

    finally:
        _ = logger.close()

################################################################################

def validate_infodict(dirpath, dirdict, shelfdict,
                               limits={'normal': 0}, logger=None):

    dirpath = os.path.abspath(dirpath)
    pdsdir = pdsfile.PdsFile.from_abspath(dirpath)

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)
        logger.replace_root(pdsdir.root_)

    logger.open('Validating file info for', dirpath, limits=limits)

    try:
        keys = dirdict.keys()
        for key in keys:
            if key in shelfdict:
                dirinfo = dirdict[key]
                shelfinfo = shelfdict[key]

                (bytes1, count1, modtime1, checksum1, size1) = dirinfo
                (bytes2, count2, modtime2, checksum2, size2) = shelfinfo

                agreement = True
                if bytes1 != bytes2:
                    logger.error('File size mismatch %d %d' %
                                    (bytes1, bytes2), key)
                    agreement = False

                if count1 != count2:
                    logger.error('Child count mismatch %d %d' %
                                    (count1, count1), key)
                    agreement = False

                if modtime1 != modtime2:
                    logger.error('Modification time mismatch "%s" "%s"' %
                        (modtime1, modtime2), key)
                    agreement = False

                if checksum1 != checksum1:
                    logger.error('Modification time mismatch', key)
                    agreement = False

                if size1 != size2:
                    logger.error('Display size mismatch', key)
                    agreement = False

                if agreement:
                    logger.normal('File info matches', key)

                del shelfdict[key]
                del dirdict[key]

        keys = dirdict.keys()
        keys.sort()
        for key in keys:
            logger.error('Missing shelf info for', key)

        keys = shelfdict.keys()
        keys.sort()
        for key in keys:
            logger.error('Shelf info for missing file', key)

    except (Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        raise

    finally:
        return logger.close()

################################################################################

def move_old_info(shelf_file, logfile, logger=None):
    """Move a file to the /logs/ directory tree and append a time tag."""

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)

    shelf_basename = os.path.basename(shelf_file)
    (shelf_prefix, shelf_ext) = os.path.splitext(shelf_basename)

    log_dir = os.path.split(logfile)[0]
    dest_template = log_dir + '/' + shelf_prefix + '_v???' + shelf_ext

    version_paths = glob.glob(dest_template)

    max_version = 0
    lskip = len(shelf_ext)
    for version_path in version_paths:
        version = int(version_path[-lskip-3:-lskip])
        max_version = max(max_version, version)

    new_version = max_version + 1
    dest = dest_template.replace('???', '%03d' % new_version)
    shutil.move(shelf_file, dest)

    logger.info('Info shelf file moved from', shelf_file)
    logger.info('Info shelf file moved to', dest)

    python_file = shelf_file[:-5] + 'py'
    dest = dest[:-5] + 'py'
    shutil.move(python_file, dest)

    return dest

################################################################################
# Simplified functions to perform tasks
################################################################################

def initialize(pdsdir, selection, logger=None):

    infofile = pdsdir.shelf_path_and_lskip(id='info')[0]

    # Check selection
    if selection:
        if logger is None:
            logger = pdslogger.PdsLogger.get_logger(LOGNAME)
        logger.fatal('File selection is disallowed for task "initialize": ' +
                     selection)
        sys.exit(1)

    # Check destination
    if os.path.exists(infofile):
        if logger is None:
            logger = pdslogger.PdsLogger.get_logger(LOGNAME)
        logger.fatal('Info file already exists: ' + infofile)
        sys.exit(1)

    # Create parent directory if necessary
    parent = os.path.split(infofile)[0]
    if not os.path.exists(parent):
        os.makedirs(parent)

    # Generate info
    infodict = generate_infodict(pdsdir, selection, logger=logger)

    # Save info file
    shelve_infodict(pdsdir, infodict, logger=logger)

def reinitialize(pdsdir, selection, logger=None):

    infofile = pdsdir.shelf_path_and_lskip(id='info')[0]

    # Create parent directory if necessary
    parent = os.path.split(infofile)[0]
    if not os.path.exists(parent):
        os.makedirs(parent)

    # Generate info
    infodict = generate_infodict(pdsdir, selection, logger=logger)

    # Move old file if necessary
    if os.path.exists(infofile):
        logfile = pdsfile.PdsFile.log_path_for_shelf(infofile, 'reinitialize',
                                                     selection)
        move_old_info(infofile, logfile, logger=logger)

    # Save info file
    shelve_infodict(pdsdir, infodict, logger=logger)

def validate(pdsdir, selection, logger=None):

    shelf_infodict = load_infodict(infofile, logger=logger)
    dir_infodict = generate_infodict(pdsdir, selection, logger=logger)

    # Validate
    validate_infodict(pdsdir, dir_infodict, shelf_infodict, logger=logger)

def repair(pdsdir, selection, logger=None):

    infofile = pdsdir.shelf_path_and_lskip(id='info')[0]

    shelf_infodict = load_infodict(infofile, logger=logger)
    dir_infodict = generate_infodict(pdsdir, selection, logger=logger)

    # For a single selection, use the old information
    if selection:
        key = dir_infodict.keys()[0]
        value = dir_infodict[key]
        dir_infodict = shelf_infodict.copy()
        dir_infodict[key] = value

    # Compare
    canceled = (dir_infodict == shelf_infodict)
    if canceled:
        if logger is None:
            logger = pdslogger.PdsLogger.get_logger(LOGNAME)
        logger.info('Info is up to date; repair canceled', infofile)
        return

    # Move files and write new info
    logfile = pdsfile.PdsFile.log_path_for_shelf(infofile, 'repair', selection)
    move_old_info(infofile, logfile, logger=logger)
    shelve_infodict(pdsdir, dir_infodict, logger=logger)

def update(pdsdir, selection, logger=None):

    infofile = pdsdir.shelf_path_and_lskip(id='info')[0]

    shelf_infodict = load_infodict(pdsdir, logger=logger)
    dir_infodict = generate_infodict(pdsdir, selection, shelf_infodict,
                                             logger=logger)

    # Compare
    canceled = (dir_infodict == shelf_infodict)
    if canceled:
        if logger is None:
            logger = pdslogger.PdsLogger.get_logger(LOGNAME)
        logger.info('Info is up to date; update canceled', infofile)
        return

    # Write checksum file
    logfile = pdsfile.PdsFile.log_path_for_shelf(infofile, 'repair', selection)
    move_old_info(infofile, logfile, logger=logger)
    shelve_infodict(pdsdir, dir_infodict, logger=logger)

################################################################################
################################################################################

if __name__ == '__main__':

    # Set up parser
    parser = argparse.ArgumentParser(
        description='pdsinfoshelf: Create, maintain and validate shelf files ' +
                    'containing basic information about each file.')

    parser.add_argument('--initialize', const='initialize',
                        default='', action='store_const', dest='task',
                        help='Create an infoshelf file for a volume. Abort '   +
                             'if the file already exists.')

    parser.add_argument('--reinitialize', const='reinitialize',
                        default='', action='store_const', dest='task',
                        help='Create an infoshelf file for a volume. Replace ' +
                             'the file if it already exists. If a single '     +
                             'file is specified, such as one archive file in ' +
                             'a volume set, then only information about that ' +
                             'file is re-initialized.')

    parser.add_argument('--validate', const='validate',
                        default='', action='store_const', dest='task',
                        help='Validate every file in a volume against the '    +
                             'contents of its infoshelf file. If a single '    +
                             'file is specified, such as an archive file in '  +
                             'a volume set, then only information about that ' +
                             'file is validated')

    parser.add_argument('--repair', const='repair',
                        default='', action='store_const', dest='task',
                        help='Validate every file in a volume against the '    +
                             'contents of its infoshelf file. If any file '    +
                             'has changed, the infoshelf file is replaced. '   +
                             'If a single file is specified, such as an '      +
                             'archive file in a volume set, then only '        +
                             'information about that file is repaired.')

    parser.add_argument('--update', const='update',
                        default='', action='store_const', dest='task',
                        help='Search a directory for any new files and add '   +
                             'their information to the infoshelf file. '       +
                             'Information about pre-existing files is not '    +
                             'updated.')

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

    parser.add_argument('--quiet', '-q', default=False, action='store_true',
                        help='Do not also log to the terminal.')


    # Parse and validate the command line
    args = parser.parse_args()

    if not args.task:
        print 'pdsinfoshelf error: Missing task'
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
    log_path_ = os.path.join(log_root, 'infoshelf')

    LOGGER = pdslogger.PdsLogger(LOGNAME)

    if not args.quiet:
        LOGGER.add_handler(pdslogger.stdout_handler)

    warning_handler = pdslogger.warning_handler(log_path_)
    LOGGER.add_handler(warning_handler)

    error_handler = pdslogger.error_handler(log_path_)
    LOGGER.add_handler(error_handler)

    LOGGER.open(' '.join(sys.argv))
    try:

        # Generate a list of tuples (pdsfile, selection)
        info = []
        for path in args.volume:

            path = os.path.abspath(path)
            pdsf = pdsfile.PdsFile.from_abspath(path)
            if pdsf.checksums_:
                raise ValueError('No infoshelves for checksum files')

            if pdsf.is_volset_dir():
                # Info about archive directories is stored by volset
                if pdsf.archives_:
                    info.append((pdsf, None))
                # Others are checksumed by volume
                else:
                    info += [(pdsf.child(c), None) for c in pdsf.childnames]

            elif pdsf.is_volume_dir():
                # Shelve one volume
                info.append((pdsf, None))

            elif pdsf.isdir:
                raise ValueError('Invalid directory for an infoshelf: ' +
                                 pdsf.logical_path)

            else:
                pdsdir = pdsf.parent()
                if pdsf.is_volume_file():
                    # Shelve one archive file
                    info.append((pdsdir, pdsf.basename))
                elif pdsdir.is_volume_dir():
                    # Shelve one top-level file in volume
                    info.append((pdsdir, pdsf.basename))
                else:
                    raise ValueError('Invalid file for an infoshelf: ' +
                                     pdsf.logical_path)

        # Loop through tuples...
        for (pdsdir, selection) in info:

            infofile = pdsdir.shelf_path_and_lskip(id='info')[0]

            if selection:
                pdsf = pdsdir.child(os.path.basename(selection))
            else:
                pdsf = pdsdir

            checkfile = pdsdir.checksum_path_and_lskip()[0]

            logfile = pdsfile.PdsFile.log_path_for_shelf(infofile, args.task,
                                                         selection)
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
                    reinitialize(pdsdir, selection)

                elif args.task == 'validate':
                    validate(pdsdir, selection)

                elif args.task == 'repair':
                    repair(pdsdir, selection)

                else:   # update
                    update(pdsdir, selection)

            except (Exception, KeyboardInterrupt), e:
                LOGGER.exception(e)
                raise

            finally:
                _ = LOGGER.close()

    except (Exception, KeyboardInterrupt) as e:
        LOGGER.exception(e)
        print sys.exc_info()[2]
        status = 1
        raise

    finally:
        (fatal, errors, warnings, tests) = LOGGER.close()
        if fatal or errors: status = 1

    sys.exit(status)
