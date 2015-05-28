# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadHoster import DeadHoster


class IfileIt(DeadHoster):
    __name    = "IfileIt"
    __type    = "hoster"
    __version = "0.29"

    __pattern = r'^unmatchable$'
    __config  = []  #@TODO: Remove in 0.4.10

    __description = """Ifile.it"""
    __license     = "GPLv3"
    __authors     = [("zoidberg", "zoidberg@mujmail.cz")]
