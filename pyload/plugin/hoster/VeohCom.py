# -*- coding: utf-8 -*-

import re

from pyload.plugin.internal.SimpleHoster import SimpleHoster


class VeohCom(SimpleHoster):
    __name    = "VeohCom"
    __type    = "hoster"
    __version = "0.22"

    __pattern = r'http://(?:www\.)?veoh\.com/(tv/)?(watch|videos)/(?P<ID>v\w+)'
    __config  = [("use_premium", "bool"         , "Use premium account if available", True  ),
                   ("quality"    , "Low;High;Auto", "Quality"                         , "Auto")]

    __description = """Veoh.com hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("Walter Purcaro", "vuolter@gmail.com")]


    NAME_PATTERN    = r'<meta name="title" content="(?P<N>.*?)"'
    OFFLINE_PATTERN = r'>Sorry, we couldn\'t find the video you were looking for'

    URL_REPLACEMENTS = [(__pattern + ".*", r'http://www.veoh.com/watch/\g<ID>')]

    COOKIES = [("veoh.com", "lassieLocale", "en")]


    def setup(self):
        self.resumeDownload = True
        self.multiDL        = True
        self.chunkLimit     = -1


    def handle_free(self, pyfile):
        quality = self.getConfig('quality')
        if quality == "Auto":
            quality = ("High", "Low")

        for q in quality:
            pattern = r'"fullPreviewHash%sPath":"(.+?)"' % q
            m = re.search(pattern, self.html)
            if m:
                pyfile.name += ".mp4"
                self.link = m.group(1).replace("\\", "")
                return
            else:
                self.logInfo(_("No %s quality video found") % q.upper())
        else:
            self.fail(_("No video found!"))
