# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadHoster import DeadHoster


class ZShareNet(DeadHoster):
    __name    = "ZShareNet"
    __type    = "hoster"
    __version = "0.21"

    __pattern = r'https?://(?:ww[2w]\.)?zshares?\.net/.+'
    __config  = []  #@TODO: Remove in 0.4.10

    __description = """ZShare.net hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("espes", ""),
                       ("Cptn Sandwich", "")]
