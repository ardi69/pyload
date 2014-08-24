# -*- coding: utf-8 -*-

from threading import Lock

from pyload.network.Browser import Browser
from pyload.network.Bucket import Bucket
from pyload.network.HTTPRequest import HTTPRequest
from pyload.network.CookieJar import CookieJar
from pyload.network.XDCCRequest import XDCCRequest


class RequestFactory:

    def __init__(self, core):
        self.lock = Lock()
        self.core = core
        self.config = core.config
        self.bucket = Bucket()
        self.updateBucket()
        self.cookiejars = {}

    def iface(self):
        return self.config.get("download", "interface")

    def getRequest(self, pluginName, account=None, type="HTTP"):
        self.lock.acquire()

        if type == "XDCC":
            return XDCCRequest(proxies=self.getProxies())

        req = Browser(self.bucket, self.getOptions())

        if account:
            cj = self.getCookieJar(pluginName, account)
            req.setCookieJar(cj)
        else:
            req.setCookieJar(CookieJar(pluginName))

        self.lock.release()
        return req

    def getHTTPRequest(self, **kwargs):
        """ returns a http request, dont forget to close it ! """
        options = self.getOptions()
        options.update(kwargs) # submit kwargs as additional options
        return HTTPRequest(CookieJar(None), options)

    def getURL(self, *args, **kwargs):
        """ see HTTPRequest for argument list """
        h = HTTPRequest(None, self.getOptions())
        try:
            rep = h.load(*args, **kwargs)
        finally:
            h.close()

        return rep

    def getCookieJar(self, pluginName, account=None):
        if (pluginName, account) in self.cookiejars:
            return self.cookiejars[(pluginName, account)]

        cj = CookieJar(pluginName, account)
        self.cookiejars[(pluginName, account)] = cj
        return cj

    def getProxies(self):
        """ returns a proxy list for the request classes """
        if not self.config.get("proxy", "activated"):
            return {}
        else:
            type = "http"
            setting = self.config.get("proxy", "type").lower()
            if setting == "socks4":
                type = "socks4"
            elif setting == "socks5":
                type = "socks5"

            username = None
            if self.config.get("proxy", "username") and self.config.get("proxy", "username").lower() != "none":
                username = self.config.get("proxy", "username")

            pw = None
            if self.config.get("proxy", "password") and self.config.get("proxy", "password").lower() != "none":
                pw = self.config.get("proxy", "password")

            return {
                'type': type,
                'address': self.config.get("proxy", "host"),
                'port': self.config.get("proxy", "port"),
                'username': username,
                'password': pw,
                }

    def getOptions(self):
        """ returns options needed for pycurl """
        return {'interface': self.iface(),
                'proxies': self.getProxies(),
                'ipv6': self.config.get("download", "ipv6")}

    def updateBucket(self):
        """ set values in the bucket according to settings """
        if not self.config.get("download", "limit_speed"):
            self.bucket.setRate(-1)
        else:
            self.bucket.setRate(self.config.get("download", "max_speed") * 1024)


def getURL(*args, **kwargs):
    return pycore.requestFactory.getURL(*args, **kwargs)


def getRequest(*args, **kwargs):
    return pycore.requestFactory.getHTTPRequest()
