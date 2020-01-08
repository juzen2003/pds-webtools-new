#!/usr/bin/env python3
################################################################################
# # pdslinkshelf.py library and main program
#
# Syntax:
#   pdslinkshelf.py --task path [path ...]
# 
# Enter the --help option to see more information.
################################################################################

import sys
import os
import shelve
import pickle
import shutil
import glob
import re
import argparse

import pdslogger
import pdsfile
import translator

try:
    GDBM_MODULE = __import__("gdbm")
except ImportError:
    GDBM_MODULE = __import__("dbm.gnu")

if sys.version_info >= (3,0):
    ENCODING = {'encoding': 'latin-1'}
else:
    ENCODING = {}

LOGNAME = 'pds.validation.links'
LOGROOT_ENV = 'PDS_LOG_ROOT'

# Holds log file directories temporarily, used by move_old_links()
LOGDIRS = []

REPAIRS = translator.TranslatorByRegex([
    ('.*/COCIRS_[01].*/DATAINFO.TXT', 0,
        {'DIAG.FMT'         : 'DATA/UNCALIBR/DIAG.FMT',
         'FRV.FMT'          : 'DATA/UNCALIBR/FRV.FMT',
         'GEO.FMT'          : 'DATA/NAV_DATA/GEO.FMT',
         'HSK.FMT'          : 'DATA/HSK_DATA/HSK.FMT',
         'IFGM.FMT'         : 'DATA/UNCALIBR/IFGM.FMT',
         'IHSK.FMT'         : 'DATA/UNCALIBR/IHSK.FMT',
         'ISPM.FMT'         : 'DATA/APODSPEC/ISPM.FMT',
         'OBS.FMT'          : 'DATA/UNCALIBR/OBS.FMT',
         'POI.FMT'          : 'DATA/NAV_DATA/POI.FMT',
         'RIN.FMT'          : 'DATA/NAV_DATA/RIN.FMT',
         'TAR.FMT'          : 'DATA/NAV_DATA/TAR.FMT'}),
    ('.*/COCIRS_[56].*/TUTORIAL.TXT', 0,
        {'GEODATA.FMT'      : 'DATA/GEODATA/GEODATA.FMT',
         'ISPMDATA.FMT'     : 'DATA/ISPMDATA/ISPMDATA.FMT',
         'POIDATA.FMT'      : 'DATA/POIDATA/POIDATA.FMT',
         'RINDATA.FMT'      : 'DATA/RINDATA/RINDATA.FMT',
         'TARDATA.FMT'      : 'DATA/TARDATA/TARDATA.FMT',
         'filename.FMT'     : ''}),
    ('.*/COCIRS_[56].*/AAREADME.TXT', 0,
        {'REF.CAT'          : 'CATALOG/CIRSREF.CAT'}),
    ('.*/COISS_0.*\.lbl', 0,
        {'PREFIX8.FMT'  : 'label/prefix.fmt'}),
    ('.*/COISS_[012].*/(archsis|aareadme)\.txt', 0,
        {'Calds.CAT'    : '../../COISS_0xxx/COISS_0001/catalog/calds.cat',
         'calds.cat'    : '../../COISS_0xxx/COISS_0001/catalog/calds.cat',
         'Jupiterds.CAT': '../../COISS_1xxx/COISS_1001/catalog/jupiterds.cat',
         'jupiterds.cat': '../../COISS_1xxx/COISS_1001/catalog/jupiterds.cat',
         'Saturnds.CAT' : '../../COISS_2xxx/COISS_2001/catalog/saturnds.cat',
         'saturnds.cat' : '../../COISS_2xxx/COISS_2001/catalog/saturnds.cat'}),
    ('.*/metadata/.*/COUVIS_0.*_index.lbl', 0,
        {'CUBEDS.CAT'       : ''}),
    ('.*/COUVIS_0.*(CATALOG/\w+\.CAT|README\.TXT|INDEX.LBL)', 0,
        {'CUBEDS.CAT'       : 'CATALOG/SCUBEDS.CAT',
         'SPECDS.CAT'       : 'CATALOG/SSPECDS.CAT',
         'XCALDS.CAT'       : 'CATALOG/SCALDS.CAT',
         'XCUBEDS.CAT'      : 'CATALOG/SCUBEDS.CAT',
         'XSPECDS.CAT'      : 'CATALOG/SSPECDS.CAT',
         'XSSBDS.CAT'       : 'CATALOG/SSSBDS.CAT',
         'XWAVDS.CAT'       : 'CATALOG/SWAVDS.CAT'}),
    ('.*/COUVIS_8.*(AAREADME|CATINFO)\.TXT', 0,
        {'INST.CAT'         : 'CATALOG/UVISINST.CAT'}),
    ('.*/COVIMS_0001/.*\.(lbl|txt)', 0,
        {'band_bin_center.fmt'   : '../../COVIMS_0002/label/band_bin_center.fmt',
         'core_description.fmt'  : '../../COVIMS_0002/label/core_description.fmt',
         'suffix_description.fmt': '../../COVIMS_0002/label/suffix_description.fmt',
         'BAND_BIN_CENTER.FMT'   : '../../COVIMS_0002/label/band_bin_center.fmt',
         'CORE_DESCRIPTION.FMT'  : '../../COVIMS_0002/label/core_description.fmt',
         'SUFFIX_DESCRIPTION.FMT': '../../COVIMS_0002/label/suffix_description.fmt'}),
    ('.*/COVIMS_0.*\.txt', 0,
        {'suffix.cat'       : '',
         'center.fmt'       : 'label/band_bin_center.fmt'}),
    ('.*/GO_00.*/AAREADME.TXT', 0,
        {'ttds.cat'         : '../GO_0020/CATALOG/TTDS.CAT'}),
    ('.*/HSTJ.*/(AAREADME|CATINFO).TXT', 0,
        {'NST.CAT'          : 'CATALOG/INST.CAT'}),
    ('.*/NHSP.*/AAREADME.TXT', 0,
        {'personel.cat'     : 'CATALOG/PERSONNEL.CAT',
         'spiceds.cat'      : 'CATALOG/SPICE_INST.CAT'}),
    ('.*/RPX_0401/AAREADME.TXT', 0,
        {'INSTHOST.CAT'     : 'CATALOG/HOST.CAT'}),
    ('.*/VGIRIS_0001/.*(AAREADME|DATAINFO).TXT', 0,
        {'JUPITER_ASCII.FMT': 'DATA/JUPITER_VG1/JUPITER_ASCII.FMT',
         'JUPITER_LSB.FMT'  : 'DATA/JUPITER_VG1/JUPITER_LSB.FMT',
         'JUPITER_MSB.FMT'  : 'DATA/JUPITER_VG1/JUPITER_MSB.FMT',
         'SATURN_ASCII.FMT' : '',
         'SATURN_LSB.FMT'   : '',
         'SATURN_MSB.FMT'   : '',
         'VGnINST.CAT'      : 'CATALOG/VG1INST',
         'VGnHOST.CAT'      : 'CATALOG/VG1HOST'}),
    ('.*/VGIRIS_0002/.*(AAREADME|DATAINFO).TXT', 0,
        {'JUPITER_ASCII.FMT': '',
         'JUPITER_LSB.FMT'  : '',
         'JUPITER_MSB.FMT'  : '',
         'SATURN_ASCII.FMT' : 'DATA/SATURN_VG1/SATURN_ASCII.FMT',
         'SATURN_LSB.FMT'   : 'DATA/SATURN_VG1/SATURN_LSB.FMT',
         'SATURN_MSB.FMT'   : 'DATA/SATURN_VG1/SATURN_MSB.FMT',
         'VGnINST.CAT'      : 'CATALOG/VG1INST',
         'VGnHOST.CAT'      : 'CATALOG/VG1HOST'}),
    ('.*/VG_2001/.*/VG2_SAT\.LBL', 0,
        {'IRIS_ROWFMT.FMT'  : 'JUPITER/IRISHEDR.FMT'}),
    ('.*/VG_2001/AAREADME.TXT', 0,
        {'IRISHEDR.FMT'     : 'JUPITER/IRISHEDR.FMT',
         'IRISTRGP.FMT'     : 'JUPITER/CALIB/IRISTRGP.FMT'}),
    ('.*/VG_28[0-9]{2}/.*INFO.TXT', 0,
        {'INST.CAT'         : 'CATALOG/VG1INST.CAT',
         'VGnNINST.CAT'     : 'CATALOG/VG1INST.CAT',
         'VGnHOST.CAT'      : 'CATALOG/VG1HOST.CAT',
         'RS1SINST.CAT'     : 'CATALOG/VG1SINST.CAT',
         'RS2UINST.CAT'     : 'CATALOG/VG2UINST.CAT'}),
    ('.*/VG_280./.*/L3GUIDE.TXT', 0,
        {'RTLMTAB.FMT'      : ''}),
    ('.*/VG_2803/.*/RS.R1BFV\.LBL', 0,
        {'RS_R1BFT.FMT'     : 'RS_R1BFV.FMT'}),
    ('.*/VGISS_[56].*/CATALOG/CATINFO.TXT', 0,
        {'VGnNINST.CAT'     : 'CATALOG/VG1NINST.CAT',
         'VGnHOST.CAT'      : 'CATALOG/VG1HOST.CAT'}),
])

################################################################################

EXTS_WO_LABELS = set(['.LBL', '.CAT', '.TXT', '.FMT', '.SFD'])

def generate_links(dirpath, limits={'info':100, 'ds_store':10}, logger=None):
    """Generate a dictionary keyed by the absolute file path for files in the
    given directory tree, which must correspond to a volume.

    Files ending in .LBL, .CAT and .TXT return a list of tuples
        (recno, basename, target)
    where:
        basename is the name of a file linked from or labeled by this file;
        recno is the record number where the basename appears;
        target is the absolute path to the target of this link.

    Other keys return a single string, which indicates the absolute path to the
    label file describing this file.

    Unlabeled files not ending in .LBL, .CAT or .TXT return an empty string.
    """

    dirpath = os.path.abspath(dirpath)
    pdsdir = pdsfile.PdsFile.from_abspath(dirpath)

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)

    logger.replace_root(pdsdir.root_)
    logger.open('Finding link files', dirpath, limits)

    try:
        # Walk the directory tree...
        link_dict = {}
        for (root, dirs, files) in os.walk(dirpath):

            # Create an empty entry in the dictionary for each file found
            # (For files that do not contain links and are not labeled or linked
            # by another file, this entry will remain empty.)
            abspaths = []
            for basename in files:
                abspath = os.path.join(root, basename)

                if basename == '.DS_Store':    # skip .DS_Store files
                    logger.ds_store('.DS_Store file skipped', abspath)
                    continue

                if basename.startswith('._'):   # skip dot_underscore files
                    logger.dot_underscore('dot_underscore file skipped',
                                          abspath)
                    continue

                if basename.startswith('.'):    # skip invisible files
                    logger.invisible('Invisible file skipped', abspath)
                    continue

                abspaths.append(abspath)
                link_dict[abspath] = ''

            # If necessary, search the file for links
            for abspath in abspaths:
                ext = abspath[-4:].upper()
                if ext not in EXTS_WO_LABELS: continue
                islabel = (ext == '.LBL')

                tuples = read_links(abspath, files, logger=logger)

                # Identify all files that might be labeled by this file
                if islabel:
                    for tuple in tuples:
                        if (len(tuple) == 3 and
                            tuple[1][-4:].upper() not in EXTS_WO_LABELS):
                                link_dict[tuple[-1]] = abspath

                # Save the list of linked and labeled files
                link_dict[abspath] = tuples

        # Walk of tree is now complete

        # Update absolute paths to non-local files (.FMT for example)
        for (key, tuples) in link_dict.items():
            if type(tuples) == str: continue

            key_basename = os.path.basename(key)
            key_islabel = key_basename.upper().endswith('.LBL')

            updates = []
            for tuple in tuples:
                if len(tuple) == 3: # Target is in this dir and already filled
                    if tuple[2]:
                        updates.append(tuple)
                    # if third element is blank, no target was identified

                else:
                    (recno, basename) = tuple

                    # Locate elsewhere in the tree
                    absfile = locate_link(key, basename)
                    if absfile:
                        logger.info('Located "%s"' % basename, absfile)
                        updates.append((recno, basename, absfile))
                    elif basename.upper().endswith('.FMT'):
                        logger.warn('Unable to locate .fmt file "%s"' % basename, key)
                    else:
                        logger.info('Reference to file "%s" ignored' % basename, key)

            link_dict[key] = updates

        return link_dict

    except (Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        raise

    finally:
        _ = logger.close()

LINK_REGEX = re.compile('\w[-A-Z0-9_]+\.[A-Z](?!\w{4})\w{0,3}', re.I)

def read_links(abspath, basenames, logger=None):
    """Return a list of tuples (recno, basename[, abspath]) linked or labeled
    by this file.

    basenames is a list of all the base filenames in the same directory. This is
    used to associate files with their labels.

    abspath points to the target of the link. It is present if it was found
    among the target's name was basenames or else if it was filled in via a
    repair rule. Otherwise, the tuple just contains (recno, basename) and
    another attempt will be made to fill in the path to the target.
    """

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)

    repair_dict = REPAIRS.first(abspath)

    with open(abspath, 'r', **ENCODING) as f:
        recs = f.readlines()

    basenames_upper = [b.upper() for b in basenames]

    self_basename_upper = os.path.basename(abspath).upper()
    parent_ = os.path.split(abspath)[0] + '/'
    volume_ = pdsfile.PdsFile.from_abspath(abspath).volume_abspath() + '/'

    links = []
    for recno in range(len(recs)):
        rec = recs[recno]
        while True:
            matchobj = LINK_REGEX.search(rec)
            if matchobj is None: break

            match = matchobj.group(0)
            match_upper = match.upper()

            # Ignore self-references
            if match_upper == self_basename_upper:
                rec = rec[matchobj.end():]

            # Repair known misidentifications
            elif repair_dict and (match in repair_dict):
                repair = repair_dict[match]
                if repair:
                    links.append((recno, match, volume_ + repair))
                    logger.info('Repairing link "%s"->"%s"' % (match, repair),
                                abspath, force=True)
                else:
                    logger.info('Ignoring link "%s"' % match,
                                abspath, force=True)

            # .CAT and .FMT files require a search
            elif len(match) > 4 and match[-4:].upper() in ('.CAT', '.FMT'):
                links.append((recno, match))
                logger.info('Found "%s"' % match, abspath)

            # Other references must be in the current directory
            else:
                try:
                    k = basenames_upper.index(match_upper)
                    links.append((recno, match, parent_ + basenames[k]))
                    logger.info('Found "%s"' % match, abspath)
                except ValueError:
                    pass

            rec = rec[matchobj.end():]

    return links

def locate_link(abspath, filename):
    """Return the absolute path associated with a link in a PDS file. This is
    done by searching up the tree and also by looking inside the LABEL,
    CATALOG and INCLUDE directories if they exist."""

    filename_upper = filename.upper()

    parts = abspath.split('/')[:-1]
    while len(parts) > 5:
        testpath = '/'.join(parts)
        basenames = os.listdir(testpath)
        uppercase = [b.upper() for b in basenames]
        try:
            k = uppercase.index(filename_upper)
            return testpath + '/' + basenames[k]
        except ValueError:
            pass

        for dirname in ['LABEL', 'CATALOG', 'INCLUDE']:
            try:
                k = uppercase.index(dirname)
                subnames = os.listdir(testpath + '/' + basenames[k])
                subupper = [s.upper() for s in subnames]
                try:
                    kk = subupper.index(filename_upper)
                    return testpath + '/' + basenames[k] + '/' + subnames[kk]
                except ValueError:
                    pass
            except ValueError:
                pass

        parts = parts[:-1]

    return ''

################################################################################

def shelve_links(dirpath, link_dict, limits={}, logger=None):
    """Write a new link shelf file for a directory tree."""

    # Initialize
    dirpath = os.path.abspath(dirpath)
    pdsdir = pdsfile.PdsFile.from_abspath(dirpath)

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)

    logger.replace_root(pdsdir.root_)
    logger.open('Shelving link file info for', dirpath, limits)

    try:
        (shelf_path, lskip) = pdsdir.shelf_path_and_lskip(id='links')
        logger.info('Shelf file', shelf_path)

        # Create a dictionary using interior paths instead of absolute paths
        interior_dict = {}
        for (key, values) in link_dict.items():
            if type(values) == str:
                interior_dict[key[lskip:]] = values[lskip:]
            else:
                new_list = []
                for (basename, recno, link_abspath) in values:
                    new_list.append((basename, recno, link_abspath[lskip:]))

                interior_dict[key[lskip:]] = new_list

        # Write the shelf
        # shelf = shelve.open(shelf_path, flag='n')
        shelf = shelve.Shelf(GDBM_MODULE.open(shelf_path, 'n'))

        for (key, values) in interior_dict.items():
            shelf[key] = values

        shelf.close()

        # Write the pickle file
        pickle_path = shelf_path.rpartition('.')[0] + '.pickle'
        with open(pickle_path, 'wb') as f:
            pickle.dump(interior_dict, f)

    except (Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        raise

    finally:
        _ = logger.close()

    logger.open('Writing Python dictionary', dirpath)
    try:
        # Determine the maximum length of the file path and basename
        len_key = 0
        len_base = 0
        for (key, value) in interior_dict.items():
            len_key = max(len_key, len(key))
            if type(value) != str:
                tuples = value
                for (recno, basename, interior_path) in tuples:
                    len_base = max(len_base, len(basename))

        len_key = min(len_key, 60)

        # Write the python dictionary version
        python_path = shelf_path.rpartition('.')[0] + '.py'
        name = os.path.basename(python_path)
        parts = name.split('_')
        name = '_'.join(parts[:2]) + '_links'
        keys = list(interior_dict.keys())
        keys.sort()

        with open(python_path, 'w', **ENCODING) as f:
            f.write(name + ' = {\n')
            for valtype in (list, str):
              for key in keys:
                if type(interior_dict[key]) != valtype: continue

                f.write('  "%s"' % key)
                if len(key) < len_key:
                    f.write((len_key - len(key)) * ' ')
                f.write(': ')
                tuple_indent = max(len(key),len_key) + 7

                values = interior_dict[key]
                if type(values) == str:
                    f.write('"%s",\n' % values)
                elif len(values) == 0:
                    f.write('[],\n')
                else:
                    f.write('[')
                    for k in range(len(values)):
                        (recno, basename, interior_path) = values[k]
                        f.write('(%4d, ' % recno)
                        f.write('"%s, ' % (basename + '"' +
                                           (len_base-len(basename)) * ' '))
                        f.write('"%s")' % interior_path)

                        if k < len(values) - 1:
                            f.write(',\n' + tuple_indent * ' ')
                        else:
                            f.write('],\n')

            f.write('}\n\n')

    except (Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        raise

    finally:
        _ = logger.close()

################################################################################

def load_links(dirpath, limits={}, logger=None):
    """Load link dictionary from a shelf file, converting interior paths to
    absolute paths."""

    dirpath = os.path.abspath(dirpath)
    pdsdir = pdsfile.PdsFile.from_abspath(dirpath)

    dirpath_ = dirpath.rstrip('/') + '/'

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)

    logger.replace_root(pdsdir.root_)
    logger.open('Reading link file info for', dirpath, limits)

    try:
        (shelf_path, lskip) = pdsdir.shelf_path_and_lskip(id='links')
        prefix_ = pdsdir.volume_abspath() + '/'

        logger.info('Shelf file', shelf_path)

        if not os.path.exists(shelf_path):
            raise IOError('File not found: ' + shelf_path)

        # Read the shelf file and convert to a dictionary
        # On failure, read pickle file
        try:
            # shelf = shelve.open(shelf_path, flag='r')
            shelf = shelve.Shelf(GDBM_MODULE.open(shelf_path, 'r'))

        except Exception:
            pickle_path = shelf_path.rpartition('.')[0] + '.pickle'
            with open(pickle_path, 'rb') as f:
                interior_dict = pickle.load(f)

        else:
            interior_dict = {}
            for key in shelf.keys():
                interior_dict[key] = shelf[key]

            shelf.close()

        # Convert interior paths to absolute paths
        link_dict = {}
        for (key, values) in interior_dict.items():
            long_key = dirpath_ + key

            if type(values) == str:
                if values == '':
                    link_dict[long_key] = ''
                else:
                    link_dict[long_key] = dirpath_ + values
            else:
                new_list = []
                for (recno, basename, interior_path) in values:
                    new_list.append((recno, basename, dirpath_ + interior_path))

                link_dict[long_key] = new_list

        return link_dict

    except (Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        raise

    finally:
        _ = logger.close()

################################################################################

def validate_links(dirpath, dirdict, shelfdict, limits={}, logger=None):

    dirpath = os.path.abspath(dirpath)
    pdsdir = pdsfile.PdsFile.from_abspath(dirpath)

    if logger is None:
        logger = pdslogger.PdsLogger.get_logger(LOGNAME)

    logger.replace_root(pdsdir.root_)
    logger.open('Validating link file info for', dirpath, limits=limits)

    try:
        keys = list(dirdict.keys())
        for key in keys:
            if key in shelfdict:
                dirinfo = dirdict[key]
                shelfinfo = shelfdict[key]

                if type(dirinfo) == list:
                    dirinfo.sort()

                if type(shelfinfo) == list:
                    shelfinfo.sort()

                if dirinfo != shelfinfo:
                    logger.error('Link target mismatch', key)

                del shelfdict[key]
                del dirdict[key]

        keys = list(dirdict.keys())
        keys.sort()
        for key in keys:
            logger.error('Missing link info for', key)

        keys = list(shelfdict.keys())
        keys.sort()
        for key in keys:
            logger.error('Shelf link info found for missing file', key)

    except (Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        raise

    finally:
        return logger.close()

################################################################################

def move_old_links(shelf_file, logger=None):
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
            logger.info('Link shelf file moved from: ' + shelf_file)
            from_logged = True

        logger.info('Link shelf file moved to ' + dest)

        python_file = shelf_file.rpartition('.')[0] + '.py'
        dest = dest.rpartition('.')[0] + '.py'
        shutil.copy(python_file, dest)

################################################################################
# Simplified functions to perform tasks
################################################################################

def initialize(pdsdir, logger=None):

    linkfile = pdsdir.shelf_path_and_lskip(id='links')[0]

    # Check destination
    if os.path.exists(linkfile):
        raise IOError('Link file already exists: ' + linkfile)

    # Create parent directory if necessary
    parent = os.path.split(linkfile)[0]
    if not os.path.exists(parent):
        os.makedirs(parent)

    # Generate link info
    link_dict = generate_links(pdsdir.abspath, logger=logger)

    # Move old file if necessary
    if os.path.exists(linkfile):
        move_old_links(linkfile, logger=logger)

    # Save link files
    shelve_links(pdsdir.abspath, link_dict, logger=logger)

def reinitialize(pdsdir, logger=None):

    linkfile = pdsdir.shelf_path_and_lskip(id='links')[0]

    # Create parent directory if necessary
    parent = os.path.split(linkfile)[0]
    if not os.path.exists(parent):
        os.makedirs(parent)

    # Generate link info
    link_dict = generate_links(pdsdir.abspath, logger=logger)

    # Move old file if necessary
    if os.path.exists(linkfile):
        move_old_links(linkfile, logger=logger)

    # Save link files
    shelve_links(pdsdir.abspath, link_dict, logger=logger)

def validate(pdsdir, logger=None):

    dir_links = generate_links(pdsdir.abspath, logger=logger)
    shelf_links = load_links(pdsdir.abspath, logger=logger)

    # Validate
    validate_links(pdsdir.abspath, dir_links, shelf_links, logger=logger)

def repair(pdsdir, logger=None):

    linkfile = pdsdir.shelf_path_and_lskip(id='links')[0]

    dir_links = generate_links(pdsdir.abspath, logger=logger)
    shelf_links = load_links(pdsdir.abspath, logger=logger)

    # Compare
    canceled = (dir_links == shelf_links)
    if canceled:
        if logger is None:
            logger = pdslogger.PdsLogger.get_logger(LOGNAME)

        logger.info('Link file is up to date; repair canceled', linkfile)
        return

    # Move files and write new info
    move_old_links(linkfile, logger=logger)
    shelve_links(pdsdir.abspath, dir_links, logger=logger)

################################################################################

if __name__ == '__main__':

    # Set up parser
    parser = argparse.ArgumentParser(
        description='pdslinkshelf: Create, maintain and validate shelves of '  +
                    'links between files.')

    parser.add_argument('--initialize', const='initialize',
                        default='', action='store_const', dest='task',
                        help='Create a link shelf file for a volume. Abort '   +
                             'if the checksum file already exists.')

    parser.add_argument('--reinitialize', const='reinitialize',
                        default='', action='store_const', dest='task',
                        help='Create a link shelf file for a volume. Replace ' +
                             'the file if it already exists.')

    parser.add_argument('--validate', const='validate',
                        default='', action='store_const', dest='task',
                        help='Validate every link in a volume directory tree ' +
                             'against its link shelf file.')

    parser.add_argument('--repair', const='repair',
                        default='', action='store_const', dest='task',
                        help='Validate every link in a volume directory tree ' +
                             'against its link shelf file. If any '            +
                             'disagreement  is found, replace the shelf '      +
                             'file; otherwise leave it unchanged.')

    parser.add_argument('volume', nargs='+', type=str,
                        help='The path to the root directory of a volume.')

    parser.add_argument('--log', '-l', type=str, default='',
                        help='Optional root directory for a duplicate of the ' +
                             'log files. If not specified, the value of '      +
                             'environment variable "%s" ' % LOGROOT_ENV        +
                             'is used. In addition, individual logs are '      +
                             'written into the "logs" directory parallel to '  +
                             '"holdings". Logs are created inside the '        +
                             '"pdslinkshelf" subdirectory of each log root '   +
                             'directory.'
                             )

    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Do not also log to the terminal.')

    # Parse and validate the command line
    args = parser.parse_args()

    if not args.task:
        print('pdslinkshelf error: Missing task')
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
        path = os.path.join(args.log, 'pdslinkshelf')
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
            print('No infoshelves for checksum files: ' + path)
            sys.exit(1)

        if pdsf.archives_:
            print('No linkshelves for archive files: ' + path)
            sys.exit(1)

        if pdsf.is_volset_dir():
            paths += [os.path.join(path, c) for c in pdsf.childnames]

        else:
            paths.append(os.path.abspath(path))

    # Loop through tuples...
    logger.open(' '.join(sys.argv))
    try:
        for path in paths:

            pdsdir = pdsfile.PdsFile.from_abspath(path)
            linkfile = pdsdir.shelf_path_and_lskip(id='links')[0]

            # Save logs in up to two places
            logfiles = set([pdsdir.log_path_for_volume(id='links',
                                                       task=args.task,
                                                       dir='pdslinkshelf'),
                            pdsdir.log_path_for_volume(id='links',
                                                       task=args.task,
                                                       dir='pdslinkshelf',
                                                       place='parallel')])

            # Create all the handlers for this level in the logger
            local_handlers = []
            LOGDIRS = []            # used by move_old_links()
            for logfile in logfiles:
                local_handlers.append(pdslogger.file_handler(logfile))
                logdir = os.path.split(logfile)[0]
                LOGDIRS.append(os.path.split(logfile)[0])

                # These handlers are only used if they don't already exist
                warning_handler = pdslogger.warning_handler(logdir)
                error_handler = pdslogger.error_handler(logdir)
                local_handlers += [warning_handler, error_handler]

            # Open the next level of the log
            logger.open('Task "' + args.task + '" for', path,
                        handler=local_handlers)

            try:
                for logfile in logfiles:
                    logger.info('Log file', logfile)

                if args.task == 'initialize':
                    initialize(pdsdir)

                elif args.task == 'reinitialize':
                    reinitialize(pdsdir)

                elif args.task == 'validate':
                    validate(pdsdir)

                else:
                    repair(pdsdir)

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
