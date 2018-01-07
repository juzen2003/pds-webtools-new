####################################################################################################################################
# rules/COISS_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

key_from_path = translator.TranslatorByRegex([
    (r'.*calibrated/COISS_([12])xxx(|_.*)',                   re.I, r'calibrated/COISS_\1xxx\2'),
    (r'[-a-z]+/COISS_([0-3])xxx(|_.*)/COISS_([0-3][0-9]{3})', re.I, r'COISS_\1xxx/COISS_\3'),
    (r'[-a-z]+/COISS_([0-3])xxx(|_.*)',                       re.I, r'COISS_\1xxx\2'),
])

description_and_icon_by_dict = translator.TranslatorByDict({
    'calibrated/COISS_1xxx'      : ('Cassini Jupiter image collection, CISSCAL 3.8', 'VOLDIR'),
    'calibrated/COISS_2xxx'      : ('Cassini Saturn image collection, CISSCAL 3.8',  'VOLDIR'),
    'calibrated/COISS_1xxx_v1.0' : ('Cassini Jupiter image collection, CISSCAL 3.6', 'VOLDIR'),
    'calibrated/COISS_2xxx_v1.0' : ('Cassini Saturn image collection, CISSCAL 3.6',  'VOLDIR'),

    'COISS_0xxx'           : ('Cassini ISS calibration data collection, software v3.8', 'VOLDIR'),
    'COISS_0xxx_v1'        : ('Cassini ISS calibration data collection, software v3.3', 'VOLDIR'),
    'COISS_0xxx_v2'        : ('Cassini ISS calibration data collection, software v3.6', 'VOLDIR'),
    'COISS_0xxx/COISS_0001': ('Cassini ISS calibration data',            'VOLUME'),
    'COISS_0xxx/COISS_0002': ('Cassini ISS calibration data',            'VOLUME'),
    'COISS_0xxx/COISS_0003': ('Cassini ISS calibration data',            'VOLUME'),
    'COISS_0xxx/COISS_0004': ('Cassini ISS calibration data',            'VOLUME'),
    'COISS_0xxx/COISS_0005': ('Cassini ISS calibration data',            'VOLUME'),
    'COISS_0xxx/COISS_0006': ('Cassini ISS calibration data',            'VOLUME'),
    'COISS_0xxx/COISS_0007': ('Cassini ISS calibration data',            'VOLUME'),
    'COISS_0xxx/COISS_0008': ('Cassini ISS calibration data',            'VOLUME'),
    'COISS_0xxx/COISS_0009': ('Cassini ISS calibration data',            'VOLUME'),
    'COISS_0xxx/COISS_0010': ('Cassini ISS calibration data',            'VOLUME'),
    'COISS_0xxx/COISS_0011': ('Cassini ISS calibration data',            'VOLUME'),

    'COISS_1xxx'           : ('Cassini Jupiter image collection',                                                     'VOLDIR'),
    'COISS_1xxx/COISS_1001': ('Cassini ISS Jupiter images 1999-01-09 to 2000-10-31 (SC clock 1294562621-1351672562)', 'VOLUME'),
    'COISS_1xxx/COISS_1002': ('Cassini ISS Jupiter images 2000-11-01 to 2000-11-24 (SC clock 1351738505-1353756211)', 'VOLUME'),
    'COISS_1xxx/COISS_1003': ('Cassini ISS Jupiter images 2000-11-24 to 2000-12-07 (SC clock 1353756264-1354880622)', 'VOLUME'),
    'COISS_1xxx/COISS_1004': ('Cassini ISS Jupiter images 2000-12-07 to 2001-01-07 (SC clock 1354880674-1357563782)', 'VOLUME'),
    'COISS_1xxx/COISS_1005': ('Cassini ISS Jupiter images 2001-01-07 to 2001-01-28 (SC clock 1357564437-1359362640)', 'VOLUME'),
    'COISS_1xxx/COISS_1006': ('Cassini ISS Jupiter images 2001-01-28 to 2001-03-17 (SC clock 1359362918-1363539029)', 'VOLUME'),
    'COISS_1xxx/COISS_1007': ('Cassini ISS Jupiter images 2001-03-17 to 2002-07-09 (SC clock 1363539046-1404903619)', 'VOLUME'),
    'COISS_1xxx/COISS_1008': ('Cassini ISS Jupiter images 2002-07-15 to 2003-10-13 (SC clock 1405398451-1444749812)', 'VOLUME'),
    'COISS_1xxx/COISS_1009': ('Cassini ISS Jupiter images 2003-10-14 to 2003-12-25 (SC clock 1444855355-1451040707)', 'VOLUME'),

    'COISS_2xxx'           : ('Cassini Saturn image collection',                                                     'VOLDIR'),
    'COISS_2xxx/COISS_2001': ('Cassini ISS Saturn images 2004-02-06 to 2004-04-18 (SC clock 1454725799-1460960370)', 'VOLUME'),
    'COISS_2xxx/COISS_2002': ('Cassini ISS Saturn images 2004-04-18 to 2004-05-18 (SC clock 1460960653-1463538454)', 'VOLUME'),
    'COISS_2xxx/COISS_2003': ('Cassini ISS Saturn images 2004-05-18 to 2004-06-11 (SC clock 1463538486-1465673464)', 'VOLUME'),
    'COISS_2xxx/COISS_2004': ('Cassini ISS Saturn images 2004-06-11 to 2004-07-27 (SC clock 1465674474-1469618468)', 'VOLUME'),
    'COISS_2xxx/COISS_2005': ('Cassini ISS Saturn images 2004-07-27 to 2004-09-02 (SC clock 1469618498-1472806264)', 'VOLUME'),
    'COISS_2xxx/COISS_2006': ('Cassini ISS Saturn images 2004-09-02 to 2004-09-28 (SC clock 1472808133-1475024077)', 'VOLUME'),
    'COISS_2xxx/COISS_2007': ('Cassini ISS Saturn images 2004-09-28 to 2004-10-28 (SC clock 1475025239-1477653092)', 'VOLUME'),
    'COISS_2xxx/COISS_2008': ('Cassini ISS Saturn images 2004-10-28 to 2005-01-16 (SC clock 1477654052-1484573247)', 'VOLUME'),
    'COISS_2xxx/COISS_2009': ('Cassini ISS Saturn images 2005-01-16 to 2005-02-27 (SC clock 1484573287-1488210311)', 'VOLUME'),
    'COISS_2xxx/COISS_2010': ('Cassini ISS Saturn images 2005-02-27 to 2005-03-31 (SC clock 1488210347-1491006407)', 'VOLUME'),
    'COISS_2xxx/COISS_2011': ('Cassini ISS Saturn images 2005-04-01 to 2005-05-04 (SC clock 1491006469-1493885777)', 'VOLUME'),
    'COISS_2xxx/COISS_2012': ('Cassini ISS Saturn images 2005-05-04 to 2005-06-24 (SC clock 1493885952-1498313926)', 'VOLUME'),
    'COISS_2xxx/COISS_2013': ('Cassini ISS Saturn images 2005-06-25 to 2005-06-30 (SC clock 1498351302-1498825765)', 'VOLUME'),
    'COISS_2xxx/COISS_2014': ('Cassini ISS Saturn images 2005-07-01 to 2005-08-20 (SC clock 1498916026-1503245000)', 'VOLUME'),
    'COISS_2xxx/COISS_2015': ('Cassini ISS Saturn images 2005-08-20 to 2005-09-30 (SC clock 1503245364-1506814111)', 'VOLUME'),
    'COISS_2xxx/COISS_2016': ('Cassini ISS Saturn images 2005-10-01 to 2005-11-08 (SC clock 1506820484-1510120372)', 'VOLUME'),
    'COISS_2xxx/COISS_2017': ('Cassini ISS Saturn images 2005-11-09 to 2005-12-26 (SC clock 1510209958-1514331366)', 'VOLUME'),
    'COISS_2xxx/COISS_2018': ('Cassini ISS Saturn images 2005-12-27 to 2005-12-31 (SC clock 1514336432-1514757207)', 'VOLUME'),
    'COISS_2xxx/COISS_2019': ('Cassini ISS Saturn images 2006-01-01 to 2006-01-27 (SC clock 1514778150-1517073119)', 'VOLUME'),
    'COISS_2xxx/COISS_2020': ('Cassini ISS Saturn images 2006-01-27 to 2006-03-08 (SC clock 1517073787-1520512984)', 'VOLUME'),
    'COISS_2xxx/COISS_2021': ('Cassini ISS Saturn images 2006-03-08 to 2006-03-30 (SC clock 1520513038-1522397049)', 'VOLUME'),
    'COISS_2xxx/COISS_2022': ('Cassini ISS Saturn images 2006-04-01 to 2006-05-11 (SC clock 1522542710-1526038532)', 'VOLUME'),
    'COISS_2xxx/COISS_2023': ('Cassini ISS Saturn images 2006-05-11 to 2006-06-30 (SC clock 1526038904-1530366500)', 'VOLUME'),
    'COISS_2xxx/COISS_2024': ('Cassini ISS Saturn images 2006-07-01 to 2006-09-05 (SC clock 1530431890-1536146633)', 'VOLUME'),
    'COISS_2xxx/COISS_2025': ('Cassini ISS Saturn images 2006-09-05 to 2006-09-29 (SC clock 1536146675-1538259248)', 'VOLUME'),
    'COISS_2xxx/COISS_2026': ('Cassini ISS Saturn images 2006-10-06 to 2006-11-20 (SC clock 1538857861-1542736726)', 'VOLUME'),
    'COISS_2xxx/COISS_2027': ('Cassini ISS Saturn images 2006-11-20 to 2006-12-31 (SC clock 1542736808-1546289032)', 'VOLUME'),
    'COISS_2xxx/COISS_2028': ('Cassini ISS Saturn images 2007-01-01 to 2007-01-29 (SC clock 1546382075-1548767008)', 'VOLUME'),
    'COISS_2xxx/COISS_2029': ('Cassini ISS Saturn images 2007-01-29 to 2007-02-19 (SC clock 1548767805-1550618373)', 'VOLUME'),
    'COISS_2xxx/COISS_2030': ('Cassini ISS Saturn images 2007-02-20 to 2007-03-31 (SC clock 1550624072-1554072073)', 'VOLUME'),
    'COISS_2xxx/COISS_2031': ('Cassini ISS Saturn images 2007-04-01 to 2007-05-09 (SC clock 1554109736-1557390129)', 'VOLUME'),
    'COISS_2xxx/COISS_2032': ('Cassini ISS Saturn images 2007-05-09 to 2007-06-14 (SC clock 1557397493-1560553326)', 'VOLUME'),
    'COISS_2xxx/COISS_2033': ('Cassini ISS Saturn images 2007-06-14 to 2007-06-30 (SC clock 1560553717-1561883275)', 'VOLUME'),
    'COISS_2xxx/COISS_2034': ('Cassini ISS Saturn images 2007-07-01 to 2007-08-04 (SC clock 1561952692-1564917387)', 'VOLUME'),
    'COISS_2xxx/COISS_2035': ('Cassini ISS Saturn images 2007-08-04 to 2007-09-02 (SC clock 1564917520-1567394149)', 'VOLUME'),
    'COISS_2xxx/COISS_2036': ('Cassini ISS Saturn images 2007-09-02 to 2007-09-26 (SC clock 1567440376-1569482804)', 'VOLUME'),
    'COISS_2xxx/COISS_2037': ('Cassini ISS Saturn images 2007-09-26 to 2007-09-30 (SC clock 1569482858-1569890022)', 'VOLUME'),
    'COISS_2xxx/COISS_2038': ('Cassini ISS Saturn images 2007-10-01 to 2007-11-08 (SC clock 1569962752-1573185858)', 'VOLUME'),
    'COISS_2xxx/COISS_2039': ('Cassini ISS Saturn images 2007-11-08 to 2007-12-21 (SC clock 1573186007-1576929166)', 'VOLUME'),
    'COISS_2xxx/COISS_2040': ('Cassini ISS Saturn images 2007-12-21 to 2007-12-31 (SC clock 1576929618-1577768880)', 'VOLUME'),
    'COISS_2xxx/COISS_2041': ('Cassini ISS Saturn images 2008-01-01 to 2008-02-04 (SC clock 1577839260-1580849129)', 'VOLUME'),
    'COISS_2xxx/COISS_2042': ('Cassini ISS Saturn images 2008-02-04 to 2008-03-28 (SC clock 1580849252-1585391135)', 'VOLUME'),
    'COISS_2xxx/COISS_2043': ('Cassini ISS Saturn images 2008-03-28 to 2008-03-30 (SC clock 1585391194-1585611101)', 'VOLUME'),
    'COISS_2xxx/COISS_2044': ('Cassini ISS Saturn images 2008-04-01 to 2008-05-10 (SC clock 1585730357-1589107702)', 'VOLUME'),
    'COISS_2xxx/COISS_2045': ('Cassini ISS Saturn images 2008-05-10 to 2008-06-18 (SC clock 1589107813-1592481245)', 'VOLUME'),
    'COISS_2xxx/COISS_2046': ('Cassini ISS Saturn images 2008-06-19 to 2008-06-30 (SC clock 1592543393-1593561976)', 'VOLUME'),
    'COISS_2xxx/COISS_2047': ('Cassini ISS Saturn images 2008-07-01 to 2008-08-19 (SC clock 1593596285-1597823599)', 'VOLUME'),
    'COISS_2xxx/COISS_2048': ('Cassini ISS Saturn images 2008-08-19 to 2008-09-30 (SC clock 1597823640-1601512734)', 'VOLUME'),
    'COISS_2xxx/COISS_2049': ('Cassini ISS Saturn images 2008-10-01 to 2008-11-07 (SC clock 1601512974-1604716205)', 'VOLUME'),
    'COISS_2xxx/COISS_2050': ('Cassini ISS Saturn images 2008-11-07 to 2008-12-21 (SC clock 1604723151-1608523623)', 'VOLUME'),
    'COISS_2xxx/COISS_2051': ('Cassini ISS Saturn images 2008-12-21 to 2008-12-31 (SC clock 1608534761-1609436118)', 'VOLUME'),
    'COISS_2xxx/COISS_2052': ('Cassini ISS Saturn images 2009-01-02 to 2009-02-10 (SC clock 1609568158-1612979183)', 'VOLUME'),
    'COISS_2xxx/COISS_2053': ('Cassini ISS Saturn images 2009-02-10 to 2009-03-31 (SC clock 1612979357-1617237040)', 'VOLUME'),
    'COISS_2xxx/COISS_2054': ('Cassini ISS Saturn images 2009-04-02 to 2009-05-26 (SC clock 1617409134-1622025718)', 'VOLUME'),
    'COISS_2xxx/COISS_2055': ('Cassini ISS Saturn images 2009-05-26 to 2009-06-30 (SC clock 1622025854-1625075053)', 'VOLUME'),
    'COISS_2xxx/COISS_2056': ('Cassini ISS Saturn images 2009-07-01 to 2009-08-16 (SC clock 1625115007-1629142938)', 'VOLUME'),
    'COISS_2xxx/COISS_2057': ('Cassini ISS Saturn images 2009-08-16 to 2009-09-28 (SC clock 1629144588-1632806885)', 'VOLUME'),
    'COISS_2xxx/COISS_2058': ('Cassini ISS Saturn images 2009-10-05 to 2009-11-21 (SC clock 1633455171-1637523061)', 'VOLUME'),
    'COISS_2xxx/COISS_2059': ('Cassini ISS Saturn images 2009-11-21 to 2009-12-28 (SC clock 1637523963-1640704638)', 'VOLUME'),
    'COISS_2xxx/COISS_2060': ('Cassini ISS Saturn images 2010-01-01 to 2010-03-05 (SC clock 1641073110-1646527388)', 'VOLUME'),
    'COISS_2xxx/COISS_2061': ('Cassini ISS Saturn images 2010-03-06 to 2010-03-29 (SC clock 1646529634-1648584112)', 'VOLUME'),
    'COISS_2xxx/COISS_2062': ('Cassini ISS Saturn images 2010-04-02 to 2010-06-12 (SC clock 1648877202-1655080267)', 'VOLUME'),
    'COISS_2xxx/COISS_2063': ('Cassini ISS Saturn images 2010-06-12 to 2010-06-30 (SC clock 1655080582-1656635176)', 'VOLUME'),
    'COISS_2xxx/COISS_2064': ('Cassini ISS Saturn images 2010-07-04 to 2010-09-10 (SC clock 1656912467-1662813261)', 'VOLUME'),
    'COISS_2xxx/COISS_2065': ('Cassini ISS Saturn images 2010-09-10 to 2010-09-25 (SC clock 1662813709-1664093964)', 'VOLUME'),
    'COISS_2xxx/COISS_2066': ('Cassini ISS Saturn images 2010-10-03 to 2010-12-24 (SC clock 1664840648-1671890732)', 'VOLUME'),
    'COISS_2xxx/COISS_2067': ('Cassini ISS Saturn images 2011-01-02 to 2011-03-31 (SC clock 1672660827-1680244602)', 'VOLUME'),
    'COISS_2xxx/COISS_2068': ('Cassini ISS Saturn images 2011-04-06 to 2011-06-26 (SC clock 1680805726-1687817348)', 'VOLUME'),
    'COISS_2xxx/COISS_2069': ('Cassini ISS Saturn images 2011-07-01 to 2011-09-26 (SC clock 1688230146-1695761375)', 'VOLUME'),
    'COISS_2xxx/COISS_2070': ('Cassini ISS Saturn images 2011-09-26 to 2011-09-30 (SC clock 1695761447-1696077664)', 'VOLUME'),
    'COISS_2xxx/COISS_2071': ('Cassini ISS Saturn images 2011-10-01 to 2011-12-31 (SC clock 1696121676-1704030594)', 'VOLUME'),
    'COISS_2xxx/COISS_2072': ('Cassini ISS Saturn images 2012-01-01 to 2012-03-14 (SC clock 1704074445-1710379894)', 'VOLUME'),
    'COISS_2xxx/COISS_2073': ('Cassini ISS Saturn images 2012-03-14 to 2012-03-29 (SC clock 1710382571-1711687639)', 'VOLUME'),
    'COISS_2xxx/COISS_2074': ('Cassini ISS Saturn images 2012-04-03 to 2012-06-11 (SC clock 1712152543-1718118023)', 'VOLUME'),
    'COISS_2xxx/COISS_2075': ('Cassini ISS Saturn images 2012-06-11 to 2012-06-30 (SC clock 1718119408-1719746078)', 'VOLUME'),
    'COISS_2xxx/COISS_2076': ('Cassini ISS Saturn images 2012-07-01 to 2012-09-28 (SC clock 1719863067-1727539077)', 'VOLUME'),
    'COISS_2xxx/COISS_2077': ('Cassini ISS Saturn images 2012-09-28 to 2012-09-28 (SC clock 1727539149-1727552003)', 'VOLUME'),
    'COISS_2xxx/COISS_2078': ('Cassini ISS Saturn images 2012-10-01 to 2012-11-28 (SC clock 1727769521-1732777784)', 'VOLUME'),
    'COISS_2xxx/COISS_2079': ('Cassini ISS Saturn images 2012-11-29 to 2012-12-31 (SC clock 1732865787-1735607575)', 'VOLUME'),
    'COISS_2xxx/COISS_2080': ('Cassini ISS Saturn images 2013-01-03 to 2013-02-23 (SC clock 1735908278-1740280668)', 'VOLUME'),
    'COISS_2xxx/COISS_2081': ('Cassini ISS Saturn images 2013-02-23 to 2013-03-31 (SC clock 1740280710-1743467682)', 'VOLUME'),
    'COISS_2xxx/COISS_2082': ('Cassini ISS Saturn images 2013-04-01 to 2013-05-30 (SC clock 1743477116-1748625981)', 'VOLUME'),
    'COISS_2xxx/COISS_2083': ('Cassini ISS Saturn images 2013-05-30 to 2013-06-30 (SC clock 1748626053-1751330607)', 'VOLUME'),
    'COISS_2xxx/COISS_2084': ('Cassini ISS Saturn images 2013-07-01 to 2013-09-06 (SC clock 1751331503-1757175175)', 'VOLUME'),
    'COISS_2xxx/COISS_2085': ('Cassini ISS Saturn images 2013-09-06 to 2013-09-26 (SC clock 1757175247-1758918748)', 'VOLUME'),
    'COISS_2xxx/COISS_2086': ('Cassini ISS Saturn images 2013-10-05 to 2013-12-30 (SC clock 1759651485-1767109007)', 'VOLUME'),
    'COISS_2xxx/COISS_2087': ('Cassini ISS Saturn images 2013-12-30 to 2013-12-31 (SC clock 1767109051-1767192839)', 'VOLUME'),
    'COISS_2xxx/COISS_2088': ('Cassini ISS Saturn images 2014-01-01 to 2014-03-08 (SC clock 1767238900-1773012835)', 'VOLUME'),
    'COISS_2xxx/COISS_2089': ('Cassini ISS Saturn images 2014-03-08 to 2014-03-31 (SC clock 1773012952-1774999982)', 'VOLUME'),
    'COISS_2xxx/COISS_2090': ('Cassini ISS Saturn images 2014-04-01 to 2014-06-30 (SC clock 1775058271-1782846178)', 'VOLUME'),
    'COISS_2xxx/COISS_2091': ('Cassini ISS Saturn images 2014-07-02 to 2014-09-22 (SC clock 1782983662-1790054929)', 'VOLUME'),
    'COISS_2xxx/COISS_2092': ('Cassini ISS Saturn images 2014-09-22 to 2014-09-28 (SC clock 1790079091-1790610212)', 'VOLUME'),
    'COISS_2xxx/COISS_2093': ('Cassini ISS Saturn images 2014-10-04 to 2014-12-27 (SC clock 1791082749-1798389055)', 'VOLUME'),
    'COISS_2xxx/COISS_2094': ('Cassini ISS Saturn images 2015-01-01 to 2015-03-15 (SC clock 1798826178-1805088123)', 'VOLUME'),
    'COISS_2xxx/COISS_2095': ('Cassini ISS Saturn images 2015-03-15 to 2015-03-31 (SC clock 1805088285-1806531309)', 'VOLUME'),
    'COISS_2xxx/COISS_2096': ('Cassini ISS Saturn images 2015-04-01 to 2015-06-04 (SC clock 1806543575-1812113482)', 'VOLUME'),
    'COISS_2xxx/COISS_2097': ('Cassini ISS Saturn images 2015-06-04 to 2015-06-30 (SC clock 1812153586-1814394077)', 'VOLUME'),
    'COISS_2xxx/COISS_2098': ('Cassini ISS Saturn images 2015-07-01 to 2015-09-11 (SC clock 1814434042-1820645736)', 'VOLUME'),
    'COISS_2xxx/COISS_2099': ('Cassini ISS Saturn images 2015-09-11 to 2015-09-30 (SC clock 1820648741-1822320949)', 'VOLUME'),
    'COISS_2xxx/COISS_2100': ('Cassini ISS Saturn images 2015-10-01 to 2015-12-22 (SC clock 1822395209-1829502100)', 'VOLUME'),
    'COISS_2xxx/COISS_2101': ('Cassini ISS Saturn images 2015-12-23 to 2015-12-30 (SC clock 1829539156-1830149298)', 'VOLUME'),
    'COISS_2xxx/COISS_2102': ('Cassini ISS Saturn images 2016-01-02 to 2016-03-22 (SC clock 1830403828-1837312933)', 'VOLUME'),
    'COISS_2xxx/COISS_2103': ('Cassini ISS Saturn images 2016-03-22 to 2016-03-29 (SC clock 1837313417-1837988603)', 'VOLUME'),
    'COISS_2xxx/COISS_2104': ('Cassini ISS Saturn images 2016-04-01 to 2016-06-11 (SC clock 1838169062-1844315705)', 'VOLUME'),
    'COISS_2xxx/COISS_2105': ('Cassini ISS Saturn images 2016-06-11 to 2016-06-30 (SC clock 1844319700-1845993030)', 'VOLUME'),
    'COISS_2xxx/COISS_2106': ('Cassini ISS Saturn images 2016-07-01 to 2016-08-31 (SC clock 1846032655-1851331437)', 'VOLUME'),
    'COISS_2xxx/COISS_2107': ('Cassini ISS Saturn images 2016-08-31 to 2016-09-27 (SC clock 1851331524-1853706504)', 'VOLUME'),
    'COISS_2xxx/COISS_2108': ('Cassini ISS Saturn images 2016-10-01 to 2016-12-07 (SC clock 1854009318-1859794656)', 'VOLUME'),
    'COISS_2xxx/COISS_2109': ('Cassini ISS Saturn images 2016-12-07 to 2016-12-31 (SC clock 1859795917-1861911431)', 'VOLUME'),

    'COISS_3xxx'           : ('Cassini cartographic maps',                       'VOLDIR'),
    'COISS_3xxx_v1'        : ('Cassini cartographic maps, superseded releases',  'VOLDIR'),
    'COISS_3xxx/COISS_3001': ('Cassini cartographic maps of Phoebe',             'VOLUME'),
    'COISS_3xxx/COISS_3002': ('Cassini cartographic maps of Enceladus',          'VOLUME'),
    'COISS_3xxx/COISS_3003': ('Cassini cartographic maps of Dione',              'VOLUME'),
    'COISS_3xxx/COISS_3004': ('Cassini cartographic maps of Tethys',             'VOLUME'),
    'COISS_3xxx/COISS_3005': ('Cassini cartographic maps of Iapetus',            'VOLUME'),
    'COISS_3xxx/COISS_3006': ('Cassini cartographic maps of Mimas',              'VOLUME'),
    'COISS_3xxx/COISS_3007': ('Cassini cartographic maps of Rhea',               'VOLUME'),
}, key_from_path)

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*/data/.*/N[0-9_]+\.img',                     re.I, ('Narrow-angle image, VICAR',     'IMAGE'   )),
    (r'volumes/.*/data/.*/W[0-9_]+\.img',                     re.I, ('Wide-angle image, VICAR',       'IMAGE'   )),
    (r'volumes/.*/data/.*/extras(/\w+)*(|/)',                 re.I, ('Preview image collection',      'BROWDIR' )),
    (r'volumes/.*/data/.*/extras/.*\.(jpeg|jpeg_small|tiff)', re.I, ('Preview image',                 'BROWSE'  )),
    (r'volumes/.*/COISS_0011/document/.*/[0-9]+\.[0-9]+(|/)', re.I, ('Calibration report',            'INFODIR' )),
    (r'volumes/.*/data(|/\w*)',                               re.I, ('Images grouped by SC clock',    'IMAGEDIR')),

    (r'calibrated/.*_calib\.img',                             re.I, ('Calibrated image, VICAR',       'IMAGE'   )),
    (r'calibrated/.*/data(|/\w+)',                            re.I, ('Calibrated images by SC clock', 'IMAGEDIR')),
    (r'calibrated/\w+(|/\w+)',                                re.I, ('Calibrated image collection',   'IMAGEDIR')),

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
    (r'volumes/(.*/data/\w+/.*)\.(\w+)',  0, (r'previews/\1_thumb.*',
                                              r'previews/\1_small.*',
                                              r'previews/\1_med.*',
                                              r'previews/\1_full.*')),
    (r'calibrated/(COISS_....)(|_.*?)/(\w+/data/\w+/.*)_CALIB\.(\w+)', 0, (r'previews/\1/\3_thumb.*',
                                                                           r'previews/\1/\3_small.*',
                                                                           r'previews/\1/\3_med.*',
                                                                           r'previews/\1/\3_full.*')),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'previews/(.*)_(\w+\..*)',     0, r'volumes/\1.*'),
    (r'previews/(\w+/\w+/data/\w+)', 0, r'volumes/\1'),
    (r'previews/(\w+/\w+/data)',     0, r'volumes/\1'),
    (r'calibrated/(COISS_....)(|_.*?)/(\w+/data/\w+/\w+)_(CALIB\..*)', 0, r'volumes/\1/\3.*'),
    (r'calibrated/(COISS_....)(|_.*?)/(\w+/data/\w+)',                 0, r'volumes/\1/\3'),
    (r'calibrated/(COISS_....)(|_.*?)/(\w+/data)',                     0, r'volumes/\1/\3'),
    (r'calibrated/(COISS_....)(|_.*?)/(\w+)',                          0, r'volumes/\1/\3'),
    (r'calibrated/(COISS_....)(|_.*?)',                                0, r'volumes/\1'),
])

volumes_to_calibrated = translator.TranslatorByRegex([
    (r'volumes/(.*)\..*',           0, r'calibrated/\1_CALIB.*'),
    (r'volumes/(\w+/\w+/data)',     0, r'calibrated/\1'),
    (r'volumes/(\w+/\w+/data/\w+)', 0, r'calibrated/\1'),
])

volumes_to_previews = translator.TranslatorByRegex([
    (r'volumes/(.*)\..*',           0, r'previews/\1_*.*'),
    (r'volumes/(\w+/\w+/data)',     0, r'previews/\1'),
    (r'volumes/(\w+/\w+/data/\w+)', 0, r'previews/\1'),
])

volumes_to_volumes = translator.TranslatorByRegex([

    (r'(volumes/.*)/extras/\w+/(\w+)\.(.*)', 0, [r'\1/data/\2.*',
                                                 r'\1/extras/*/\2.*']),
    (r'(volumes/.*)/data/(\w+)\.(.*)',       0,  r'volumes/\1/extras/*/\2.*'),

    (r'(volumes/.*)/extras/\w+/(\w+)',       0, [r'\1/data/\2',
                                                 r'\1/extras/*/\2']),
    (r'(volumes/.*)/data/(\w+)',             0,  r'\1/extras/*/\2'),

    (r'(volumes/.*)/extras(|/\w+)',          0, [r'\1/data', r'\1/extras/*']),
    (r'(volumes/.*)/data',                   0,  r'\1/extras/*'),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews|calibrated)/COISS_[12]xxx(|_.*)/COISS_..../data(|/\w+)',       0, (True, True, True )),
    (r'(volumes|previews|calibrated)/COISS_[12]xxx(|_.*)/COISS_..../extras/\w+(|/\w+)', 0, (True, True, True )),
    (r'volumes/COISS_3xxx(|_.*)/COISS_..../data/(images|maps)',                         0, (True, True, False)),
    (r'volumes/COISS_3xxx(|_.*)/COISS_..../extras/\w+/images',                          0, (True, True, False)),
    (r'previews/COISS_3xxx(|_.*)/COISS_..../data/(images|maps)',                        0, (True, True, False)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'volumes/COISS_0xxx(|_\w+)/COISS_....',                    0, r'volumes/COISS_0xxx\1/*'),
    (r'volumes/COISS_0xxx(|_\w+)/COISS_..../data',               0, r'volumes/COISS_0xxx\1/*/data'),
    (r'volumes/COISS_0xxx(|_\w+)/COISS_..../data/(\w+)',         0, r'volumes/COISS_0xxx\1/*/data/\2'),
    (r'volumes/COISS_0xxx(|_\w+)/COISS_..../data/(\w+/\w+)',     0, r'volumes/COISS_0xxx\1/*/data/\2'),
    (r'volumes/COISS_0xxx(|_\w+)/COISS_..../data/(\w+/\w+)/\w+', 0, r'volumes/COISS_0xxx\1/*/data/\2/*'),

    (r'(volumes|previews)/COISS_3xxx(|_\w+)/COISS_....',                    0, r'\1/COISS_3xxx\2/*'),
    (r'(volumes|previews)/COISS_3xxx(|_\w+)/COISS_..../data',               0, r'\1/COISS_3xxx\2/*/data'),
    (r'(volumes|previews)/COISS_3xxx(|_\w+)/COISS_..../data/(\w+)',         0, r'\1/COISS_3xxx\2/*/data/\3'),
    (r'(volumes|previews)/COISS_3xxx(|_\w+)/COISS_..../extras',             0, r'\1/COISS_3xxx\2/*/extras'),
    (r'(volumes|previews)/COISS_3xxx(|_\w+)/COISS_..../extras/(\w+)',       0, r'\1/COISS_3xxx\2/*/extras/\3'),
    (r'(volumes|previews)/COISS_3xxx(|_\w+)/COISS_..../extras/(\w+)/\w+',   0, r'\1/COISS_3xxx\2/*/extras/\3/*'),

    (r'(volumes|previews|calibrated)/(COISS_[12]...)(|_.*?)/COISS_....',            0, r'\1/\2\3/*'),
    (r'(volumes|previews|calibrated)/(COISS_[12]...)(|_.*?)/COISS_..../data',       0, r'\1/\2\3/*/data'),
    (r'(volumes|previews|calibrated)/(COISS_[12]...)(|_.*?)/COISS_..../data/(\w+)', 0, r'\1/\2\3/*/data/*'),

    (r'volumes/(COISS_[12]xxx)/COISS_..../extras/(\w+)/\w+', 0, r'volumes/\1/*/extras/\2/*'),
    (r'volumes/(COISS_[12]xxx)/COISS_..../extras/(\w+)',     0, r'volumes/\1/*/extras/\2'),
    (r'volumes/(COISS_[12]xxx)/COISS_..../(\w+)',            0, r'volumes/\1/*/\2'),
])

####################################################################################################################################
# SORT_KEY
####################################################################################################################################

sort_key = translator.TranslatorByRegex([

    # Skips over N or W, placing files into chronological order
    (r'([NW])([0-9]{10}_[0-9]+(?:|_\w+))\.(.*)', 0, r'\2\1\3'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class COISS_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('COISS_[0123]xxx', re.I, 'COISS_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_dict + description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS
    SORT_KEY = sort_key + pdsfile.PdsFile.SORT_KEY
    ASSOCIATIONS_TO_VOLUMES = associations_to_volumes + pdsfile.PdsFile.ASSOCIATIONS_TO_VOLUMES

    VIEWABLES = {'default': default_viewables}

    VOLUMES_TO_ASSOCIATIONS = pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS.copy()
    VOLUMES_TO_ASSOCIATIONS['volumes'] = volumes_to_volumes + pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS['volumes']
    VOLUMES_TO_ASSOCIATIONS['calibrated'] = volumes_to_calibrated + pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS['calibrated']
    VOLUMES_TO_ASSOCIATIONS['previews'] = volumes_to_previews + pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS['previews']

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COISS_xxxx'] = COISS_xxxx

####################################################################################################################################
