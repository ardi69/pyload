# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadHoster import DeadHoster


class TurbouploadCom(DeadHoster):
    __name__    = "TurbouploadCom"
    __type__    = "hoster"
    __version__ = "0.03"

    __pattern__ = r'http://(?:www\.)?turboupload\.com/(\w+)'
    __config__  = []

    __description__ = """Turboupload.com hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("zoidberg", "zoidberg@mujmail.cz")]
