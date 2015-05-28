# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadCrypter import DeadCrypter


class MBLinkInfo(DeadCrypter):
    __name    = "MBLinkInfo"
    __type    = "crypter"
    __version = "0.03"

    __pattern = r'http://(?:www\.)?mblink\.info/?\?id=(\d+)'
    __config  = []  #@TODO: Remove in 0.4.10

    __description = """MBLink.info decrypter plugin"""
    __license     = "GPLv3"
    __authors     = [("Gummibaer", "Gummibaer@wiki-bierkiste.de"),
                       ("stickell", "l.stickell@yahoo.it")]
