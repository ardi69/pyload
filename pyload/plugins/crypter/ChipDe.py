# -*- coding: utf-8 -*-

import re
from pyload.plugins.Crypter import Crypter


class ChipDe(Crypter):
    __name__ = "ChipDe"
    __type__ = "crypter"
    __version__ = "0.1"

    __pattern__ = r'http://(?:www\.)?chip.de/video/.*\.html'

    __description__ = """Chip.de decrypter plugin"""
    __author_name__ = "4Christopher"
    __author_mail__ = "4Christopher@gmx.de"


    def decrypt(self, pyfile):
        self.html = self.load(pyfile.url)
        m = re.search(r'"(http://video.chip.de/\d+?/.*)"', self.html)
        if m:
            self.urls = [m.group(1)]
            self.logDebug('The file URL is %s' % self.urls[0])
        else:
            self.error("Failed to find the URL")
