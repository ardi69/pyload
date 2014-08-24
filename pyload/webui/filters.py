# -*- coding: utf-8 -*-

from os import path

quotechar = "::/"

def quotepath(path):
    try:
        return path.replace("../", quotechar)
    except AttributeError:
        return path
    except:
        return ""

def unquotepath(path):
    try:
        return path.replace(quotechar, "../")
    except AttributeError:
        return path
    except:
        return ""

def path_make_absolute(path):
    p = path.abspath(path)
    if p[-1] == path.sep:
        return p
    else:
        return p + path.sep

def path_make_relative(path):
    p = path.relpath(path)
    if p[-1] == path.sep:
        return p
    else:
        return p + path.sep

def truncate(value, n):
    if (n - len(value)) < 3:
        return value[:n]+"..."
    return value

def date(date, format):
    return date
