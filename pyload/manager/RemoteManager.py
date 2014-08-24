# -*- coding: utf-8 -*-

from threading import Thread
from traceback import print_exc


class BackendBase(Thread):

    def __init__(self, manager):
        Thread.__init__(self)

        self.m = manager

        self.enabled = True
        self.running = False

    def run(self):
        self.running = True
        try:
            self.serve()
        except Exception, e:
            self.m.log.error(_("Remote backend error: %s") % e)
            if self.m.core.debug:
                print_exc()
        finally:
            self.running = False

    def setup(self, host, port):
        pass

    def checkDeps(self):
        return True

    def serve(self):
        pass

    def shutdown(self):
        pass

    def stop(self):
        self.enabled = False# set flag and call shutdowm message, so thread can react
        self.shutdown()


class RemoteManager:
    available = []

    def __init__(self, core):
        self.core = core
        self.config = core.config
        self.log = core.log
        self.backends = []

        if self.core.remote:
            self.available.append("ThriftBackend")
#        else:
#            self.available.append("SocketBackend")


    def startBackends(self):
        host = self.config.get("remote", "host")
        port = self.config.get("remote", "port")

        for b in self.available:
            klass = getattr(__import__("pyload.remote.%s" % b, globals(), locals(), [b], -1), b)
            backend = klass(self)
            if not backend.checkDeps():
                continue
            try:
                backend.setup(host, port)
                self.log.info(_("Starting %(name)s: %(addr)s:%(port)s") % {'name': b, 'addr': host, 'port': port})
            except Exception, e:
                self.log.error(_("Failed loading backend %(name)s | %(error)s") % {'name': b, 'error': str(e)})
                if self.core.debug:
                    print_exc()
            else:
                backend.start()
                self.backends.append(backend)

            port += 1
