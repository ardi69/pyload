# -*- coding: utf-8 -*-

import subprocess
import sys

from os import path
from urllib import quote

from pyload.utils import encode, uniqify


class JsEngine:
    """ JS Engine superclass """

    def __init__(self, engine=None):  #: engine can be a jse name """string""" or an AbstractEngine """class"""

        self.engine = None  #: Default engine Instance

        if not ENGINES:
            pycore.log.critical("No JS Engine found!")
            return

        if not engine:
            engine = pycore.config.get("general", "jsengine")

        if engine != "auto" and self.set(engine) is False:
            engine = "auto"
            pycore.log.warning("JS Engine set to \"auto\" for safely")

        if engine == "auto":
            for E in self.find():
                if self.set(E) is True:
                    break
            else:
                pycore.log.error("No JS Engine available")


    @classmethod
    def find(cls):
        """ Check if there is any engine available """
        return [E for E in ENGINES if E.find()]


    def get(self, engine):
        """ Convert engine name (string) to relative JSE class (AbstractEngine extended) """
        if isinstance(engine, string):
            engine_name = engine.lower()
            for E in ENGINES:
                if E.NAME == engine_name:  #: doesn't check if E(NGINE) is available, just convert string to class
                    JSE = E
                    break
            else:
                JSE = None
        elif issubclass(engine, AbstractEngine):
            JSE = engine
        else:
            JSE = None
        return JSE


    def set(self, engine):
        """ Set engine name (string) or JSE class (AbstractEngine extended) as default engine """
        if isinstance(engine, string):
            self.set(self.get(engine))
        elif issubclass(engine, AbstractEngine) and engine.find():
            self.engine = engine
            return True
        else:
            return False


    def eval(self, script, engine=None):  #: engine can be a jse name """string""" or an AbstractEngine """class"""
        if not engine:
            JSE = self.engine
        else:
            JSE = self.get(engine)

        if not JSE:
            return None

        script = encode(script)

        out, err = JSE.eval(script)

        results = [out]

        if pycore.config.get("general", "debug"):
            if err:
                pycore.log.debug(JSE.NAME + ":", err)

            engines = self.find()
            engines.remove(JSE)
            for E in engines:
                out, err = E.eval(script)
                res = err or out
                pycore.log.debug(E.NAME + ":", res)
                results.append(res)

            if len(results) > 1 and len(uniqify(results)) > 1:
                pycore.log.warning("JS output of two or more engines mismatch")

        return results[0]


class AbstractEngine:
    """ JSE base class """

    NAME = ""

    def __init__(self):
        self.setup()
        self.available = self.find()

    def setup(self):
        pass

    @classmethod
    def find(cls):
        """ Check if the engine is available """
        try:
            __import__(cls.NAME)
        except ImportError:
            try:
                out, err = cls().eval("print(23+19)")
            except:
                res = False
            else:
                res = True if out == "42" else False
        else:
            res = True
        finally:
            return res

    def _eval(args):
        if not self.available:
            return None, "JS Engine \"%s\" not found" % self.NAME

        try:
            p = subprocess.Popen(args,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 bufsize=-1)
            return map(lambda x: x.strip(), p.communicate())
        except e:
            return None, e


    def eval(script):
        raise NotImplementedError


class Pyv8Engine(AbstractEngine):

    NAME = "pyv8"

    def eval(self, script):
        if not self.available:
            return None, "JS Engine \"%s\" not found" % self.NAME

        try:
            rt = PyV8.JSContext()
            rt.enter()
            res = rt.eval(script), None  #@TODO: parse stderr
        except e:
            res = None, e
        finally:
            return res


class MozillaEngine(AbstractEngine):

    NAME = "spidermonkey"

    def setup(self):
        subprocess.Popen(["js", "-v"], bufsize=-1).communicate()

    def eval(self, script):
        script = "print(eval(unescape('%s')))" % quote(script)
        args = ["js", "-e", script]
        return self._eval(args)


class NodeEngine(AbstractEngine):

    NAME = "nodejs"

    def setup(self):
        subprocess.Popen(["node", "-v"], bufsize=-1).communicate()

    def eval(self, script):
        script = "console.log(eval(unescape('%s')))" % quote(script)
        args = ["node", "-e", script]
        return self._eval(args)


class RhinoEngine(AbstractEngine):

    NAME = "rhino"

    def setup(self):
        jspath = [
            "/usr/share/java*/js.jar",
            "js.jar",
            path.join(pypath, "js.jar")
        ]
        for p in jspath:
            if path.exists(p):
                self.path = p
                break
        else:
            self.path = ""

    def eval(self, script):
        script = "print(eval(unescape('%s')))" % quote(script)
        args = ["java", "-cp", self.path, "org.mozilla.javascript.tools.shell.Main", "-e", script]
        return self._eval(args).decode("utf8").encode("ISO-8859-1")


class JscEngine(AbstractEngine):

    NAME = "javascriptcore"

    def setup(self):
        jspath = "/System/Library/Frameworks/JavaScriptCore.framework/Resources/jsc"
        self.path = jspath if path.exists(jspath) else ""

    def eval(self, script):
        script = "print(eval(unescape('%s')))" % quote(script)
        args = [self.path, "-e", script]
        return self._eval(args)


#@NOTE: Priority ordered
ENGINES = [MozillaEngine, Pyv8Engine, NodeEngine, RhinoEngine]

if sys.platform == "darwin":
    ENGINES.insert(JscEngine)
