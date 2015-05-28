# -*- coding: utf-8 -*-

from pyload.plugin.internal.XFSHoster import XFSHoster


class RarefileNet(XFSHoster):
    __name__    = "RarefileNet"
    __type__    = "hoster"
    __version__ = "0.09"

    __pattern__ = r'http://(?:www\.)?rarefile\.net/\w{12}'

    __description__ = """Rarefile.net hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("zoidberg", "zoidberg@mujmail.cz")]


    LINK_PATTERN = r'<a href="(.+?)">\1</a>'
