################################################################################
# finder_colors.py
#
# Mark Showalter, SETI Institute, April 2017
################################################################################

# import os
# import subprocess
# 
# COLOR_VALUES = {
#     'none'   : 0,
#     'orange' : 1,
#     'red'    : 2,
#     'yellow' : 3,
#     'blue'   : 4,
#     'violet' : 5,
#     'purple' : 5,
#     'green'  : 6,
#     'gray'   : 7,
#     'grey'   : 7,
# }
# 
# def set_color(filepath, color):
#     filepath = os.path.abspath(filepath)
#     color = color.lower()
#     script = ('tell application "Finder" to set label index of ' +
#               '(POSIX file "%s" as alias) to %d' % (filepath,
#                                                     COLOR_VALUES[color]))
#     cmd = ['osascript', '-e', script]
# 
# #     _ = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE)
#     _ = subprocess.call(['osascript', '-e', script])


# This does not seem to work
# 
# from xattr import xattr
# 
# def set_color(filename, color_name):
#     print('I am running!!!', filename, color_name)
#     colors = ['none', 'gray', 'green', 'purple', 'blue', 'yellow', 'red', 'orange']
#     key = u'com.apple.FinderInfo'
#     attrs = xattr(filename)
#     current = attrs.copy().get(key, chr(0)*32)
#     changed = current[:9] + chr(colors.index(color_name)*2) + current[10:]
#     attrs.set(key, changed)
# 

import sys
import xattr

BYTES32 = bytes(32)
COLORS = ['none', 'gray', 'green', 'violet', 'blue', 'yellow', 'red', 'orange']
FINDER_KEY = u'com.apple.FinderInfo'

def set_color(filename, color_name):
    if sys.platform != 'darwin': return

    attrs = xattr.xattr(filename)
    current = attrs.copy().get(FINDER_KEY, BYTES32)
    changed = current[:9] + bytes([COLORS.index(color_name)*2]) + current[10:]
    attrs.set(FINDER_KEY, changed)

