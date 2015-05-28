# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadCrypter import DeadCrypter


class DuploadOrg(DeadCrypter):
    __name__    = "DuploadOrg"
    __type__    = "crypter"
    __version__ = "0.02"

    __pattern__ = r'http://(?:www\.)?dupload\.org/folder/\d+'
    __config__  = []

    __description__ = """Dupload.org folder decrypter plugin"""
    __license__     = "GPLv3"
    __authors__     = [("stickell", "l.stickell@yahoo.it")]
