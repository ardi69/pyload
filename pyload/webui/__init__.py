# -*- coding: utf-8 -*-

import os
import sys

import bottle

from os import path


debug = pycore.config.get("general", "debug") or "-d" in sys.argv or "--debug" in sys.argv
bottle.debug(debug)



API = pycore.api

THEME_DIR = path.abspath(path.join(__file__, "..", "themes"))
THEME = pycore.config.get('webinterface', 'theme')

PREFIX = pycore.config.get('webinterface', 'prefix')

if PREFIX:
    PREFIX = PREFIX.rstrip("/")
    if PREFIX and not PREFIX.startswith("/"):
        PREFIX = "/" + PREFIX



from jinja2 import Environment, FileSystemLoader, PrefixLoader, FileSystemBytecodeCache

cache = path.join("./tmp", "jinja_cache")
if not path.exists(cache):
    os.makedirs(cache)

bcc = FileSystemBytecodeCache(cache, '%s.cache')
loader = FileSystemLoader(THEME_DIR)

ENV = Environment(loader=loader, extensions=['jinja2.ext.i18n', 'jinja2.ext.autoescape'], trim_blocks=True, auto_reload=False,
                  bytecode_cache=bcc)


from pyload.utils import decode, formatSize
from pyload.webui.filters import quotepath, path_make_relative, path_make_absolute, truncate, date

ENV.filters['quotepath'] = quotepath
ENV.filters['truncate'] = truncate
ENV.filters['date'] = date
ENV.filters['path_make_relative'] = path_make_relative
ENV.filters['path_make_absolute'] = path_make_absolute
ENV.filters['decode'] = decode
ENV.filters['type'] = lambda x: str(type(x))
ENV.filters['formatsize'] = formatSize
ENV.filters['getitem'] = lambda x, y: x.__getitem__(y)

if PREFIX:
    ENV.filters['url'] = lambda x: x
else:
    ENV.filters['url'] = lambda x: PREFIX + x if x.startswith("/") else x



from gettext import gettext

gettext.setpaths([path.join(os.sep, "usr", "share", "pyload", "locale"), None])
translation = gettext.translation("django", path.join(pypath, "locale"),
                                  languages=[pycore.config.get("general", "language"), "en"],
                                  fallback=True)
translation.install(True)

ENV.install_gettext_translations(translation)



from beaker.middleware import SessionMiddleware
from bottle import run, app

from pyload.webui.middlewares import StripPathMiddleware, PrefixMiddleware

session_opts = {'session.type': "file",
                'session.cookie_expires': False,
                'session.data_dir': "./tmp",
                'session.auto': False}
session = SessionMiddleware(app(), session_opts)

APP = StripPathMiddleware(session)

if PREFIX:
    APP = PrefixMiddleware(APP, prefix=PREFIX)


def run_server(host, port, server):
    run(app=APP, host=host, port=port, quiet=True, server=server)



import pyload.webui.app
