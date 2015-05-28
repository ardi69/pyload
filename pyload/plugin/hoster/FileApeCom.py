# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadHoster import DeadHoster


class FileApeCom(DeadHoster):
    __name    = "FileApeCom"
    __type    = "hoster"
    __version = "0.12"

    __pattern = r'http://(?:www\.)?fileape\.com/(index\.php\?act=download\&id=|dl/)\w+'
    __config  = []  #@TODO: Remove in 0.4.10

    __description = """FileApe.com hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("espes", "")]
