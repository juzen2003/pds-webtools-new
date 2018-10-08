################################################################################
# pdsiterator.py: PdsIterator class iterates across related files, jumping
#   into adjacent directories and parallel volumes when required.
################################################################################

import os
import fnmatch
import glob
import pdsfile

# Python 2 and 3 compatible, byte strings and unicode
def _isstr(x): return isinstance(x, ("".__class__, u"".__class__))

# Useful filters
def dirs_only(parent_pdsfile, basename):
    if parent_pdsfile is None: return True

    child_pdsfile = parent_pdsfile.child(basename)
    return child_pdsfile.isdir

def same_in_next_anchor(parent_pdsfile, basename):
    parts = pdsfile.PdsFile.from_logical_path(self.current_logical_path).split()
    return basename.endswith(parts[1] + parts[2])

################################################################################
# Cache
################################################################################

DIRECTORY_CACHE = {}

################################################################################
# PdsDirIterator
################################################################################

class PdsDirIterator(object):

    def __init__(self, pdsf, sign=1):

        global DIRECTORY_CACHE

        if pdsf is None:
            self.neighbors = []
            self.neighbor_index = 0
            self.current_logical_path = None
            self.sign = 1

        fnmatch_patterns = pdsf.NEIGHBORS.first(pdsf.logical_path)
        if _isstr(fnmatch_patterns):
            fnmatch_patterns = (fnmatch_patterns,)

        if fnmatch_patterns:
            if fnmatch_patterns in DIRECTORY_CACHE:
                logical_paths = DIRECTORY_CACHE[fnmatch_patterns]
            else:
                paths = []
                for fnmatch_pattern in fnmatch_patterns:
                    abspaths = glob.glob(pdsf.root_ + fnmatch_pattern)
                    abspaths = [pdsfile.repair_case(p) for p in abspaths]
                    abspaths = [a for a in abspaths if os.path.isdir(a)]
                    paths += pdsfile.PdsFile.logicals_for_abspaths(abspaths)

                # Remove duplicates
                paths = list(set(paths))

                # Remove blanks (although they shouldn't be there)
                if '' in paths:
                    paths.remove('')

                # Sort based on the rules
                logical_paths = pdsfile.PdsFile.sort_logical_paths(paths)
                DIRECTORY_CACHE[fnmatch_patterns] = logical_paths

        else:
            logical_paths = [pdsf.logical_path]

        self.sign = -1 if sign < 0 else +1
        self.current_logical_path = pdsf.logical_path

        self.neighbor_index = logical_paths.index(pdsf.logical_path)
        self.neighbors = logical_paths
        self.neighbors_lc = [p.lower() for p in logical_paths]

        # Case-insensitive search
        logical_path_lc = pdsf.logical_path.lower()

    def copy(self, sign=None):
        """Return a clone of this iterator, possibly reversed."""

        if sign is None:
            sign1 = self.sign
        else:
            sign1 = -1 if sign < 0 else +1

        pdsf = pdsfile.PdsFile.from_logical_path(self.current_logical_path)
        this = PdsDirIterator(pdsf, sign=sign1)

        return this

    ############################################################################
    # Iterator
    ############################################################################

    def __iter__(self):
        return self

    def next(self):
        """Iterator returns (logical_path, display path, level)"""

        prev_logical_path = self.current_logical_path

        # Try to return the next neighbor
        self.neighbor_index += self.sign
        if self.neighbor_index < 0: raise StopIteration
        if self.neighbor_index >= len(self.neighbors): raise StopIteration

        # If we get this far, figure out what to return

        # Find the common parts of the previous logical path and this one
        neighbor = self.neighbors[self.neighbor_index]
        prev_parts = prev_logical_path.split('/')
        new_parts = neighbor.split('/')

        for k in range(len(prev_parts)):
            if prev_parts[k] != new_parts[k]:
                break

        # The display path is the string starting where prev and this differ
        new_parts = new_parts[k:]
        display_path = '/'.join(new_parts)

        # Level is 0 if prev and this are the same up to the basename; otherwise
        # level is 1.
        if len(new_parts) == 1:
            level = 0
        else:
            level = 1

        return (neighbor, display_path, level)

################################################################################
# PdsFileIterator
################################################################################

class PdsFileIterator(object):

    def __init__(self, pdsf, sign=1, pattern=None, exclude=None, filter=None):

        parent = pdsf.parent()
        self.dir_iterator = PdsDirIterator(parent, sign)

        self.pattern = pattern or self.NEIGHBORS.first(self.logical_path)
        self.exclude = exclude
        self.filter = filter
        self.sign = self.dir_iterator.sign
        self.current_logical_path = pdsf.logical_path

        basenames = self._filter_names(parent, parent.childnames)
        self.sibnames = parent.logicals_for_basenames(basenames)
        self.sibnames_lc = [p.lower() for p in self.sibnames]

        # Case-insensitive search
        logical_path_lc = pdsf.logical_path.lower()
        self.sibling_index = self.sibnames_lc.index(logical_path_lc)

    def copy(self, sign=None):
        """Return a clone of this iterator."""

        if sign is None:
            sign1 = self.sign
        else:
            sign1 = -1 if sign < 0 else +1

        pdsf = pdsfile.PdsFile.from_logical_path(self.current_logical_path)
        this = PdsFileIterator(pdsf, sign=sign1,
                               pattern=self.pattern, exclude=self.exclude,
                               filter=self.filter)

        return this

    def _filter_names(self, parent, basenames):
        if self.pattern:
            basenames = [s for s in basenames
                         if fnmatch.fnmatch(s, self.pattern)]
        if self.exclude:
            basenames = [s for s in basenames
                         if not fnmatch.fnmatch(s, self.exclude)]
        if self.filter:
            basenames = [s for s in basenames if self.filter(parent, s)]

        return basenames

    ############################################################################
    # Iterator
    ############################################################################

    def __iter__(self):
        return self

    def next(self):
        """Iterator returns (logical_path, display path, level of jump)

        Level of jump is 0 for a sibling, 1 for a cousin.

        Display path is the part of the path that has changed.
            At level 0, it is basename;
            At level 1, it is parent directory/basename;
        """

        # Try to return the next sibling
        try:
            self.sibling_index += self.sign
            if self.sibling_index < 0: raise IndexError()

            sibname = self.sibnames[self.sibling_index]

        # Jump to adjacent directory if necessary
        except IndexError:
            return self.next_cousin()

        # Otherwise return the next sibling
        else:
            self.current_logical_path = sibname
            return (sibname, os.path.basename(sibname), 0)

    def next_cousin(self):
        """Move the iteration into the adjacent parent directory."""

        prev_logical_path = self.current_logical_path

        # Go to the next parent
        (parent_logical_path, parent_display_path, _) = self.dir_iterator.next()
        parent = pdsfile.PdsFile.from_logical_path(parent_logical_path)

        # Load the next set of siblings
        basenames = self._filter_names(parent, parent.childnames)
        self.sibnames = parent.logicals_for_basenames(basenames)

        # Return the first new sibling
        if self.sign > 0:
            self.sibling_index = -1
        else:
            self.sibling_index = len(self.sibnames)

        (logical_path, basename, _) = self.next()
        return (logical_path, parent_display_path + '/' + basename, 1)

################################################################################
# PdsRowIterator
################################################################################

class PdsRowIterator(object):

    def __init__(self, pdsf, sign=1):

        self.parent_pdsf = pdsf.parent()
        self.parent_logical_path_ = self.parent_pdsf.logical_path + '/'

        self.sign = sign
        self.sibnames = self.parent_pdsf.childnames
        self.sibnames_lc = [n.lower() for n in self.sibnames]

        # Case-insensitive search
        basename_lc = pdsf.basename.lower()
        self.sibling_index = self.sibnames_lc.index(basename_lc)

    def copy(self, sign=None):
        """Return a clone of this iterator."""

        if sign is None:
            sign1 = self.sign
        else:
            sign1 = -1 if sign < 0 else +1

        childname = self.sibnames[self.sibling_index]
        return PdsRowIterator(self.parent_pdsf.child(childname), sign=sign1)

    ############################################################################
    # Iterator
    ############################################################################

    def __iter__(self):
        return self

    def next(self):
        """Iterator returns (logical_path, display path, level of jump)

        Level of jump is 0 for a sibling, 1 for a cousin.

        Display path is the part of the path that has changed.
            At level 0, it is basename;
            At level 1, it is parent directory/basename;
        """

        self.sibling_index += self.sign
        if self.sibling_index < 0: raise StopIteration
        if self.sibling_index >= len(self.sibnames): raise StopIteration

        sibname = self.sibnames[self.sibling_index]
        return (self.parent_logical_path_ + sibname, sibname, 0)

################################################################################
