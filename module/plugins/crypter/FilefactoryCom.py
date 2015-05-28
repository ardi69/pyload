# -*- coding: utf-8 -*-

from pyload.plugin.internal.SimpleCrypter import SimpleCrypter


class FilefactoryCom(SimpleCrypter):
    __name__    = "FilefactoryCom"
    __type__    = "crypter"
    __version__ = "0.32"

    __pattern__ = r'https?://(?:www\.)?filefactory\.com/(?:f|folder)/\w+'
    __config__  = [("use_premium"       , "bool", "Use premium account if available"   , True),
                   ("use_subfolder"     , "bool", "Save package to subfolder"          , True),
                   ("subfolder_per_pack", "bool", "Create a subfolder for each package", True)]

    __description__ = """Filefactory.com folder decrypter plugin"""
    __license__     = "GPLv3"
    __authors__     = [("stickell", "l.stickell@yahoo.it")]


    COOKIES = [("filefactory.com", "locale", "en_US.utf8")]

    LINK_PATTERN  = r'<td>\s*<a href="(.+?)"'
    NAME_PATTERN  = r'<h1>Files in <span>(?P<N>.+?)<'
    PAGES_PATTERN = r'data-paginator-totalPages="(\d+)'


    def loadPage(self, page_n):
        return self.load(self.pyfile.url, get={'page': page_n, 'show': 100})
