# -*- coding: utf-8 -*-

from pyload.utils import json_loads
from pyload.network.RequestFactory import getURL
from pyload.plugins.internal.MultiHoster import MultiHoster


class MultiDebridCom(MultiHoster):
    __name__ = "MultiDebridCom"
    __type__ = "addon"
    __version__ = "0.01"

    __config__ = [("activated", "bool", "Activated", False),
                  ("hosterListMode", "all;listed;unlisted", "Use for hosters (if supported)", "all"),
                  ("hosterList", "str", "Hoster list (comma separated)", ""),
                  ("unloadFailing", "bool", "Revert to standard download if download fails", False),
                  ("interval", "int", "Reload interval in hours (0 to disable)", 24)]

    __description__ = """Multi-debrid.com addon plugin"""
    __author_name__ = "stickell"
    __author_mail__ = "l.stickell@yahoo.it"


    def getHoster(self):
        json_data = getURL('http://multi-debrid.com/api.php?hosts', decode=True)
        self.logDebug('JSON data: ' + json_data)
        json_data = json_loads(json_data)

        return json_data['hosts']
