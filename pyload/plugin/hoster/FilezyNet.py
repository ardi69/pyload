# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadHoster import DeadHoster


class FilezyNet(DeadHoster):
    __name    = "FilezyNet"
    __type    = "hoster"
    __version = "0.20"

    __pattern = r'http://(?:www\.)?filezy\.net/\w{12}'
    __config  = []  #@TODO: Remove in 0.4.10

    __description = """Filezy.net hoster plugin"""
    __license     = "GPLv3"
    __authors     = []
