####################################################################################################################################
# rules/HSTxx_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# DESCRIPTION_AND_ICON
####################################################################################################################################

key_from_path = translator.TranslatorByRegex([
    (r'[-a-z]+/(HST.x_xxxx)(|_.*)/(HST.[01]_[0-9]{4})', re.I, r'\1/\3'),
    (r'[-a-z]+/(HST.x_xxxx)(|_.*)',                     re.I, r'\1\2'),
])

description_and_icon_by_dict = translator.TranslatorByDict({
    'HSTIx_xxxx'           : ('HST WFC3 placeholder volumes for OPUS queries',                     'VOLDIR'),
    'HSTIx_xxxx/HSTI1_1556': ('HST WFC3 images of the Pluto system      2010-04-24 to 2010-09-06', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_1559': ('HST WFC3 images of the Jupiter system    2009-09-22 to 2009-09-23', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_1573': ('HST WFC3 images of the Uranus system     2009-11-11 to 2010-06-04', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_1630': ('HST WFC3 images of Uranus & Neptune      2009-08-29 to 2010-08-28', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_1656': ('HST WFC3 images of the Neptune system    2009-08-19 to 2009-08-19', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_2003': ('HST WFC3 images of the Jupiter system    2009-07-23 to 2009-08-08', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_2045': ('HST WFC3 images of the Jupiter system    2009-11-02 to 2009-11-03', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_2119': ('HST WFC3 images of the Jupiter system    2010-06-07 to 2010-06-07', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_2237': ('HST WFC3 images of TNOs                  2010-08-31 to 2012-03-18', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_2245': ('HST WFC3 images of the Uranus system     2010-09-12 to 2010-11-30', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_2436': ('HST WFC3 images of the Pluto system      2011-06-28 to 2011-07-18', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_2463': ('HST WFC3 images of the Uranus system     2011-12-20 to 2011-12-29', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_2665': ('HST WFC3 images of the Uranus system     2011-10-13 to 2011-12-08', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_2675': ('HST WFC3 images of the Neptune system    2011-06-25 to 2011-07-02', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_2801': ('HST WFC3 images of the Pluto system      2012-06-27 to 2012-07-09', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_2894': ('HST WFC3 images of the Uranus system     2012-09-30 to 2012-09-30', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_3055': ('HST WFC3 images of the Uranus system     2012-10-19 to 2013-09-10', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_3067': ('HST WFC3 images of the Jupiter system    2012-08-14 to 2012-09-20', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_3663': ('HST WFC3 images of KBOs                  2014-10-15 to 2014-10-22', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_3664': ('HST WFC3 images of KBOs                  2014-11-27 to 2015-04-24', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_3667': ('HST WFC3 images of the Pluto system      2015-03-02 to 2015-10-24', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_3668': ('HST WFC3 images of the Eris & Makemake   2015-01-29 to 2015-04-29', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_3692': ('HST WFC3 images of KBOs                  2014-10-05 to 2015-06-02', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_3712': ('HST WFC3 images of the Uranus system     2014-10-14 to 2014-10-14', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_3713': ('HST WFC3 images of the Chariklo          2015-06-07 to 2015-08-13', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_3716': ('HST WFC3 images of KBOs                  2014-10-06 to 2015-06-07', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_3829': ('HST WFC3 images of the Jupiter system    2015-03-11 to 2015-03-15', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_3873': ('HST WFC3 images of Haumea                2014-12-04 to 2015-06-30', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_4042': ('HST WFC3 images of the Jupiter system    2015-01-24 to 2015-01-24', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_4053': ('HST WFC3 images of KBOs                  2015-05-04 to 2015-07-04', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_4064': ('HST WFC3 images of the Saturn system     2015-06-29 to 2015-07-01', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_4334': ('HST WFC3 images of Jupiter & Uranus      2015-09-12 to 2016-02-10', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_4492': ('HST WFC3 images of the Neptune system    2016-05-15 to 2016-05-16', 'VOLUME'),
    'HSTIx_xxxx/HSTI1_4499': ('HST WFC3 images of the Mars system       2016-05-12 to 2016-05-12', 'VOLUME'),

    'HSTJx_xxxx'           : ('HST ACS placeholder volumes for OPUS queries',                      'VOLDIR'),
    'HSTJx_xxxx_v1'        : ('HST ACS placeholder volumes for OPUS queries, superseded releases', 'VOLDIR'),
    'HSTJx_xxxx/HSTJ0_9296': ('HST ACS images of the Jupiter system     2003-12-01 to 2003-12-01', 'VOLUME'),
    'HSTJx_xxxx/HSTJ0_9354': ('HST ACS images of the Saturn system      2003-03-07 to 2004-03-22', 'VOLUME'),
    'HSTJx_xxxx/HSTJ0_9384': ('HST ACS images of the Mars system        2003-01-09 to 2003-06-28', 'VOLUME'),
    'HSTJx_xxxx/HSTJ0_9385': ('HST ACS images of the Saturn system      2002-12-02 to 2002-12-02', 'VOLUME'),
    'HSTJx_xxxx/HSTJ0_9426': ('HST ACS images of the Jupiter system     2002-12-01 to 2003-02-05', 'VOLUME'),
    'HSTJx_xxxx/HSTJ0_9440': ('HST ACS images of the Jupiter system     2003-02-24 to 2004-01-15', 'VOLUME'),
    'HSTJx_xxxx/HSTJ0_9725': ('HST ACS images of the Uranus system      2003-08-30 to 2003-08-30', 'VOLUME'),
    'HSTJx_xxxx/HSTJ0_9745': ('HST ACS images of the Saturn system      2003-12-31 to 2003-12-31', 'VOLUME'),
    'HSTJx_xxxx/HSTJ0_9823': ('HST ACS images of the Uranus system      2003-07-12 to 2004-06-05', 'VOLUME'),
    'HSTJx_xxxx/HSTJ0_9975': ('HST ACS images of the Mars system        2003-08-05 to 2004-02-15', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_0102': ('HST ACS images of the Uranus system      2004-08-20 to 2005-05-29', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_0140': ('HST ACS images of the Jupiter system     2005-01-25 to 2005-05-06', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_0156': ('HST ACS images of the Saturn system      2005-02-17 to 2005-02-17', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_0192': ('HST ACS images of the Jupiter system     2005-01-19 to 2005-01-19', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_0398': ('HST ACS images of the Neptune system     2004-11-06 to 2005-06-26', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_0422': ('HST ACS images of the Neptune system     2005-06-15 to 2005-06-20', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_0423': ('HST ACS images of the Neptune system     2005-04-29 to 2005-04-30', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_0427': ('HST ACS images of the Pluto system       2005-05-15 to 2005-05-18', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_0473': ('HST ACS images of the Uranus system      2005-08-07 to 2006-06-16', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_0502': ('HST ACS images of the Uranus system      2005-08-10 to 2005-08-24', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_0506': ('HST ACS images of the Saturn system      2005-10-26 to 2005-11-02', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_0507': ('HST ACS images of the Jupiter system     2006-02-07 to 2006-04-14', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_0534': ('HST ACS images of Uranus & Neptune       2005-08-27 to 2006-07-23', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_0774': ('HST ACS images of the Pluto system       2006-02-15 to 2006-03-02', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_0782': ('HST ACS images of the Jupiter system     2006-04-16 to 2006-04-25', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_0783': ('HST ACS images of the Jupiter system     2006-04-08 to 2006-04-08', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_0805': ('HST ACS images of the Uranus system      2006-07-25 to 2006-08-24', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_0870': ('HST ACS images of the Uranus system      2006-08-16 to 2006-09-05', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_0871': ('HST ACS images of the Jupiter system     2007-02-25 to 2007-02-27', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_1055': ('HST ACS images of the Saturn system      2007-01-23 to 2007-01-23', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_1085': ('HST ACS images of the Jupiter system     2007-04-18 to 2007-04-18', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_1566': ('HST ACS images of the Saturn system      2009-01-23 to 2009-02-09', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_1970': ('HST ACS images of the Saturn system      2009-01-23 to 2009-02-12', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_1984': ('HST ACS images of the Saturn system      2009-02-17 to 2009-03-07', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_2003': ('HST ACS images of the Jupiter system     2009-09-08 to 2009-09-08', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_2176': ('HST ACS images of the Saturn system      2011-04-01 to 2011-04-09', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_2395': ('HST ACS images of the Saturn system      2011-03-12 to 2011-03-12', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_2601': ('HST ACS images of the Uranus system      2011-11-09 to 2011-11-23', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_2660': ('HST ACS images of the Saturn system      2012-03-28 to 2012-04-06', 'VOLUME'),
    'HSTJx_xxxx/HSTJ1_3012': ('HST ACS images of the Uranus system      2012-09-27 to 2012-09-27', 'VOLUME'),

    'HSTUx_xxxx'           : ('HST WFPC2 placeholder volumes for OPUS queries',                    'VOLDIR'),
    'HSTUx_xxxx/HSTU0_5167': ('HST WFPC2 images of the Jupiter system   1995-04-15 to 1995-04-15', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_5216': ('HST WFPC2 images of the Jupiter system   1994-06-07 to 1994-06-18', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_5217': ('HST WFPC2 images of the Jupiter system   1994-05-19 to 1994-05-31', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_5218': ('HST WFPC2 images of the Jupiter system   1994-05-20 to 1994-05-20', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_5219': ('HST WFPC2 images of the Saturn system    1994-10-09 to 1994-10-09', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_5220': ('HST WFPC2 images of the Uranus system    1994-08-22 to 1994-08-22', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_5221': ('HST WFPC2 images of the Neptune system   1994-06-27 to 1994-10-13', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_5313': ('HST WFPC2 images of the Jupiter system   1995-02-13 to 1995-02-18', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_5321': ('HST WFPC2 images of the Uranus system    1994-08-14 to 1994-08-14', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_5392': ('HST WFPC2 images of the Jupiter system   1994-03-05 to 1994-03-19', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_5508': ('HST WFPC2 images of the Saturn system    1994-10-04 to 1994-10-18', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_5640': ('HST WFPC2 images of the Jupiter system   1994-05-17 to 1994-05-18', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_5642': ('HST WFPC2 images of the Jupiter system   1994-07-15 to 1994-08-25', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_5776': ('HST WFPC2 images of the Saturn system    1994-12-01 to 1994-12-01', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_5782': ('HST WFPC2 images of the Saturn system    1995-05-22 to 1995-05-22', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_5824': ('HST WFPC2 images of the Saturn system    1995-11-21 to 1995-11-22', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_5828': ('HST WFPC2 images of the Jupiter system   1996-06-23 to 1997-07-03', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_5831': ('HST WFPC2 images of the Neptune system   1995-09-01 to 1997-07-05', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_5836': ('HST WFPC2 images of the Saturn system    1995-08-09 to 1995-11-28', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_5837': ('HST WFPC2 images of the Jupiter system   1995-06-26 to 1995-08-19', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6009': ('HST WFPC2 images of the Jupiter system   1995-10-04 to 1996-05-17', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6025': ('HST WFPC2 images of the Jupiter system   1996-04-23 to 1996-04-23', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6028': ('HST WFPC2 images of the Jupiter system   1995-07-03 to 1995-07-08', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6029': ('HST WFPC2 images of the Jupiter system   1995-07-14 to 1995-07-14', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6030': ('HST WFPC2 images of outer planets        1995-07-03 to 1995-11-17', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6141': ('HST WFPC2 images of the Jupiter system   1995-03-03 to 1995-04-07', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6145': ('HST WFPC2 images of the Jupiter system   1995-03-09 to 1995-03-24', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6215': ('HST WFPC2 images of the Saturn system    1995-10-15 to 1995-10-31', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6216': ('HST WFPC2 images of the Saturn system    1995-05-22 to 1995-11-20', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6218': ('HST WFPC2 images of the Jupiter system   1995-07-19 to 1996-08-10', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6219': ('HST WFPC2 images of the Neptune system   1995-09-13 to 1995-09-14', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6295': ('HST WFPC2 images of the Saturn system    1995-09-29 to 1995-10-08', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6315': ('HST WFPC2 images of the Jupiter system   1995-09-26 to 1995-09-26', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6328': ('HST WFPC2 images of the Saturn system    1995-11-18 to 1995-11-18', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6452': ('HST WFPC2 images of the Jupiter system   1996-06-27 to 1997-06-27', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6509': ('HST WFPC2 images of the Jupiter system   1996-06-26 to 1997-06-25', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6648': ('HST WFPC2 images of the Saturn system    1997-09-10 to 1997-09-11', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6650': ('HST WFPC2 images of the Neptune system   1996-08-13 to 1996-08-14', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6662': ('HST WFPC2 images of the Jupiter system   1997-05-05 to 1997-08-09', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6733': ('HST WFPC2 images of the Saturn system    1996-10-17 to 1996-10-29', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6743': ('HST WFPC2 images of the Jupiter system   1996-09-03 to 1997-05-06', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6752': ('HST WFPC2 images of the Jupiter system   1996-07-02 to 1999-10-07', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6753': ('HST WFPC2 images of the Neptune system   1997-07-03 to 1997-07-06', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6774': ('HST WFPC2 images of the Jupiter system   1996-07-24 to 1997-07-22', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6803': ('HST WFPC2 images of the Saturn system    1998-11-01 to 1998-11-01', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6806': ('HST WFPC2 images of the Saturn system    1996-09-30 to 1997-01-10', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6818': ('HST WFPC2 images of the Uranus system    1997-07-31 to 1997-08-01', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6842': ('HST WFPC2 images of the Jupiter system   1996-03-02 to 1996-03-02', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6846': ('HST WFPC2 images of the Neptune system   1996-03-08 to 1996-03-08', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_6853': ('HST WFPC2 images of the Jupiter system   1997-05-17 to 1997-10-25', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_7308': ('HST WFPC2 images of the Jupiter system   1997-07-03 to 1997-09-20', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_7321': ('HST WFPC2 images of the Saturn system    1997-11-04 to 1997-11-04', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_7324': ('HST WFPC2 images of the Neptune system   1998-08-11 to 1998-08-12', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_7427': ('HST WFPC2 images of the Saturn system    1997-09-22 to 1998-10-24', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_7429': ('HST WFPC2 images of the Uranus system    1997-07-07 to 1997-10-16', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_7430': ('HST WFPC2 images of the Jupiter system   1997-09-18 to 1997-11-06', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_7589': ('HST WFPC2 images of the Jupiter system   1997-07-12 to 1997-07-12', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_7616': ('HST WFPC2 images of the Jupiter system   1998-06-03 to 1998-07-16', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_7717': ('HST WFPC2 images of the multiple systems 1998-11-06 to 2000-11-26', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_8148': ('HST WFPC2 images of the Jupiter system   1999-08-11 to 1999-10-14', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_8169': ('HST WFPC2 images of the Jupiter system   1999-07-02 to 1999-10-11', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_8398': ('HST WFPC2 images of the Saturn system    1999-08-25 to 1999-11-07', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_8405': ('HST WFPC2 images of the Jupiter system   1999-06-08 to 1999-06-08', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_8577': ('HST WFPC2 images of the Mars system      2001-01-16 to 2001-09-15', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_8579': ('HST WFPC2 images of the Mars system      2001-05-27 to 2001-05-27', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_8580': ('HST WFPC2 images of the Saturn system    2000-11-16 to 2000-11-23', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_8634': ('HST WFPC2 images of Uranus & Neptune     2000-08-07 to 2001-06-27', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_8660': ('HST WFPC2 images of the Saturn system    2000-08-04 to 2000-12-06', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_8680': ('HST WFPC2 images of the Uranus system    2000-06-16 to 2000-06-18', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_8802': ('HST WFPC2 images of the Saturn system    2001-09-08 to 2002-01-31', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_8871': ('HST WFPC2 images of the Jupiter system   2000-09-02 to 2000-09-02', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_9235': ('HST WFPC2 images of the Uranus system    2001-07-12 to 2001-07-13', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_9256': ('HST WFPC2 images of the Saturn system    2001-09-28 to 2001-09-28', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_9341': ('HST WFPC2 images of the Saturn system    2002-09-21 to 2002-12-17', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_9344': ('HST WFPC2 images of the Uranus system    2002-08-05 to 2002-08-06', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_9354': ('HST WFPC2 images of the Saturn system    2003-03-07 to 2003-03-07', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_9385': ('HST WFPC2 images of the Saturn system    2002-11-27 to 2002-11-27', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_9393': ('HST WFPC2 images of the Neptune system   2002-08-09 to 2002-08-10', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_9725': ('HST WFPC2 images of the Uranus system    2003-08-29 to 2003-08-29', 'VOLUME'),
    'HSTUx_xxxx/HSTU0_9809': ('HST WFPC2 images of the Saturn system    2003-08-25 to 2004-03-30', 'VOLUME'),
    'HSTUx_xxxx/HSTU1_0170': ('HST WFPC2 images of Uranus & Neptune     2004-07-16 to 2005-06-12', 'VOLUME'),
    'HSTUx_xxxx/HSTU1_0357': ('HST WFPC2 images of the Jupiter system   2004-12-20 to 2005-01-14', 'VOLUME'),
    'HSTUx_xxxx/HSTU1_0468': ('HST WFPC2 images of the Jupiter system   2007-04-09 to 2007-05-01', 'VOLUME'),
    'HSTUx_xxxx/HSTU1_0534': ('HST WFPC2 images of Uranus & Neptune     2005-07-22 to 2006-07-02', 'VOLUME'),
    'HSTUx_xxxx/HSTU1_0782': ('HST WFPC2 images of the Jupiter system   2007-03-08 to 2007-05-11', 'VOLUME'),
    'HSTUx_xxxx/HSTU1_0862': ('HST WFPC2 images of the Saturn system    2007-02-09 to 2007-02-11', 'VOLUME'),
    'HSTUx_xxxx/HSTU1_0870': ('HST WFPC2 images of the Uranus system    2007-05-20 to 2007-06-17', 'VOLUME'),
    'HSTUx_xxxx/HSTU1_0871': ('HST WFPC2 images of the Jupiter system   2007-02-14 to 2007-02-28', 'VOLUME'),
    'HSTUx_xxxx/HSTU1_1085': ('HST WFPC2 images of the Jupiter system   2007-03-13 to 2007-05-09', 'VOLUME'),
    'HSTUx_xxxx/HSTU1_1096': ('HST WFPC2 images of the Jupiter system   2007-02-17 to 2007-03-26', 'VOLUME'),
    'HSTUx_xxxx/HSTU1_1102': ('HST WFPC2 images of the Jupiter system   2008-05-09 to 2008-05-10', 'VOLUME'),
    'HSTUx_xxxx/HSTU1_1118': ('HST WFPC2 images of the Uranus system    2007-07-28 to 2007-07-29', 'VOLUME'),
    'HSTUx_xxxx/HSTU1_1156': ('HST WFPC2 images of the multiple systems 2007-08-11 to 2008-09-10', 'VOLUME'),
    'HSTUx_xxxx/HSTU1_1292': ('HST WFPC2 images of the Uranus system    2007-07-04 to 2007-10-01', 'VOLUME'),
    'HSTUx_xxxx/HSTU1_1310': ('HST WFPC2 images of the Jupiter system   2007-06-05 to 2007-06-05', 'VOLUME'),
    'HSTUx_xxxx/HSTU1_1498': ('HST WFPC2 images of the Jupiter system   2008-05-15 to 2008-07-08', 'VOLUME'),
    'HSTUx_xxxx/HSTU1_1956': ('HST WFPC2 images of the Saturn system    2008-11-19 to 2009-05-04', 'VOLUME'),

    'HSTOx_xxxx'           : ('HST STIS placeholder volumes for OPUS queries',                     'VOLDIR'),
    'HSTOx_xxxx/HSTO0_6854': ('HST STIS data for the Saturn system      1997-10-11 to 1997-12-05', 'VOLUME'),
    'HSTOx_xxxx/HSTO0_7308': ('HST STIS data for the Jupiter system     1997-07-03 to 2001-02-01', 'VOLUME'),
    'HSTOx_xxxx/HSTO0_7309': ('HST STIS data for the Jupiter system     1999-01-11 to 1999-01-14', 'VOLUME'),
    'HSTOx_xxxx/HSTO0_7316': ('HST STIS data for the Saturn system      1999-09-12 to 2000-12-05', 'VOLUME'),
    'HSTOx_xxxx/HSTO0_7317': ('HST STIS data for the Jupiter system     1998-11-06 to 2000-10-21', 'VOLUME'),
    'HSTOx_xxxx/HSTO0_7439': ('HST STIS data for the Uranus system      1998-07-29 to 1998-09-15', 'VOLUME'),
    'HSTOx_xxxx/HSTO0_7444': ('HST STIS data for the Jupiter system     1999-08-27 to 1999-09-23', 'VOLUME'),
    'HSTOx_xxxx/HSTO0_7583': ('HST STIS data for the Jupiter system     1998-08-21 to 1998-08-27', 'VOLUME'),
    'HSTOx_xxxx/HSTO0_7769': ('HST STIS data for the Jupiter system     1999-08-14 to 1999-08-16', 'VOLUME'),
    'HSTOx_xxxx/HSTO0_7939': ('HST STIS data for the Jupiter system     1998-10-30 to 1998-10-30', 'VOLUME'),
    'HSTOx_xxxx/HSTO0_8108': ('HST STIS data for the Jupiter system     1999-11-11 to 2001-01-26', 'VOLUME'),
    'HSTOx_xxxx/HSTO0_8158': ('HST STIS data for the Saturn system      2000-12-07 to 2000-12-08', 'VOLUME'),
    'HSTOx_xxxx/HSTO0_8169': ('HST STIS data for the Jupiter system     1999-07-02 to 2000-12-19', 'VOLUME'),
    'HSTOx_xxxx/HSTO0_8171': ('HST STIS data for the Jupiter system     1999-08-08 to 2000-11-14', 'VOLUME'),
    'HSTOx_xxxx/HSTO0_8224': ('HST STIS data for the Jupiter system     1999-10-05 to 2000-12-23', 'VOLUME'),
    'HSTOx_xxxx/HSTO0_8661': ('HST STIS data for Jupiter & Uranus       2000-11-27 to 2000-12-08', 'VOLUME'),
    'HSTOx_xxxx/HSTO0_9035': ('HST STIS data for the Uranus system      2002-08-19 to 2002-08-19', 'VOLUME'),
    'HSTOx_xxxx/HSTO0_9119': ('HST STIS data for Jupiter & Saturn       2001-11-04 to 2001-12-31', 'VOLUME'),
    'HSTOx_xxxx/HSTO0_9440': ('HST STIS data for the Jupiter system     2003-02-24 to 2004-01-15', 'VOLUME'),
    'HSTOx_xxxx/HSTO0_9685': ('HST STIS data for the Jupiter system     2003-02-24 to 2003-02-26', 'VOLUME'),
    'HSTOx_xxxx/HSTO1_0083': ('HST STIS data for the Saturn system      2004-01-08 to 2004-01-30', 'VOLUME'),
    'HSTOx_xxxx/HSTO1_2239': ('HST STIS data for the Uranus system      2011-08-31 to 2011-09-02', 'VOLUME'),
    'HSTOx_xxxx/HSTO1_2478': ('HST STIS data for the Saturn system      2012-04-28 to 2012-05-29', 'VOLUME'),
    'HSTOx_xxxx/HSTO1_2883': ('HST STIS data for the Jupiter system     2012-11-14 to 2014-01-24', 'VOLUME'),
    'HSTOx_xxxx/HSTO1_2894': ('HST STIS data for the Uranus system      2012-09-27 to 2012-09-28', 'VOLUME'),
    'HSTOx_xxxx/HSTO1_3012': ('HST STIS data for the Uranus system      2012-09-26 to 2012-10-28', 'VOLUME'),
    'HSTOx_xxxx/HSTO1_3679': ('HST STIS data for the Jupiter system     2014-11-07 to 2015-04-14', 'VOLUME'),
    'HSTOx_xxxx/HSTO1_3694': ('HST STIS data for the Saturn system      2015-04-18 to 2015-07-10', 'VOLUME'),
    'HSTOx_xxxx/HSTO1_3736': ('HST STIS data for the Pluto system       2015-06-11 to 2015-06-12', 'VOLUME'),
    'HSTOx_xxxx/HSTO1_3805': ('HST STIS data for the Jupiter system     2015-02-21 to 2015-03-11', 'VOLUME'),
    'HSTOx_xxxx/HSTO1_3829': ('HST STIS data for the Jupiter system     2014-12-28 to 2015-03-06', 'VOLUME'),

}, key_from_path)

description_and_icon_by_regex = translator.TranslatorByRegex([
    (r'volumes/.*/data/visit_..',                    re.I, ('Images grouped by visit',              'IMAGEDIR')),
    (r'volumes/.*/data/visit.*/.*\.TIF',             re.I, ('16-bit unscaled TIFF of raw image',    'IMAGE')   ),
    (r'volumes/.*/data/visit.*/.*DRZ\.JPG',          re.I, ('Preview of "drizzled" image',          'IMAGE')   ),
    (r'volumes/.*/data/visit.*/.*_(D0M|RAW).*\.JPG', re.I, ('Preview of raw image',                 'IMAGE')   ),
    (r'volumes/.*/data/visit.*/.*_X1D.*\.JPG',       re.I, ('Line plot of spectrum',                'DATA')    ),
    (r'volumes/.*/data/visit.*/.*_X2D.*\.JPG',       re.I, ('Preview of 2-D image',                 'IMAGE')   ),
    (r'volumes/.*/data/visit.*/.*_FLT.*\.JPG',       re.I, ('Preview of calibrated image',          'IMAGE')   ),
    (r'volumes/.*/data/visit.*/.*\.ASC',             re.I, ('Listing of FITS label info',           'INFO')    ),
    (r'volumes/.*/data/visit.*/.*\.LBL',             re.I, ('PDS label with download instructions', 'LABEL')   ),
])

####################################################################################################################################
# SPLIT_RULES
####################################################################################################################################

split_rules = translator.TranslatorByRegex([
    (r'([IJUO]\w{8})(|_\w+)\.(.*)', 0, (r'\1', r'\2', r'.\3')),
])

####################################################################################################################################
# ASSOCIATIONS
####################################################################################################################################

associations_to_volumes = translator.TranslatorByRegex([
    (r'previews/(.*)_(thumb|small|med|full)\.jpg', 0, r'volumes/\1_*.*'),
])

volumes_to_previews = translator.TranslatorByRegex([
    (r'volumes/(.*/DATA/VISIT_..)/([IJUO]\w{8})(|_\w+)\.(.*)', 0, [r'previews/\1/\2_thumb.jpg',
                                                                   r'previews/\1/\2_small.jpg',
                                                                   r'previews/\1/\2_med.jpg',
                                                                   r'previews/\1/\2_full.jpg']),
])

####################################################################################################################################
# VIEWABLES
####################################################################################################################################

default_viewables = translator.TranslatorByRegex([
    (r'volumes/(.*/DATA/VISIT_..)/([IJUO]\w{8})(|_\w+)\.(.*)', 0, (r'previews/\1/\2_thumb.jpg',
                                                                   r'previews/\1/\2_small.jpg',
                                                                   r'previews/\1/\2_med.jpg',
                                                                   r'previews/\1/\2_full.jpg')),
])

####################################################################################################################################
# VIEW_OPTIONS (grid_view_allowed, multipage_view_allowed, continuous_view_allowed)
####################################################################################################################################

view_options = translator.TranslatorByRegex([
    (r'(volumes|previews)/HST.x_xxxx/HST.._..../DATA(|/VISIT_..)', 0, (True, True, True)),
])

####################################################################################################################################
# NEIGHBORS
####################################################################################################################################

neighbors = translator.TranslatorByRegex([
    (r'(volumes|previews)/(HST.x_xxxx/HST.._..../DATA)',            re.I, r'\1/\2'),
    (r'(volumes|previews)/(HST.x_xxxx/HST.._..../DATA)/(VISIT_..)', re.I, r'\1/\2/*'),
])

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class HSTxx_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('HST.x_xxxx', re.I, 'HSTxx_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

    DESCRIPTION_AND_ICON = description_and_icon_by_dict + description_and_icon_by_regex + pdsfile.PdsFile.DESCRIPTION_AND_ICON
    SPLIT_RULES = split_rules + pdsfile.PdsFile.SPLIT_RULES
    VIEW_OPTIONS = view_options + pdsfile.PdsFile.VIEW_OPTIONS
    NEIGHBORS = neighbors + pdsfile.PdsFile.NEIGHBORS
    ASSOCIATIONS_TO_VOLUMES = associations_to_volumes + pdsfile.PdsFile.ASSOCIATIONS_TO_VOLUMES

    VOLUMES_TO_ASSOCIATIONS = pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS.copy()
    VOLUMES_TO_ASSOCIATIONS['previews'] = volumes_to_previews + pdsfile.PdsFile.VOLUMES_TO_ASSOCIATIONS['previews']

    VIEWABLES = {'default': default_viewables}

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['HSTxx_xxxx'] = HSTxx_xxxx

####################################################################################################################################
