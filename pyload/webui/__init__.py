# -*- coding: utf-8 -*-
# @author: RaNaN, vuolter

import os
import sys

import beaker.middleware
import bottle
import jinja2

from pyload.utils import pylgettext as gettext

from pyload.Thread import Server
from pyload.utils.middlewares import StripPathMiddleware, GZipMiddleWare, PrefixMiddleware
from pyload.network.JsEngine import JsEngine
from pyload.utils import decode, format_size


THEME_DIR  = os.path.abspath(os.path.join(os.path.dirname(__file__), "themes"))
PYLOAD_DIR = os.path.abspath(os.path.join(THEME_DIR, "..", "..", ".."))

sys.path.append(PYLOAD_DIR)

PYLOAD = Server.core.api
config = Server.core.config
JS = JsEngine(Server.core)

PREFIX = config.get('webui', 'prefix')

if PREFIX:
    PREFIX = PREFIX.rstrip("/")
    if not PREFIX.startswith("/"):
        PREFIX = "/" + PREFIX

DEBUG = config.get("general", "debug_mode") or "-d" in sys.argv or "--debug" in sys.argv
bottle.debug(DEBUG)

cache = os.path.join("tmp", "jinja_cache")
if not os.path.exists(cache):
    os.makedirs(cache)

bcc = jinja2.FileSystemBytecodeCache(cache, '%s.cache')

loader = jinja2.FileSystemLoader([THEME_DIR,
                                 os.path.join(THEME_DIR, config.get('webui', 'theme').capitalize())])

env = jinja2.Environment(loader=loader, extensions=['jinja2.ext.i18n', 'jinja2.ext.autoescape'], trim_blocks=True, auto_reload=False,
                  bytecode_cache=bcc)

from pyload.utils.filters import quotepath, path_make_relative, path_make_absolute, truncate, date

env.filters['quotepath'] = quotepath
env.filters['truncate'] = truncate
env.filters['date'] = date
env.filters['path_make_relative'] = path_make_relative
env.filters['path_make_absolute'] = path_make_absolute
env.filters['decode'] = decode
env.filters['type'] = lambda x: str(type(x))
env.filters['formatsize'] = format_size
env.filters['getitem'] = lambda x, y: x.__getitem__(y)
if PREFIX:
    env.filters['url'] = lambda x: x
else:
    env.filters['url'] = lambda x: PREFIX + x if x.startswith("/") else x

gettext.setpaths([os.path.join(os.sep, "usr", "share", "pyload", "locale"), None])
translation = gettext.translation("django", os.path.join(PYLOAD_DIR, "locale"),
    languages=[config.get("general", "language"), "en"],fallback=True)
translation.install(True)
env.install_gettext_translations(translation)

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': False,
    'session.data_dir': './tmp',
    'session.auto': False
}

web = StripPathMiddleware(beaker.middleware.SessionMiddleware(bottle.app(), session_opts))
web = GZipMiddleWare(web)

if PREFIX:
    web = PrefixMiddleware(web, prefix=PREFIX)

from pyload.webui import App


def run_auto(host="0.0.0.0", port="8000"):
    bottle.run(app=web, host=host, port=port, server="auto", quiet=True)


def run_lightweight(host="0.0.0.0", port="8000"):
    bottle.run(app=web, host=host, port=port, server="bjoern", quiet=True)


def run_threaded(host="0.0.0.0", port="8000", theads=3, cert="", key=""):
    import wsgiserver

    if cert and key:
        wsgiserver.CherryPyWSGIServer.ssl_certificate = cert
        wsgiserver.CherryPyWSGIServer.ssl_private_key = key

    wsgiserver.CherryPyWSGIServer.numthreads = theads

    from pyload.webui.App.utils import CherryPyWSGI

    bottle.run(app=web, host=host, port=port, server=CherryPyWSGI, quiet=True)


def run_fcgi(host="0.0.0.0", port="8000"):
    bottle.run(app=web, host=host, port=port, server=bottle.FlupFCGIServer, quiet=True)
