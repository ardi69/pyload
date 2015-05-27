# -*- coding: utf-8 -*-

import re

from pyload.plugin.internal.SimpleHoster import SimpleHoster


class VimeoCom(SimpleHoster):
    __name    = "VimeoCom"
    __type    = "hoster"
    __version = "0.04"

    __pattern = r'https?://(?:www\.)?(player\.)?vimeo\.com/(video/)?(?P<ID>\d+)'
    __config  = [("use_premium", "bool"                       , "Use premium account if available" , True     ),
                   ("quality"    , "Lowest;Mobile;SD;HD;Highest", "Quality"                          , "Highest"),
                   ("original"   , "bool"                       , "Try to download the original file", True     )]

    __description = """Vimeo.com hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("Walter Purcaro", "vuolter@gmail.com")]


    NAME_PATTERN         = r'<title>(?P<N>.+) on Vimeo<'
    OFFLINE_PATTERN      = r'class="exception_header"'
    TEMP_OFFLINE_PATTERN = r'Please try again in a few minutes.<'

    URL_REPLACEMENTS = [(__pattern + ".*", r'https://www.vimeo.com/\g<ID>')]

    COOKIES = [("vimeo.com", "language", "en")]


    def setup(self):
        self.resumeDownload = True
        self.multiDL        = True
        self.chunkLimit     = -1


    def handle_free(self, pyfile):
        password = self.getPassword()

        if self.js and 'class="btn iconify_down_b"' in self.html:
            html    = self.js.eval(self.load(pyfile.url, get={'action': "download", 'password': password}, decode=True))
            pattern = r'href="(?P<URL>http://vimeo\.com.+?)".*?\>(?P<QL>.+?) '
        else:
            html    = self.load("https://player.vimeo.com/video/" + self.info['pattern']['ID'], get={'password': password})
            pattern = r'"(?P<QL>\w+)":{"profile".*?"(?P<URL>http://pdl\.vimeocdn\.com.+?)"'

        link = dict((l.group('QL').lower(), l.group('URL')) for l in re.finditer(pattern, html))

        if self.getConfig('original'):
            if "original" in link:
                self.link = link[q]
                return
            else:
                self.logInfo(_("Original file not downloadable"))

        quality = self.getConfig('quality')
        if quality == "Highest":
            qlevel = ("hd", "sd", "mobile")
        elif quality == "Lowest":
            qlevel = ("mobile", "sd", "hd")
        else:
            qlevel = quality.lower()

        for q in qlevel:
            if q in link:
                self.link = link[q]
                return
            else:
                self.logInfo(_("No %s quality video found") % q.upper())
        else:
            self.fail(_("No video found!"))
