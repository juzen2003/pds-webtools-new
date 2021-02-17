#!/usr/bin/env python3
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
import pickle
import shutil
import glob
import datetime
import argparse
from PIL import Image

import pdslogger
import pdsfile
import pdschecksums

# Holds log file directories temporarily, used by move_old_info()
LOGDIRS = []

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
        """Info about the given abspath."""

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
                logger.fatal('Missing entry in checksum file', abspath)
                raise

            size = (0,0)
            ext = os.path.splitext(abspath)[1]
            if ext.lower() in PREVIEW_EXTS:
                try:
                    im = Image.open(abspath)
                    size = im.size
                    im.close()
                except Exception:
                    logger.error('Preview size not found', abspath)

        logger.normal('File info generated', abspath)
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
            for (key, value) in infodict.items():
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

    logger.replace_root(pdsdir.root_)
    logger.open('Shelving file info for', dirpath, limits=limits)

    try:
        (shelf_path, lskip) = pdsdir.shelf_path_and_lskip(id='info')
        logger.info('Shelf file', shelf_path)

        # Write the pickle file
        pickle_dict = {}
        for (key, values) in infodict.items():
            short_key = key[lskip:]
            pickle_dict[short_key] = values

        with open(shelf_path, 'wb') as f:
            pickle.dump(pickle_dict, f)

    except (Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        raise

    finally:
        _ = logger.close()

    logger.open('Writing Python dictionary', dirpath, limits=limits)
    try:
        # Determine the maximum length of the file path
        len_path = 0
        for (abspath, values) in infodict.items():
            len_path = max(len_path, len(abspath))

        len_path -= lskip

        # Write the python dictionary version
        python_path = shelf_path.rpartition('.')[0] + '.py'
        name = os.path.basename(python_path)
        parts = name.split('_')
        name = '_'.join(parts[:2]) + '_info'
        abspaths = list(infodict.keys())
        abspaths.sort()

        with open(python_path, 'w', encoding='latin-1') as f:
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

        # Read the shelf file and convert to a dictionary
        with open(shelf_path, 'rb') as f:
            shelf = pickle.load(f)

        infodict = {}
        for key in shelf.keys():
            if key == '':
                infodict[dirpath_[:-1]] = shelf[key]
            else:
                infodict[dirpath_[:lskip] + key] = shelf[key]

        return infodict

    except (Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        raise

    finally:
        _ = logger.close()

################################################################################

def validate_infodict(pdsdir, dirdict, shelfdict, selection,
                      limits={'normal': 0}, logger=None):

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)

    logger.replace_root(pdsdir.root_)

    if selection:
        logger.open('Validating file info for selection %s' % selection,
                    pdsdir.abspath, limits=limits)
    else:
        logger.open('Validating file info for', pdsdir.abspath, limits=limits)

    # Prune the shelf dictionary if necessary
    if selection:
        keys = list(shelfdict.keys())
        full_path = os.path.join(pdsdir.abspath, selection)
        for key in keys:
            if key != full_path:
                del shelfdict[key]

    try:
        keys = list(dirdict.keys())
        for key in keys:
            if key in shelfdict:
                dirinfo = dirdict[key]
                shelfinfo = shelfdict[key]

                (bytes1, count1, modtime1, checksum1, size1) = dirinfo
                (bytes2, count2, modtime2, checksum2, size2) = shelfinfo

                # Truncate modtimes to seconds
                modtime1 = modtime1.rpartition('.')[0]
                modtime2 = modtime2.rpartition('.')[0]

                agreement = True
                if bytes1 != bytes2:
                    logger.error('File size mismatch %d %d' %
                                    (bytes1, bytes2), key)
                    agreement = False

                if count1 != count2:
                    logger.error('Child count mismatch %d %d' %
                                    (count1, count1), key)
                    agreement = False

                if abs(modtime1 != modtime2) > 1:
                    logger.error('Modification time mismatch "%s" "%s"' %
                        (modtime1, modtime2), key)
                    agreement = False

                if checksum1 != checksum1:
                    logger.error('Checksum mismatch', key)
                    agreement = False

                if size1 != size2:
                    logger.error('Display size mismatch', key)
                    agreement = False

                if agreement:
                    logger.normal('File info matches', key)

                del shelfdict[key]
                del dirdict[key]

        keys = list(dirdict.keys())
        keys.sort()
        for key in keys:
            logger.error('Missing shelf info for', key)

        keys = list(shelfdict.keys())
        keys.sort()
        for key in keys:
            logger.error('Shelf info for missing file', key)

    except (Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        raise

    finally:
        return logger.close()

################################################################################

def move_old_info(shelf_file, logger=None):
    """Move a file to the /logs/ directory tree and append a time tag."""

    if not os.path.exists(shelf_file): return

    shelf_basename = os.path.basename(shelf_file)
    (shelf_prefix, shelf_ext) = os.path.splitext(shelf_basename)

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)

    from_logged = False
    for log_dir in LOGDIRS:
        dest_template = log_dir + '/' + shelf_prefix + '_v???' + shelf_ext
        version_paths = glob.glob(dest_template)

        max_version = 0
        lskip = len(shelf_ext)
        for version_path in version_paths:
            version = int(version_path[-lskip-3:-lskip])
            max_version = max(max_version, version)

        new_version = max_version + 1
        dest = dest_template.replace('???', '%03d' % new_version)
        shutil.copy(shelf_file, dest)

        if not from_logged:
            logger.info('Info shelf file moved from: ' + shelf_file)
            from_logged = True

        logger.info('Info shelf file moved to', dest)

        python_file = shelf_file.rpartition('.')[0] + '.py'
        dest = dest.rpartition('.')[0] + '.py'
        shutil.copy(python_file, dest)

################################################################################
# Simplified functions to perform tasks
################################################################################

def initialize(pdsdir, selection=None, logger=None):

    infofile = pdsdir.shelf_path_and_lskip(id='info')[0]

    # Check selection
    if selection:
        raise ValueError('File selection is disallowed for task ' +
                         '"initialize": ' + selection)

    # Check destination
    if os.path.exists(infofile):
        raise IOError('Info file already exists: ' + infofile)

    # Create parent directory if necessary
    parent = os.path.split(infofile)[0]
    if not os.path.exists(parent):
        os.makedirs(parent)

    # Generate info
    infodict = generate_infodict(pdsdir, selection, logger=logger)

    # Save info file
    shelve_infodict(pdsdir, infodict, logger=logger)

def reinitialize(pdsdir, selection=None, logger=None):

    infofile = pdsdir.shelf_path_and_lskip(id='info')[0]

    # Create parent directory if necessary
    parent = os.path.split(infofile)[0]
    if not os.path.exists(parent):
        os.makedirs(parent)

    # Generate info
    infodict = generate_infodict(pdsdir, selection, logger=logger)

    # Move old file if necessary
    if os.path.exists(infofile):
        move_old_info(infofile, logger=logger)

    # Save info file
    shelve_infodict(pdsdir, infodict, logger=logger)

def validate(pdsdir, selection=None, logger=None):

    shelf_infodict = load_infodict(pdsdir, logger=logger)
    dir_infodict = generate_infodict(pdsdir, selection, logger=logger)

    # Validate
    validate_infodict(pdsdir, dir_infodict, shelf_infodict, selection=selection,
                      logger=logger)

def repair(pdsdir, selection=None, logger=None):

    infofile = pdsdir.shelf_path_and_lskip(id='info')[0]

    shelf_infodict = load_infodict(pdsdir, logger=logger)
    dir_infodict = generate_infodict(pdsdir, selection, logger=logger)

    # For a single selection, use the old information
    if selection:
        key = list(dir_infodict.keys())[0]
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
    move_old_info(infofile, logger=logger)
    shelve_infodict(pdsdir, dir_infodict, logger=logger)

def update(pdsdir, selection=None, logger=None):

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
    move_old_info(infofile, logger=logger)
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
                        help='Optional root directory for a duplicate of the ' +
                             'log files. If not specified, the value of '      +
                             'environment variable "%s" ' % LOGROOT_ENV        +
                             'is used. In addition, individual logs are '      +
                             'written into the "logs" directory parallel to '  +
                             '"holdings". Logs are created inside the '        +
                             '"pdsinfoshelf" subdirectory of each log root '   +
                             'directory.'
                             )

    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Do not also log to the terminal.')


    # Parse and validate the command line
    args = parser.parse_args()

    if not args.task:
        print('pdsinfoshelf error: Missing task')
        sys.exit(1)

    status = 0

    # Define the logging directory
    if args.log == '':
        try:
            args.log = os.environ[LOGROOT_ENV]
        except KeyError:
            args.log = None

    # Initialize the logger
    logger = pdslogger.PdsLogger(LOGNAME)
    pdsfile.PdsFile.set_log_root(args.log)

    if not args.quiet:
        logger.add_handler(pdslogger.stdout_handler)

    if args.log:
        path = os.path.join(args.log, 'pdsinfoshelf')
        warning_handler = pdslogger.warning_handler(path)
        logger.add_handler(warning_handler)

        error_handler = pdslogger.error_handler(path)
        logger.add_handler(error_handler)

    # Generate a list of tuples (pdsfile, selection) before logging
    info = []
    for path in args.volume:

        if not os.path.exists(path):
            print('No such file or directory: ' + path)
            sys.exit(1)

        path = os.path.abspath(path)
        pdsf = pdsfile.PdsFile.from_abspath(path)
        if pdsf.checksums_:
            print('No infoshelves for checksum files: ' + path)
            sys.exit(1)

        if pdsf.is_volset_dir():
            # Info about archive directories is stored by volset
            if pdsf.archives_:
                info.append((pdsf, None))

            # Others are checksumed by volume
            else:
                children = [pdsf.child(c) for c in pdsf.childnames]
                info += [(c, None) for c in children if c.isdir]
                        # "if c.isdir" is False for volset level readme files

        elif pdsf.is_volume_dir():
            # Shelve one volume
            info.append((pdsf, None))

        elif pdsf.isdir:
            print('Invalid directory for an infoshelf: ' + pdsf.logical_path)
            sys.exit(1)

        else:
            pdsdir = pdsf.parent()
            if pdsf.is_volume_file():
                # Shelve one archive file
                info.append((pdsdir, pdsf.basename))
            elif pdsdir.is_volume_dir():
                # Shelve one top-level file in volume
                info.append((pdsdir, pdsf.basename))
            else:
                print('Invalid file for an infoshelf: ' + pdsf.logical_path)
                sys.exit(1)

    # Open logger and loop through tuples...
    logger.open(' '.join(sys.argv))
    try:
        for (pdsdir, selection) in info:

            infofile = pdsdir.shelf_path_and_lskip(id='info')[0]

            if selection:
                pdsf = pdsdir.child(os.path.basename(selection))
            else:
                pdsf = pdsdir

            # Save logs in up to two places
            if pdsf.volname:
                logfiles = set([pdsf.log_path_for_volume(id='info',
                                                         task=args.task,
                                                         dir='pdsinfoshelf'),
                                pdsf.log_path_for_volume(id='info',
                                                         task=args.task,
                                                         dir='pdsinfoshelf',
                                                         place='parallel')])
            else:
                logfiles = set([pdsf.log_path_for_volset(id='info',
                                                         task=args.task,
                                                         dir='pdsinfoshelf'),
                                pdsf.log_path_for_volset(id='info',
                                                         task=args.task,
                                                         dir='pdsinfoshelf',
                                                         place='parallel')])

            # Create all the handlers for this level in the logger
            local_handlers = []
            LOGDIRS = []            # used by move_old_info()
            for logfile in logfiles:
                local_handlers.append(pdslogger.file_handler(logfile))
                logdir = os.path.split(logfile)[0]
                LOGDIRS.append(os.path.split(logfile)[0])

                # These handlers are only used if they don't already exist
                warning_handler = pdslogger.warning_handler(logdir)
                error_handler = pdslogger.error_handler(logdir)
                local_handlers += [warning_handler, error_handler]

            # Open the next level of the log
            if selection:
                logger.open('Task "' + args.task + '" for selection ' +
                            selection, pdsdir.abspath, handler=local_handlers)
            else:
                logger.open('Task "' + args.task + '" for', path,
                            handler=local_handlers)

            try:
                for logfile in logfiles:
                    logger.info('Log file', logfile)

                if args.task == 'initialize':
                    initialize(pdsdir, selection)

                elif args.task == 'reinitialize':
                    if selection:       # don't erase everything else!
                        update(pdsdir, selection)
                    else:
                        reinitialize(pdsdir, selection)

                elif args.task == 'validate':
                    validate(pdsdir, selection)

                elif args.task == 'repair':
                    repair(pdsdir, selection)

                else:   # update
                    update(pdsdir, selection)

            except (Exception, KeyboardInterrupt) as e:
                logger.exception(e)
                raise

            finally:
                _ = logger.close()

    except (Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        print(sys.exc_info()[2])
        status = 1
        raise

    finally:
        (fatal, errors, warnings, tests) = logger.close()
        if fatal or errors: status = 1

    sys.exit(status)
