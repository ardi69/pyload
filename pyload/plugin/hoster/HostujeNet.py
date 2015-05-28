# -*- coding: utf-8 -*-

import re

from pyload.plugin.internal.SimpleHoster import SimpleHoster


class HostujeNet(SimpleHoster):
    __name    = "HostujeNet"
    __type    = "hoster"
    __version = "0.01"

    __pattern = r'http://(?:www\.)?hostuje\.net/\w+'

    __description = """Hostuje.net hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("GammaC0de", None)]


    NAME_PATTERN    = r'<input type="hidden" name="name" value="(?P<N>.+?)">'
    SIZE_PATTERN    = r'<b>Rozmiar:</b> (?P<S>[\d.,]+) (?P<U>[\w^_]+)<br>'
    OFFLINE_PATTERN = ur'Podany plik nie został odnaleziony\.\.\.'


    def setup(self):
        self.multiDL    = True
        self.chunkLimit = 1


    def handle_free(self, pyfile):
        m = re.search(r'<script src="([\w^_]+.php)"></script>', self.html)
        if m:
            jscript = self.load("http://hostuje.net/" + m.group(1))
            m = re.search(r"\('(\w+\.php\?i=\w+)'\);", jscript)
            if m:
                self.load("http://hostuje.net/" + m.group(1))
            else:
                self.error(_("unexpected javascript format"))
        else:
            self.error(_("script not found"))

        action, inputs = self.parseHtmlForm(pyfile.url.replace(".", "\.").replace( "?", "\?"))
        if not action:
            self.error(_("form not found"))

        self.download(action, post=inputs)
