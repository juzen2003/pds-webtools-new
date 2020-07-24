####################################################################################################################################
# rules/RPX_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

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

    DESCRIPTION_AND_ICON = description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON

    def FILENAME_KEYLEN(self):
        """9 for files in the HST series RPX_0001-5; 0 otherwise."""

        # Use the length of the HST group ID for RPX_0001-5
        if '/RPX_000' in self.abspath:
            return 9

        return 0

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['RPX_xxxx'] = RPX_xxxx

####################################################################################################################################
