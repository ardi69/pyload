# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadHoster import DeadHoster


class EgoFilesCom(DeadHoster):
    __name__    = "EgoFilesCom"
    __type__    = "hoster"
    __version__ = "0.16"

    __pattern__ = r'https?://(?:www\.)?egofiles\.com/\w+'
    __config__  = []

    __description__ = """Egofiles.com hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("stickell", "l.stickell@yahoo.it")]
