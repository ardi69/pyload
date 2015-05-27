# -*- coding: utf-8 -*-

from __future__ import with_statement

import os
import shutil
import time
import traceback

from pyload.utils import encode, decode


CONF_VERSION = 1


class ConfigParser(object):
    """
    holds and manage the configuration

    current dict layout:

    {

     section: {
      option: {
            value:
            type:
            desc:
      }
      desc:

    }
    """

    def __init__(self):
        """Constructor"""
        self.config = {}  #: the config values
        self.plugin = {}  #: the config for plugins
        self.oldRemoteData = {}

        self.pluginCB = None  #: callback when plugin config value is changed

        self.checkVersion()

        self.readConfig()


    def checkVersion(self, n=0):
        """Determines if config need to be copied"""
        try:
            if not os.path.exists("pyload.conf"):
                shutil.copy(os.path.join(pypath, "pyload", "config", "default.conf"), "pyload.conf")

            if not os.path.exists("plugin.conf"):
                with open("plugin.conf", "wb") as f:
                    f.write("version: " + str(CONF_VERSION))

            with open("pyload.conf", "rb") as f:
                v = f.readline()
            v = v[v.find(":") + 1:].strip()

            if not v or int(v) < CONF_VERSION:
                shutil.copy(os.path.join(pypath, "pyload", "config", "default.conf"), "pyload.conf")
                print "Old version of config was replaced"

            with open("plugin.conf", "rb") as f:
                v = f.readline()
            v = v[v.find(":") + 1:].strip()

            if not v or int(v) < CONF_VERSION:
                with open("plugin.conf", "wb") as f:
                    f.write("version: " + str(CONF_VERSION))
                print "Old version of plugin-config replaced"

        except Exception:
            if n >= 3:
                raise
            time.sleep(0.3)
            self.checkVersion(n + 1)


    def readConfig(self):
        """Reads the config file"""
        self.config = self.parseConfig(os.path.join(pypath, "pyload", "config", "default.conf"))
        self.plugin = self.parseConfig("plugin.conf")

        try:
            homeconf = self.parseConfig("pyload.conf")
            if "username" in homeconf['remote']:
                if "password" in homeconf['remote']:
                    self.oldRemoteData = {"username": homeconf['remote']['username']['value'],
                                          "password": homeconf['remote']['username']['value']}
                    del homeconf['remote']['password']
                del homeconf['remote']['username']
            self.updateValues(homeconf, self.config)
        except Exception:
            print "Config Warning"
            traceback.print_exc()


    def parseConfig(self, config):
        """Parses a given configfile"""

        with open(config) as f:
            config = f.read()

        config = config.splitlines()[1:]

        conf = {}

        section, option, value, typ, desc = "", "", "", "", ""

        listmode = False

        for line in config:
            comment = line.rfind("#")
            if line.find(":", comment) < 0 > line.find("=", comment) and comment > 0 and line[comment - 1].isspace():
                line = line.rpartition("#")  #: removes comments
                if line[1]:
                    line = line[0]
                else:
                    line = line[2]

            line = line.strip()

            try:
                if line == "":
                    continue
                elif line.endswith(":"):
                    section, none, desc = line[:-1].partition('-')
                    section = section.strip()
                    desc = desc.replace('"', "").strip()
                    conf[section] = {"desc": desc}
                else:
                    if listmode:
                        if line.endswith("]"):
                            listmode = False
                            line = line.replace("]", "")

                        value += [self.cast(typ, x.strip()) for x in line.split(",") if x]

                        if not listmode:
                            conf[section][option] = {"desc": desc,
                                                     "type": typ,
                                                     "value": value,
                                                     "idx": len(conf[section])}


                    else:
                        content, none, value = line.partition("=")

                        content, none, desc = content.partition(":")

                        desc = desc.replace('"', "").strip()

                        typ, none, option = content.strip().rpartition(" ")

                        value = value.strip()
                        typ   = typ.strip()

                        if value.startswith("["):
                            if value.endswith("]"):
                                listmode = False
                                value = value[:-1]
                            else:
                                listmode = True

                            value = [self.cast(typ, x.strip()) for x in value[1:].split(",") if x]
                        else:
                            value = self.cast(typ, value)

                        if not listmode:
                            conf[section][option] = {"desc": desc,
                                                     "type": typ,
                                                     "value": value,
                                                     "idx": len(conf[section])}

            except Exception, e:
                print "Config Warning"
                traceback.print_exc()

        return conf


    def updateValues(self, config, dest):
        """Sets the config values from a parsed config file to values in destination"""

        for section in config.iterkeys():
            if section in dest:
                for option in config[section].iterkeys():
                    if option in ("desc", "outline"):
                        continue

                    if option in dest[section]:
                        dest[section][option]['value'] = config[section][option]['value']

                    # else:
                       # dest[section][option] = config[section][option]


                    # else:
                       # dest[section] = config[section]


    def saveConfig(self, config, filename):
        """Saves config to filename"""
        with open(filename, "wb") as f:
            try:
                os.chmod(filename, 0600)
            except Exception:
                pass

            f.write("version: %i \n" % CONF_VERSION)
            for section in config.iterkeys():
                f.write('\n%s - "%s":\n' % (section, config[section]['desc']))

                for option, data in sorted(config[section].items(), key=lambda i: i[1]['idx'] if i[0] not in ("desc", "outline") else 0):
                    if option in ("desc", "outline"):
                        continue

                    if isinstance(data['value'], list):
                        value = "[ \n"
                        for x in data['value']:
                            value += "\t\t" + str(x) + ",\n"
                        value += "\t\t]\n"
                    else:
                        if isinstance(data['value'], basestring):
                            value = data['value'] + "\n"
                        else:
                            value = str(data['value']) + "\n"
                    try:
                        f.write('\t%s %s : "%s" = %s' % (data['type'], option, data['desc'], value))
                    except UnicodeEncodeError:
                        f.write('\t%s %s : "%s" = %s' % (data['type'], option, data['desc'], encode(value)))


    def cast(self, typ, value):
        """Cast value to given format"""
        if not isinstance(value, basestring):
            return value

        elif typ == "int":
            return int(value)
        elif typ == "bool":
            return value.lower() in ("1", "true", "on", "an", "yes")
        elif typ == "time":
            if not value:
                value = "0:00"
            if not ":" in value:
                value += ":00"
            return value
        elif typ in ("str", "file", "folder"):
            return encode(value)
        else:
            return value


    def save(self):
        """Saves the configs to disk"""
        self.saveConfig(self.config, "pyload.conf")
        self.saveConfig(self.plugin, "plugin.conf")


    def __getitem__(self, section):
        """Provides dictonary like access: c['section']['option']"""
        return Section(self, section)


    def get(self, section, option):
        """Get value"""
        value = self.config[section][option]['value']
        return decode(value)


    def set(self, section, option, value):
        """Set value"""
        value = self.cast(self.config[section][option]['type'], value)
        self.config[section][option]['value'] = value
        self.save()


    def getPlugin(self, plugin, option):
        """Gets a value for a plugin"""
        value = self.plugin[plugin][option]['value']
        return encode(value)


    def setPlugin(self, plugin, option, value):
        """Sets a value for a plugin"""

        value = self.cast(self.plugin[plugin][option]['type'], value)

        if self.pluginCB: self.pluginCB(plugin, option, value)

        self.plugin[plugin][option]['value'] = value
        self.save()


    def removeDeletedPlugins(self, plugins):
        for name in self.plugin.keys():
            if not name in plugins:
                del self.plugin[name]


    def getMetaData(self, section, option):
        """Get all config data for an option"""
        return self.config[section][option]


    def addPluginConfig(self, name, config, outline=""):
        """Adds config options with tuples (name, type, desc, default)"""
        if name not in self.plugin:
            conf = {"desc": name,
                    "outline": outline}
            self.plugin[name] = conf
        else:
            conf = self.plugin[name]
            conf['outline'] = outline

        for item in config:
            if item[0] in conf:
                conf[item[0]]['type'] = item[1]
                conf[item[0]]['desc'] = item[2]
            else:
                conf[item[0]] = {
                    "desc": item[2],
                    "type": item[1],
                    "value": self.cast(item[1], item[3]),
                    "idx": len(conf)
                }

        values = [x[0] for x in config] + ["desc", "outline"]
        # delete old values
        for item in conf.keys():
            if item not in values:
                del conf[item]


    def deleteConfig(self, name):
        """Removes a plugin config"""
        if name in self.plugin:
            del self.plugin[name]


class Section(object):
    """Provides dictionary like access for configparser"""

    def __init__(self, parser, section):
        """Constructor"""
        self.parser = parser
        self.section = section


    def __getitem__(self, item):
        """Getitem"""
        return self.parser.get(self.section, item)


    def __setitem__(self, item, value):
        """Setitem"""
        self.parser.set(self.section, item, value)
