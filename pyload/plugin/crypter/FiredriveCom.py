# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadCrypter import DeadCrypter


class FiredriveCom(DeadCrypter):
    __name    = "FiredriveCom"
    __type    = "crypter"
    __version = "0.03"

    __pattern = r'https?://(?:www\.)?(firedrive|putlocker)\.com/share/.+'
    __config  = []  #@TODO: Remove in 0.4.10

    __description = """Firedrive.com folder decrypter plugin"""
    __license     = "GPLv3"
    __authors     = [("Walter Purcaro", "vuolter@gmail.com")]
