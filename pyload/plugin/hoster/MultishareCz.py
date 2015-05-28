# -*- coding: utf-8 -*-

import random

from pyload.plugin.internal.SimpleHoster import SimpleHoster


class MultishareCz(SimpleHoster):
    __name    = "MultishareCz"
    __type    = "hoster"
    __version = "0.40"

    __pattern = r'http://(?:www\.)?multishare\.cz/stahnout/(?P<ID>\d+)'
    __config  = [("use_premium", "bool", "Use premium account if available", True)]

    __description = """MultiShare.cz hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("zoidberg", "zoidberg@mujmail.cz")]


    SIZE_REPLACEMENTS = [('&nbsp;', '')]

    CHECK_TRAFFIC = True
    MULTI_HOSTER  = True

    INFO_PATTERN    = ur'(?:<li>Název|Soubor): <strong>(?P<N>[^<]+)</strong><(?:/li><li|br)>Velikost: <strong>(?P<S>[^<]+)</strong>'
    OFFLINE_PATTERN = ur'<h1>Stáhnout soubor</h1><p><strong>Požadovaný soubor neexistuje.</strong></p>'


    def handle_free(self, pyfile):
        self.download("http://www.multishare.cz/html/download_free.php", get={'ID': self.info['pattern']['ID']})


    def handle_premium(self, pyfile):
        self.download("http://www.multishare.cz/html/download_premium.php", get={'ID': self.info['pattern']['ID']})


    def handle_multi(self, pyfile):
        self.html = self.load('http://www.multishare.cz/html/mms_ajax.php', post={"link": pyfile.url}, decode=True)

        self.checkInfo()

        if not self.checkTrafficLeft():
            self.fail(_("Not enough credit left to download file"))

        self.download("http://dl%d.mms.multishare.cz/html/mms_process.php" % round(random.random() * 10000 * random.random()),
                      get={'u_ID'  : self.acc_info['u_ID'],
                           'u_hash': self.acc_info['u_hash'],
                           'link'  : pyfile.url},
                      disposition=True)
