####################################################################################################################################
# rules/COCIRS_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

key_from_path = translator.TranslatorByRegex([
    (r'[-a-z]+/COCIRS_([0156])xxx(|_.*)/COCIRS_([0156][0-9]{3})', re.I, r'COCIRS_\1xxx/COCIRS_\3'),
    (r'[-a-z]+/COCIRS_([0156])xxx(|_.*)',                         re.I, r'COCIRS_\1xxx\2'),
])

description_and_icon_by_dict = translator.TranslatorByDict({
    'COCIRS_0xxx'            : ('Cassini CIRS thermal infrared data: raw and calibrated v3.2, map cubes v1.0', 'VOLDIR'),
    'COCIRS_0xxx'            : ('Cassini CIRS thermal infrared data: raw and calibrated v3.2, map cubes v1.0', 'VOLDIR'),
    'COCIRS_0xxx_v1.1'       : ('Cassini CIRS thermal infrared data: raw and calibrated v2.0',                 'VOLDIR'),
    'COCIRS_0xxx_v1'         : ('Cassini CIRS thermal infrared data: raw and calibrated v1.0',                 'VOLDIR'),
    'COCIRS_1xxx'            : ('Cassini CIRS thermal infrared data: raw and calibrated v3.2, map cubes v1.0', 'VOLDIR'),
    'COCIRS_1xxx_v1.1'       : ('Cassini CIRS thermal infrared data: raw and calibrated v2.0',                 'VOLDIR'),
    'COCIRS_1xxx_v1'         : ('Cassini CIRS thermal infrared data: raw and calibrated v1.0',                 'VOLDIR'),
    'COCIRS_5xxx'            : ('Cassini CIRS data, simplified formats, from 2010 calibration',                'VOLDIR'),
    'COCIRS_6xxx'            : ('Cassini CIRS data, simplified formats, from 2010 calibration',                'VOLDIR'),

    'COCIRS_0xxx/COCIRS_0010': ('Cassini CIRS data 2000-10-01 to 2000-10-31 (SC clock 1349064638-1351714314)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0011': ('Cassini CIRS data 2000-11-01 to 2000-11-30 (SC clock 1351743050-1354306315)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0012': ('Cassini CIRS data 2000-12-01 to 2000-12-31 (SC clock 1354334762-1356984721)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0101': ('Cassini CIRS data 2001-01-01 to 2001-01-31 (SC clock 1357013457-1359648735)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0102': ('Cassini CIRS data 2001-02-01 to 2001-02-28 (SC clock 1359706270-1362082363)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0103': ('Cassini CIRS data 2001-03-01 to 2001-03-22 (SC clock 1362111099-1363925596)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0104': ('Cassini CIRS data 2001-04-24 to 2001-04-29 (SC clock 1366820224-1367252537)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0107': ('Cassini CIRS data 2001-07-09 to 2001-07-11 (SC clock 1373343157-1373573621)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0110': ('Cassini CIRS data 2001-10-28 to 2001-10-31 (SC clock 1382933621-1383207317)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0201': ('Cassini CIRS data 2002-01-15 to 2002-01-20 (SC clock 1389788405-1390176949)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0205': ('Cassini CIRS data 2002-05-09 to 2002-05-28 (SC clock 1399608757-1401308221)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0207': ('Cassini CIRS data 2002-07-11 to 2002-07-31 (SC clock 1405066613-1406837877)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0209': ('Cassini CIRS data 2002-09-01 to 2002-10-06 (SC clock 1409545013-1412554693)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0210': ('Cassini CIRS data 2002-10-01 to 2002-10-30 (SC clock 1412194677-1414671540)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0301': ('Cassini CIRS data 2003-01-22 to 2003-01-25 (SC clock 1421929140-1422174005)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0304': ('Cassini CIRS data 2003-04-16 to 2003-04-30 (SC clock 1429229951-1430425215)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0306': ('Cassini CIRS data 2003-06-01 to 2003-06-29 (SC clock 1433132412-1435537339)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0401': ('Cassini CIRS Saturn data 2004-01-11 to 2004-01-31 (SC clock 1452486011-1454271804)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0402': ('Cassini CIRS Saturn data 2004-02-01 to 2004-02-29 (SC clock 1454300539-1456777404)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0403': ('Cassini CIRS Saturn data 2004-03-04 to 2004-03-31 (SC clock 1457137346-1459455804)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0404': ('Cassini CIRS Saturn data 2004-04-01 to 2004-04-30 (SC clock 1459482364-1462047867)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0405': ('Cassini CIRS Saturn data 2004-05-01 to 2004-05-31 (SC clock 1462076604-1464726286)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0406': ('Cassini CIRS Saturn data 2004-06-01 to 2004-06-30 (SC clock 1464755004-1467318268)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0407': ('Cassini CIRS Saturn data 2004-07-01 to 2004-07-31 (SC clock 1467347004-1469996732)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0408': ('Cassini CIRS Saturn data 2004-08-01 to 2004-08-31 (SC clock 1470018313-1472675132)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0409': ('Cassini CIRS Saturn data 2004-09-01 to 2004-09-30 (SC clock 1472690548-1475267132)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0410': ('Cassini CIRS Saturn data 2004-10-01 to 2004-10-31 (SC clock 1475295868-1477945532)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0411': ('Cassini CIRS Saturn data 2004-11-01 to 2004-11-30 (SC clock 1477974267-1480537596)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0412': ('Cassini CIRS Saturn data 2004-12-01 to 2004-12-31 (SC clock 1480566331-1483215996)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0501': ('Cassini CIRS Saturn data 2005-01-01 to 2005-01-31 (SC clock 1483244732-1485894377)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0502': ('Cassini CIRS Saturn data 2005-02-01 to 2005-02-28 (SC clock 1485923013-1488326525)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0503': ('Cassini CIRS Saturn data 2005-03-01 to 2005-03-31 (SC clock 1488342376-1490992041)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0504': ('Cassini CIRS Saturn data 2005-04-01 to 2005-04-30 (SC clock 1491020777-1493584041)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0505': ('Cassini CIRS Saturn data 2005-05-01 to 2005-05-31 (SC clock 1493605569-1496262504)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0506': ('Cassini CIRS Saturn data 2005-06-01 to 2005-06-30 (SC clock 1496291241-1498854504)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0507': ('Cassini CIRS Saturn data 2005-07-01 to 2005-07-31 (SC clock 1498883241-1501532904)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0508': ('Cassini CIRS Saturn data 2005-08-01 to 2005-08-31 (SC clock 1501556781-1504211311)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0509': ('Cassini CIRS Saturn data 2005-09-01 to 2005-09-30 (SC clock 1504240041-1506803311)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0510': ('Cassini CIRS Saturn data 2005-10-01 to 2005-10-31 (SC clock 1506829289-1509481769)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0511': ('Cassini CIRS Saturn data 2005-11-01 to 2005-11-30 (SC clock 1509510505-1512073769)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0512': ('Cassini CIRS Saturn data 2005-12-01 to 2005-12-31 (SC clock 1512102505-1514752169)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0601': ('Cassini CIRS Saturn data 2006-01-01 to 2006-01-31 (SC clock 1514780905-1517430632)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0602': ('Cassini CIRS Saturn data 2006-02-01 to 2006-02-28 (SC clock 1517450044-1519849833)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0603': ('Cassini CIRS Saturn data 2006-03-01 to 2006-03-31 (SC clock 1519878568-1522528232)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0604': ('Cassini CIRS Saturn data 2006-04-01 to 2006-04-30 (SC clock 1522556969-1525120238)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0605': ('Cassini CIRS Saturn data 2006-05-01 to 2006-05-31 (SC clock 1525148969-1527798696)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0606': ('Cassini CIRS Saturn data 2006-06-01 to 2006-06-30 (SC clock 1527827415-1530390696)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0607': ('Cassini CIRS Saturn data 2006-07-01 to 2006-07-31 (SC clock 1530419433-1533069123)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0608': ('Cassini CIRS Saturn data 2006-08-01 to 2006-08-31 (SC clock 1533097833-1535758297)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0609': ('Cassini CIRS Saturn data 2006-09-01 to 2006-09-30 (SC clock 1535776233-1538339561)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0610': ('Cassini CIRS Saturn data 2006-10-01 to 2006-10-31 (SC clock 1538368296-1541017961)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0611': ('Cassini CIRS Saturn data 2006-11-01 to 2006-11-30 (SC clock 1541046697-1543609961)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0612': ('Cassini CIRS Saturn data 2006-12-01 to 2006-12-31 (SC clock 1543638696-1546288425)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0701': ('Cassini CIRS Saturn data 2007-01-01 to 2007-01-31 (SC clock 1546317159-1548966825)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0702': ('Cassini CIRS Saturn data 2007-02-01 to 2007-02-28 (SC clock 1548995560-1551386025)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0703': ('Cassini CIRS Saturn data 2007-03-01 to 2007-03-31 (SC clock 1551414760-1554064425)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0704': ('Cassini CIRS Saturn data 2007-04-01 to 2007-04-30 (SC clock 1554093160-1556656489)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0705': ('Cassini CIRS Saturn data 2007-05-01 to 2007-05-31 (SC clock 1556685224-1559334888)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0706': ('Cassini CIRS Saturn data 2007-06-01 to 2007-06-30 (SC clock 1559363625-1561926888)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0707': ('Cassini CIRS Saturn data 2007-07-01 to 2007-07-31 (SC clock 1561950118-1564605292)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0708': ('Cassini CIRS Saturn data 2007-08-01 to 2007-08-31 (SC clock 1564634025-1567283753)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0709': ('Cassini CIRS Saturn data 2007-09-01 to 2007-09-30 (SC clock 1567310761-1569875773)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0710': ('Cassini CIRS Saturn data 2007-10-01 to 2007-10-31 (SC clock 1569904509-1572554189)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0711': ('Cassini CIRS Saturn data 2007-11-01 to 2007-11-30 (SC clock 1572582925-1575146183)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0712': ('Cassini CIRS Saturn data 2007-12-01 to 2007-12-31 (SC clock 1575174919-1577824583)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0801': ('Cassini CIRS Saturn data 2008-01-01 to 2008-01-31 (SC clock 1577853319-1580503047)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0802': ('Cassini CIRS Saturn data 2008-02-01 to 2008-02-29 (SC clock 1580527176-1583008647)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0803': ('Cassini CIRS Saturn data 2008-03-01 to 2008-03-31 (SC clock 1583037382-1585687046)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0804': ('Cassini CIRS Saturn data 2008-04-01 to 2008-04-30 (SC clock 1585715783-1588279047)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0805': ('Cassini CIRS Saturn data 2008-05-01 to 2008-05-31 (SC clock 1588307783-1590957510)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0806': ('Cassini CIRS Saturn data 2008-06-01 to 2008-06-30 (SC clock 1590984535-1593549511)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0807': ('Cassini CIRS Saturn data 2008-07-01 to 2008-07-31 (SC clock 1593578247-1596227910)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0808': ('Cassini CIRS Saturn data 2008-08-01 to 2008-08-31 (SC clock 1596256647-1598906375)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0809': ('Cassini CIRS Saturn data 2008-09-01 to 2008-09-30 (SC clock 1598930253-1601498375)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0810': ('Cassini CIRS Saturn data 2008-10-01 to 2008-10-31 (SC clock 1601527111-1604176775)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0811': ('Cassini CIRS Saturn data 2008-11-01 to 2008-11-30 (SC clock 1604191983-1606768776)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0812': ('Cassini CIRS Saturn data 2008-12-01 to 2008-12-31 (SC clock 1606797511-1609447239)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0901': ('Cassini CIRS Saturn data 2009-01-01 to 2009-01-31 (SC clock 1609475975-1612125639)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0902': ('Cassini CIRS Saturn data 2009-02-01 to 2009-02-28 (SC clock 1612153543-1614544839)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0903': ('Cassini CIRS Saturn data 2009-03-01 to 2009-03-31 (SC clock 1614573574-1617223303)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0904': ('Cassini CIRS Saturn data 2009-04-01 to 2009-04-30 (SC clock 1617252036-1619815302)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0905': ('Cassini CIRS Saturn data 2009-05-01 to 2009-05-31 (SC clock 1619829671-1622493702)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0906': ('Cassini CIRS Saturn data 2009-06-01 to 2009-06-30 (SC clock 1622522439-1625085766)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0907': ('Cassini CIRS Saturn data 2009-07-01 to 2009-07-31 (SC clock 1625112285-1627764166)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0908': ('Cassini CIRS Saturn data 2009-08-01 to 2009-08-31 (SC clock 1627784159-1630443743)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0909': ('Cassini CIRS Saturn data 2009-09-01 to 2009-09-30 (SC clock 1630471303-1633035641)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0910': ('Cassini CIRS Saturn data 2009-10-01 to 2009-10-31 (SC clock 1633063302-1635713031)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0911': ('Cassini CIRS Saturn data 2009-11-01 to 2009-11-30 (SC clock 1635737807-1638305031)', 'VOLUME'),
    'COCIRS_0xxx/COCIRS_0912': ('Cassini CIRS Saturn data 2009-12-01 to 2009-12-31 (SC clock 1638333705-1640983431)', 'VOLUME'),

    'COCIRS_1xxx/COCIRS_1001': ('Cassini CIRS Saturn data 2010-01-01 to 2010-01-31 (SC clock 1641012167-1643672697)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1002': ('Cassini CIRS Saturn data 2010-02-01 to 2010-02-28 (SC clock 1643690582-1646081095)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1003': ('Cassini CIRS Saturn data 2010-03-01 to 2010-03-31 (SC clock 1646109831-1648759495)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1004': ('Cassini CIRS Saturn data 2010-04-01 to 2010-04-30 (SC clock 1648788231-1651351495)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1005': ('Cassini CIRS Saturn data 2010-05-01 to 2010-05-31 (SC clock 1651380230-1654029958)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1006': ('Cassini CIRS Saturn data 2010-06-01 to 2010-06-30 (SC clock 1654058695-1656621959)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1007': ('Cassini CIRS Saturn data 2010-07-01 to 2010-07-31 (SC clock 1656650694-1659300359)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1008': ('Cassini CIRS Saturn data 2010-08-01 to 2010-08-31 (SC clock 1659329095-1661978823)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1009': ('Cassini CIRS Saturn data 2010-09-01 to 2010-09-30 (SC clock 1662007559-1664570823)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1010': ('Cassini CIRS Saturn data 2010-10-01 to 2010-10-31 (SC clock 1664599559-1667249223)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1011': ('Cassini CIRS Saturn data 2010-11-01 to 2010-11-30 (SC clock 1667277959-1669841236)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1012': ('Cassini CIRS Saturn data 2010-12-01 to 2010-12-31 (SC clock 1669869971-1672519700)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1101': ('Cassini CIRS Saturn data 2011-01-01 to 2011-01-31 (SC clock 1672548403-1675211497)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1102': ('Cassini CIRS Saturn data 2011-02-01 to 2011-02-28 (SC clock 1675226819-1677623691)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1103': ('Cassini CIRS Saturn data 2011-03-01 to 2011-03-31 (SC clock 1677638611-1680295700)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1104': ('Cassini CIRS Saturn data 2011-04-01 to 2011-04-30 (SC clock 1680324436-1682887764)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1105': ('Cassini CIRS Saturn data 2011-05-01 to 2011-05-31 (SC clock 1682916500-1685566164)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1106': ('Cassini CIRS Saturn data 2011-06-01 to 2011-06-30 (SC clock 1685594900-1688158164)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1107': ('Cassini CIRS Saturn data 2011-07-01 to 2011-07-31 (SC clock 1688186899-1690836564)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1108': ('Cassini CIRS Saturn data 2011-08-01 to 2011-08-31 (SC clock 1690862049-1693515027)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1109': ('Cassini CIRS Saturn data 2011-09-01 to 2011-09-30 (SC clock 1693541857-1696107027)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1110': ('Cassini CIRS Saturn data 2011-10-01 to 2011-10-31 (SC clock 1696135764-1698785452)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1111': ('Cassini CIRS Saturn data 2011-11-01 to 2011-11-30 (SC clock 1698812422-1701377427)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1112': ('Cassini CIRS Saturn data 2011-12-01 to 2011-12-31 (SC clock 1701399101-1704055891)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1201': ('Cassini CIRS Saturn data 2012-01-01 to 2012-01-31 (SC clock 1704084628-1706734291)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1202': ('Cassini CIRS Saturn data 2012-02-01 to 2012-02-29 (SC clock 1706763028-1709239892)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1203': ('Cassini CIRS Saturn data 2012-03-01 to 2012-03-31 (SC clock 1709268628-1711920209)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1204': ('Cassini CIRS Saturn data 2012-04-01 to 2012-04-30 (SC clock 1711947027-1714510356)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1205': ('Cassini CIRS Saturn data 2012-05-01 to 2012-05-31 (SC clock 1714539091-1717188755)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1206': ('Cassini CIRS Saturn data 2012-06-01 to 2012-06-30 (SC clock 1717211707-1719786798)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1207': ('Cassini CIRS Saturn data 2012-07-01 to 2012-07-31 (SC clock 1719809490-1722459164)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1208': ('Cassini CIRS Saturn data 2012-08-01 to 2012-08-31 (SC clock 1722487891-1725137618)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1209': ('Cassini CIRS Saturn data 2012-09-01 to 2012-09-30 (SC clock 1725166355-1727737750)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1210': ('Cassini CIRS Saturn data 2012-10-01 to 2012-10-31 (SC clock 1727758354-1730408019)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1211': ('Cassini CIRS Saturn data 2012-11-01 to 2012-11-30 (SC clock 1730436755-1733000082)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1212': ('Cassini CIRS Saturn data 2012-12-01 to 2012-12-31 (SC clock 1733028806-1735678483)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1301': ('Cassini CIRS Saturn data 2013-01-01 to 2013-01-31 (SC clock 1735707219-1738364054)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1302': ('Cassini CIRS Saturn data 2013-02-01 to 2013-02-28 (SC clock 1738385619-1740776091)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1303': ('Cassini CIRS Saturn data 2013-03-01 to 2013-03-31 (SC clock 1740804819-1743454547)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1304': ('Cassini CIRS Saturn data 2013-04-01 to 2013-04-30 (SC clock 1743483283-1746046593)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1305': ('Cassini CIRS Saturn data 2013-05-01 to 2013-05-31 (SC clock 1746075283-1748724962)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1306': ('Cassini CIRS Saturn data 2013-06-01 to 2013-06-30 (SC clock 1748753683-1751316947)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1307': ('Cassini CIRS Saturn data 2013-07-01 to 2013-07-31 (SC clock 1751345682-1753995411)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1308': ('Cassini CIRS Saturn data 2013-08-01 to 2013-08-31 (SC clock 1754024147-1756673810)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1309': ('Cassini CIRS Saturn data 2013-09-01 to 2013-09-30 (SC clock 1756697195-1759276650)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1310': ('Cassini CIRS Saturn data 2013-10-01 to 2013-10-31 (SC clock 1759294528-1761944210)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1311': ('Cassini CIRS Saturn data 2013-11-01 to 2013-11-30 (SC clock 1761972947-1764536275)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1312': ('Cassini CIRS Saturn data 2013-12-01 to 2013-12-31 (SC clock 1764565011-1767214674)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1401': ('Cassini CIRS Saturn data 2014-01-01 to 2014-01-31 (SC clock 1767243411-1769893082)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1402': ('Cassini CIRS Saturn data 2014-02-01 to 2014-02-28 (SC clock 1769921811-1772312305)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1403': ('Cassini CIRS Saturn data 2014-03-01 to 2014-03-31 (SC clock 1772341011-1774990739)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1404': ('Cassini CIRS Saturn data 2014-04-01 to 2014-04-30 (SC clock 1775013635-1777582739)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1405': ('Cassini CIRS Saturn data 2014-05-01 to 2014-05-31 (SC clock 1777611475-1780261139)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1406': ('Cassini CIRS Saturn data 2014-06-01 to 2014-06-30 (SC clock 1780289875-1782853153)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1407': ('Cassini CIRS Saturn data 2014-07-01 to 2014-07-31 (SC clock 1782881874-1785531604)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1408': ('Cassini CIRS Saturn data 2014-08-01 to 2014-08-31 (SC clock 1785560340-1788210003)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1409': ('Cassini CIRS Saturn data 2014-09-01 to 2014-09-30 (SC clock 1788238737-1790802015)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1410': ('Cassini CIRS Saturn data 2014-10-01 to 2014-10-31 (SC clock 1790821709-1793480416)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1411': ('Cassini CIRS Saturn data 2014-11-01 to 2014-11-30 (SC clock 1793509204-1796072468)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1412': ('Cassini CIRS Saturn data 2014-12-01 to 2014-12-31 (SC clock 1796101204-1798750867)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1501': ('Cassini CIRS Saturn data 2015-01-01 to 2015-01-31 (SC clock 1798773290-1801429292)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1502': ('Cassini CIRS Saturn data 2015-02-01 to 2015-02-28 (SC clock 1801445594-1803848531)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1503': ('Cassini CIRS Saturn data 2015-03-01 to 2015-03-31 (SC clock 1803877268-1806530937)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1504': ('Cassini CIRS Saturn data 2015-04-01 to 2015-04-30 (SC clock 1806555668-1809118988)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1505': ('Cassini CIRS Saturn data 2015-05-01 to 2015-05-31 (SC clock 1809147615-1811797332)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1506': ('Cassini CIRS Saturn data 2015-06-01 to 2015-06-30 (SC clock 1811826067-1814389396)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1507': ('Cassini CIRS Saturn data 2015-07-01 to 2015-07-31 (SC clock 1814418098-1817067796)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1508': ('Cassini CIRS Saturn data 2015-08-01 to 2015-08-31 (SC clock 1817091776-1819746196)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1509': ('Cassini CIRS Saturn data 2015-09-01 to 2015-09-30 (SC clock 1819774932-1822338196)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1510': ('Cassini CIRS Saturn data 2015-10-01 to 2015-10-31 (SC clock 1822366931-1825025548)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1511': ('Cassini CIRS Saturn data 2015-11-01 to 2015-11-30 (SC clock 1825045311-1827612116)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1512': ('Cassini CIRS Saturn data 2015-12-01 to 2015-12-31 (SC clock 1827637389-1830287059)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1601': ('Cassini CIRS Saturn data 2016-01-01 to 2016-01-31 (SC clock 1830312163-1832965464)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1602': ('Cassini CIRS Saturn data 2016-02-01 to 2016-02-29 (SC clock 1832994196-1835471124)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1603': ('Cassini CIRS Saturn data 2016-03-01 to 2016-03-31 (SC clock 1835499860-1838149524)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1604': ('Cassini CIRS Saturn data 2016-04-01 to 2016-04-30 (SC clock 1838178260-1840741524)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1605': ('Cassini CIRS Saturn data 2016-05-01 to 2016-05-31 (SC clock 1840764849-1843420828)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1606': ('Cassini CIRS Saturn data 2016-06-01 to 2016-06-30 (SC clock 1843445012-1846011988)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1607': ('Cassini CIRS Saturn data 2016-07-01 to 2016-07-31 (SC clock 1846040724-1848690388)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1608': ('Cassini CIRS Saturn data 2016-08-01 to 2016-08-31 (SC clock 1848714357-1851372378)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1609': ('Cassini CIRS Saturn data 2016-09-01 to 2016-09-30 (SC clock 1851397523-1853960853)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1610': ('Cassini CIRS Saturn data 2016-10-01 to 2016-10-31 (SC clock 1853989587-1856639252)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1611': ('Cassini CIRS Saturn data 2016-11-01 to 2016-11-30 (SC clock 1856667988-1859235608)', 'VOLUME'),
    'COCIRS_1xxx/COCIRS_1612': ('Cassini CIRS Saturn data 2016-12-01 to 2016-12-31 (SC clock 1859259987-1861909652)', 'VOLUME'),

    'COCIRS_5xxx/COCIRS_5401': ('Cassini CIRS data, reformatted, 2004-01-13 to 2004-01-24 (SC clock 1452654168-1453621646)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5402': ('Cassini CIRS data, reformatted, 2004-02-05 to 2004-02-28 (SC clock 1454690839-1456686298)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5403': ('Cassini CIRS data, reformatted, 2004-03-05 to 2004-03-30 (SC clock 1457223224-1459308003)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5404': ('Cassini CIRS data, reformatted, 2004-04-03 to 2004-04-28 (SC clock 1459651372-1461843335)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5405': ('Cassini CIRS data, reformatted, 2004-05-02 to 2004-05-31 (SC clock 1462150328-1464736536)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5406': ('Cassini CIRS data, reformatted, 2004-06-02 to 2004-06-22 (SC clock 1464845254-1466587627)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5407': ('Cassini CIRS data, reformatted, 2004-07-01 to 2004-07-31 (SC clock 1467343959-1470011067)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5408': ('Cassini CIRS data, reformatted, 2004-08-01 to 2004-09-01 (SC clock 1470011079-1472689497)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5409': ('Cassini CIRS data, reformatted, 2004-09-01 to 2004-09-30 (SC clock 1472689497-1475281477)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5410': ('Cassini CIRS data, reformatted, 2004-10-01 to 2004-10-31 (SC clock 1475281513-1477958964)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5411': ('Cassini CIRS data, reformatted, 2004-11-01 to 2004-11-30 (SC clock 1477970759-1480527275)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5412': ('Cassini CIRS data, reformatted, 2004-12-01 to 2004-12-31 (SC clock 1480569376-1483230343)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5501': ('Cassini CIRS data, reformatted, 2005-01-16 to 2005-01-31 (SC clock 1484526403-1485843863)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5502': ('Cassini CIRS data, reformatted, 2005-02-01 to 2005-03-01 (SC clock 1485908811-1488327995)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5503': ('Cassini CIRS data, reformatted, 2005-03-01 to 2005-03-31 (SC clock 1488327995-1491006408)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5504': ('Cassini CIRS data, reformatted, 2005-04-01 to 2005-04-30 (SC clock 1491006413-1493598422)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5505': ('Cassini CIRS data, reformatted, 2005-05-01 to 2005-05-31 (SC clock 1493598431-1496265887)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5506': ('Cassini CIRS data, reformatted, 2005-06-01 to 2005-06-30 (SC clock 1496338079-1498824201)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5507': ('Cassini CIRS data, reformatted, 2005-07-01 to 2005-08-01 (SC clock 1498873995-1501547322)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5508': ('Cassini CIRS data, reformatted, 2005-08-01 to 2005-08-31 (SC clock 1501547322-1504170294)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5509': ('Cassini CIRS data, reformatted, 2005-09-01 to 2005-09-29 (SC clock 1504287829-1506658404)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5510': ('Cassini CIRS data, reformatted, 2005-10-04 to 2005-10-31 (SC clock 1507152907-1509436655)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5511': ('Cassini CIRS data, reformatted, 2005-11-02 to 2005-12-01 (SC clock 1509618562-1512088144)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5512': ('Cassini CIRS data, reformatted, 2005-12-01 to 2005-12-29 (SC clock 1512088149-1514579655)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5601': ('Cassini CIRS data, reformatted, 2006-01-01 to 2006-01-31 (SC clock 1514785645-1517444782)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5602': ('Cassini CIRS data, reformatted, 2006-02-01 to 2006-02-28 (SC clock 1517445033-1519836590)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5603': ('Cassini CIRS data, reformatted, 2006-03-01 to 2006-03-26 (SC clock 1519867806-1522038541)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5604': ('Cassini CIRS data, reformatted, 2006-04-01 to 2006-04-30 (SC clock 1522547543-1525121542)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5605': ('Cassini CIRS data, reformatted, 2006-05-01 to 2006-05-31 (SC clock 1525142949-1527813047)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5606': ('Cassini CIRS data, reformatted, 2006-06-01 to 2006-06-30 (SC clock 1527813047-1530384298)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5607': ('Cassini CIRS data, reformatted, 2006-07-01 to 2006-07-31 (SC clock 1530440593-1533079850)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5608': ('Cassini CIRS data, reformatted, 2006-08-03 to 2006-08-31 (SC clock 1533309695-1535761893)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5609': ('Cassini CIRS data, reformatted, 2006-09-01 to 2006-09-30 (SC clock 1535761913-1538323726)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5610': ('Cassini CIRS data, reformatted, 2006-10-01 to 2006-10-31 (SC clock 1538399829-1541009529)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5611': ('Cassini CIRS data, reformatted, 2006-11-01 to 2006-11-30 (SC clock 1541071761-1543617080)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5612': ('Cassini CIRS data, reformatted, 2006-12-01 to 2006-12-31 (SC clock 1543631563-1546290092)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5701': ('Cassini CIRS data, reformatted, 2007-01-01 to 2007-02-01 (SC clock 1546309979-1548981184)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5702': ('Cassini CIRS data, reformatted, 2007-02-01 to 2007-02-28 (SC clock 1548981184-1551349915)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5703': ('Cassini CIRS data, reformatted, 2007-03-01 to 2007-03-31 (SC clock 1551414267-1554018404)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5704': ('Cassini CIRS data, reformatted, 2007-04-01 to 2007-04-29 (SC clock 1554097510-1556567264)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5705': ('Cassini CIRS data, reformatted, 2007-05-01 to 2007-05-31 (SC clock 1556720346-1559275931)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5706': ('Cassini CIRS data, reformatted, 2007-06-01 to 2007-07-01 (SC clock 1559362523-1561941306)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5707': ('Cassini CIRS data, reformatted, 2007-07-01 to 2007-07-31 (SC clock 1561941307-1564618389)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5708': ('Cassini CIRS data, reformatted, 2007-08-01 to 2007-09-01 (SC clock 1564624490-1567298099)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5709': ('Cassini CIRS data, reformatted, 2007-09-01 to 2007-09-30 (SC clock 1567298111-1569865151)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5710': ('Cassini CIRS data, reformatted, 2007-10-01 to 2007-10-31 (SC clock 1569938819-1572548683)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5711': ('Cassini CIRS data, reformatted, 2007-11-03 to 2007-12-01 (SC clock 1572779144-1575160550)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5712': ('Cassini CIRS data, reformatted, 2007-12-01 to 2007-12-31 (SC clock 1575160562-1577795605)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5801': ('Cassini CIRS data, reformatted, 2008-01-01 to 2008-02-01 (SC clock 1577863464-1580517402)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5802': ('Cassini CIRS data, reformatted, 2008-02-01 to 2008-03-01 (SC clock 1580517402-1583023005)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5803': ('Cassini CIRS data, reformatted, 2008-03-01 to 2008-04-01 (SC clock 1583023006-1585701448)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5804': ('Cassini CIRS data, reformatted, 2008-04-01 to 2008-05-01 (SC clock 1585701448-1588293446)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5805': ('Cassini CIRS data, reformatted, 2008-05-01 to 2008-06-01 (SC clock 1588293446-1590971910)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5806': ('Cassini CIRS data, reformatted, 2008-06-01 to 2008-06-30 (SC clock 1590971910-1593563825)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5807': ('Cassini CIRS data, reformatted, 2008-07-01 to 2008-08-01 (SC clock 1593563891-1596242329)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5808': ('Cassini CIRS data, reformatted, 2008-08-01 to 2008-09-01 (SC clock 1596242329-1598920750)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5809': ('Cassini CIRS data, reformatted, 2008-09-01 to 2008-10-01 (SC clock 1598920750-1601512738)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5810': ('Cassini CIRS data, reformatted, 2008-10-01 to 2008-11-01 (SC clock 1601512737-1604191155)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5811': ('Cassini CIRS data, reformatted, 2008-11-01 to 2008-11-30 (SC clock 1604191155-1606758207)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5812': ('Cassini CIRS data, reformatted, 2008-12-01 to 2008-12-31 (SC clock 1606840544-1609438675)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5901': ('Cassini CIRS data, reformatted, 2009-01-01 to 2009-02-01 (SC clock 1609478409-1612140016)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5902': ('Cassini CIRS data, reformatted, 2009-02-01 to 2009-03-01 (SC clock 1612140016-1614559232)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5903': ('Cassini CIRS data, reformatted, 2009-03-01 to 2009-03-31 (SC clock 1614559231-1617235494)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5904': ('Cassini CIRS data, reformatted, 2009-04-01 to 2009-05-01 (SC clock 1617243364-1619829672)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5905': ('Cassini CIRS data, reformatted, 2009-05-01 to 2009-05-31 (SC clock 1619829672-1622500668)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5906': ('Cassini CIRS data, reformatted, 2009-06-04 to 2009-07-01 (SC clock 1622816619-1625100104)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5907': ('Cassini CIRS data, reformatted, 2009-07-01 to 2009-07-31 (SC clock 1625100109-1627778505)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5908': ('Cassini CIRS data, reformatted, 2009-08-01 to 2009-09-01 (SC clock 1627778555-1630456943)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5909': ('Cassini CIRS data, reformatted, 2009-09-01 to 2009-09-30 (SC clock 1630456943-1633048892)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5910': ('Cassini CIRS data, reformatted, 2009-10-01 to 2009-10-31 (SC clock 1633048964-1635657113)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5911': ('Cassini CIRS data, reformatted, 2009-11-01 to 2009-11-30 (SC clock 1635727690-1638279012)', 'VOLUME'),
    'COCIRS_5xxx/COCIRS_5912': ('Cassini CIRS data, reformatted, 2009-12-01 to 2010-01-01 (SC clock 1638323061-1640997821)', 'VOLUME'),

    'COCIRS_6xxx/COCIRS_6001': ('Cassini CIRS data, reformatted, 2010-01-01 to 2010-02-01 (SC clock 1640997821-1643676237)', 'VOLUME'),
    'COCIRS_6xxx/COCIRS_6002': ('Cassini CIRS data, reformatted, 2010-02-01 to 2010-03-01 (SC clock 1643676242-1646095456)', 'VOLUME'),
    'COCIRS_6xxx/COCIRS_6003': ('Cassini CIRS data, reformatted, 2010-03-01 to 2010-04-01 (SC clock 1646095456-1648773882)', 'VOLUME'),
    'COCIRS_6xxx/COCIRS_6004': ('Cassini CIRS data, reformatted, 2010-04-01 to 2010-04-30 (SC clock 1648773882-1651332653)', 'VOLUME'),
    'COCIRS_6xxx/COCIRS_6005': ('Cassini CIRS data, reformatted, 2010-05-01 to 2010-06-01 (SC clock 1651367874-1654044314)', 'VOLUME'),
    'COCIRS_6xxx/COCIRS_6006': ('Cassini CIRS data, reformatted, 2010-06-01 to 2010-06-30 (SC clock 1654044314-1656588197)', 'VOLUME'),
}, key_from_path)

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*/data/cube',                re.I, ('Derived spectral image cubes', 'CUBEDIR')),
    (r'volumes/.*/data/cube/[^/]',           re.I, ('Image cubes by projection',    'CUBEDIR')),
    (r'volumes/.*/data/tsdr',                re.I, ('Data files',                   'DATADIR')),
    (r'volumes/.*/data/.*apodspec',          re.I, ('Calibrated spectra',           'DATADIR')),
    (r'volumes/.*/data/.*hsk_data',          re.I, ('Housekeeping data',            'DATADIR')),
    (r'volumes/.*/data/.*nav_data',          re.I, ('Geometry data',                'GEOMDIR')),
    (r'volumes/.*/data/.*uncalibr',          re.I, ('Uncalibrated data',            'DATADIR')),
    (r'volumes/.*/extras/cube_overview/\w+', re.I, ('Browse image collection',      'BROWDIR')),
    (r'volumes/COCIRS_[56].*\.png',          re.I, ('Browse diagram',               'DIAGRAM' )),
    (r'diagrams/COCIRS_[56].*\.png',         re.I, ('Observation diagram',          'DIAGRAM' )),
    (r'volumes/COCIRS_[56].*/BROWSE',        re.I, ('Observation diagrams',         'DIAGDIR' )),
    (r'diagrams/COCIRS_[56].*/BROWSE',       re.I, ('Observation diagrams',         'DIAGDIR' )),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    # COCIRS_[56]xxx, diagrams to volumes
    (r'diagrams/(COCIRS_[56].*)/BROWSE',                                0, [r'volumes/\1/BROWSE',
                                                                            r'volumes/\1/DATA']),
    (r'diagrams/(COCIRS_[56].*)/BROWSE/(\w+)',                          0, [r'volumes/\1/BROWSE/\2',
                                                                            r'volumes/\1/DATA']),
    (r'diagrams/(COCIRS_[56].*)/BROWSE/(\w+/\w+)_\w+\.jpg',             0,  r'volumes/\1/BROWSE/\2.*'),

    (r'diagrams/(COCIRS_[56].*)/BROWSE/\w+/RIN(\w+)_(FP.)\..*',         0, [r'volumes/\1/DATA/*/RIN\2_\3.*',
                                                                            r'volumes/\1/DATA/*/ISPM\2_\3.*',
                                                                            r'volumes/\1/DATA/*/SPEC\2_\3.*',
                                                                            r'volumes/\1/DATA/*/TAR\2_\3.*',
                                                                            r'volumes/\1/DATA/*/GEO\2_699.*']),

    (r'diagrams/(COCIRS_[56].*)/BROWSE/\w+/POI(\w+)_(FP.)_(6..)\..*',   0, [r'volumes/\1/DATA/*/GEO\2_\4.*',
                                                                            r'volumes/\1/DATA/*/ISPM\2_\3.*',
                                                                            r'volumes/\1/DATA/*/SPEC\2_\3.*',
                                                                            r'volumes/\1/DATA/*/TAR\2_\3.*',
                                                                            r'volumes/\1/DATA/*/POI\2_\3.*']),

    (r'diagrams/(COCIRS_[56].*)/BROWSE/\w+/IMG(\w+)_(FP.)\..*',         0, [r'volumes/\1/DATA/*/GEO\2_*.*',
                                                                            r'volumes/\1/DATA/*/ISPM\2_\3.*',
                                                                            r'volumes/\1/DATA/*/SPEC\2_\3.*',
                                                                            r'volumes/\1/DATA/*/TAR\2_\3.*',
                                                                            r'volumes/\1/DATA/*/POI\2_\3.*',
                                                                            r'volumes/\1/DATA/*/RIN\2_\3.*']),

    # COCIRS_[01]xxx, previews to volumes
    (r'previews/(COCIRS_[01].*)/DATA/CUBE',                             0, [r'volumes/\1/DATA/CUBE',
                                                                            r'volumes/\1/EXTRAS/CUBE_OVERVIEW']),
    (r'previews/(COCIRS_[01].*)/DATA/CUBE/(\w+)',                       0, [r'volumes/\1/DATA/CUBE/\2',
                                                                            r'volumes/\1/EXTRAS/CUBE_OVERVIEW/\2']),
    (r'previews/(COCIRS_[01].*)/DATA/CUBE/(\w+/\w+)_\w+.jpg',           0, [r'volumes/\1/DATA/CUBE/\2*',
                                                                            r'volumes/\1/EXTRAS/CUBE_OVERVIEW/\2*']),
])

volumes_to_volumes = translator.TranslatorByRegex([

    # COCIRS_[56]xxx, BROWSE directory to DATA directory
    (r'(volumes/COCIRS_[56].*)/BROWSE(|/\w+)',                              0,  r'\1/DATA'),
    (r'(volumes/COCIRS_[56].*)/BROWSE/\w+/[A-Z]+([0-9]+)(_FP.)\..*',        0, [r'\1/DATA/*/*\2\3*',
                                                                                r'\1/DATA/GEODATA/GEO\2*']),
    (r'(volumes/COCIRS_[56].*)/BROWSE/\w+/[A-Z]+([0-9]+)(_FP.)(_6..)\..*',  0, [r'\1/DATA/*/*\2\3*',
                                                                                r'\1/DATA/*/*/GEO\2\4*']),
    # COCIRS_[56]xxx, BROWSE directory to BROWSE directory
    (r'(volumes/COCIRS_[56].*)/BROWSE/\w+/[A-Z]+([0-9]+)(_FP.)(|_6..)\..*', 0, r'\1/BROWSE/*/*\2\3*.*'),

    # COCIRS_[56]xxx, DATA directory to DATA directory
    (r'(volumes/COCIRS_[56].*/DATA/\w+/[A-Z]+[0-9]+)_FP.(.*)',              0, r'\1_FP*'),                      # other focal planes
    (r'(volumes/COCIRS_[56].*/DATA)/\w+/[A-Z]+([0-9]+_FP.).*',              0, [r'\1/*/*\2*',                   # same FP, other file types
                                                                                r'\1/GEODATA/GEO\2_6??.*']),    # related GEO files
    (r'(volumes/COCIRS_[56].*/DATA)/\w+/GEO(\w+)_6.*',                      0, r'\1/*/*\2*.*'),                 # ignore FPs for GEO files

    # COCIRS_[56]xxx, DATA directory to BROWSE directory
    (r'(volumes/COCIRS_[56].*)/DATA(|/\w+)',                                0, r'\1/BROWSE'),
    (r'(volumes/COCIRS_[56].*)/DATA/\w+/[A-Z]+([0-9]+_FP.)\..*',            0, r'\1/BROWSE/*/*\2*'),
    (r'(volumes/COCIRS_[56].*)/DATA/\w+/[A-Z]+([0-9]+)_6..\..*',            0, r'\1/BROWSE/*/*\2*'),

    # COCIRS_[01]xxx, DATA to EXTRAS
    (r'(volumes/COCIRS_[01].*)/DATA/CUBE',                              0,  r'\1/EXTRAS/CUBE_OVERVIEW'),
    (r'(volumes/COCIRS_[01].*)/DATA/CUBE/(\w+)',                        0,  r'\1/EXTRAS/CUBE_OVERVIEW/\2'),
    (r'(volumes/COCIRS_[01].*)/DATA/CUBE/(\w+/\w+)\..*',                0,  r'\1/EXTRAS/CUBE_OVERVIEW/\2*.*'),

    # COCIRS_[01]xxx, EXTRAS to DATA
    (r'(volumes/COCIRS_[01].*)/EXTRAS/CUBE_OVERVIEW',                   0,  r'\1/DATA/CUBE'),
    (r'(volumes/COCIRS_[01].*)/EXTRAS/CUBE_OVERVIEW/(\w+)',             0,  r'\1/DATA/CUBE/\2'),
    (r'(volumes/COCIRS_[01].*)/EXTRAS/CUBE_OVERVIEW/(\w+/\w+)\..*',     0,  r'\1/DATA/CUBE/\2*.*'),
])

volumes_to_previews = translator.TranslatorByRegex([
    (r'volumes/(COCIRS_[01].*)/DATA/CUBE',                              0,  r'previews/\1/DATA/CUBE'),
    (r'volumes/(COCIRS_[01].*)/DATA/CUBE/(\w+)',                        0,  r'previews/\1/DATA/CUBE/\2'),
    (r'volumes/(COCIRS_[01].*)/DATA/CUBE/(\w+/\w+)\..*',                0,  r'previews/\1/DATA/CUBE/\2*.*'),

    (r'volumes/(COCIRS_[01].*)/EXTRAS/CUBE_OVERVIEW',                   0,  r'previews/\1/DATA/CUBE'),
    (r'volumes/(COCIRS_[01].*)/EXTRAS/CUBE_OVERVIEW/(\w+)',             0,  r'previews/\1/DATA/CUBE/\2'),
    (r'volumes/(COCIRS_[01].*)/EXTRAS/CUBE_OVERVIEW/(\w+/\w+)\..*',     0,  r'previews/\1/DATA/CUBE/\2*.*'),
])

volumes_to_diagrams = translator.TranslatorByRegex([
    (r'volumes/(COCIRS_[56].*)/BROWSE',                             0,  r'diagrams/\1/BROWSE'),
    (r'volumes/(COCIRS_[56].*)/BROWSE/(\w+)',                       0,  r'diagrams/\1/BROWSE/\2'),
    (r'volumes/(COCIRS_[56].*)/BROWSE/(.*)\..*',                    0,  r'diagrams/\1/BROWSE/\2*'),

    (r'volumes/(COCIRS_[56].*)/DATA(|\w+)',                         0,  r'diagrams/\1/BROWSE'),
    (r'volumes/(COCIRS_[56].*)/DATA/RINDATA/RIN(\w+).*',            0,  r'diagrams/\1/BROWSE/*/RIN\2*'),
    (r'volumes/(COCIRS_[56].*)/DATA/GEODATA/GEO(\w+)_(6..).*',      0,  r'diagrams/\1/BROWSE/*/POI\2_FP?_\3*'),
    (r'volumes/(COCIRS_[56].*)/DATA/GEODATA/GEO(\w+)_699.*',        0,  r'diagrams/\1/BROWSE/SATURN/POI\2_FP?*'),
    (r'volumes/(COCIRS_[56].*)/DATA/APODSPEC/SPEC(\w+).*',          0,  r'diagrams/\1/BROWSE/*/*\2*'),
    (r'volumes/(COCIRS_[56].*)/DATA/ISPMDATA/ISPM(\w+).*',          0,  r'diagrams/\1/BROWSE/*/*\2*'),
    (r'volumes/(COCIRS_[56].*)/DATA/TARDATA/TAR(\w+).*',            0,  r'diagrams/\1/BROWSE/*/*\2*'),
    (r'volumes/(COCIRS_[56].*)/DATA/POIDATA/POI(\w+).*',            0,  r'diagrams/\1/BROWSE/*/*\2*'),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'volumes/(COCIRS_[01].*)/DATA/CUBE/(\w+/\w+)\.tar\.gz',        0, r'previews/\1/DATA/CUBE/\2_*.jpg'),
    (r'volumes/(COCIRS_[01].*)/EXTRAS/CUBE_OVERVIEW/(\w+/\w+)\.JPG', 0, r'previews/\1/DATA/CUBE/\2_*.jpg'),

    (r'volumes/(COCIRS_[56].*)/BROWSE/(.*)_\w+\..*',                0,  r'diagrams/\1/BROWSE/\2*.jpg'),
    (r'volumes/(COCIRS_[56].*)/DATA/RINDATA/RIN(\w+)\..*',          0, (r'diagrams/\1/BROWSE/S_RINGS/RIN\2_*.jpg',
                                                                        r'diagrams/\1/BROWSE/TARGETS/IMG\2_*.jpg')),
    (r'volumes/(COCIRS_[56].*)/DATA/GEODATA/GEO(\w+)_(6..)\..*',    0, (r'diagrams/\1/BROWSE/*/POI\2_FP?_\3_*.jpg',
                                                                        r'diagrams/\1/BROWSE/TARGETS/IMG\2_FP?_*.jpg')),
    (r'volumes/(COCIRS_[56].*)/DATA/POIDATA/POI(\w+)\..*',          0, r'diagrams/\1/BROWSE/TARGETS/IMG\2_*.jpg'),
    (r'volumes/(COCIRS_[56].*)/DATA/APODSPEC/SPEC(\w+)\..*',        0, r'diagrams/\1/BROWSE/TARGETS/IMG\2_*.jpg'),
    (r'volumes/(COCIRS_[56].*)/DATA/ISPMDATA/ISPM(\w+)\..*',        0, r'diagrams/\1/BROWSE/TARGETS/IMG\2_*.jpg'),
    (r'volumes/(COCIRS_[56].*)/DATA/TARDATA/TAR(\w+)\..*',          0, r'diagrams/\1/BROWSE/TARGETS/IMG\2_*.jpg'),
])

s_rings_viewables = translator.TranslatorByRegex([
    (r'volumes/(COCIRS_[56].*)/DATA/\w+/(SPEC|ISPM|TAR)(\w+)\..*',  0, r'diagrams/\1/BROWSE/S_RINGS/RIN\2_*.jpg'),
    (r'volumes/(COCIRS_[56].*)/DATA/\w+/GEO(\w+)_699\..*',          0, r'diagrams/\1/BROWSE/S_RINGS/RIN\2_*.jpg'),
])

saturn_viewables = translator.TranslatorByRegex([
    (r'volumes/(COCIRS_[56].*)/DATA/\w+/(SPEC|ISPM|TAR|POI)(\w+)\..*', 0, r'diagrams/\1/BROWSE/SATURN/POI\2_*.jpg'),
    (r'volumes/(COCIRS_[56].*)/DATA/\w+/GEO(\w+)_699\..*',             0, r'diagrams/\1/BROWSE/SATURN/POI\2_*.jpg'),
])

spice_lookup = {
    601: 'Mimas',
    602: 'Enceladus',
    603: 'Tethys',
    604: 'Dione',
    605: 'Rhea',
    606: 'Titan',
    607: 'Hyperion',
    608: 'Iapetus',
    609: 'Phoebe',
    610: 'Janus',
    611: 'Epimetheus',
    612: 'Helene',
    613: 'Telesto',
    614: 'Calypso',
    615: 'Atlas',
    616: 'Prometheus',
    617: 'Pandora',
    618: 'Pan',
}

viewables = {}
for (id, name) in spice_lookup.iteritems():
    viewables[name] = translator.TranslatorByRegex([
        (r'volumes/(COCIRS_[56].*)/DATA/\w+/(SPEC|ISPM|TAR|POI)(\w+)\..*', 0, (r'diagrams/\1/BROWSE/*/POI\2_%3d_*.jpg' % id,)),
        (r'volumes/(COCIRS_[56].*)/DATA/\w+/GEO(\w+)_%3d\..*' % id,        0, (r'diagrams/\1/BROWSE/*/POI\2_%3d_*.jpg' % id,)),
])

viewables['default'] = default_viewables
viewables['Rings'] = s_rings_viewables
viewables['Saturn'] = saturn_viewables

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews)/COCIRS_[01]xxx(|_.*)/\w+/DATA/CUBE/(|\w+)',         0, (True, True, True )),
    (r'volumes/COCIRS_[01]xxx(|_.*)/COCIRS_..../EXTRAS/CUBE_OVERVIEW/(|\w+)', 0, (True, True, True )),

    (r'(volumes|diagrams)/COCIRS_[56]xxx/\w+/DATA/\w+(|/\w+)',                0, (True, True, True )),
    (r'(volumes|diagrams)/COCIRS_[56]xxx/\w+/BROWSE/\w+(|/\w+)',              0, (True, True, True )),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'(volumes|diagrams)/COCIRS_[56]xxx(|_\w+)/\w+/(DATA|BROWSE)',              0, r'\1/COCIRS_[56]xxx\2/*/\3'),
    (r'(volumes|diagrams)/COCIRS_[56]xxx(|_\w+)/\w+/(DATA|BROWSE)/(\w+)',        0, r'\1/COCIRS_[56]xxx\2/*/\3/\4'),
    (r'(volumes|diagrams)/COCIRS_[56]xxx(|_\w+)/\w+/(DATA|BROWSE)/(\w+)/.*',     0, r'\1/COCIRS_[56]xxx\2/*/\3/\4/*'),

    (r'(volumes|previews)/COCIRS_[01]xxx(|_\w+)/\w+/(DATA|EXTRAS)',              0, r'\1/COCIRS_[01]xxx\2/*/\3'),
    (r'(volumes|previews)/COCIRS_[01]xxx(|_\w+)/\w+/(DATA|EXTRAS)/(\w+)',        0, r'\1/COCIRS_[01]xxx\2/*/\3/\4'),
    (r'(volumes|previews)/COCIRS_[01]xxx(|_\w+)/\w+/(DATA|EXTRAS)/(\w+/\w+)',    0, r'\1/COCIRS_[01]xxx\2/*/\3/\4'),
    (r'(volumes|previews)/COCIRS_[01]xxx(|_\w+)/\w+/(DATA|EXTRAS)/(\w+/\w+)/.*', 0, r'\1/COCIRS_[01]xxx\2/*/\3/\4/*'),
])

####################################################################################################################################
# SPLIT_RULES
####################################################################################################################################

split_rules = translator.TranslatorByRegex([
    (r'(.*)\.tar.gz', 0, (r'\1', '', '.tar.gz')),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class COCIRS_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('COCIRS_[0156]xxx', re.I, 'COCIRS_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    ASSOCIATIONS_TO_VOLUMES = associations_to_volumes + pdsfile.PdsFile.ASSOCIATIONS_TO_VOLUMES
    DESCRIPTION_AND_ICON = description_and_icon_by_dict + description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS
    SPLIT_RULES = split_rules + pdsfile.PdsFile.SPLIT_RULES

    VIEWABLES = viewables

    VOLUMES_TO_ASSOCIATIONS = pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS.copy()
    VOLUMES_TO_ASSOCIATIONS['volumes'] = volumes_to_volumes + pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS['volumes']
    VOLUMES_TO_ASSOCIATIONS['diagrams'] = volumes_to_diagrams + pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS['diagrams']
    VOLUMES_TO_ASSOCIATIONS['previews'] = volumes_to_previews + pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS['previews']

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['COCIRS_xxxx'] = COCIRS_xxxx

####################################################################################################################################

