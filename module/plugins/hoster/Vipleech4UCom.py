# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadHoster import DeadHoster


class Vipleech4UCom(DeadHoster):
    __name__    = "Vipleech4UCom"
    __type__    = "hoster"
    __version__ = "0.20"

    __pattern__ = r'http://(?:www\.)?vipleech4u\.com/manager\.php'
    __config__  = []

    __description__ = """Vipleech4u.com hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("Kagenoshin", "kagenoshin@gmx.ch")]
