# -*- coding: utf-8 -*-
#
### Store all usefull functions here ###

import os
import re
import sys
import time

from gettext import gettext
from htmlentitydefs import name2codepoint
from itertools import islice
from os import path
from string import maketrans

# abstraction layer for json operations
try:
    import simplejson as json
except ImportError:
    import json

json_loads = json.loads
json_dumps = json.dumps


from pyload.utils import convert
from pyload.utils.decorators import *


def chunks(iterable, size):
    it = iter(iterable)
    item = list(islice(it, size))
    while item:
        yield item
        item = list(islice(it, size))


def chmod(*args):
    try:
        os.chmod(*args)
    except:
        pass


def decode(string):
    """ Decode string to unicode with utf8 """
    if type(string) == str:
        return string.decode("utf8", "replace")
    else:
        return string


def encode(string):
    """ Decode string to utf8 """
    if type(string) == unicode:
        return string.encode("utf8", "replace")
    else:
        return string


def remove_chars(string, repl):
    """ Remove all chars in repl from string """
    if type(repl) == unicode:
        for badc in list(repl):
            string = string.replace(badc, "")
        return string
    else:
        if type(string) == str:
            return string.translate(maketrans("", ""), repl)
        elif type(string) == unicode:
            return string.translate(dict([(ord(s), None) for s in repl]))


def safe_filename(name):
    """ Remove bad chars """
    name = name.encode('ascii', 'replace')  # Non-ASCII chars usually breaks file saving. Replacing.
    if os.name == "nt":
        return remove_chars(name, u'\00\01\02\03\04\05\06\07\10\11\12\13\14\15\16\17\20\21\22\23\24\25\26\27\30\31\32'
                                  u'\33\34\35\36\37/\\?%*:|"<>')
    else:
        return remove_chars(name, u'\0/\\"')

@deprecated(by=safe_filename)
def save_path(name):
    pass


def safe_join(*args):
    """ Join a path, encoding aware """
    return fs_encode(path.join(*[x if type(x) == unicode else decode(x) for x in args]))

@deprecated(by=safe_join)
def save_join(*args):
    pass


# File System Encoding functions:
# Use fs_encode before accesing files on disk, it will encode the string properly

if sys.getfilesystemencoding().startswith("ANSI"):
    def fs_encode(string):
        try:
            string = string.encode('utf-8')
        finally:
            return string

    fs_decode = decode #decode utf8

else:
    fs_encode = fs_decode = lambda x: x  # do nothing


def get_console_encoding(enc):
    if os.name == "nt":
        if enc == "cp65001":  #: aka UTF-8
            enc = "cp850"
            print "WARNING: Windows codepage 65001 (UTF-8) is not supported. Used \"%s\" instead." % enc
    else:
        enc = "utf8"

    return enc


def compare_time(start, end):
    start = map(int, start)
    end = map(int, end)

    if start == end:
        res = True
    else:
        now = list(time.localtime()[3:5])
        if start < now < end:
            res = True
        elif start > end and (now > start or now < end):
            res = True
        elif start < now > end < start:
            res = True
        else:
            res = False

    return res


def format_size(size):
    """ Format size of bytes """
    size = int(size)
    steps = 0
    sizes = ("B", "KiB", "MiB", "GiB", "TiB")

    while size > 1000:
        size /= 1024.0
        steps += 1

    return "%.2f %s" % (size, sizes[steps])

@deprecated(by=format_size)
def formatSize(*args):
    pass


def format_speed(speed):
    return format_size(speed) + "/s"

@deprecated(by=format_speed)
def formatSpeed(*args):
    pass


def free_space(folder):
    """ Return free storing space on device (in bytes) """
    if os.name == "nt":
        import ctypes

        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
    else:
        s = os.statvfs(folder)
        return s.f_bsize * s.f_bavail

@deprecated(by=free_space)
def freeSpace(*args):
    pass


def fs_bsize(folder):
    """ Get optimal file system buffer size (in bytes) for I/O calls """
    folder = fs_encode(folder)

    if os.name == "nt":
        import ctypes

        drive = "%s\\" % path.splitdrive(folder)[0]
        cluster_sectors, sector_size = ctypes.c_longlong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceW(ctypes.c_wchar_p(drive), ctypes.pointer(cluster_sectors), ctypes.pointer(sector_size), None, None)
        return cluster_sectors * sector_size
    else:
        return os.statvfs(folder).f_bsize


def uniqify(seq):  #: Originally by Dave Kirby
    """ Remove duplicates from list preserving order """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if x not in seen and not seen_add(x)]


def parse_size(string, unit=None, to_unit="byte"):
    """ Get file size from string and return it properly converted to number """
    if isinstance(string, basestring):
        m = re.match(r".*?([\d.,]+)(?: *([a-zA-Z]+))?", string.strip().lower())
        if m:
            value = int(m.group(1).replace(",", "."))  #@TODO: float support
            if not unit:
                try:
                    unit = m.group(2)
                except:
                    unit = "byte"
        else:
            value = None
    else:
        try:
            value = int(string)  #@TODO: float support
        except:
            value = None

    if not unit or value is None:
        return 0
    else:
        return convert.size(value, unit, to_unit) or 0


@deprecated(by=parse_size)
def parseFileSize(*args):
    pass


def fixup(m):
    text = m.group(0)
    if text[:2] == "&#":
        # character reference
        try:
            if text[:3] == "&#x":
                text = unichr(int(text[3:-1], 16))
            else:
                text = unichr(int(text[2:-1]))
        except ValueError:
            pass
    else:
        # named entity
        try:
            name = text[1:-1]
            text = unichr(name2codepoint[name])
        except KeyError:
            pass

    return text


def has_method(obj, name):
    """ Check if "name" was defined in obj, (false if it was inhereted) """
    return hasattr(obj, '__dict__') and name in obj.__dict__


def html_unescape(text):
    """ Remove HTML or XML character references and entities from a text string """
    return re.sub("&#?\w+;", fixup, text)


def load_translation(name, locale, default="en"):
    """ Load language and return its translation object or None """
    try:
        gettext.setpaths([path.join(os.sep, "usr", "share", "pyload", "locale"), None])
        translation = gettext.translation(name, self.path("locale"),
                                          languages=[locale, default], fallback=True)
    except:
        return None
    else:
        translation.install(True)
        return translation
