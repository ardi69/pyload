# -*- coding: utf-8 -*-

import re

from pyload.plugin.internal.SimpleCrypter import SimpleCrypter


class FreetexthostCom(SimpleCrypter):
    __name    = "FreetexthostCom"
    __type    = "crypter"
    __version = "0.01"

    __pattern = r'http://(?:www\.)?freetexthost\.com/\w+'
    __config  = [("use_premium"       , "bool", "Use premium account if available"   , True),
                   ("use_subfolder"     , "bool", "Save package to subfolder"          , True),
                   ("subfolder_per_pack", "bool", "Create a subfolder for each package", True)]

    __description = """Freetexthost.com decrypter plugin"""
    __license     = "GPLv3"
    __authors     = [("stickell", "l.stickell@yahoo.it")]


    def getLinks(self):
        m = re.search(r'<div id="contentsinner">\s*(.+)<div class="viewcount">', self.html, re.S)
        if m is None:
            self.error(_("Unable to extract links"))
        links = m.group(1)
        return links.strip().split("<br />\r\n")
