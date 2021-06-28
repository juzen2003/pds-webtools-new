################################################################################
# pdsviewable.py
################################################################################

import os
from PIL import Image

import pdslogger

################################################################################
# Class definitions
################################################################################

class PdsViewable(object):
    """Contains the minimum information needed to show an image in HTML."""

    def __init__(self, abspath, url, width, height, bytecount, alt='',
                       name='', pdsf=None):

        # Core properties of a viewable
        self.abspath = abspath
        self.url = url
        self.width = width
        self.height = height
        self.bytes = bytecount
        self.alt = alt

        # Optional
        self.name = name    # Named viewables cannot be looked up by size
        self.pdsf = pdsf    # Optional

        self.width_over_height = float(self.width) / float(self.height)
        self.height_over_width = float(self.height) / float(self.width)

    def __repr__(self):
        return 'PdsViewable("' + self.abspath + '")'

    def assign_name(self, name):
        """Assign a name to this PdsViewable"""

        self.name = name

    def copy(self):
        """An exact copy of this PdsViewable"""

        return PdsViewable(self.abspath, self.url, self.width, self.height,
                           self.bytes, self.alt, self.name, self.pdsf)

    def to_dict(self, exclude=[]):
        """Return the attributes of a PdsViewable object as a dictionary
        suitable for JSON.

        The abspath, url, and alt, and attributes can optionally be excluded.
        If the name attribute is blank, it is excluded."""

        d = {'width':  self.width,
             'height': self.height,
             'bytes':  self.bytes}

        # Include optional parts optionally
        if 'abspath' not in exclude:
            d['abspath'] = self.abspath

        if 'url' not in exclude:
            d['url'] = self.url

        if 'alt' not in exclude:
            d['alt'] = self.alt

        if self.name:
            d['name'] = self.name

        return d

    @staticmethod
    def from_dict(d):
        """Construct a PdsViewable object from the dictionary returned by
        to_dict.

        If the alt attribute is missing, the basename of the abspath or url
        is used in its place.
        """

        abspath = d.get('abspath', '')
        url     = d.get('url',  '')
        alt     = d.get('alt',  os.path.basename(abspath or url))
        name    = d.get('name', '')

        return PdsViewable(abspath, url, d['width'], d['height'], d['bytes'],
                           alt, name)

    @staticmethod
    def from_pdsfile(pdsf, name=''):
        """Construct a PdsViewable object from a PdsFile representing a file
        that happens to be viewable, such as a JPEG or PNG."""

        if not pdsf.width:
            raise ValueError('PdsFile is not viewable: ' + pdsf.abspath)

        return PdsViewable(pdsf.abspath, pdsf.url, pdsf.width, pdsf.height,
                           pdsf.size_bytes, os.path.basename(pdsf.logical_path),
                           name, pdsf)

################################################################################
################################################################################
################################################################################

class PdsViewSet(object):
    """Viewables selectable by size or name."""

    def __init__(self, viewables=[], priority=0, include_named_in_sizes=False):

        self.priority = priority    # Used to prioritize among icon sets
        self.viewables = set()      # All the PdsViewable objects

        self.by_width = {}          # Keyed by width in pixels
        self.by_height = {}         # Keyed by height in pixels
        self.by_name = {}           # Keyed by name; these PdsViewables might
                                    # not appear in other dictionaries

        self.widths = []            # sorted smallest to largest
        self.heights = []           # ditto

        for viewable in viewables:
            self.append(viewable, include_named_in_sizes=include_named_in_sizes)

    def __bool__(self):
        return len(self.viewables) > 0

    def __repr__(self):
        if not self.viewables:
            return 'PdsViewSet()'

        if self.widths:
            selected = self.by_width[self.widths[-1]]
        else:
            selected = list(self.viewables)[0]

        count = len(self.viewables)
        if count == 1:
            return f'PdsViewSet("{selected.abspath}")'
        else:
            return f'PdsViewSet("{selected.abspath}"...[{count}])'

    def append(self, viewable, include_named_in_sizes=False):
        """Append the given PdsViewable to this PdsViewSet.

        If include_named_in_sizes is True, then a named viewable is added to the
        dictionaries keyed by size. Otherwise, not. This allows a PdsViewable
        object called "full" to be accessible by name but never to be used by
        for_width, for_height, or for_frame. Often, our "full" products do not
        look the same as the smaller versions because, for example, the smaller
        versions are color-coded but the "full" version is not. In this case,
        we want to ensure that the color-coded are always used in web pages
        unless "full" is requested explicitly.
        """

        if viewable in self.viewables: return

        # Allow a recursive call
        if isinstance(viewable, PdsViewSet):
            for viewable in viewable.viewables:
                self.append(viewable)
                return

        self.viewables.add(viewable)

        # Update the dictionary by name if it has a name
        if viewable.name:
            self.by_name[viewable.name] = viewable
            if not include_named_in_sizes: return

        # Update the dictionary by width
        # Unnamed viewables take precedence; named ones are overridden
        if (viewable.width not in self.by_width) or (not viewable.name):
            self.by_width[viewable.width] = viewable

        # Update the dictionary by height
        if (viewable.height not in self.by_height) or (not viewable.name):
            self.by_height[viewable.height] = viewable

        # Sort lists of widths and heights
        self.widths = list(self.by_width.keys())
        self.widths.sort()

        self.heights = list(self.by_height.keys())
        self.heights.sort()

    @staticmethod
    def from_dict(d):
        """Alternative constructor from a JSON-friendly dictionary generated by
        from_dict()."""

        obj = PdsViewSet(priority=d.get('priority', 0))
        for v in d['viewables']:
            obj.append(PdsViewable.from_dict(v))

        return obj

    def to_dict(self, exclude=['abspath', 'alt']):
        """Return a the info in this PdsViewSet encoded into JSON-friendly
        dictionaries."""

        d = {'viewables': [v.to_dict(exclude) for v in self.viewables]}
        if self.priority != 0:
            d['priority'] = self.priority       # defaults to zero

        return d

    def by_match(self, match):
        """Return a PdsViewable that contains the given match string"""

        for v in self.viewables:
            if match in (v.abspath + v.url):
                return v

        return None

    @property
    def thumbnail(self):
        thumb = self.by_match('_thumb')
        if not thumb:
            thumb = self.by_height[self.heights[0]]

        return thumb

    @property
    def small(self):
        return self.by_match('_small')

    @property
    def medium(self):
        return self.by_match('_med')

    @property
    def full_size(self):
        """The viewable designated as "full" or else the largest."""

        if 'full' in self.by_name:
            return self.by_name['full']

        return self.by_height[self.heights[-1]]

    def __len__(self):
        """Number of PdsViewables organized by size in this PdsViewSet."""

        return len(self.widths)

    def for_width(self, size):
        """The PdsViewable for the specified width."""

        if not self.viewables:
            raise IOError('No viewables have been defined')

        if self.widths:
            for key in self.widths:
                if key >= size:
                    pdsview = self.by_width[key]
                    break
        elif 'full' in self.by_name:
            pdsview = self.by_name['full']
        else:
            pdsview = list(self.viewables)[0]

        result = pdsview.copy()
        result.height = max(1, int(pdsview.height_over_width * size + 0.5))
        result.width = size
        return result

    def for_height(self, size):
        """The PdsViewable for the specified height."""

        if not self.viewables:
            raise IOError('No viewables have been defined')

        if self.heights:
            for key in self.heights:
                if key >= size:
                    pdsview = self.by_height[key]
                    break
        elif 'full' in self.by_name:
            pdsview = self.by_name['full']
        else:
            pdsview = list(self.viewables)[0]

        result = pdsview.copy()
        result.width = max(1, int(pdsview.width_over_height * size + 0.5))
        result.height = size
        return result

    def for_frame(self, width, height=None):
        """The PdsViewable to fit inside the specified rectangle."""

        if height is None:
            height = width

        pdsview = self.for_width(width)
        if pdsview.height > height:
            pdsview = self.for_height(height)
            pdsview.width = min(pdsview.width, width)

        return pdsview

    @staticmethod
    def from_pdsfiles(pdsfiles, validate=False, full_is_special=True):
        """A PdsViewSet constructed from a list of viewable PdsFile objects."""

        if type(pdsfiles) not in (list,tuple):
            pdsfiles = [pdsfiles]

        viewables = []
        full_viewable = None
        for pdsf in pdsfiles:
            if full_is_special and '_full.' in pdsf.logical_path:
                name = 'full'
            else:
                name = ''

            try:
                viewable = PdsViewable.from_pdsfile(pdsf, name=name)
            except ValueError:
                if validate: raise
            else:
                if name == 'full':
                    full_viewable = viewable
                else:
                    viewables.append(viewable)

        if viewables or full_viewable:
            viewset = PdsViewSet(viewables)
            if full_viewable:
                viewset.append(full_viewable)
            return viewset

        return None

################################################################################
# ICON definitions
################################################################################

# This is a dictionary keyed by the icon_type. It returns (priority, filename).
# Priority is just a rough number to indicate that, when several files share an
# icon, the icon with the higher priority will be used. Primarily, this ensures
# that we do not use the label icon when a more specific icon is available.
#
# Some files contain the string formatting pattern '%s', which allows for a more
# specific version of an icon type to be used. Right now, this is just used with
# folders, where the "-open" suffix shows the folder to be open rather than
# closed.

ICON_FILENAME_VS_TYPE = {       # (priority, icon URL)
    'UNKNOWN'  : (10, 'document_generic.png'),
    'LABEL'    : ( 0, 'document_label.png'),
    'DATA'     : (20, 'document_binary.png'),
    'DIAGRAM'  : (20, 'document_diagram.png'),
    'TABLE'    : (30, 'document_table.png'),
    'IMAGE'    : (40, 'document_image.png'),
    'BROWSE'   : (50, 'document_preview.png'),
    'GEOM'     : (60, 'document_geometry.png'),
    'CUBE'     : (70, 'document_cube.png'),
    'VOLUME'   : (80, 'document_volume%s.png'),
    'TOPFILE'  : (85, 'document_viewmaster.png'),
    'SERIES'   : (90, 'document_series.png'),

    'INFO'     : (21, 'document_info.png'),
    'INDEX'    : (31, 'document_index.png'),
    'CODE'     : (41, 'document_software.png'),
    'LINK'     : (51, 'document_link.png'),

    'FOLDER'   : ( 4, 'folder_generic%s.png' ),
    'INFODIR'  : (24, 'folder_info%s.png'),
    'INDEXDIR' : (34, 'folder_index%s.png'),
    'CODEDIR'  : (44, 'folder_software%s.png'),
    'EXTRADIR' : (46, 'folder_extras%s.png'),
    'LABELDIR' : (55, 'folder_labels%s.png'),
    'CHECKDIR' : (65, 'folder_checksums%s.png'),
    'VOLDIR'   : (75, 'folder_volumes%s.png'),
    'IMAGEDIR' : (85, 'folder_images%s.png'),
    'TARDIR'   : (95, 'folder_archives%s.png'),
    'CUBEDIR'  : (96, 'folder_cubes%s.png'),
    'SERIESDIR': (97, 'folder_series%s.png'),

    'DATADIR'  : (22, 'folder_binary%s.png'),
    'BROWDIR'   :(52, 'folder_previews%s.png'),
    'GEOMDIR'  : (62, 'folder_geometry%s.png'),
    'DIAGDIR'  : (53, 'folder_diagrams%s.png'),

    'CHECKSUM' : (90, 'document_checksums.png'),
    'TARBALL'  : (91, 'document_archive.png'),
    'TOPDIR'   : (92, 'folder_viewmaster%s.png'),
}

# Icons are currently defined in specific sizes, as indicated by the name of the
# icon file's parent directory. ICON_URL_DIR_VS_SIZE, defined above, is a list
# of tuples (size in pixels, URL path) that indicates where to look for an icon
# of a particular size. Within each of these directory paths, the file names are
# identical.

ICON_DIR_VS_SIZE = [( 30, 'png-30/'),
                    ( 50, 'png-50/'),
                    (100, 'png-100/'),
                    (200, 'png-200/')]

# Create a dictionary of PdsViewSets keyed by [icon_type, open_state]:

ICON_SET_BY_TYPE = {}

def load_icons(path, url, color='blue', logger=None):
    """Loads icons for use by PdsViewable.iconset_for()."""

    for (icon_type, icon_info) in ICON_FILENAME_VS_TYPE.items():
        (priority, template) = icon_info

        icon_path_ = path.rstrip('/') + '/'
        icon_url_  = url.rstrip('/') + '/'

        for is_open in (True, False):
            pdsviews = []

            if '%s' in template:
                if is_open:
                    basename = template % '_open'
                else:
                    basename = template % ''
            else:
                basename = template

            for (size, icon_dir_) in ICON_DIR_VS_SIZE:
                relpath = color + '/' + icon_dir_ + basename
                abspath = icon_path_ + relpath

                try:
                    im = Image.open(abspath)
                except FileNotFoundError:
                    (width, height) = (size, size)
                    bytecount = 0
                    if logger:
                        logger.error('Missing icon file', abspath)
                else:
                    (width, height) = im.size
                    im.close()
                    bytecount = os.stat(abspath).st_size

                pdsview = PdsViewable(icon_path_ + relpath, icon_url_ + relpath,
                                      width, height, icon_type + ' icon',
                                      bytecount)
                pdsviews.append(pdsview)

            ICON_SET_BY_TYPE[icon_type,
                             is_open] = PdsViewSet(pdsviews, priority)

        ICON_SET_BY_TYPE[icon_type] = ICON_SET_BY_TYPE[icon_type, False]

################################################################################
# Method to select among multiple icons
################################################################################

def iconset_for(pdsfiles, is_open=False):
    """Select the icon set for a list of PdsFiles. Use the icon_type highest in
    priority."""

    if type(pdsfiles) != list:
        pdsfiles = [pdsfiles]

    icon_type = 'UNKNOWN'
    (priority, template) = ICON_FILENAME_VS_TYPE[icon_type]

    for pdsf in pdsfiles:
        test_type = pdsf.icon_type
        (new_priority, _) = ICON_FILENAME_VS_TYPE[test_type]
        if new_priority > priority:
            priority = new_priority
            icon_type = test_type

    return ICON_SET_BY_TYPE[icon_type, is_open]

################################################################################
