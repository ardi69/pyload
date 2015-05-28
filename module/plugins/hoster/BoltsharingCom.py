# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadHoster import DeadHoster


class BoltsharingCom(DeadHoster):
    __name__    = "BoltsharingCom"
    __type__    = "hoster"
    __version__ = "0.02"

    __pattern__ = r'http://(?:www\.)?boltsharing\.com/\w{12}'
    __config__  = []

    __description__ = """Boltsharing.com hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("zoidberg", "zoidberg@mujmail.cz")]
