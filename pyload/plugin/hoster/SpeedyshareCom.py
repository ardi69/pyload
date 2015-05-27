# -*- coding: utf-8 -*-
#
# Test links:
#   http://speedy.sh/ep2qY/Zapp-Brannigan.jpg

import re

from pyload.plugin.internal.SimpleHoster import SimpleHoster


class SpeedyshareCom(SimpleHoster):
    __name    = "SpeedyshareCom"
    __type    = "hoster"
    __version = "0.05"

    __pattern = r'https?://(?:www\.)?(speedyshare\.com|speedy\.sh)/\w+'
    __config  = [("use_premium", "bool", "Use premium account if available", True)]

    __description = """Speedyshare.com hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("zapp-brannigan", "fuerst.reinje@web.de")]


    NAME_PATTERN = r'class=downloadfilename>(?P<N>.*)</span></td>'
    SIZE_PATTERN = r'class=sizetagtext>(?P<S>.*) (?P<U>[kKmM]?[iI]?[bB]?)</div>'

    OFFLINE_PATTERN = r'class=downloadfilenamenotfound>.*</span>'

    LINK_FREE_PATTERN = r'<a href=\'(.*)\'><img src=/gf/slowdownload\.png alt=\'Slow Download\' border=0'


    def setup(self):
        self.multiDL = False
        self.chunkLimit = 1


    def handle_free(self, pyfile):
        m = re.search(self.LINK_FREE_PATTERN, self.html)
        if m is None:
            self.link = m.group(1)
