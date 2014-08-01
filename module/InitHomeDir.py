# -*- coding: utf-8 -*-
"""
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License,
    or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see <http://www.gnu.org/licenses/>.

    @author: RaNaN

    This modules inits working directories and global variables, pydir and homedir
"""

import __builtin__
import sys

from os import chdir, makedirs, path
from os.path import abspath, exists, expanduser, join
from sys import argv, platform


__builtin__.owd = abspath("")  # original working directory
__builtin__.pypath = abspath(join(__file__, "..", ".."))

sys.path.append(join(pypath, "module", "lib"))

homedir = expanduser("~")

if platform == 'nt':
    if homedir == "~":
        import ctypes

        CSIDL_APPDATA = 26
        _SHGetFolderPath = ctypes.windll.shell32.SHGetFolderPathW
        _SHGetFolderPath.argtypes = [ctypes.wintypes.HWND,
                                     ctypes.c_int,
                                     ctypes.wintypes.HANDLE,
                                     ctypes.wintypes.DWORD, ctypes.wintypes.LPCWSTR]

        path_buf = ctypes.wintypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        result = _SHGetFolderPath(0, CSIDL_APPDATA, 0, 0, path_buf)
        homedir = path_buf.value

__builtin__.homedir = homedir

args = " ".join(argv[1:])

# dirty method to set configdir from commandline arguments
if "--configdir=" in args:
    for aa in argv:
        if aa.startswith("--configdir="):
            configdir = aa.replace("--configdir=", "", 1).strip()
elif exists(join(pypath, "module", "config", "configdir")):
    f = open(join(pypath, "module", "config", "configdir"), "rb")
    c = f.read().strip()
    f.close()
    configdir = join(pypath, c)
else:
    if platform in ("posix", "linux2"):
        configdir = join(homedir, ".pyload")
    else:
        configdir = join(homedir, "pyload")

if not exists(configdir):
    makedirs(configdir, 0700)

__builtin__.configdir = configdir
chdir(configdir)

#print "Using %s as working directory." % configdir
