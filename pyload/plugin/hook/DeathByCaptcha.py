# -*- coding: utf-8 -*-

from __future__ import with_statement

import base64
import re
import time

import pycurl

from pyload.utils import json_loads
from pyload.network.HTTPRequest import BadHeader
from pyload.network.RequestFactory import getRequest
from pyload.plugin.Hook import Hook, threaded


class DeathByCaptchaException(Exception):
    DBC_ERRORS = {'not-logged-in': 'Access denied, check your credentials',
                  'invalid-credentials': 'Access denied, check your credentials',
                  'banned': 'Access denied, account is suspended',
                  'insufficient-funds': 'Insufficient account balance to decrypt CAPTCHA',
                  'invalid-captcha': 'CAPTCHA is not a valid image',
                  'service-overload': 'CAPTCHA was rejected due to service overload, try again later',
                  'invalid-request': 'Invalid request',
                  'timed-out': 'No CAPTCHA solution received in time'}


    def __init__(self, err):
        self.err = err


    def getCode(self):
        return self.err


    def getDesc(self):
        if self.err in self.DBC_ERRORS.keys():
            return self.DBC_ERRORS[self.err]
        else:
            return self.err


    def __str__(self):
        return "<DeathByCaptchaException %s>" % self.err


    def __repr__(self):
        return "<DeathByCaptchaException %s>" % self.err


class DeathByCaptcha(Hook):
    __name    = "DeathByCaptcha"
    __type    = "hook"
    __version = "0.06"

    __config = [("username", "str", "Username", ""),
                ("passkey", "password", "Password", ""),
                ("force", "bool", "Force DBC even if client is connected", False)]

    __description = """Send captchas to DeathByCaptcha.com"""
    __license     = "GPLv3"
    __authors     = [("RaNaN"   , "RaNaN@pyload.org"),
                     ("zoidberg", "zoidberg@mujmail.cz")]


    API_URL = "http://api.dbcapi.me/api/"


    def activate(self):
        if self.getConfig('ssl'):
            self.API_URL = self.API_URL.replace("http://", "https://")


    def api_response(self, api="captcha", post=False, multipart=False):
        req = getRequest()
        req.c.setopt(pycurl.HTTPHEADER, ["Accept: application/json", "User-Agent: pyLoad %s" % self.core.version])

        if post:
            if not isinstance(post, dict):
                post = {}
            post.update({"username": self.getConfig('username'),
                         "password": self.getConfig('passkey')})

        res = None
        try:
            json = req.load("%s%s" % (self.API_URL, api),
                            post=post,
                            multipart=multipart)
            self.logDebug(json)
            res = json_loads(json)

            if "error" in res:
                raise DeathByCaptchaException(res['error'])
            elif "status" not in res:
                raise DeathByCaptchaException(str(res))

        except BadHeader, e:
            if 403 == e.code:
                raise DeathByCaptchaException('not-logged-in')
            elif 413 == e.code:
                raise DeathByCaptchaException('invalid-captcha')
            elif 503 == e.code:
                raise DeathByCaptchaException('service-overload')
            elif e.code in (400, 405):
                raise DeathByCaptchaException('invalid-request')
            else:
                raise

        finally:
            req.close()

        return res


    def getCredits(self):
        res = self.api_response("user", True)

        if 'is_banned' in res and res['is_banned']:
            raise DeathByCaptchaException('banned')
        elif 'balance' in res and 'rate' in res:
            self.info.update(res)
        else:
            raise DeathByCaptchaException(res)


    def getStatus(self):
        res = self.api_response("status", False)

        if 'is_service_overloaded' in res and res['is_service_overloaded']:
            raise DeathByCaptchaException('service-overload')


    def submit(self, captcha, captchaType="file", match=None):
        #@NOTE: Workaround multipart-post bug in HTTPRequest.py
        if re.match("^\w*$", self.getConfig('passkey')):
            multipart = True
            data = (pycurl.FORM_FILE, captcha)
        else:
            multipart = False
            with open(captcha, 'rb') as f:
                data = f.read()
            data = "base64:" + base64.b64encode(data)

        res = self.api_response("captcha", {"captchafile": data}, multipart)

        if "captcha" not in res:
            raise DeathByCaptchaException(res)
        ticket = res['captcha']

        for _i in xrange(24):
            time.sleep(5)
            res = self.api_response("captcha/%d" % ticket, False)
            if res['text'] and res['is_correct']:
                break
        else:
            raise DeathByCaptchaException('timed-out')

        result = res['text']
        self.logDebug("Result %s : %s" % (ticket, result))

        return ticket, result


    def captchaTask(self, task):
        if "service" in task.data:
            return False

        if not task.isTextual():
            return False

        if not self.getConfig('username') or not self.getConfig('passkey'):
            return False

        if self.core.isClientConnected() and not self.getConfig('force'):
            return False

        try:
            self.getStatus()
            self.getCredits()
        except DeathByCaptchaException, e:
            self.logError(e.getDesc())
            return False

        balance, rate = self.info['balance'], self.info['rate']
        self.logInfo(_("Account balance"),
                     _("US$%.3f (%d captchas left at %.2f cents each)") % (balance / 100,
                                                                           balance // rate, rate))

        if balance > rate:
            task.handler.append(self)
            task.data['service'] = self.__name__
            task.setWaiting(180)
            self._processCaptcha(task)


    def captchaInvalid(self, task):
        if task.data['service'] == self.__name__ and "ticket" in task.data:
            try:
                res = self.api_response("captcha/%d/report" % task.data['ticket'], True)

            except DeathByCaptchaException, e:
                self.logError(e.getDesc())

            except Exception, e:
                self.logError(e)


    @threaded
    def _processCaptcha(self, task):
        c = task.captchaFile
        try:
            ticket, result = self.submit(c)
        except DeathByCaptchaException, e:
            task.error = e.getCode()
            self.logError(e.getDesc())
            return

        task.data['ticket'] = ticket
        task.setResult(result)
