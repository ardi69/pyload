# -*- coding: utf-8 -*-

from pyload.plugin.internal.MultiHoster import MultiHoster


class RehostTo(MultiHoster):
    __name__    = "RehostTo"
    __type__    = "hoster"
    __version__ = "0.21"

    __pattern__ = r'https?://.*rehost\.to\..+'
    __config__  = [("use_premium", "bool", "Use premium account if available", True)]

    __description__ = """Rehost.com multi-hoster plugin"""
    __license__     = "GPLv3"
    __authors__     = [("RaNaN", "RaNaN@pyload.org")]


    def handle_premium(self, pyfile):
        self.download("http://rehost.to/process_download.php",
                      get={'user': "cookie",
                           'pass': self.account.getAccountInfo(self.user)['session'],
                           'dl'  : pyfile.url},
                      disposition=True)
