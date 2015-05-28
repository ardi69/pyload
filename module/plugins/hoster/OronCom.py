# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadHoster import DeadHoster


class OronCom(DeadHoster):
    __name__    = "OronCom"
    __type__    = "hoster"
    __version__ = "0.14"

    __pattern__ = r'https?://(?:www\.)?oron\.com/\w{12}'
    __config__  = []

    __description__ = """Oron.com hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("chrox", "chrox@pyload.org"),
                       ("DHMH", "DHMH@pyload.org")]
