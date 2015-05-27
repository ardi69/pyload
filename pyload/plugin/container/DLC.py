# -*- coding: utf-8 -*-

from __future__ import with_statement

import re
import xml.dom.minidom

import Crypto

from pyload.plugin.Container import Container
from pyload.utils import decode, fs_encode


class DLC(Container):
    __name    = "DLC"
    __type    = "container"
    __version = "0.24"

    __pattern = r'.+\.dlc$'

    __description = """DLC container decrypter plugin"""
    __license     = "GPLv3"
    __authors     = [("RaNaN", "RaNaN@pyload.org"),
                       ("spoob", "spoob@pyload.org"),
                       ("mkaay", "mkaay@mkaay.de"),
                       ("Schnusch", "Schnusch@users.noreply.github.com"),
                       ("Walter Purcaro", "vuolter@gmail.com")]


    KEY     = "cb99b5cbc24db398"
    IV      = "9bc24cb995cb8db3"
    API_URL = "http://service.jdownloader.org/dlcrypt/service.php?srcType=dlc&destType=pylo&data=%s"


    def decrypt(self, pyfile):
        fs_filename = fs_encode(pyfile.url.strip())
        with open(fs_filename) as dlc:
            data = dlc.read().strip()

        data += '=' * (-len(data) % 4)

        dlc_key     = data[-88:]
        dlc_data    = data[:-88].decode('base64')
        dlc_content = self.load(self.API_URL % dlc_key)

        try:
            rc = re.search(r'<rc>(.+)</rc>', dlc_content, re.S).group(1).decode('base64')

        except AttributeError:
            self.fail(_("Container is corrupted"))

        key = iv = Crypto.Cipher.AES.new(self.KEY, Crypto.Cipher.AES.MODE_CBC, self.IV).decrypt(rc)

        self.data     = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CBC, iv).decrypt(dlc_data).decode('base64')
        self.packages = [(name or pyfile.name, links, name or pyfile.name) \
                         for name, links in self.getPackages()]


    def getPackages(self):
        root    = xml.dom.minidom.parseString(self.data).documentElement
        content = root.getElementsByTagName("content")[0]
        return self.parsePackages(content)


    def parsePackages(self, startNode):
        return [(decode(node.getAttribute("name")).decode('base64'), self.parseLinks(node)) \
                for node in startNode.getElementsByTagName("package")]


    def parseLinks(self, startNode):
        return [node.getElementsByTagName("url")[0].firstChild.data.decode('base64') \
                for node in startNode.getElementsByTagName("file")]
