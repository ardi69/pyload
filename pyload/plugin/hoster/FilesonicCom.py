# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadHoster import DeadHoster


class FilesonicCom(DeadHoster):
    __name    = "FilesonicCom"
    __type    = "hoster"
    __version = "0.35"

    __pattern = r'http://(?:www\.)?filesonic\.com/file/\w+'
    __config  = []  #@TODO: Remove in 0.4.10

    __description = """Filesonic.com hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("jeix", "jeix@hasnomail.de"),
                       ("paulking", "")]
