# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadHoster import DeadHoster


class SockshareCom(DeadHoster):
    __name    = "SockshareCom"
    __type    = "hoster"
    __version = "0.05"

    __pattern = r'http://(?:www\.)?sockshare\.com/(mobile/)?(file|embed)/(?P<ID>\w+)'
    __config  = []  #@TODO: Remove in 0.4.10

    __description = """Sockshare.com hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("jeix", "jeix@hasnomail.de"),
                       ("stickell", "l.stickell@yahoo.it"),
                       ("Walter Purcaro", "vuolter@gmail.com")]
