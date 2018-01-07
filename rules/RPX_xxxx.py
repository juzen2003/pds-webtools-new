####################################################################################################################################
# rules/RPX_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

key_from_path = translator.TranslatorByRegex([
    (r'[-a-z]+/RPX_xxxx(|_\w+)/RPX_([0-9]{4})', re.I, r'RPX_xxxx/RPX_\2'),
    (r'[-a-z]+/RPX_xxxx(|_\w+)',                re.I, r'RPX_xxxx'),
])

description_and_icon_by_dict = translator.TranslatorByDict({
    'RPX_xxxx'         : ('Earth-based data from the 1995 Saturn ring plane crossing',                               'VOLDIR'),
    'RPX_xxxx/RPX_0001': ('HST WFPC2 observations of the 1995 Saturn ring plane crossing, 1994-10 to 1995-05',       'VOLUME'),
    'RPX_xxxx/RPX_0002': ('HST WFPC2 observations of the 1995 Saturn ring plane crossing, 1995-05',                  'VOLUME'),
    'RPX_xxxx/RPX_0003': ('HST WFPC2 observations of the 1995 Saturn ring plane crossing, 1995-08',                  'VOLUME'),
    'RPX_xxxx/RPX_0004': ('HST WFPC2 observations of the 1995 Saturn ring plane crossing, 1995-08 to 1995-11',       'VOLUME'),
    'RPX_xxxx/RPX_0005': ('HST WFPC2 observations of the 1995 Saturn ring plane crossing, 1995-11',                  'VOLUME'),
    'RPX_xxxx/RPX_0101': ('HST observations of the 1995 Saturn ring plane crossing, Willam Herschel Telescope',      'VOLUME'),
    'RPX_xxxx/RPX_0201': ('HST observations of the 1995 Saturn ring plane crossing, IRTF',                           'VOLUME'),
    'RPX_xxxx/RPX_0301': ('HST observations of the 1995 Saturn ring plane crossing, Canada-France-Hawaii Telescope', 'VOLUME'),
    'RPX_xxxx/RPX_0401': ('HST observations of the 1995 Saturn ring plane crossing, WIYN Telescope, Kitt Peak',      'VOLUME'),
}, key_from_path)

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*/rpx_00.*/BROWSE',   re.I, ('Browse GIFs',                   'BROWDIR' )),
    (r'volumes/.*/rpx_00.*/CALIMAGE', re.I, ('Calibrated images',             'IMAGEDIR')),
    (r'volumes/.*/rpx_00.*/CALMASK',  re.I, ('Calibrated image masks',        'DATADIR' )),
    (r'volumes/.*/rpx_00.*/ENGDATA',  re.I, ('Engineering data',              'DATADIR' )),
    (r'volumes/.*/rpx_00.*/ENGMASK',  re.I, ('Engineering data masks',        'DATADIR' )),
    (r'volumes/.*/rpx_00.*/HEADER',   re.I, ('HST header files',              'DATADIR' )),
    (r'volumes/.*/rpx_00.*/RAWIMAGE', re.I, ('Raw images',                    'IMAGEDIR')),
    (r'volumes/.*/rpx_00.*/RAWMASK',  re.I, ('Raw image masks',               'DATADIR' )),
    (r'volumes/.*/rpx_00.*/CALIMAGE/.*\.IMG', re.I, ('Calibrated image, FITS',          'IMAGE'   )),
    (r'volumes/.*/rpx_00.*/CALMASK/.*\.ZIP',  re.I, ('Image mask, zipped FITS',         'DATA'    )),
    (r'volumes/.*/rpx_00.*/ENGDATA/.*\.ZIP',  re.I, ('Engineering data, zipped FITS',   'DATA'    )),
    (r'volumes/.*/rpx_00.*/ENGMASK/.*\.ZIP',  re.I, ('Engineering mask, zipped FITS',   'DATA'    )),
    (r'volumes/.*/rpx_00.*/HEADER/.*\.ZIP',   re.I, ('HST header file, zipped FITS',    'DATA'    )),
    (r'volumes/.*/rpx_00.*/RAWIMAGE/.*\.ZIP', re.I, ('Raw image, zipped FITS',          'IMAGE'   )),
    (r'volumes/.*/rpx_00.*/RAWMASK/.*\.ZIP',  re.I, ('Raw image mask, zipped FITS',     'DATA'    )),
    (r'volumes/.*/rpx_00.*/[0-9]{6}XX',       re.I, ('Data files by year and month',    'IMAGEDIR')),
    (r'volumes/.*/rpx_00.*/[0-9]{6}XX/\w+',   re.I, ('Data files by observing program', 'IMAGEDIR')),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class RPX_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('RPX_xxxx', re.I, 'RPX_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_dict + description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['RPX_xxxx'] = RPX_xxxx

####################################################################################################################################
