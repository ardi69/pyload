# -*- coding: utf-8 -*-
# @author: jeix

import os
import select
import socket
import struct
import time

from pyload.plugin.Plugin import Abort


class XDCCRequest(object):

    def __init__(self, timeout=30, proxies={}):

        self.proxies = proxies
        self.timeout = timeout

        self.filesize = 0
        self.recv = 0
        self.speed = 0

        self.abort = False


    def createSocket(self):
        # proxytype = None
        # proxy = None
        # if self.proxies.has_key("socks5"):
            # proxytype = socks.PROXY_TYPE_SOCKS5
            # proxy = self.proxies['socks5']
        # elif self.proxies.has_key("socks4"):
            # proxytype = socks.PROXY_TYPE_SOCKS4
            # proxy = self.proxies['socks4']
        # if proxytype:
            # sock = socks.socksocket()
            # t = _parse_proxy(proxy)
            # sock.setproxy(proxytype, addr=t[3].split(":")[0], port=int(t[3].split(":")[1]), username=t[1], password=t[2])
        # else:
            # sock = socket.socket()
        # return sock

        return socket.socket()


    def download(self, ip, port, filename, irc, progress=None):

        ircbuffer = ""
        lastUpdate = time.time()
        cumRecvLen = 0

        dccsock = self.createSocket()

        dccsock.settimeout(self.timeout)
        dccsock.connect((ip, port))

        if os.path.exists(filename):
            i = 0
            nameParts = filename.rpartition(".")
            while True:
                newfilename = "%s-%d%s%s" % (nameParts[0], i, nameParts[1], nameParts[2])
                i += 1

                if not os.path.exists(newfilename):
                    filename = newfilename
                    break

        fh = open(filename, "wb")

        # recv loop for dcc socket
        while True:
            if self.abort:
                dccsock.close()
                fh.close()
                os.remove(filename)
                raise Abort

            self._keepAlive(irc, ircbuffer)

            data = dccsock.recv(4096)
            dataLen = len(data)
            self.recv += dataLen

            cumRecvLen += dataLen

            now = time.time()
            timespan = now - lastUpdate
            if timespan > 1:
                self.speed = cumRecvLen / timespan
                cumRecvLen = 0
                lastUpdate = now

                if progress:
                    progress(self.percent)

            if not data:
                break

            fh.write(data)

            # acknowledge data by sending number of recceived bytes
            dccsock.send(struct.pack('!I', self.recv))

        dccsock.close()
        fh.close()

        return filename


    def _keepAlive(self, sock, *readbuffer):
        fdset = select.select([sock], [], [], 0)
        if sock not in fdset[0]:
            return

        readbuffer += sock.recv(1024)
        temp = readbuffer.split("\n")
        readbuffer = temp.pop()

        for line in temp:
            line  = line.rstrip()
            first = line.split()
            if first[0] == "PING":
                sock.send("PONG %s\r\n" % first[1])


    def abortDownloads(self):
        self.abort = True


    @property
    def size(self):
        return self.filesize


    @property
    def arrived(self):
        return self.recv


    @property
    def percent(self):
        return (self.recv * 100) / self.filesize if elf.filesize else 0


    def close(self):
        pass
