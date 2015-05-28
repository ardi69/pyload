# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadHoster import DeadHoster


class FilezyNet(DeadHoster):
    __name__    = "FilezyNet"
    __type__    = "hoster"
    __version__ = "0.20"

    __pattern__ = r'http://(?:www\.)?filezy\.net/\w{12}'
    __config__  = []

    __description__ = """Filezy.net hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = []
