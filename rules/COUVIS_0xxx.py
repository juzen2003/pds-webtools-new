####################################################################################################################################
# rules/COUVIS_0xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

key_from_path = translator.TranslatorByRegex([
    (r'[-a-z]+/COUVIS_0xxx(|_\w+)/COUVIS_(0[0-9]{3})(|/)', re.I, r'COUVIS_0xxx/COUVIS_\2'),
    (r'[-a-z]+/COUVIS_0xxx(|_\w+)',                        re.I, r'COUVIS_0xxx'),
])

description_and_icon_by_dict = translator.TranslatorByDict({
    'COUVIS_0xxx'            : ('Cassini UVIS (ultraviolet spectrometer) data collection',                     'VOLDIR'),
    'COUVIS_0xxx/COUVIS_0001': ('Cassini UVIS data 1999-01-07 to 2000-12-31 (SC clock 1294420183-1356956400)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0002': ('Cassini UVIS data 2001-01-01 to 2001-03-31 (SC clock 1357007021-1364774880)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0003': ('Cassini UVIS data 2001-04-01 to 2002-02-15 (SC clock 1364775615-1392458352)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0004': ('Cassini UVIS data 2002-02-14 to 2002-12-31 (SC clock 1392337464-1420051276)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0005': ('Cassini UVIS data 2003-01-02 to 2003-12-24 (SC clock 1420106524-1450969731)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0006': ('Cassini UVIS data 2003-12-24 to 2004-05-18 (SC clock 1450940692-1463592253)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0007': ('Cassini UVIS Saturn data 2004-05-19 to 2004-06-21 (SC clock 1463624099-1466514293)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0008': ('Cassini UVIS Saturn data 2004-07-01 to 2004-09-30 (SC clock 1467352379-1475279648)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0009': ('Cassini UVIS Saturn data 2004-09-30 to 2004-12-31 (SC clock 1475201091-1483226223)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0010': ('Cassini UVIS Saturn data 2004-12-31 to 2005-03-31 (SC clock 1483223240-1491000403)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0011': ('Cassini UVIS Saturn data 2005-04-01 to 2005-06-30 (SC clock 1491023510-1498835165)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0012': ('Cassini UVIS Saturn data 2005-07-01 to 2005-10-01 (SC clock 1498835186-1506847245)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0013': ('Cassini UVIS Saturn data 2005-09-29 to 2005-12-31 (SC clock 1506689171-1514695055)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0014': ('Cassini UVIS Saturn data 2006-01-01 to 2006-03-31 (SC clock 1514782087-1522508375)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0015': ('Cassini UVIS Saturn data 2006-04-01 to 2006-06-30 (SC clock 1522545042-1530386246)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0016': ('Cassini UVIS Saturn data 2006-07-01 to 2006-09-30 (SC clock 1530435286-1538305876)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0017': ('Cassini UVIS Saturn data 2006-10-01 to 2006-12-31 (SC clock 1538365297-1546290558)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0018': ('Cassini UVIS Saturn data 2007-01-01 to 2007-03-31 (SC clock 1546355368-1554074554)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0019': ('Cassini UVIS Saturn data 2007-03-31 to 2007-06-30 (SC clock 1554074627-1561914636)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0020': ('Cassini UVIS Saturn data 2007-07-01 to 2007-09-30 (SC clock 1562002088-1569872197)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0021': ('Cassini UVIS Saturn data 2007-10-01 to 2007-12-31 (SC clock 1569936252-1577774372)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0022': ('Cassini UVIS Saturn data 2008-01-01 to 2008-03-31 (SC clock 1577869010-1585696703)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0023': ('Cassini UVIS Saturn data 2008-04-01 to 2008-06-30 (SC clock 1585735025-1593517593)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0024': ('Cassini UVIS Saturn data 2008-07-01 to 2008-09-30 (SC clock 1593635715-1601481652)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0025': ('Cassini UVIS Saturn data 2008-10-01 to 2008-12-31 (SC clock 1601538407-1609435609)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0026': ('Cassini UVIS Saturn data 2009-01-02 to 2009-03-31 (SC clock 1609572386-1617176831)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0027': ('Cassini UVIS Saturn data 2009-04-01 to 2009-06-30 (SC clock 1617239839-1625080028)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0028': ('Cassini UVIS Saturn data 2009-07-01 to 2009-09-30 (SC clock 1625117322-1633036339)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0029': ('Cassini UVIS Saturn data 2009-10-01 to 2009-12-31 (SC clock 1633050431-1640947353)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0030': ('Cassini UVIS Saturn data 2010-01-01 to 2010-03-30 (SC clock 1641074259-1648666196)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0031': ('Cassini UVIS Saturn data 2010-04-01 to 2010-06-30 (SC clock 1648802103-1656556010)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0032': ('Cassini UVIS Saturn data 2010-07-04 to 2010-09-29 (SC clock 1656944842-1664484587)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0033': ('Cassini UVIS Saturn data 2010-10-03 to 2010-12-31 (SC clock 1664814978-1672451021)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0034': ('Cassini UVIS Saturn data 2011-01-01 to 2011-03-31 (SC clock 1672544709-1680255450)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0035': ('Cassini UVIS Saturn data 2011-04-02 to 2011-06-29 (SC clock 1680427360-1688008580)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0036': ('Cassini UVIS Saturn data 2011-07-01 to 2011-09-30 (SC clock 1688189568-1696086490)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0037': ('Cassini UVIS Saturn data 2011-10-01 to 2011-12-31 (SC clock 1696121989-1704039240)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0038': ('Cassini UVIS Saturn data 2012-01-01 to 2012-03-31 (SC clock 1704078010-1711916690)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0039': ('Cassini UVIS Saturn data 2012-04-02 to 2012-06-30 (SC clock 1712030100-1719783280)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0040': ('Cassini UVIS Saturn data 2012-07-01 to 2012-09-30 (SC clock 1719818420-1727742421)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0041': ('Cassini UVIS Saturn data 2012-10-02 to 2012-12-31 (SC clock 1727864820-1735614023)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0042': ('Cassini UVIS Saturn data 2013-01-02 to 2013-03-31 (SC clock 1735795011-1743397031)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0043': ('Cassini UVIS Saturn data 2013-04-01 to 2013-06-30 (SC clock 1743475671-1751270529)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0044': ('Cassini UVIS Saturn data 2013-07-01 to 2013-09-30 (SC clock 1751345649-1759273132)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0045': ('Cassini UVIS Saturn data 2013-10-01 to 2013-12-31 (SC clock 1759280403-1767203202)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0046': ('Cassini UVIS Saturn data 2014-01-01 to 2014-03-31 (SC clock 1767266343-1775004210)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0047': ('Cassini UVIS Saturn data 2014-04-01 to 2014-06-30 (SC clock 1775005511-1782861202)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0048': ('Cassini UVIS Saturn data 2014-07-01 to 2014-09-30 (SC clock 1782868936-1790791641)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0049': ('Cassini UVIS Saturn data 2014-10-02 to 2014-12-31 (SC clock 1790898442-1798741083)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0050': ('Cassini UVIS Saturn data 2015-01-01 to 2015-03-31 (SC clock 1798829919-1806532773)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0051': ('Cassini UVIS Saturn data 2015-04-01 to 2015-06-30 (SC clock 1806542043-1814401063)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0052': ('Cassini UVIS Saturn data 2015-07-02 to 2015-09-30 (SC clock 1814509973-1822350994)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0053': ('Cassini UVIS Saturn data 2015-10-01 to 2015-12-31 (SC clock 1822366078-1830279925)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0054': ('Cassini UVIS Saturn data 2016-01-01 to 2016-03-31 (SC clock 1830306971-1838101636)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0055': ('Cassini UVIS Saturn data 2016-04-01 to 2016-06-30 (SC clock 1838208737-1846001165)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0056': ('Cassini UVIS Saturn data 2016-07-01 to 2016-09-30 (SC clock 1846112674-1853903812)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0057': ('Cassini UVIS Saturn data 2016-10-01 to 2016-12-30 (SC clock 1853975456-1861772866)', 'VOLUME'),
    'COUVIS_0xxx/COUVIS_0058': ('Cassini UVIS Saturn data 2017-01-01 to 2017-03-31 (SC clock 1861943868-1869672278)', 'VOLUME'),
}, key_from_path)

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*/DATA',          re.I, ('Data files grouped by date', 'CUBEDIR')),
    (r'volumes/.*/DATA/\w+',      re.I, ('Data files grouped by date', 'CUBEDIR')),
    (r'volumes/.*/HSP\w+\.DAT',   re.I, ('Time series data',           'DATA')),
    (r'volumes/.*/HDAC\w+\.DAT',  re.I, ('Binary data cube',           'DATA')),
    (r'volumes/.*/\w+\.DAT',      re.I, ('Spectral data cube',         'CUBE')),
    (r'volumes/.*\.txt_[0-9].*',  re.I, ('Text file',                  'INFO')),
    (r'volumes/.*OLD.DIR',        re.I, ('Directory',                  'FOLDER')),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'previews/(.*)_(\w+\.png)',    0, r'volumes/\1.*'),
    (r'previews/(\w+/\w+/DATA/\w+)', 0, r'volumes/\1'),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews)/COUVIS_0xxx/COUVIS_..../DATA(|/\w+)', 0, (True, True, True)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'volumes/(\w+)/COUVIS_[0-9]{4}/DATA/(\w+)', 0, r'volumes/\1/*/DATA/*'),
    (r'volumes/(\w+)/COUVIS_[0-9]{4}/DATA',       0, r'volumes/\1/*/DATA'),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'volumes/(.*/DATA/\w+/.*)\.(\w+)', 0, (r'previews/\1_thumb.png',
                                             r'previews/\1_small.png',
                                             r'previews/\1_med.png',
                                             r'previews/\1_full.png')),
])

####################################################################################################################################
# SORT_KEY
####################################################################################################################################

sort_key = translator.TranslatorByRegex([
    (r'^(EUV|FUV|HSP|HDAC)([0-9]{4}_[0-9]{3}_[0-9]{2}_[0-9]{2}.*)_thumb(\..*)', 0, r'\2\1_1thumb\3'),
    (r'^(EUV|FUV|HSP|HDAC)([0-9]{4}_[0-9]{3}_[0-9]{2}_[0-9]{2}.*)_small(\..*)', 0, r'\2\1_2small\3'),
    (r'^(EUV|FUV|HSP|HDAC)([0-9]{4}_[0-9]{3}_[0-9]{2}_[0-9]{2}.*)_med(\..*)',   0, r'\2\1_3med\3'),
    (r'^(EUV|FUV|HSP|HDAC)([0-9]{4}_[0-9]{3}_[0-9]{2}_[0-9]{2}.*)_full(\..*)',  0, r'\2\1_4full\3'),
    (r'^(EUV|FUV|HSP|HDAC)([0-9]{4}_[0-9]{3}_[0-9]{2}_[0-9]{2}.*)(\.DAT|LBL)',  0, r'\2\1\3'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class COUVIS_0xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('COUVIS_0xxx', re.I, 'COUVIS_0xxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_dict + description_and_icon_by_regex+ pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS
    SORT_KEY = sort_key + pdsfile.PdsFile.SORT_KEY
    ASSOCIATIONS_TO_VOLUMES = associations_to_volumes + pdsfile.PdsFile.ASSOCIATIONS_TO_VOLUMES

    VIEWABLES = {'default': default_viewables}

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COUVIS_0xxx'] = COUVIS_0xxx

####################################################################################################################################
