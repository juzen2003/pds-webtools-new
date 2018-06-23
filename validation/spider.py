#!/usr/bin/env python
################################################################################
# Program spider.py
#
# Syntax:
#   spider.py [options] server volume_path [volume_path...]
#
# Example:
#   spider.py pds-rings.seti.org COISS_2xxx/COISS_2101 ASTROM_xxxx
#
# Use option --help for more information.
#
# The log file for each path is named spider_yyyy-mm-dd_volset[-volname].log.
# An additional log file called spider_ERRORS.og only logs errors.
#
# MRS, September 2017
################################################################################

import sys, os
import random
import pickle
import datetime
import re
import argparse

from bs4 import BeautifulSoup
import urllib2
import pycurl
from StringIO import StringIO

import pdsfile
import pdslogger

LOGNAME = 'pds.viewmaster.spider'
LOGROOT_ENV = 'PDS_LOG_ROOT'

################################################################################
# Internal functions
################################################################################

def curl_url(url):
    """Return the content of the URL as a text string."""

    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.FOLLOWLOCATION, True)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    return buffer.getvalue()

def get_viewmaster_hrefs(url):
    """Return a list of all the hrefs in the results of submitting this query to
    viewmaster."""

    html = curl_url(url)

    if '404 Not Found' in html:
        return None
    if 'encountered an internal error' in html:
        return None

    soup = BeautifulSoup(html, 'lxml')
    href_tags = soup.find_all(href=True)

    # A directory should have hrefs
    if '.' not in url[-8:] and len(href_tags) == 0:
        return None

    viewmaster_hrefs = []
    for tag in href_tags:
        href = tag.attrs['href']
        parts = href.split('viewmaster/')
        if len(parts) == 2:
            viewmaster_hrefs.append(parts[1])

    return viewmaster_hrefs

def random_tree_search(viewmaster_, start, regex, logger, handler=None,
                                    limit=1000):
    """Recursively check every link in a tree of Viewmaster.

    Input:
        viewmaster_ URL of the server, 'http' to '/viewmaster/'.
        start       staring query, e.g., "COISS_2xxx/COISS_2101"
        regex       a regular expression to filter the links checked, preventing
                    the spidering of the entire tree. For example, the pattern
                    "COISS_2xxx/COISS_2101" will only check links from pages
                    inside one of the COISS_2101 trees.
        logger      PdsLogger to use.
        handler     an optional, additional handler to use just for this search.
        limit       maximum number of links to check.
    """

    unchecked_by_depth = {}
    checked = set()
    errors = set()
    from_urls = {}
    full_urls = {}

    def check1(key):
        """Check one key. A key is a logical file path (starting from the
        category). A key may optionally end in '?', in which case the URL will
        include an option. full_urls[key] returns a list of logical paths,
        including options, that match this key.

        In the end, we check each URL without any options, and the same URL
        with one set of randomly chosen options.
        """

        # Don't re-check
        if key in checked: return False
        checked.add(key)

        # Randomly choose a matching URL
        full_url = random.choice(full_urls[key])

        # Progress info for log files
        progress = '%3d/%-4s' % (len(checked), len(full_urls))

        # Log an invalid URL
        if (' ' in full_url or '<' in full_url or '>' in full_url):
                logger.error('%s | Invalid URL in %s' %
                             (progress, from_urls[key]), full_url)
                return True

        # Find all the URLs on this page
        found_urls = get_viewmaster_hrefs(viewmaster_ + full_url)

        # A return value of None indicates a 404 error or a fancy index
        if found_urls is None:
            errors.add(full_url)
            logger.error('%s | Invalid link from %s' %
                         (progress, from_urls[key]), full_url)
            return True

        # Log the valid URL
        logger.info('%s | Valid' % progress,
                    full_url + ' (%d)' % len(found_urls))

        # Add all URLs found to the queue
        for found_url in found_urls:

            # Skip URLs that don't match the regular expression
            if not regex.match(found_url): continue

            # Generate the key with optional trailing question mark
            newkey = ''.join(found_url.partition('?')[:2])
            if newkey in checked: continue

            # Save basic info
            from_urls[newkey] = full_url

            if newkey not in full_urls:
                full_urls[newkey] = []
            if found_url not in full_urls[newkey]:
                full_urls[newkey].append(found_url)

            # Add it to the list of found URLs, organized by depth
            # Depth = number of slashes in logical path
            depth = len(newkey.split('/'))
            if depth not in unchecked_by_depth:
                unchecked_by_depth[depth] = []
            if newkey not in unchecked_by_depth[depth]:
                unchecked_by_depth[depth].append(newkey)

        return True

    def random_unchecked_key():
        """Returns a randomly-selected, unchecked key."""

        # When all the lists are empty, stop
        if len(unchecked_by_depth) == 0:
            return None

        # Choose a random depth. This makes sure deeper depths don't totally
        # dominate
        while len(unchecked_by_depth) > 0:
            random_depth = random.choice(unchecked_by_depth.keys())
            if len(unchecked_by_depth[random_depth]) == 0:
                del unchecked_by_depth[random_depth]
            else:
                break

        if len(unchecked_by_depth) == 0:
            return None

        # Choose and remove a random key at the selected depth
        random_key = random.choice(unchecked_by_depth[random_depth])
        unchecked_by_depth[random_depth].remove(random_key)

        # If list at this depth is empty, delete it
        if len(unchecked_by_depth[random_depth]) == 0:
            del unchecked_by_depth[random_depth]

        return random_key

    #### Begin active code

    # Open the logger (including new handler if provided)
    logger.open('Spider link check', start, handler=handler)

    # Compile the regular expression
    if type(regex) == str:
        regex = re.compile(regex, re.I)

    # List information about run
    logger.info('Regex', regex.pattern)
    logger.info('Limit', str(limit))

    # Loop through unchecked keys till the limit is reached
    key = start
    full_urls[start] = [start]
    from_urls[start] = ''
    try:
        check1(key)

        counter = 1
        while (counter < limit):

            key = random_unchecked_key()
            if key is None: break

            ok = check1(key)
            if ok:
                counter += 1

    except BaseException as e:
        logger.exception(e, key)

    finally:
        return logger.close()

################################################################################

# Set up parser
parser = argparse.ArgumentParser(description='Spider: Link tester for ' +
                                             'Viewmaster')
parser.add_argument('server', type=str,
                    help='URL of a server running Viewmaster.')
parser.add_argument('volume', nargs='+', type=str,
                    help='Starting volset or volset/volume for this search.')
parser.add_argument('-n', type=int, default=1000,
                    help='Number of links to check; default 1000.')
parser.add_argument('--scope', '-s', type=str, default='volume',
                    choices=['volume', 'volset', 'all'],
                    help='Scope of search. Options are: ' +
                         '"volume" to stay within this volume; ' +
                         '"volset" to stay within this volume set; ' +
                         '"all" for a search of unlimited scope. ' +
                         'Default is "volume".')
parser.add_argument('--log', '-l', type=str, default='',
                    help='Directory for the log files. If not specified, ' +
                         'log files are written to the "viewmaster" '      +
                         'subdirectory of the path defined by '            +
                         'environment variable "%s". ' % LOGROOT_ENV       +
                         'If this is undefined, logs are written to the '  +
                         '"Logs" subdirectory of the current working '     +
                         'directory.')

parser.add_argument('--verbose', '-v', action='store_true',
                    help='Also log progress to to terminal.')

# Parse command line
namespace = parser.parse_args()

# Always log errors separately
logger = pdslogger.PdsLogger(LOGNAME, limits={'info':-1, 'normal':-1})

# Define the logging directory
if namespace.log:
    log_root = namespace.log
else:
    try:
        log_root = os.path.join(os.environ[LOGROOT_ENV], 'viewmaster')
    except KeyError:
        log_root = 'Logs'

# Initialize the logger
pdsfile.PdsFile.set_log_root(log_root)
log_path_ = os.path.join(log_root, 'viewmaster')

# Log to stdout if requested
if namespace.verbose:
    logger.add_handler(pdslogger.stdout_handler)

warning_handler = pdslogger.warning_handler(log_path_)
logger.add_handler(warning_handler)

error_handler = pdslogger.error_handler(log_path_)
logger.add_handler(error_handler)

# Intepret the server
server = namespace.server
if not server.startswith('http'):
    server = 'http://' + server

viewmaster_ = server.rstrip('/') + '/viewmaster/'

# For each volume set or volume name in list...
errors = 0
for arg in namespace.volume:

    # Add the handler specifically for this arg
    log_file = os.path.join(namespace.log, 'spider.log')
    handler = pdslogger.file_handler(log_file,
                                     level='info',
                                     suffix=arg.replace('/','-'),
                                     rotation='ymd')

    # Determine scope
    parts = arg.split('/')
    if parts[0] == '' and len(parts) > 1:
        parts = parts[1:]
    lparts = len(parts)

    if namespace.scope == 'volume':
        nparts = min(lparts, 2)
    elif namespace.scope == 'volset':
        nparts = min(lparts, 1)
    else:
        nparts = 0

    regex = re.compile('.*/' + '/'.join(parts[:nparts]), re.I)

    tuple = random_tree_search(viewmaster_, 'volumes/' + arg, regex,
                               logger=logger, handler=handler,
                               limit=namespace.n)
    errors += tuple[0] + tuple[1]

# Exit status is 1 if any error was found
if errors:
    sys.exit(1)

################################################################################
