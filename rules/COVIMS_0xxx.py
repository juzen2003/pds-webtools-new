####################################################################################################################################
# rules/COVIMS_0xxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

key_from_path = translator.TranslatorByRegex([
    (r'[-a-z]+/COVIMS_\w+/COVIMS_(0[0-9]{3}|UNKS)', re.I, r'COVIMS_0xxx/COVIMS_\1'),
    (r'[-a-z]+/COVIMS_\w+',                         re.I, r'COVIMS_0xxx'),
])

description_and_icon_by_dict = translator.TranslatorByDict({
    'COVIMS_0xxx'            : ('Cassini VIMS near IR image cube collection',                                                 'VOLDIR'),
    'COVIMS_0xxx/COVIMS_0001': ('Cassini VIMS near IR image cubes 1999-01-10 to 2000-09-18 (SC clock 1294638283-1347975444)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0002': ('Cassini VIMS near IR image cubes 2000-11-15 to 2001-02-27 (SC clock 1352959095-1361942689)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0003': ('Cassini VIMS near IR image cubes 2001-03-26 to 2004-05-12 (SC clock 1364267566-1463071469)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0004': ('Cassini VIMS near IR image cubes 2004-05-15 to 2004-09-30 (SC clock 1463282549-1475280734)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0005': ('Cassini VIMS near IR image cubes 2004-10-01 to 2005-01-01 (SC clock 1475284734-1483237494)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0006': ('Cassini VIMS near IR image cubes 2005-01-15 to 2005-04-01 (SC clock 1484504514-1491006839)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0007': ('Cassini VIMS near IR image cubes 2005-04-01 to 2005-06-29 (SC clock 1491009142-1498752814)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0008': ('Cassini VIMS near IR image cubes 2005-07-03 to 2005-09-28 (SC clock 1499045884-1506582872)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0009': ('Cassini VIMS near IR image cubes 2005-10-01 to 2005-12-29 (SC clock 1506820472-1514578647)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0010': ('Cassini VIMS near IR image cubes 2006-01-02 to 2006-02-09 (SC clock 1514910709-1518212295)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0011': ('Cassini VIMS near IR image cubes 2006-02-10 to 2006-03-21 (SC clock 1518266882-1521668794)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0012': ('Cassini VIMS near IR image cubes 2006-04-09 to 2006-07-01 (SC clock 1523286567-1530491440)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0013': ('Cassini VIMS near IR image cubes 2006-07-01 to 2006-09-30 (SC clock 1530409863-1538299393)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0014': ('Cassini VIMS near IR image cubes 2006-10-07 to 2006-11-17 (SC clock 1538944759-1542414875)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0015': ('Cassini VIMS near IR image cubes 2006-11-17 to 2006-12-31 (SC clock 1542414904-1546295238)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0016': ('Cassini VIMS near IR image cubes 2007-01-01 to 2007-02-14 (SC clock 1546355132-1550156074)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0017': ('Cassini VIMS near IR image cubes 2007-02-15 to 2007-03-10 (SC clock 1550192768-1552178144)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0018': ('Cassini VIMS near IR image cubes 2007-03-10 to 2007-03-31 (SC clock 1552178203-1554072094)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0019': ('Cassini VIMS near IR image cubes 2007-04-05 to 2007-05-14 (SC clock 1554455530-1557859097)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0020': ('Cassini VIMS near IR image cubes 2007-05-17 to 2007-06-30 (SC clock 1558072781-1561897192)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0021': ('Cassini VIMS near IR image cubes 2007-07-01 to 2007-08-08 (SC clock 1561952753-1565267525)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0022': ('Cassini VIMS near IR image cubes 2007-08-09 to 2007-09-30 (SC clock 1565326867-1569855321)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0023': ('Cassini VIMS near IR image cubes 2007-10-01 to 2008-01-01 (SC clock 1569961098-1577839206)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0024': ('Cassini VIMS near IR image cubes 2008-01-01 to 2008-03-13 (SC clock 1577839206-1584060292)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0025': ('Cassini VIMS near IR image cubes 2008-03-14 to 2008-03-30 (SC clock 1584170165-1585587888)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0026': ('Cassini VIMS near IR image cubes 2008-04-01 to 2008-05-03 (SC clock 1585708668-1588550252)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0027': ('Cassini VIMS near IR image cubes 2008-05-05 to 2008-05-29 (SC clock 1588665217-1590713054)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0028': ('Cassini VIMS near IR image cubes 2008-05-29 to 2008-06-30 (SC clock 1590713054-1593518872)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0029': ('Cassini VIMS near IR image cubes 2008-07-02 to 2008-08-03 (SC clock 1593650532-1596452517)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0030': ('Cassini VIMS near IR image cubes 2008-08-03 to 2008-10-01 (SC clock 1596456707-1601513441)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0031': ('Cassini VIMS near IR image cubes 2008-10-01 to 2008-11-19 (SC clock 1601513441-1605800383)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0032': ('Cassini VIMS near IR image cubes 2008-11-19 to 2009-01-01 (SC clock 1605802708-1609461650)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0033': ('Cassini VIMS near IR image cubes 2009-01-01 to 2009-01-23 (SC clock 1609461650-1611427409)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0034': ('Cassini VIMS near IR image cubes 2009-01-24 to 2009-03-12 (SC clock 1611476375-1615510945)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0035': ('Cassini VIMS near IR image cubes 2009-03-18 to 2009-03-29 (SC clock 1616051245-1617062239)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0036': ('Cassini VIMS near IR image cubes 2009-04-03 to 2009-06-27 (SC clock 1617449578-1624835778)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0037': ('Cassini VIMS near IR image cubes 2009-07-02 to 2009-09-05 (SC clock 1625234639-1630865987)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0038': ('Cassini VIMS near IR image cubes 2009-09-06 to 2009-09-21 (SC clock 1630912090-1632191966)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0039': ('Cassini VIMS near IR image cubes 2009-10-05 to 2009-12-05 (SC clock 1633412166-1638666843)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0040': ('Cassini VIMS near IR image cubes 2009-12-05 to 2009-12-29 (SC clock 1638723725-1640819314)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0041': ('Cassini VIMS near IR image cubes 2010-01-01 to 2010-04-01 (SC clock 1641049810-1648774239)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0042': ('Cassini VIMS near IR image cubes 2010-04-01 to 2010-06-24 (SC clock 1648776234-1656073949)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0043': ('Cassini VIMS near IR image cubes 2010-07-04 to 2010-09-27 (SC clock 1656912134-1664264332)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0044': ('Cassini VIMS near IR image cubes 2010-10-13 to 2010-12-24 (SC clock 1665639872-1671887570)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0045': ('Cassini VIMS near IR image cubes 2011-01-09 to 2011-03-15 (SC clock 1673261211-1678845052)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0046': ('Cassini VIMS near IR image cubes 2011-03-15 to 2011-04-01 (SC clock 1678890289-1680310097)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0047': ('Cassini VIMS near IR image cubes 2011-04-01 to 2011-06-25 (SC clock 1680310140-1687660640)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0048': ('Cassini VIMS near IR image cubes 2011-07-03 to 2011-09-14 (SC clock 1688392546-1694661424)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0049': ('Cassini VIMS near IR image cubes 2011-09-14 to 2011-09-30 (SC clock 1694663069-1696077695)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0050': ('Cassini VIMS near IR image cubes 2011-10-01 to 2011-12-31 (SC clock 1696121519-1704028764)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0051': ('Cassini VIMS near IR image cubes 2012-01-01 to 2012-03-30 (SC clock 1704073953-1711795750)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0052': ('Cassini VIMS near IR image cubes 2012-04-02 to 2012-06-29 (SC clock 1712022876-1719708734)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0053': ('Cassini VIMS near IR image cubes 2012-07-01 to 2012-09-28 (SC clock 1719818187-1727553190)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0054': ('Cassini VIMS near IR image cubes 2012-10-01 to 2012-12-08 (SC clock 1727787251-1733631554)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0055': ('Cassini VIMS near IR image cubes 2012-12-08 to 2012-12-30 (SC clock 1733636304-1735601503)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0056': ('Cassini VIMS near IR image cubes 2013-01-03 to 2013-02-14 (SC clock 1735908309-1739511070)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0057': ('Cassini VIMS near IR image cubes 2013-02-15 to 2013-03-31 (SC clock 1739615685-1743456021)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0058': ('Cassini VIMS near IR image cubes 2013-04-01 to 2013-04-24 (SC clock 1743476711-1745489397)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0059': ('Cassini VIMS near IR image cubes 2013-04-28 to 2013-06-05 (SC clock 1745866125-1749088868)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0060': ('Cassini VIMS near IR image cubes 2013-06-05 to 2013-06-29 (SC clock 1749109412-1751229453)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0061': ('Cassini VIMS near IR image cubes 2013-07-02 to 2013-08-04 (SC clock 1751426927-1754291754)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0062': ('Cassini VIMS near IR image cubes 2013-08-05 to 2013-09-19 (SC clock 1754396868-1758282369)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0063': ('Cassini VIMS near IR image cubes 2013-10-05 to 2013-12-24 (SC clock 1759652615-1766584704)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0064': ('Cassini VIMS near IR image cubes 2013-12-25 to 2013-12-31 (SC clock 1766654706-1767195106)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0065': ('Cassini VIMS near IR image cubes 2014-01-01 to 2014-03-08 (SC clock 1767238950-1772963682)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0066': ('Cassini VIMS near IR image cubes 2014-03-08 to 2014-03-31 (SC clock 1772965513-1774984718)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0067': ('Cassini VIMS near IR image cubes 2014-04-01 to 2014-06-12 (SC clock 1775057912-1781228519)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0068': ('Cassini VIMS near IR image cubes 2014-06-15 to 2014-06-30 (SC clock 1781539290-1782853229)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0069': ('Cassini VIMS near IR image cubes 2014-07-02 to 2014-08-27 (SC clock 1782983163-1787811716)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0070': ('Cassini VIMS near IR image cubes 2014-08-27 to 2014-09-28 (SC clock 1787814162-1790610819)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0071': ('Cassini VIMS near IR image cubes 2014-10-02 to 2014-12-30 (SC clock 1790962394-1798609733)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0072': ('Cassini VIMS near IR image cubes 2015-01-01 to 2015-03-13 (SC clock 1798847389-1804941513)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0073': ('Cassini VIMS near IR image cubes 2015-03-13 to 2015-03-31 (SC clock 1804941513-1806538560)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0074': ('Cassini VIMS near IR image cubes 2015-04-01 to 2015-05-28 (SC clock 1806548996-1811484110)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0075': ('Cassini VIMS near IR image cubes 2015-05-28 to 2015-06-19 (SC clock 1811544309-1813428194)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0076': ('Cassini VIMS near IR image cubes 2015-07-03 to 2015-09-30 (SC clock 1814628244-1822341937)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0077': ('Cassini VIMS near IR image cubes 2015-10-01 to 2015-12-31 (SC clock 1822390743-1830233463)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0078': ('Cassini VIMS near IR image cubes 2016-01-02 to 2016-03-31 (SC clock 1830405810-1838163403)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0079': ('Cassini VIMS near IR image cubes 2016-04-01 to 2016-05-29 (SC clock 1838164763-1843180674)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0080': ('Cassini VIMS near IR image cubes 2016-05-29 to 2016-06-30 (SC clock 1843196151-1845993297)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0081': ('Cassini VIMS near IR image cubes 2016-07-01 to 2016-08-17 (SC clock 1846035543-1850136900)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0082': ('Cassini VIMS near IR image cubes 2016-08-18 to 2016-09-15 (SC clock 1850220206-1852624927)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0083': ('Cassini VIMS near IR image cubes 2016-09-15 to 2016-09-30 (SC clock 1852626663-1853972955)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0084': ('Cassini VIMS near IR image cubes 2016-10-01 to 2016-11-03 (SC clock 1854009215-1856896440)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0085': ('Cassini VIMS near IR image cubes 2016-11-04 to 2016-12-26 (SC clock 1856977062-1861436124)', 'VOLUME'),
    'COVIMS_0xxx/COVIMS_0086': ('Cassini VIMS near IR image cubes 2016-12-26 to 2016-12-31 (SC clock 1861464723-1861918752)', 'VOLUME'),
}, key_from_path)

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*/data',                                      re.I, ('Data files grouped by date', 'CUBEDIR')),
    (r'volumes/.*/dat/\w+',                                   re.I, ('Data files grouped by date', 'CUBEDIR')),
    (r'volumes/.*/extras',                                    re.I, ('Browse image collection',    'BROWDIR')),
    (r'volumes/.*/data/.*/extras/\w+',                        re.I, ('Browse image collection',    'BROWDIR')),
    (r'volumes/.*/data/.*/extras/.*\.(jpeg|jpeg_small|tiff)', re.I, ('Browse image',               'BROWSE' )),
    (r'volumes/.*/software.*cube_prep/cube_prep',             re.I, ('Program binary',             'CODE'   )),
    (r'volumes/.*/software.*/PPVL_report',                    re.I, ('Program binary',             'CODE'   )),

    (r'.*/thumbnail(/\w+)*',            re.I, ('Small browse images',           'BROWDIR' )),
    (r'.*/thumbnail/.*\.(gif|jpg|jpeg|jpeg_small|tif|tiff|png)', 
                                        re.I, ('Small browse image',            'BROWSE'  )),
    (r'.*/tiff(/\w+)*',                 re.I, ('Full-size browse images',       'BROWDIR' )),
    (r'.*/tiff/.*\.(gif|jpg|jpeg|jpeg_small|tif|tiff|png)', 
                                        re.I, ('Full-size browse image',        'BROWSE'  )),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'volumes/(.*/data/\w+/.*)\.(\w+)', 0, (r'previews/\1_thumb.png',
                                             r'previews/\1_small.png',
                                             r'previews/\1_med.png',
                                             r'previews/\1_full.png')),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

volumes_to_volumes = translator.TranslatorByRegex([
    (r'volumes/(.*)/extras/\w+/(.*)(\..*)\.(jpeg|jpeg_small|tiff)', 0, [r'volumes/\1/data/\2.*',
                                                                        r'volumes/\1/extras/*/\2.*']),
    (r'volumes/(.*)/extras/\w+(|/.*)',                              0, [r'volumes/\1/data\2',
                                                                        r'volumes/\1/extras/*\2']),
    (r'volumes/(.*)/extras',                                        0,  r'volumes/\1/data'),
    (r'volumes/(.*)/data/(.*)',                                     0,  r'volumes/\1/extras/*/\2*'),
    (r'volumes/(.*)/data/(.*)\.(.*)',                               0,  r'volumes/\1/extras/*/\2*'),
    (r'volumes/(.*)/data',                                          0,  r'volumes/\1/extras/*'),
])

associations_to_volumes = translator.TranslatorByRegex([
    (r'previews/(.*)_(\w+\.png)',      0, r'volumes/\1.*'),
    (r'previews/(\w+/\w+/data/\w+)',   0, r'volumes/\1'),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews)/\w+/\w+/data(|/\w+)',       0, (True, True, True)),
    (r'(volumes|previews)/\w+/\w+/extras/\w+(|/\w+)', 0, (True, True, True)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'(volumes|previews)/(\w+)/\w+/data/\w+', 0, r'\1/\2/*/data/*'),
    (r'(volumes|previews)/(\w+)/\w+/data',     0, r'\1/\2/*/data'),

    (r'volumes/(\w+)/\w+/extras/(\w+)/\w+', 0, r'volumes/\1/*/extras/\2/*'),
    (r'volumes/(\w+)/\w+/extras/(\w+)',     0, r'volumes/\1/*/extras/\2'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class COVIMS_0xxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('COVIMS_0xxx', re.I, 'COVIMS_0xxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_dict + description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    ASSOCIATIONS_TO_VOLUMES = associations_to_volumes + pdsfile.PdsFile.ASSOCIATIONS_TO_VOLUMES
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS

    VIEWABLES = {'default': default_viewables}

    VOLUMES_TO_ASSOCIATIONS = pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS.copy()
    VOLUMES_TO_ASSOCIATIONS['volumes'] = volumes_to_volumes + pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS['volumes']

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COVIMS_0xxx'] = COVIMS_0xxx

####################################################################################################################################

