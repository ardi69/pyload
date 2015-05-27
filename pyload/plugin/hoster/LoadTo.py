# -*- coding: utf-8 -*-
#
# Test links:
#   http://www.load.to/JWydcofUY6/random.bin
#   http://www.load.to/oeSmrfkXE/random100.bin

import re

from pyload.plugin.captcha.SolveMedia import SolveMedia
from pyload.plugin.internal.SimpleHoster import SimpleHoster


class LoadTo(SimpleHoster):
    __name    = "LoadTo"
    __type    = "hoster"
    __version = "0.22"

    __pattern = r'http://(?:www\.)?load\.to/\w+'
    __config  = [("use_premium", "bool", "Use premium account if available", True)]

    __description = """Load.to hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("halfman", "Pulpan3@gmail.com"),
                       ("stickell", "l.stickell@yahoo.it")]


    NAME_PATTERN = r'<h1>(?P<N>.+)</h1>'
    SIZE_PATTERN = r'Size: (?P<S>[\d.,]+) (?P<U>[\w^_]+)'
    OFFLINE_PATTERN = r'>Can\'t find file'

    LINK_FREE_PATTERN = r'<form method="post" action="(.+?)"'
    WAIT_PATTERN = r'type="submit" value="Download \((\d+)\)"'

    URL_REPLACEMENTS = [(r'(\w)$', r'\1/')]


    def setup(self):
        self.multiDL = True
        self.chunkLimit = 1


    def handle_free(self, pyfile):
        # Search for Download URL
        m = re.search(self.LINK_FREE_PATTERN, self.html)
        if m is None:
            self.error(_("LINK_FREE_PATTERN not found"))

        self.link = m.group(1)

        # Set Timer - may be obsolete
        m = re.search(self.WAIT_PATTERN, self.html)
        if m:
            self.wait(m.group(1))

        # Load.to is using solvemedia captchas since ~july 2014:
        solvemedia  = SolveMedia(self)
        captcha_key = solvemedia.detect_key()

        if captcha_key:
            response, challenge = solvemedia.challenge(captcha_key)
            self.download(self.link,
                          post={'adcopy_challenge': challenge,
                                'adcopy_response' : response,
                                'returnUrl'       : pyfile.url})
