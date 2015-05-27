# -*- coding: utf-8 -*-

try:
    from beaker.crypto.pbkdf2 import PBKDF2

except ImportError:
    import binascii
    from beaker.crypto.pbkdf2 import pbkdf2

    class PBKDF2(object):

        def __init__(self, passphrase, salt, iterations=1000):
            self.passphrase = passphrase
            self.salt = salt
            self.iterations = iterations


        def hexread(self, octets):
            return binascii.b2a_hex(pbkdf2(self.passphrase, self.salt, self.iterations, octets))

from pyload.utils import json_loads
from pyload.plugin.Account import Account


class OboomCom(Account):
    __name    = "OboomCom"
    __type    = "account"
    __version = "0.24"

    __description = """Oboom.com account plugin"""
    __license     = "GPLv3"
    __authors     = [("stanley", "stanley.foerster@gmail.com")]


    def loadAccountData(self, user, req):
        passwd = self.getAccountData(user)['password']
        salt   = passwd[::-1]
        pbkdf2 = PBKDF2(passwd, salt, 1000).hexread(16)

        result = json_loads(req.load("https://www.oboom.com/1/login", get={"auth": user, "pass": pbkdf2}))

        if not result[0] == 200:
            self.logWarning(_("Failed to log in: %s") % result[1])
            self.wrongPassword()

        return result[1]


    def loadAccountInfo(self, name, req):
        accountData = self.loadAccountData(name, req)

        userData = accountData['user']

        if userData['premium'] == "null":
            premium = False
        else:
            premium = True

        if userData['premium_unix'] == "null":
            validUntil = -1
        else:
            validUntil = float(userData['premium_unix'])

        traffic = userData['traffic']

        trafficLeft = traffic['current']
        maxTraffic = traffic['max']

        session = accountData['session']

        return {'premium'    : premium,
                'validuntil' : validUntil,
                'trafficleft': trafficLeft,
                'maxtraffic' : maxTraffic,
                'session'    : session}


    def login(self, user, data, req):
        self.loadAccountData(user, req)
