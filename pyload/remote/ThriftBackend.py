# -*- coding: utf-8 -*-

from os.path import exists

from pyload.manager.RemoteManager import BackendBase

from pyload.remote.thriftbackend.Processor import Processor
from pyload.remote.thriftbackend.Protocol import ProtocolFactory
from pyload.remote.thriftbackend.Socket import ServerSocket
from pyload.remote.thriftbackend.Transport import TransportFactory
#from pyload.remote.thriftbackend.Transport import TransportFactoryCompressed

from thrift.server import TServer


class ThriftBackend(BackendBase):

    def setup(self, host, port):
        processor = Processor(self.api)

        key = None
        cert = None

        if self.config.get("remote", "ssl"):
            if exists(self.config.get("ssl", "cert")) and exists(self.config.get("ssl", "key")):
                self.log.info(_("Using SSL ThriftBackend"))
                key = self.config.get("ssl", "key")
                cert = self.config.get("ssl", "cert")

        transport = ServerSocket(port, host, key, cert)


#        tfactory = TransportFactoryCompressed()
        tfactory = TransportFactory()
        pfactory = ProtocolFactory()

        self.server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
        #self.server = TNonblockingServer.TNonblockingServer(processor, transport, tfactory, pfactory)

        #server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

    def serve(self):
        self.server.serve()
