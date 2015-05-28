# -*- coding: utf-8 -*-
#
# Test links:
#   http://www.solidfiles.com/d/609cdb4b1b

from pyload.plugin.internal.SimpleHoster import SimpleHoster


class SolidfilesCom(SimpleHoster):
    __name    = "SolidfilesCom"
    __type    = "hoster"
    __version = "0.02"

    __pattern = r'http://(?:www\.)?solidfiles\.com\/d/\w+'

    __description = """Solidfiles.com hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("sraedler", "simon.raedler@yahoo.de")]


    NAME_PATTERN    = r'<h1 title="(?P<N>.+?)"'
    SIZE_PATTERN    = r'<p class="meta">(?P<S>[\d.,]+) (?P<U>[\w_^]+)'
    OFFLINE_PATTERN = r'<h1>404'

    LINK_FREE_PATTERN = r'id="ddl-text" href="(.+?)"'


    def setup(self):
        self.multiDL    = True
        self.chunkLimit = 1
