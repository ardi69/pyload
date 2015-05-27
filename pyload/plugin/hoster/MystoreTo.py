# -*- coding: utf-8 -*-
#
# Test link:
#   http://mystore.to/dl/mxcA50jKfP

import re

from pyload.plugin.internal.SimpleHoster import SimpleHoster


class MystoreTo(SimpleHoster):
    __name    = "MystoreTo"
    __type    = "hoster"
    __version = "0.03"

    __pattern = r'https?://(?:www\.)?mystore\.to/dl/.+'
    __config  = [("use_premium", "bool", "Use premium account if available", True)]

    __description = """Mystore.to hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("zapp-brannigan", "")]


    NAME_PATTERN    = r'<h1>(?P<N>.+?)<'
    SIZE_PATTERN    = r'FILESIZE: (?P<S>[\d\.,]+) (?P<U>[\w^_]+)'
    OFFLINE_PATTERN = r'>file not found<'


    def setup(self):
        self.chunkLimit     = 1
        self.resumeDownload = True
        self.multiDL        = True


    def handle_free(self, pyfile):
        try:
            fid = re.search(r'wert="(.+?)"', self.html).group(1)

        except AttributeError:
            self.error(_("File-ID not found"))

        self.link = self.load("http://mystore.to/api/download",
                              post={'FID': fid})
