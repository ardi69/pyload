# -*- coding: utf-8 -*-

from pyload.plugin.internal.MultiHoster import MultiHoster


class RehostTo(MultiHoster):
    __name    = "RehostTo"
    __type    = "hoster"
    __version = "0.21"

    __pattern = r'https?://.*rehost\.to\..+'
    __config  = [("use_premium", "bool", "Use premium account if available", True)]

    __description = """Rehost.com multi-hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("RaNaN", "RaNaN@pyload.org")]


    def handle_premium(self, pyfile):
        self.download("http://rehost.to/process_download.php",
                      get={'user': "cookie",
                           'pass': self.account.getAccountInfo(self.user)['session'],
                           'dl'  : pyfile.url},
                      disposition=True)
