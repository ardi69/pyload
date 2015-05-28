# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadHoster import DeadHoster


class MegauploadCom(DeadHoster):
    __name__    = "MegauploadCom"
    __type__    = "hoster"
    __version__ = "0.31"

    __pattern__ = r'http://(?:www\.)?megaupload\.com/\?.*&?(d|v)=\w+'
    __config__  = []

    __description__ = """Megaupload.com hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("spoob", "spoob@pyload.org")]
