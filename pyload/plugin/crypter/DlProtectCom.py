# -*- coding: utf-8 -*-

import base64
import re
import time

from pyload.plugin.internal.SimpleCrypter import SimpleCrypter


class DlProtectCom(SimpleCrypter):
    __name    = "DlProtectCom"
    __type    = "crypter"
    __version = "0.03"

    __pattern = r'https?://(?:www\.)?dl-protect\.com/((en|fr)/)?\w+'
    __config  = [("use_premium"       , "bool", "Use premium account if available"   , True),
                   ("use_subfolder"     , "bool", "Save package to subfolder"          , True),
                   ("subfolder_per_pack", "bool", "Create a subfolder for each package", True)]

    __description = """Dl-protect.com decrypter plugin"""
    __license     = "GPLv3"
    __authors     = [("Walter Purcaro", "vuolter@gmail.com")]


    COOKIES = [("dl-protect.com", "l", "en")]

    OFFLINE_PATTERN = r'Unfortunately, the link you are looking for is not found'


    def getLinks(self):
        # Direct link with redirect
        if not re.match(r"https?://(?:www\.)?dl-protect\.com/.+", self.req.http.lastEffectiveURL):
            return [self.req.http.lastEffectiveURL]

        post_req = {'key'       : re.search(r'name="key" value="(.+?)"', self.html).group(1),
                    'submitform': ""}

        if "Please click on continue to see the content" in self.html:
            post_req['submitform'] = "Continue"
            self.wait(2)

        else:
            mstime  = int(round(time.time() * 1000))
            b64time = "_" + base64.urlsafe_b64encode(str(mstime)).replace("=", "%3D")

            post_req.update({'i'         : b64time,
                             'submitform': "Decrypt+link"})

            if "Password :" in self.html:
                post_req['pwd'] = self.getPassword()

            if "Security Code" in self.html:
                captcha_id   = re.search(r'/captcha\.php\?uid=(.+?)"', self.html).group(1)
                captcha_url  = "http://www.dl-protect.com/captcha.php?uid=" + captcha_id
                captcha_code = self.decryptCaptcha(captcha_url, imgtype="gif")

                post_req['secure'] = captcha_code

        self.html = self.load(self.pyfile.url, post=post_req)

        for errmsg in ("The password is incorrect", "The security code is incorrect"):
            if errmsg in self.html:
                self.fail(_(errmsg[1:]))

        return re.findall(r'<a href="([^/].+?)" target="_blank">', self.html)
