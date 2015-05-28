# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadHoster import DeadHoster


class ZShareNet(DeadHoster):
    __name__    = "ZShareNet"
    __type__    = "hoster"
    __version__ = "0.21"

    __pattern__ = r'https?://(?:ww[2w]\.)?zshares?\.net/.+'
    __config__  = []

    __description__ = """ZShare.net hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("espes", ""),
                       ("Cptn Sandwich", "")]
