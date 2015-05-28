# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadCrypter import DeadCrypter


class HotfileCom(DeadCrypter):
    __name    = "HotfileCom"
    __type    = "crypter"
    __version = "0.30"

    __pattern = r'https?://(?:www\.)?hotfile\.com/list/\w+/\w+'
    __config  = []  #@TODO: Remove in 0.4.10

    __description = """Hotfile.com folder decrypter plugin"""
    __license     = "GPLv3"
    __authors     = [("RaNaN", "RaNaN@pyload.org")]
