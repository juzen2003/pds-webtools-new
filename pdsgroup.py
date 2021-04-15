################################################################################
# File grouping class. An ordered set of PdsFiles, some of which may be hidden.
# They must share a common parent and anchor. In Viewmaster, they appear on the
# same row of a table, where a row boundaries are identified by transition
# between gray and white.
################################################################################

import pdsfile
import pdsviewable

class PdsGroup(object):

    def __init__(self, pdsfiles=[], parent=False, anchor=None, hidden=[]):

        self.parent_pdsf = parent   # False means un-initialized; None means a
                                    # merged directory
        self.anchor = None
        self.rows = []
        self.hidden = set(hidden)

        self._isdir_filled = None
        self._iconset_filled = None
        self._viewset_filled = None
        self._local_viewset_filled = None
        self._all_viewsets_filled = None

        if isinstance(pdsfiles, (list, tuple)):
            for pdsf in pdsfiles:
                self.append(pdsf)
        else:
            self.append(pdsfiles)

    def __len__(self):
        return len(self.rows) - len(self.hidden)

    def __repr__(self):
        if self.rows:
            path = self.rows[0].logical_path

            if len(self.rows) >= 2:
                return f'PdsGroup({path},...[{len(self.rows)}])'
            else:
                return f'PdsGroup({path})'
        else:
            return f'PdsGroup()'

    def copy(self):
        this = PdsGroup()
        this.parent_pdsf = self.parent_pdsf
        this.anchor = self.anchor
        this.rows = list(self.rows)
        this.hidden = self.hidden.copy()

        this._isdir_filled = self._isdir_filled
        this._iconset_filled = self._iconset_filled
        this._viewset_filled = self._viewset_filled
        this._local_viewset_filled = self._local_viewset_filled
        this._all_viewsets_filled = self._all_viewsets_filled

        return this

    @property
    def parent_logical_path(self):
        if self.parent_pdsf:
            return self.parent_pdsf.logical_path
        else:
            return ''

    @property
    def isdir(self):
        if self._isdir_filled is None:
            self._isdir_filled = any([p.isdir for p in self.rows])

        return self._isdir_filled

    @property
    def _iconset(self):
        """Internal method to return the PdsViewSet of this object's icon
        whether it is to be displayed in a closed or open state."""

        if self._iconset_filled is None:
            self._iconset_filled = {}
            for open_val in (False, True):
                best_set = pdsviewable.ICON_SET_BY_TYPE[self.rows[0].icon_type,
                                                        open_val]
                for pdsf in self.rows[1:]:
                  test = pdsviewable.ICON_SET_BY_TYPE[pdsf.icon_type, open_val]
                  if test.priority > best_set.priority:
                    best_set = test

                self._iconset_filled[open_val] = best_set

        return self._iconset_filled[False]

    @property
    def iconset_closed(self):
        _ = self._iconset
        return self._iconset_filled[0]

    @property
    def iconset_open(self):
        _ = self._iconset
        return self._iconset_filled[1]

    @property
    def viewset(self):
        """The local PdsViewSet if it exists; otherwise, the first PdsViewSet.
        """

        if self._viewset_filled is None:

            if self.local_viewset:
                self._viewset_filled = self.local_viewset

            else:
                self._viewset_filled = []
                for pdsf in self.rows:
                    if pdsf.viewset:
                        self._viewset_filled = pdsf.viewset
                        break

        return self._viewset_filled

    @property
    def local_viewset(self):
        """The PdsViewSet of this object if it is viewable; False otherwise.
        """

        if self._local_viewset_filled is None:

            viewset = pdsviewable.PdsViewSet()
            for pdsf in self.rows:
                if pdsf.local_viewset:
                    viewset.append(pdsf.local_viewset)

            if len(viewset) == len(self):
                self._local_viewset_filled = viewset
            else:
                self._local_viewset_filled = False

        return self._local_viewset_filled

    @property
    def all_viewsets(self):
        """A dictionary of all the PdsViewSets for this object
        """

        if self._all_viewsets_filled is None:

            merged_dict = {}
            for pdsf in self.rows:
                for key in pdsf.all_viewsets:
                    if key not in merged_dict:
                        merged_dict[key] = pdsf.all_viewsets[key]

            self._all_viewsets_filled = merged_dict

        return self._all_viewsets_filled

    @property
    def global_anchor(self):
        if self.parent_pdsf is False:
            raise ValueError('PdsGroup has not been initialized')

        if self.parent_pdsf is None:        # if a merged directory
            return self.anchor
        else:
            return self.parent_pdsf.global_anchor + '-' + self.anchor

    def sort(self, labels_after=None, dirs_first=None, dirs_last=None,
                   info_first=None):

        basename_dict = {}
        for pdsf in self.rows:
            basename_dict[pdsf.basename] = pdsf

        if self.parent_pdsf:
            sorted = self.parent_pdsf.sort_basenames(list(basename_dict.keys()),
                                                labels_after=labels_after,
                                                dirs_first=dirs_first,
                                                dirs_last=dirs_last,
                                                info_first=info_first)
        else:
            sorted = list(basename_dict.keys())     # for merged directories
            sorted.sort()

        self.rows = [basename_dict[key] for key in sorted]

    def append(self, pdsf, hidden=False):

        # Initialize if necessary
        if self.parent_pdsf is False:
            self.parent_pdsf = pdsf.parent()
            self.rows = [pdsf]
            self.anchor = pdsf.anchor
            return

        if self.anchor is None:
            self.anchor = pdsf.anchor

        # Same parent required
        if pdsf.parent_logical_path != self.parent_logical_path:
            raise ValueError('PdsFile does not match parent of PdsGroup: ' +
                             pdsf.parent_logical_path + ', ' +
                             self.parent_logical_path)

        # Same anchor required
        if pdsf.anchor != self.anchor:
            raise ValueError('PdsFile does not match anchor of PdsGroup: ' +
                             pdsf.anchor + ', ' + self.anchor)

        # Ignore duplicates
        for row in self.rows:
            if pdsf.logical_path == row.logical_path:
                return

        self.rows.append(pdsf)
        if hidden:
            self.hidden |= {pdsf.logical_path}

        self._isdir_filled = None
        self._iconset_filled = None
        self._viewset_filled = None
        self._local_viewset_filled = None

    def remove(self, pdsf):

        for k in range(len(self.rows)):
            logical_path = self.rows[k].logical_path
            if logical_path == pdsf.logical_path:
                del self.rows[k]
                self.hidden -= {logical_path}
                return True

        return False

    def hide(self, pdsf):

        for k in range(len(self.rows)):
            if self.rows[k].logical_path == pdsf.logical_path:
                if pdsf.logical_path not in self.hidden:
                    self.hidden |= {pdsf.logical_path}
                    return True

        return False

    def hide_all(self):
        paths = [f.logical_path for f in self.rows]
        self.hidden = set(paths)

    def unhide(self, pdsf):

        for k in range(len(self.rows)):
            if self.rows[k].logical_path == pdsf.logical_path:
                if pdsf.logical_path in self.hidden:
                    self.hidden -= {pdsf.logical_path}
                    return True

        return False

    def unhide_all(self):
        self.hidden = set()

    def iterator(self):
        return [r for r in self.rows if r.logical_path not in self.hidden]

    def iterator_for_all(self):
        return [r for r in self.rows]

    def iterator_for_hidden(self):
        return [r for r in self.rows if r.logical_path in self.hidden]

    ############################################################################
    # PdsFile grouping
    ############################################################################

    @staticmethod
    def group_children(pdsf, basenames=None):
        """Return children of this PdsFile as a list of PdsGroup objects."""

        if basenames is None:
            basenames = pdsf.childnames

        # Group basenames by anchor
        anchor_dict = {}
        for basename in basenames:
            anchor = pdsf.split_basename(basename)[0]
            if anchor not in anchor_dict:
                anchor_dict[anchor] = []

            anchor_dict[anchor].append(basename)

        # Sort basenames within each group; re-key by first basename
        basename_dict = {}
        for (anchor, basenames) in anchor_dict.items():
            sorted = pdsf.sort_basenames(basenames, labels_after=True)
            basename_dict[sorted[0]] = sorted

        # Sort keys
        keys = basename_dict.keys()
        keys = pdsf.sort_basenames(keys)

        # Return a list of lists of PdsGroup objects
        groups = []
        for key in keys:
            basenames = basename_dict[key]
            groups.append(PdsGroup(pdsf.pdsfiles_for_basenames(basenames)))

        return groups

################################################################################
