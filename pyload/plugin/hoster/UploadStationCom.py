# -*- coding: utf-8 -*-

from pyload.plugin.internal.DeadHoster import DeadHoster


class UploadStationCom(DeadHoster):
    __name    = "UploadStationCom"
    __type    = "hoster"
    __version = "0.52"

    __pattern = r'http://(?:www\.)?uploadstation\.com/file/(?P<ID>\w+)'
    __config  = []  #@TODO: Remove in 0.4.10

    __description = """UploadStation.com hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("fragonib", "fragonib[AT]yahoo[DOT]es"),
                       ("zoidberg", "zoidberg@mujmail.cz")]
