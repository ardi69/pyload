# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadHoster import DeadHoster


class WuploadCom(DeadHoster):
    __name    = "WuploadCom"
    __type    = "hoster"
    __version = "0.23"

    __pattern = r'http://(?:www\.)?wupload\..+?/file/((\w+/)?\d+)(/.*)?'
    __config  = []  #@TODO: Remove in 0.4.10

    __description = """Wupload.com hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("jeix", "jeix@hasnomail.de"),
                       ("Paul King", "")]
