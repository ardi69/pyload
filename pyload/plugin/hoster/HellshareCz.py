# -*- coding: utf-8 -*-

from pyload.plugin.internal.SimpleHoster import SimpleHoster


class HellshareCz(SimpleHoster):
    __name    = "HellshareCz"
    __type    = "hoster"
    __version = "0.85"

    __pattern = r'http://(?:www\.)?hellshare\.(?:cz|com|sk|hu|pl)/[^?]*/\d+'
    __config  = [("use_premium", "bool", "Use premium account if available", True)]

    __description = """Hellshare.cz hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("zoidberg", "zoidberg@mujmail.cz")]


    CHECK_TRAFFIC = True
    LOGIN_ACCOUNT = True

    NAME_PATTERN    = r'<h1 id="filename"[^>]*>(?P<N>[^<]+)</h1>'
    SIZE_PATTERN    = r'<strong id="FileSize_master">(?P<S>[\d.,]+)&nbsp;(?P<U>[\w^_]+)</strong>'
    OFFLINE_PATTERN = r'<h1>File not found.</h1>'

    LINK_FREE_PATTERN = LINK_PREMIUM_PATTERN = r'<a href="([^?]+/(\d+)/\?do=(fileDownloadButton|relatedFileDownloadButton-\2)-showDownloadWindow)"'


    def setup(self):
        self.resumeDownload = self.multiDL = bool(self.account)
        self.chunkLimit = 1
