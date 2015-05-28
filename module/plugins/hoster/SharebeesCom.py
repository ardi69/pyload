# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadHoster import DeadHoster


class SharebeesCom(DeadHoster):
    __name__    = "SharebeesCom"
    __type__    = "hoster"
    __version__ = "0.02"

    __pattern__ = r'http://(?:www\.)?sharebees\.com/\w{12}'
    __config__  = []

    __description__ = """ShareBees hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("zoidberg", "zoidberg@mujmail.cz")]
