# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadCrypter import DeadCrypter


class DuploadOrg(DeadCrypter):
    __name    = "DuploadOrg"
    __type    = "crypter"
    __version = "0.02"

    __pattern = r'http://(?:www\.)?dupload\.org/folder/\d+'
    __config  = []  #@TODO: Remove in 0.4.10

    __description = """Dupload.org folder decrypter plugin"""
    __license     = "GPLv3"
    __authors     = [("stickell", "l.stickell@yahoo.it")]
