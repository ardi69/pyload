# -*- coding: utf-8 -*-

import sys
from socket import error
from os.path import join
from traceback import print_exc

from thrift.transport import TTransport
#from thrift.transport.TZlibTransport import TZlibTransport
from module.remote.thriftbackend.Socket import Socket
from module.remote.thriftbackend.Protocol import Protocol

# modules should import ttypes from here, when want to avoid importing API

from module.remote.thriftbackend.thriftgen.pyload import Pyload
from module.remote.thriftbackend.thriftgen.pyload.ttypes import *


ConnectionClosed = TTransport.TTransportException


class WrongLogin(Exception):
    pass


class NoConnection(Exception):
    pass


class NoSSL(Exception):
    pass


class ThriftClient:

    def __init__(self, host="localhost", port=7227, user="", password=""):

        self.createConnection(host, port)
        try:
            self.transport.open()
        except error, e:
            if e.args and e.args[0] in (111, 10061):
                raise NoConnection
            else:
                print_exc()
                raise NoConnection

        try:
            correct = self.client.login(user, password)
        except error, e:
            if e.args and e.args[0] == 104:
                #connection reset by peer, probably wants ssl
                try:
                    self.createConnection(host, port, True)
                    #set timeout or a ssl socket will block when querying none ssl server
                    self.socket.setTimeout(10)

                except ImportError:
                    #@TODO untested
                    raise NoSSL
                try:
                   self.transport.open()
                   correct = self.client.login(user, password)
                finally:
                    self.socket.setTimeout(None)
            elif e.args and e.args[0] == 32:
                raise NoConnection
            else:
                print_exc()
                raise NoConnection

        if not correct:
            self.transport.close()
            raise WrongLogin

    def createConnection(self, host, port, ssl=False):
        self.socket = Socket(host, port, ssl)
        self.transport = TTransport.TBufferedTransport(self.socket)
#        self.transport = TZlibTransport(TTransport.TBufferedTransport(self.socket))

        protocol = Protocol(self.transport)
        self.client = Pyload.Client(protocol)

    def close(self):
        self.transport.close()

    def __getattr__(self, item):
        return getattr(self.client, item)
