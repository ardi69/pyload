# -*- coding: utf-8 -*-
#
# Test links:
#   http://www.filepup.net/files/k5w4ZVoF1410184283.html
#   http://www.filepup.net/files/R4GBq9XH1410186553.html

import re

from pyload.plugin.internal.SimpleHoster import SimpleHoster


class FilepupNet(SimpleHoster):
    __name    = "FilepupNet"
    __type    = "hoster"
    __version = "0.03"

    __pattern = r'http://(?:www\.)?filepup\.net/files/\w+'
    __config  = [("use_premium", "bool", "Use premium account if available", True)]

    __description = """Filepup.net hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("zapp-brannigan", "fuerst.reinje@web.de"),
                       ("Walter Purcaro", "vuolter@gmail.com")]


    NAME_PATTERN = r'>(?P<N>.+?)</h1>'
    SIZE_PATTERN = r'class="fa fa-archive"></i> \((?P<S>[\d.,]+) (?P<U>[\w^_]+)'

    OFFLINE_PATTERN = r'>This file has been deleted'

    LINK_FREE_PATTERN = r'(http://www\.filepup\.net/get/.+?)\''


    def setup(self):
        self.multiDL = False
        self.chunkLimit = 1


    def handle_free(self, pyfile):
        m = re.search(self.LINK_FREE_PATTERN, self.html)
        if m is None:
            self.error(_("Download link not found"))

        dl_link = m.group(1)
        self.download(dl_link, post={'task': "download"})
