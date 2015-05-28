# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadHoster import DeadHoster


class CyberlockerCh(DeadHoster):
    __name__    = "CyberlockerCh"
    __type__    = "hoster"
    __version__ = "0.02"

    __pattern__ = r'http://(?:www\.)?cyberlocker\.ch/\w+'
    __config__  = []

    __description__ = """Cyberlocker.ch hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("stickell", "l.stickell@yahoo.it")]
