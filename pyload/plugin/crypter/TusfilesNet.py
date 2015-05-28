# -*- coding: utf-8 -*-

import math
import re
import urlparse

from pyload.plugin.internal.XFSCrypter import XFSCrypter


class TusfilesNet(XFSCrypter):
    __name    = "TusfilesNet"
    __type    = "crypter"
    __version = "0.08"

    __pattern = r'https?://(?:www\.)?tusfiles\.net/go/(?P<ID>\w+)'
    __config  = [("use_subfolder"     , "bool", "Save package to subfolder"          , True),
                   ("subfolder_per_pack", "bool", "Create a subfolder for each package", True)]

    __description = """Tusfiles.net folder decrypter plugin"""
    __license     = "GPLv3"
    __authors     = [("Walter Purcaro", "vuolter@gmail.com"),
                       ("stickell", "l.stickell@yahoo.it")]


    PAGES_PATTERN = r'>\((\d+) \w+\)<'

    URL_REPLACEMENTS = [(__pattern + ".*", r'https://www.tusfiles.net/go/\g<ID>/')]


    def loadPage(self, page_n):
        return self.load(urlparse.urljoin(self.pyfile.url, str(page_n)), decode=True)


    def handle_pages(self, pyfile):
        pages = re.search(self.PAGES_PATTERN, self.html)
        if pages:
            pages = int(math.ceil(int(pages.group('pages')) / 25.0))
        else:
            return

        for p in xrange(2, pages + 1):
            self.html = self.loadPage(p)
            self.links += self.getLinks()
