# -*- coding: utf-8 -*-
# @author: RaNaN

from __future__ import with_statement

import Queue
import os
import sys
import threading
import time
import traceback
import pprint
import types

from pyload.Api import OnlineStatus
from pyload.Datatype import PyFile
from pyload.plugin.Plugin import Abort, Fail, Reconnect, Retry, SkipDownload
from pyload.utils.packagetools import parseNames
from pyload.utils import fs_join


class PluginThread(threading.Thread):
    """Abstract base class for thread types"""

    def __init__(self, manager):
        """Constructor"""
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.m = manager  #: thread manager


    def writeDebugReport(self, pyfile):
        dump_name = "debug_%s_%s.zip" % (pyfile.pluginname, time.strftime("%d-%m-%Y_%H-%M-%S"))
        dump = self.getDebugDump(pyfile)

        try:
            import zipfile

            zip = zipfile.ZipFile(dump_name, "w")

            for f in os.listdir(os.path.join("tmp", pyfile.pluginname)):
                try:
                    # avoid encoding errors
                    zip.write(os.path.join("tmp", pyfile.pluginname, f), fs_join(pyfile.pluginname, f))
                except Exception:
                    pass

            info = zipfile.ZipInfo(fs_join(pyfile.pluginname, "debug_Report.txt"), time.gmtime())
            info.external_attr = 0644 << 16L  #: change permissions

            zip.writestr(info, dump)
            zip.close()

            if not os.stat(dump_name).st_size:
                raise Exception("Empty Zipfile")

        except Exception, e:
            self.m.log.debug("Error creating zip file: %s" % e)

            dump_name = dump_name.replace(".zip", ".txt")
            with open(dump_name, "wb") as f:
                f.write(dump)

        self.m.core.log.info("Debug Report written to %s" % dump_name)


    def getDebugDump(self, pyfile):
        dump = "pyLoad %s Debug Report of %s %s \n\nTRACEBACK:\n %s \n\nFRAMESTACK:\n" % (
            self.m.core.api.getServerVersion(), pyfile.pluginname, pyfile.plugin.__version, traceback.format_exc())

        tb = sys.exc_info()[2]
        stack = []
        while tb:
            stack.append(tb.tb_frame)
            tb = tb.tb_next

        for frame in stack[1:]:
            dump += "\nFrame %s in %s at line %s\n" % (frame.f_code.co_name,
                                                       frame.f_code.co_filename,
                                                       frame.f_lineno)

            for key, value in frame.f_locals.items():
                dump += "\t%20s = " % key
                try:
                    dump += pprint.pformat(value) + "\n"
                except Exception, e:
                    dump += "<ERROR WHILE PRINTING VALUE> " + str(e) + "\n"

            del frame

        del stack  #: delete it just to be sure...

        dump += "\n\nPLUGIN OBJECT DUMP: \n\n"

        for name in dir(pyfile.plugin):
            attr = getattr(pyfile.plugin, name)
            if not name.endswith("__") and type(attr) != types.MethodType:
                dump += "\t%20s = " % name
                try:
                    dump += pprint.pformat(attr) + "\n"
                except Exception, e:
                    dump += "<ERROR WHILE PRINTING VALUE> " + str(e) + "\n"

        dump += "\nPYFILE OBJECT DUMP: \n\n"

        for name in dir(pyfile):
            attr = getattr(pyfile, name)
            if not name.endswith("__") and type(attr) != types.MethodType:
                dump += "\t%20s = " % name
                try:
                    dump += pprint.pformat(attr) + "\n"
                except Exception, e:
                    dump += "<ERROR WHILE PRINTING VALUE> " + str(e) + "\n"

        if pyfile.pluginname in self.m.core.config.plugin:
            dump += "\n\nCONFIG: \n\n"
            dump += pprint.pformat(self.m.core.config.plugin[pyfile.pluginname]) + "\n"

        return dump


    def clean(self, pyfile):
        """Set thread unactive and release pyfile"""
        self.active = True  #: release pyfile but lets the thread active
        pyfile.release()
