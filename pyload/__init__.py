# -*- coding: utf-8 -*-

__all__ = ["__status_code__", "__status__", "__version_info__", "__version__", "__license__"]

__status_code__ = 4
__status__ = {1: "Planning",
              2: "Pre-Alpha",
              3: "Alpha",
              4: "Beta",
              5: "Production/Stable",
              6: "Mature",
              7: "Inactive"}[__status_code__]  #: PyPI Development Status Classifiers

__version_info__ = (0, 4, 10)
__version__ = '.'.join(map(str(v), __version_info__))

__license__ = "GNU Affero General Public License v3"


################################# InitHomeDir #################################

import __builtin__
import os
import sys

projectdir = path.abspath(path.join(__file__, ".."))
homedir = path.expanduser("~")

if homedir == "~" and os.name == "nt":
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

try:
    p = path.join(projectdir, "config", "configdir")
    if path.exists(p):
        f = open(p, "rb")
        configdir = f.read().strip()
        f.close()
except:
    if os.name == "posix":
        configdir = path.join(homedir, ".pyload")
    else:
        configdir = path.join(homedir, "pyload")

sys.path.append(path.join(projectdir, "lib"))

__builtin__.owd = path.abspath("")  #: original working directory
__builtin__.pypath = path.abspath(path.join(projectdir, ".."))
__builtin__.pycore = None  #: Store global Core.Core instance (will be set by Core on its init)

__builtin__.projectdir = projectdir
__builtin__.homedir = homedir
__builtin__.configdir = configdir
