################################################################################
# pdsviewable.py
################################################################################

import os
from PIL import Image

################################################################################
# Class definitions
################################################################################

class PdsViewable(object):
    """Contains the minimum information needed to show an image in HTML."""

    def __init__(self, abspath, url, width, height, alt, size_bytes,
                 pdsf=None):
        self.abspath = abspath
        self.url = url
        self.width = width
        self.height = height
        self.alt = alt
        self.bytes = size_bytes
        self.pdsf = pdsf

        self.width_over_height = float(self.width) / float(self.height)
        self.height_over_width = float(self.height) / float(self.width)

    def copy(self):
        return PdsViewable(self.abspath, self.url, self.width, self.height,
                           self.alt, self.size_bytes, self.pdsf)

    @staticmethod
    def from_pdsfile(pdsf):
        if not pdsf.width:
            raise ValueError('PdsFile is not viewable: ' + pdsf.abspath)

        return PdsViewable(pdsf.abspath, pdsf.url, pdsf.width, pdsf.height,
                           pdsf.logical_path, pdsf.size_bytes, pdsf)

################################################################################
################################################################################
################################################################################

class PdsViewSet(object):
    """Viewables selectable by size."""

    def __init__(self, viewables=[], priority=0):
        self.priority = priority        # Used to prioritize among icon sets

        self.viewables_by_width = {}
        self.viewables_by_height = {}

        for viewable in viewables:
            if viewable.width not in self.viewables_by_width:
                self.viewables_by_width[viewable.width] = viewable
            if viewable.height not in self.viewables_by_height:
                self.viewables_by_height[viewable.height] = viewable

        self.widths = self.viewables_by_width.keys()
        self.widths.sort()

        self.heights = self.viewables_by_height.keys()
        self.heights.sort()

    def append(self, viewable):
        if type(viewable) == PdsViewSet:
            for view in self.viewables_by_width:
                self.append(view)
            return

        if viewable.width in self.viewables_by_width: return
        if viewable.height in self.viewables_by_height: return

        self.viewables_by_width[viewable.width] = viewable
        self.widths.append(viewable.width)
        self.widths.sort()

        self.viewables_by_height[viewable.height] = viewable
        self.heights.append(viewable.height)
        self.height.sort()

    @property
    def viewables(self):
        results = []
        for width in self.widths:
            results.append(self.viewables_by_width[width])
        return results

    @property
    def full_size(self):
        return self.viewables_by_height[self.heights[-1]]

    def __len__(self):
        return len(self.widths)

    def for_width(self, size):
        for key in self.widths:
            if key >= size:
                break

        pdsview = self.viewables_by_width[key]
        result = pdsview.copy()
        result.height = max(1, int(pdsview.height_over_width * size + 0.5))
        result.width = size
        return result

    def for_height(self, size):
        for key in self.heights:
            if key >= size:
                break

        pdsview = self.viewables_by_height[key]
        result = pdsview.copy()
        result.width = max(1, int(pdsview.width_over_height * size + 0.5))
        result.height = size
        return result

    def for_frame(self, width, height=None):
        if height is None:
            height = width

        pdsview = self.for_width(width)
        if pdsview.height > height:
            pdsview = self.for_height(height)
            pdsview.width = min(pdsview.width, width)

        return pdsview

    @staticmethod
    def from_pdsfiles(pdsfiles, validate=False):

        if type(pdsfiles) not in (list,tuple):
            pdsfiles = [pdsfiles]

        pdsviews = []
        for pdsf in pdsfiles:
            try:
                pdsviews.append(PdsViewable.from_pdsfile(pdsf))
            except ValueError:
                if validate: raise

        if pdsviews:
            return PdsViewSet(pdsviews)

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

    'INFO'     : (21, 'document_info.png'),
    'INDEX'    : (31, 'document_index.png'),
    'CODE'     : (41, 'document_software.png'),

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

    'DATADIR'  : (22, 'folder_binary%s.png'),
    'BROWDIR'   :(52, 'folder_previews%s.png'),
    'GEOMDIR'  : (62, 'folder_geometry%s.png'),
    'DIAGDIR'  : (53, 'folder_geometry%s.png'),

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

def load_icons(path, url, color='blue'):
    """Loads icons for use by PdsViewable.iconset_for()."""

    for (icon_type, icon_info) in ICON_FILENAME_VS_TYPE.items():
        (priority, template) = icon_info

        icon_path_ = path.rstrip('/') + '/'
        icon_url_  = url.rstrip('/') + '/'

        for open in (True, False):
            pdsviews = []

            if '%s' in template:
                if open:
                    basename = template % '_open'
                else:
                    basename = template % ''
            else:
                basename = template

            for (size, icon_dir_) in ICON_DIR_VS_SIZE:
                relpath = color + '/' + icon_dir_ + basename
                abspath = icon_path_ + relpath

                im = Image.open(abspath)
                (width, height) = im.size
                im.close()

                pdsview = PdsViewable(icon_path_ + relpath, icon_url_ + relpath,
                                      width, height, icon_type + ' icon')
                pdsviews.append(pdsview)

            ICON_SET_BY_TYPE[icon_type, open] = PdsViewSet(pdsviews, priority)

        ICON_SET_BY_TYPE[icon_type] = ICON_SET_BY_TYPE[icon_type, False]

################################################################################
# Method to select among multiple icons
################################################################################

def iconset_for(pdsfiles, open=False):
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

    return ICON_SET_BY_TYPE[icon_type, open]

################################################################################
