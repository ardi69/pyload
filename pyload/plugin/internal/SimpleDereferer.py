# -*- coding: utf-8 -*-

import re
import urllib

from pyload.plugin.Crypter import Crypter
from pyload.plugin.internal.SimpleHoster import getFileURL, set_cookies


class SimpleDereferer(Crypter):
    __name    = "SimpleDereferer"
    __type    = "crypter"
    __version = "0.11"

    __pattern = r'^unmatchable$'
    __config  = [("use_subfolder"     , "bool", "Save package to subfolder"          , True),
                   ("subfolder_per_pack", "bool", "Create a subfolder for each package", True)]

    __description = """Simple dereferer plugin"""
    __license     = "GPLv3"
    __authors     = [("Walter Purcaro", "vuolter@gmail.com")]


    """
    Following patterns should be defined by each crypter:

      LINK_PATTERN: Regex to catch the redirect url in group(1)
        example: LINK_PATTERN = r'<div class="link"><a href="(.+?)"'

      OFFLINE_PATTERN: (optional) Checks if the page is unreachable
        example: OFFLINE_PATTERN = r'File (deleted|not found)'

      TEMP_OFFLINE_PATTERN: (optional) Checks if the page is temporarily unreachable
        example: TEMP_OFFLINE_PATTERN = r'Server maintainance'


    You can override the getLinks method if you need a more sophisticated way to extract the redirect url.
    """

    LINK_PATTERN = None

    TEXT_ENCODING = False
    COOKIES       = True


    def decrypt(self, pyfile):
        link = getFileURL(self, pyfile.url)

        if not link:
            try:
                link = urllib.unquote(re.match(self.__pattern, pyfile.url).group('LINK'))

            except Exception:
                self.prepare()
                self.preload()
                self.checkStatus()

                link = self.getLink()

        if link.strip():
            self.urls = [link]


    def prepare(self):
        self.info = {}
        self.html = ""

        self.req.setOption("timeout", 120)

        if isinstance(self.COOKIES, list):
            set_cookies(self.req.cj, self.COOKIES)


    def preload(self):
        self.html = self.load(self.pyfile.url, cookies=bool(self.COOKIES), decode=not self.TEXT_ENCODING)

        if isinstance(self.TEXT_ENCODING, basestring):
            self.html = unicode(self.html, self.TEXT_ENCODING)


    def checkStatus(self):
        if hasattr(self, "OFFLINE_PATTERN") and re.search(self.OFFLINE_PATTERN, self.html):
            self.offline()

        elif hasattr(self, "TEMP_OFFLINE_PATTERN") and re.search(self.TEMP_OFFLINE_PATTERN, self.html):
            self.tempOffline()


    def getLink(self):
        try:
            return re.search(self.LINK_PATTERN, self.html).group(1)

        except Exception:
            pass
