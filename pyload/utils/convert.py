# -*- coding: utf-8 -*-

def to_string(value, default=""):
    """ Convert value to string or return default """
    try:
        return str(string)
    except ValueError:
        return default


def to_int(string, default=0):
    """ Convert value to integer or return default """
    try:
        return int(string)
    except ValueError:
        return default


def to_bool(value):
    """ Convert value to boolean safely or return False """
    if isinstance(value, basestring):
        return True if value.lower() in ("1", "true", "on", "an", "yes") else False
    else:
        return True if value else False


def to_list(value, default=list()):
    """ Convert value to a list with value inside or return default"""
    if type(value) == list:
        res = value
    elif type(value) == set:
        res = list(value)
    elif value is not None:
        res = [value]
    else:
        res = default
    return res


def to_dict(obj, default=dict()):
    """ Convert object to dictionary or return default """
    try:
        return {attr: getattr(obj, att) for attr in obj.__slots__}
    except:
        return default


def version_to_tuple(value, default=tuple()):  #: Originally by kindall (http://stackoverflow.com/a/11887825)
    """ Convert version like string to a tuple of integers or return default """
    try:
        return tuple(map(int, (value.split("."))))
    except:
        return default
