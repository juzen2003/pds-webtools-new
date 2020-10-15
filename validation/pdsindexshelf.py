#!/usr/bin/env python3
################################################################################
# pdsindexshelf.py library and main program
#
# Syntax:
#   pdsindexshelf.py --task index_path.tab [index_path.tab ...]
# 
# Enter the --help option to see more information.
################################################################################

import sys
import os
import shelve
import pickle
import shutil
import glob
import datetime
import argparse
from PIL import Image

import pdslogger
import pdsfile
import pdstable

try:
    GDBM_MODULE = __import__("gdbm")
except ImportError:
    GDBM_MODULE = __import__("dbm.gnu")

if sys.version_info >= (3,0):
    ENCODING = {'encoding': 'latin-1'}  # For open() of ASCII files in Python 3
else:
    ENCODING = {}

LOGNAME = 'pds.validation.indexshelf'
LOGROOT_ENV = 'PDS_LOG_ROOT'

################################################################################

def generate_indexdict(pdsf, logger=None):
    """Generate a dictionary keyed by row key for each row in the given table.
    The value returned is a list containing all the associated row indices.
    """

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)

    logger.replace_root(pdsf.root_)
    logger.info('Tabulating index rows for', pdsf.abspath)

    try:
        table = pdstable.PdsTable(pdsf.label_abspath,
                                  filename_keylen=pdsf.filename_keylen)
    except (OSError, ValueError) as e:
        logger.error(str(e))
        return None

    table.index_rows_by_filename_key()      # fills in table.filename_keys
    childnames = table.filename_keys
    indexdict = {c:table.row_indices_by_filename_key(c) for c in childnames}

    logger.info('Index rows tabulated for', pdsf.abspath)

    return indexdict

################################################################################

def shelve_indexdict(pdsf, indexdict, logger=None):
    """Write a new shelf file for the rows of this index."""

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)

    logger.replace_root(pdsf.root_)
    logger.info('Writing index shelf file', pdsf.indexshelf_abspath)

    # Write the shelf
    shelf_path = pdsf.indexshelf_abspath
    logger.info('Writing index shelf file', shelf_path)

    pdsfile.PdsFile.close_all_shelves()     # prevents multiple access to the
                                            # same shelf file

    shelf = shelve.Shelf(GDBM_MODULE.open(shelf_path, 'n'), protocol=2)
    for (key, values) in indexdict.items():
        shelf[key] = values

    shelf.close()

    # Write the pickle file
    pickle_path = shelf_path.rpartition('.')[0] + '.pickle'
    logger.info('Writing pickle file', pickle_path)

    with open(pickle_path, 'wb') as f:
        pickle.dump(indexdict, f, protocol=2)

    # Write the Python file
    python_path = shelf_path.rpartition('.')[0] + '.py'
    logger.info('Writing Python file', python_path)

    # Determine the maximum length of the keys
    len_path = 0
    for key in indexdict:
        len_path = max(len_path, len(key))

    name = os.path.basename(shelf_path).replace('.shelf', '')
    with open(python_path, 'w', **ENCODING) as f:
        f.write(name + ' = {\n')
        for key in pdsf.childnames:
            f.write('    "%s: ' % (key + '"' + (len_path-len(key)) * ' '))

            rows = indexdict[key]
            if len(rows) == 1:
                f.write('%d,\n' % rows[0])
            else:
                f.write('(')
                for row in rows[:-1]:
                    f.write('%d, ' % row)
                f.write('%d),\n' % rows[-1])

        f.write('}\n\n')

    logger.info('Three files written')

################################################################################

def load_indexdict(pdsf, logger=None):

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)

    logger.replace_root(pdsf.root_)
    logger.info('Reading index file for', pdsf.abspath)

    shelf_path = pdsf.indexshelf_abspath
    logger.info('Shelf file', shelf_path)

    # Read the shelf file and convert to a dictionary
    # On failure, read pickle file
    try:
        shelf = shelve.Shelf(GDBM_MODULE.open(shelf_path, 'r'))
        shelf_is_open = True

    except Exception:
        pickle_path = shelf_path.rpartition('.')[0] + '.pickle'
        logger.warn('Shelf read failed; reading pickle file', picklepath)
        shelf_is_open = False
        with open(pickle_path, 'rb') as f:
            shelf = pickle.load(f)

    indexdict = {}
    for key in shelf.keys():
        indexdict[key] = shelf[key]

    if shelf_is_open:
        shelf.close()

    return indexdict

################################################################################

def validate_infodict(pdsf, tabdict, shelfdict, logger=None):

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)

    logger.replace_root(pdsf.root_)
    logger.info('Validating index file for', pdsf.abspath)

    if tabdict == shelfdict:
        logger.info('Validation complete')
    else:
        logger.error('Validation failed for', pdsf.abspath)

################################################################################
# Simplified functions to perform tasks
################################################################################

def initialize(pdsf, logger=None):

    # Check destination
    if os.path.exists(pdsf.indexshelf_abspath):
        raise IOError('Index shelf file already exists: ' +
                      pdsf.indexshelf_abspath)

    reinitialize(pdsf, logger)

def reinitialize(pdsf, logger=None):

    # Create parent directory if necessary
    parent = os.path.split(pdsf.indexshelf_abspath)[0]
    if not os.path.exists(parent):
        os.makedirs(parent)

    # Generate info
    indexdict = generate_indexdict(pdsf, logger=logger)
    if indexdict is None: return

    # Save info file
    shelve_indexdict(pdsf, indexdict, logger=logger)

def validate(pdsf, logger=None):

    table_indexdict = generate_indexdict(pdsf, logger=logger)
    if table_indexdict is None: return

    shelf_indexdict = load_indexdict(pdsf, logger=logger)

    # Validate
    validate_infodict(pdsf, table_indexdict, shelf_indexdict,
                      logger=logger)

def repair(pdsf, logger=None, op='repair'):

    table_indexdict = generate_indexdict(pdsf, logger=logger)
    if table_indexdict is None: return

    shelf_indexdict = load_indexdict(pdsf, logger=logger)

    canceled = (table_indexdict == shelf_indexdict)
    if canceled:
        if logger is None:
            logger = pdslogger.PdsLogger.get_logger(LOGNAME)

        logger.info('Index is up to date; %s canceled' % op, pdsf.abspath)
        return

    # Write new info
    shelve_indexdict(pdsf, table_indexdict, logger=logger)

def update(pdsf, selection=None, logger=None):

    repair(pdsf, logger, op='update')

################################################################################
################################################################################

if __name__ == '__main__':

    # Set up parser
    parser = argparse.ArgumentParser(
        description='pdsindexshelf: Create, maintain and validate shelf files ' +
                    'containing row lookup information for index files.')

    parser.add_argument('--initialize', const='initialize',
                        default='', action='store_const', dest='task',
                        help='Create an indexshelf file for an index. Abort '  +
                             'if the file already exists.')

    parser.add_argument('--reinitialize', const='reinitialize',
                        default='', action='store_const', dest='task',
                        help='Create an indexshelf file for an index. Replace '+
                             'the file if it already exists.')

    parser.add_argument('--validate', const='validate',
                        default='', action='store_const', dest='task',
                        help='Validate an indexshelf file')

    parser.add_argument('--repair', const='repair',
                        default='', action='store_const', dest='task',
                        help='Validate an indexshelf file; replace only if '   +
                             'necessary.')

    parser.add_argument('--update', const='update',
                        default='', action='store_const', dest='task',
                        help='Same as repair.')

    parser.add_argument('table', nargs='+', type=str,
                        help='Path to an index file.')

    parser.add_argument('--log', '-l', type=str, default='',
                        help='Optional root directory for a duplicate of the ' +
                             'log files. If not specified, the value of '      +
                             'environment variable "%s" ' % LOGROOT_ENV        +
                             'is used. In addition, individual logs are '      +
                             'written into the "logs" directory parallel to '  +
                             '"holdings". Logs are created inside the "index" '+
                             'subdirectory of each log root directory.')

    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Do not also log to the terminal.')

    # Parse and validate the command line
    args = parser.parse_args()

    if not args.task:
        print('pdsindexshelf error: Missing task')
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
        path = os.path.join(args.log, 'pdsindexshelf')
        warning_handler = pdslogger.warning_handler(path)
        logger.add_handler(warning_handler)

        error_handler = pdslogger.error_handler(path)
        logger.add_handler(error_handler)

    # Generate a list of PdsFile objects before logging
    pdsfiles = []
    for path in args.table:

        if not os.path.exists(path):
            print('No such file or directory: ' + path)
            sys.exit(1)

        path = os.path.abspath(path)
        pdsf = pdsfile.PdsFile.from_abspath(path)

        pdsfiles.append(pdsf)

    # Open logger and loop through tables...
    logger.open(' '.join(sys.argv))
    try:
        for pdsf in pdsfiles:

            # Save logs in up to two places
            logfiles = [pdsf.log_path_for_index(task=args.task,
                                                dir='pdsindexshelf'),
                        pdsf.log_path_for_index(task=args.task,
                                                dir='pdsindexshelf',
                                                place='parallel')]
            if logfiles[0] == logfiles[1]:
                logfiles = logfiles[:-1]

            # Create all the handlers for this level in the logger
            local_handlers = []
            for logfile in logfiles:
                local_handlers.append(pdslogger.file_handler(logfile))
                logdir = (logfile.rpartition('/pdsindexshelf/')[0] +
                          '/pdsindexshelf')

                # These handlers are only used if they don't already exist
                warning_handler = pdslogger.warning_handler(logdir)
                error_handler = pdslogger.error_handler(logdir)
                local_handlers += [warning_handler, error_handler]

            # Open the next level of the log
            logger.open('Task "' + args.task + '" for', pdsf.abspath,
                        handler=local_handlers)

            try:
                for logfile in logfiles:
                    logger.info('Log file', logfile)

                if args.task == 'initialize':
                    initialize(pdsf)

                elif args.task == 'reinitialize':
                    reinitialize(pdsf)

                elif args.task == 'validate':
                    validate(pdsf)

                elif args.task == 'repair':
                    repair(pdsf)

                else:   # update
                    update(pdsf)

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
