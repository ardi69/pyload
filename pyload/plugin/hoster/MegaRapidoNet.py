# -*- coding: utf-8 -*-

import random

from pyload.plugin.internal.MultiHoster import MultiHoster


def random_with_N_digits(n):
    rand = "0."
    not_zero = 0
    for _i in xrange(1, n + 1):
        r = random.randint(0, 9)
        if(r > 0):
            not_zero += 1
        rand += str(r)

    if not_zero > 0:
        return rand
    else:
        return random_with_N_digits(n)


class MegaRapidoNet(MultiHoster):
    __name    = "MegaRapidoNet"
    __type    = "hoster"
    __version = "0.02"

    __pattern = r'http://(?:www\.)?\w+\.megarapido\.net/\?file=\w+'
    __config  = [("use_premium", "bool", "Use premium account if available", True)]

    __description = """MegaRapido.net multi-hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("Kagenoshin", "kagenoshin@gmx.ch")]


    LINK_PREMIUM_PATTERN = r'<\s*?a[^>]*?title\s*?=\s*?["\'].*?download["\'][^>]*?href=["\']([^"\']+)'

    ERROR_PATTERN = r'<\s*?div[^>]*?class\s*?=\s*?["\']?alert-message error.*?>([^<]*)'


    def handle_premium(self, pyfile):
        self.html = self.load("http://megarapido.net/gerar.php",
                         post={'rand'     :random_with_N_digits(16),
                               'urllist'  : pyfile.url,
                               'links'    : pyfile.url,
                               'exibir'   : "normal",
                               'usar'     : "premium",
                               'user'     : self.account.getAccountInfo(self.user).get('sid', None),
                               'autoreset': ""})

        if "desloga e loga novamente para gerar seus links" in self.html.lower():
            self.error("You have logged in at another place")

        return super(MegaRapidoNet, self).handle_premium(pyfile)
