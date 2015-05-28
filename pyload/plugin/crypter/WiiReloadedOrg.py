# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadCrypter import DeadCrypter


class WiiReloadedOrg(DeadCrypter):
    __name    = "WiiReloadedOrg"
    __type    = "crypter"
    __version = "0.11"

    __pattern = r'http://(?:www\.)?wii-reloaded\.org/protect/get\.php\?i=.+'
    __config  = []  #@TODO: Remove in 0.4.10

    __description = """Wii-Reloaded.org decrypter plugin"""
    __license     = "GPLv3"
    __authors     = [("hzpz", "")]
