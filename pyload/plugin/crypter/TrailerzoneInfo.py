# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadCrypter import DeadCrypter


class TrailerzoneInfo(DeadCrypter):
    __name    = "TrailerzoneInfo"
    __type    = "crypter"
    __version = "0.03"

    __pattern = r'http://(?:www\.)?trailerzone\.info/.+'
    __config  = []  #@TODO: Remove in 0.4.10

    __description = """TrailerZone.info decrypter plugin"""
    __license     = "GPLv3"
    __authors     = [("godofdream", "soilfiction@gmail.com")]
