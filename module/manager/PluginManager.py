# -*- coding: utf-8 -*-

import re
import sys

from itertools import chain
from os import listdir, makedirs
from os.path import isfile, join, exists
from traceback import print_exc

from SafeEval import const_eval as literal_eval


class PluginManager(object):
    ROOT = "module.plugins."
    USERROOT = "userplugins."
    TYPES = ("account", "container", "crypter", "addon", "hoster", "internal",  "ocr")

    PATTERN = re.compile(r'__pattern__.*=.*r("|\')([^"\']+)')
    VERSION = re.compile(r'__version__.*=.*("|\')([0-9.]+)')
    CONFIG = re.compile(r'__config__.*=.*\[([^\]]+)', re.MULTILINE)
    DESC = re.compile(r'__description__.?=.?("|"""|\')([^"\']+)')


    def __init__(self, core):
        self.core = core

        self.config = core.config
        self.log = core.log

        self.plugins = {}
        self.createIndex()

        #register for import addon
        sys.meta_path.append(self)


    def createIndex(self):
        """create information for all plugins available"""

        sys.path.append(pypath)

        if not exists("userplugins"):
            makedirs("userplugins")
        if not exists(join("userplugins", "__init__.py")):
            f = open(join("userplugins", "__init__.py"), "wb")
            f.close()

        self.plugins['crypter'] = self.crypterPlugins = self.parse("crypter", pattern=True)
        self.plugins['container'] = self.containerPlugins = self.parse("container", pattern=True)
        self.plugins['hoster'] = self.hosterPlugins = self.parse("hoster", pattern=True)

        self.plugins['ocr'] = self.captchaPlugins = self.parse("ocr")
        self.plugins['account'] = self.accountPlugins = self.parse("account")
        self.plugins['addon'] = self.addonPlugins = self.parse("addon")
        self.plugins['internal'] = self.internalPlugins = self.parse("internal")

        self.log.debug("created index of plugins")

    def parse(self, folder, pattern=False, home={}):
        """
        returns dict with information
        home contains parsed plugins from module.

        {
        name : {path, version, config, (pattern, re), (plugin, class)}
        }

        """
        plugins = {}
        if home:
            pfolder = join("userplugins", folder)
            if not exists(pfolder):
                makedirs(pfolder)
            if not exists(join(pfolder, "__init__.py")):
                f = open(join(pfolder, "__init__.py"), "wb")
                f.close()

        else:
            pfolder = join(pypath, "module", "plugins", folder)

        for f in listdir(pfolder):
            if (isfile(join(pfolder, f)) and f.endswith(".py") or f.endswith("_25.pyc") or f.endswith(
                "_26.pyc") or f.endswith("_27.pyc")) and not f.startswith("_"):
                data = open(join(pfolder, f))
                content = data.read()
                data.close()

                if f.endswith("_25.pyc") and sys.version_info != (2, 5):
                    continue
                elif f.endswith("_26.pyc") and sys.version_info != (2, 6):
                    continue
                elif f.endswith("_27.pyc") and sys.version_info != (2, 7):
                    continue

                name = f[:-3]
                if name[-1] == ".":
                    name = name[:-4]

                version = self.VERSION.findall(content)
                if version:
                    version = float(version[0][1])
                else:
                    version = 0

                # home contains plugins from pyload root
                if home and name in home:
                    if home[name]['v'] >= version:
                        continue

                plugins[name] = {}
                plugins[name]['v'] = version

                module = f.replace(".pyc", "").replace(".py", "")

                # the plugin is loaded from user directory
                plugins[name]['user'] = True if home else False
                plugins[name]['name'] = module

                if pattern:
                    pattern = self.PATTERN.findall(content)

                    if pattern:
                        pattern = pattern[0][1]
                    else:
                        pattern = "^unmachtable$"

                    plugins[name]['pattern'] = pattern

                    try:
                        plugins[name]['re'] = re.compile(pattern)
                    except:
                        self.log.error(_("%s has a invalid pattern.") % name)


                # internals have no config
                if folder == "internal":
                    self.config.deleteConfig(name)
                    continue

                config = self.CONFIG.findall(content)
                if config:
                    config = literal_eval(config[0].strip().replace("\n", "").replace("\r", ""))
                    desc = self.DESC.findall(content)
                    desc = desc[0][1] if desc else ""

                    if type(config[0]) == tuple:
                        config = [list(x) for x in config]
                    else:
                        config = [list(config)]

                    if folder == "addon":
                        append = True
                        for item in config:
                            if item[0] == "activated":
                                append = False

                        # activated flag missing
                        if append:
                            config.append(["activated", "bool", "Activated", False])

                    try:
                        self.config.addPluginConfig(name, config, desc)
                    except:
                        self.log.error("Invalid config in %s: %s" % (name, config))

                elif folder == "addon": #force config creation
                    desc = self.DESC.findall(content)
                    desc = desc[0][1] if desc else ""
                    config = (["activated", "bool", "Activated", False],)

                    try:
                        self.config.addPluginConfig(name, config, desc)
                    except:
                        self.log.error("Invalid config in %s: %s" % (name, config))

        if not home:
            temp = self.parse(folder, pattern, plugins)
            plugins.update(temp)

        return plugins


    def parseUrls(self, urls):
        """parse plugins for given list of urls"""

        last = None
        res = [] # tupels of (url, plugin)

        for url in urls:
            if type(url) not in (str, unicode, buffer):
                continue
            found = False

            if last and last[1]['re'].match(url):
                res.append((url, last[0]))
                continue

            for name, value in chain(self.crypterPlugins.iteritems(), self.hosterPlugins.iteritems(),
                self.containerPlugins.iteritems()):
                if value['re'].match(url):
                    res.append((url, name))
                    last = (name, value)
                    found = True
                    break

            if not found:
                res.append((url, "BasePlugin"))

        return res

    def findPlugin(self, name, pluginlist=("hoster", "crypter", "container")):
        for ptype in pluginlist:
            if name in self.plugins[ptype]:
                return self.plugins[ptype][name], ptype
        return None, None

    def getPlugin(self, name, original=False):
        """return plugin module from hoster|decrypter|container"""
        plugin, type = self.findPlugin(name)

        if not plugin:
            self.log.warning("Plugin %s not found." % name)
            plugin = self.hosterPlugins['BasePlugin']

        if "new_module" in plugin and not original:
            return plugin['new_module']

        return self.loadModule(type, name)

    def getPluginName(self, name):
        """ used to obtain new name if other plugin was injected"""
        plugin, type = self.findPlugin(name)

        if "new_name" in plugin:
            return plugin['new_name']

        return name

    def loadModule(self, type, name):
        """ Returns loaded module for plugin

        :param type: plugin type, subfolder of module.plugins
        :param name:
        """
        plugins = self.plugins[type]
        if name in plugins:
            if "module" in plugins[name]:
                return plugins[name]['module']

            try:
                module = __import__(self.ROOT + "%s.%s" % (type, plugins[name]['name']), globals(), locals(),
                    plugins[name]['name'])
                plugins[name]['module'] = module  #cache import, maybe unneeded
                return module
            except Exception, e:
                self.log.error(_("Error importing %(name)s: %(msg)s") % {'name': name, 'msg': str(e)})
                if self.core.debug:
                    print_exc()

    def loadClass(self, type, name):
        """Returns the class of a plugin with the same name"""
        module = self.loadModule(type, name)
        return getattr(module, name) if module else None

    def getAccountPlugins(self):
        """return list of account plugin names"""
        return self.accountPlugins.keys()

    def find_module(self, fullname, path=None):
        #redirecting imports if necesarry
        if fullname.startswith(self.ROOT) or fullname.startswith(self.USERROOT): #seperate pyload plugins
            user = 1 if fullname.startswith(self.USERROOT) else 0  #: used as bool and int

            split = fullname.split(".")
            if len(split) != 4 - user:
                return
            type, name = split[2 - user:4 - user]

            if type in self.plugins and name in self.plugins[type]:
                #userplugin is a newer version
                if not user and self.plugins[type][name]['user']:
                    return self
                #imported from userdir, but pyloads is newer
                if user and not self.plugins[type][name]['user']:
                    return self


    def load_module(self, name, replace=True):
        if name not in sys.modules:  #could be already in modules
            if replace:
                if self.ROOT in name:
                    newname = name.replace(self.ROOT, self.USERROOT)
                else:
                    newname = name.replace(self.USERROOT, self.ROOT)
            else:
                newname = name

            base, plugin = newname.rsplit(".", 1)

            self.log.debug("Redirected import %s -> %s" % (name, newname))

            module = __import__(newname, globals(), locals(), [plugin])
            #inject under new an old name
            sys.modules[name] = module
            sys.modules[newname] = module

        return sys.modules[name]


    def reloadPlugins(self, type_plugins):
        """ reload and reindex plugins """
        if not type_plugins:
            return None

        self.log.debug("Request reload of plugins: %s" % type_plugins)

        reloaded = []

        as_dict = {}
        for t,n in type_plugins:
            if t in ("addon", "internal"):  #: do not reload addons or internals, because would cause to much side effects
                continue
            elif t in as_dict:
                as_dict[t].append(n)
            else:
                as_dict[t] = [n]

        for type in as_dict.iterkeys():
            for plugin in as_dict[type]:
                if plugin in self.plugins[type] and "module" in self.plugins[type][plugin]:
                    self.log.debug("Reloading %s" % plugin)
                    id = (type, plugin)
                    try:
                        reload(self.plugins[type][plugin]['module'])
                    except Exception, e:
                        self.log.error("Error when reloading %s" % id, str(e))
                        continue
                    else:
                        reloaded.append(id)

        #index creation
        self.plugins['crypter'] = self.crypterPlugins = self.parse("crypter", pattern=True)
        self.plugins['container'] = self.containerPlugins = self.parse("container", pattern=True)
        self.plugins['hoster'] = self.hosterPlugins = self.parse("hoster", pattern=True)
        self.plugins['ocr'] = self.captchaPlugins = self.parse("ocr")
        self.plugins['account'] = self.accountPlugins = self.parse("account")

        if "account" in as_dict:  #: accounts needs to be reloaded
            self.core.accountManager.initPlugins()
            self.core.scheduler.addJob(0, self.core.accountManager.getAccountInfos)

        return reloaded  #: return a list of the plugins successfully reloaded

    def reloadPlugin(self, type_plugin):
        """ reload and reindex ONE plugin """
        return True if self.reloadPlugins(type_plugin) else False
