# -*- coding: utf-8 -*-
# @author: RaNaN, vuolter

import os

import bottle

from pyload.Api import has_permission, PERMS, ROLE
from pyload.webui import env


def render_to_response(file, args={}, proc=[]):
    for p in proc:
        args.update(p())
    path = "tml/" + file
    return env.get_template(path).render(**args)


def parse_permissions(session):
    perms = dict((x, False) for x in dir(PERMS) if not x.startswith("_"))
    perms['ADMIN'] = False
    perms['is_admin'] = False

    if not session.get("authenticated", False):
        return perms

    if session.get("role") == ROLE.ADMIN:
        for k in perms.iterkeys():
            perms[k] = True

    elif session.get("perms"):
        p = session.get("perms")
        get_permission(perms, p)

    return perms


def permlist():
    return [x for x in dir(PERMS) if not x.startswith("_") and x != "ALL"]


def get_permission(perms, p):
    """
    Returns a dict with permission key

    :param perms: dictionary
    :param p:  bits
    """
    for name in permlist():
        perms[name] = has_permission(p, getattr(PERMS, name))


def set_permission(perms):
    """
    Generates permission bits from dictionary

    :param perms: dict
    """
    permission = 0
    for name in dir(PERMS):
        if name.startswith("_"):
            continue

        if name in perms and perms[name]:
            permission |= getattr(PERMS, name)

    return permission


def set_session(request, info):
    s = bottle.request.environ.get('beaker.session')
    s['authenticated'] = True
    s['user_id'] = info['id']
    s['name'] = info['name']
    s['role'] = info['role']
    s['perms'] = info['permission']
    s['template'] = info['template']
    s.save()

    return s


def parse_userdata(session):
    return {"name"            : session.get("name", "Anonymous"),
            "is_admin"        : session.get("role", 1) == 0,
            "is_authenticated": session.get("authenticated", False)}


def login_required(perm=None):

    def _dec(func):

        def _view(*args, **kwargs):
            s = bottle.request.environ.get('beaker.session')
            if s.get("name", None) and s.get("authenticated", False):
                if perm:
                    perms = parse_permissions(s)
                    if perm not in perms or not perms[perm]:
                        if bottle.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                            return bottle.HTTPError(403, "Forbidden")
                        else:
                            return bottle.redirect("/nopermission")

                return func(*args, **kwargs)
            else:
                if bottle.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return bottle.HTTPError(403, "Forbidden")
                else:
                    return bottle.redirect("/login")

        return _view

    return _dec


def toDict(obj):
    return dict((att, getattr(obj, att)) for att in obj.__slots__)


class CherryPyWSGI(bottle.ServerAdapter):

    def run(self, handler):
        from wsgiserver import CherryPyWSGIServer

        server = CherryPyWSGIServer((self.host, self.port), handler)
        server.start()
