# -*- coding: utf-8 -*-
#
# Test links:
#   http://fileom.com/gycaytyzdw3g/random.bin.html

from pyload.plugin.internal.XFSHoster import XFSHoster


class FileomCom(XFSHoster):
    __name    = "FileomCom"
    __type    = "hoster"
    __version = "0.05"

    __pattern = r'https?://(?:www\.)?fileom\.com/\w{12}'

    __description = """Fileom.com hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("Walter Purcaro", "vuolter@gmail.com")]


    NAME_PATTERN = r'Filename: <span>(?P<N>.+?)<'
    SIZE_PATTERN = r'File Size: <span class="size">(?P<S>[\d.,]+) (?P<U>[\w^_]+)'

    LINK_PATTERN = r'var url2 = \'(.+?)\';'


    def setup(self):
        self.multiDL = True
        self.chunkLimit = 1
        self.resumeDownload = self.premium
