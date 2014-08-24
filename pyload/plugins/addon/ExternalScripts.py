# -*- coding: utf-8 -*-

import subprocess

from os import listdir, access, X_OK, makedirs, path

from pyload.plugins.Addon import Addon
from pyload.utils import safe_join


class ExternalScripts(Addon):
    __name__ = "ExternalScripts"
    __type__ = "addon"
    __version__ = "0.24"

    __config__ = [("activated", "bool", "Activated", True)]

    __description__ = """Run external scripts"""
    __author_name__ = ("mkaay", "RaNaN", "spoob")
    __author_mail__ = ("mkaay@mkaay.de", "ranan@pyload.org", "spoob@pyload.org")


    event_list = ["unrarFinished", "allDownloadsFinished", "allDownloadsProcessed"]


    def setup(self):
        self.scripts = {}

        folders = ["download_preparing", "download_finished", "package_finished",
                   "before_reconnect", "after_reconnect", "unrar_finished",
                   "all_dls_finished", "all_dls_processed"]

        for folder in folders:
            self.scripts[folder] = []

            self.initPluginType(folder, path.join("scripts", folder))

        for script_type, names in self.scripts.iteritems():
            if names:
                self.logInfo((_("Installed scripts for %s: ") % script_type) + ", ".join([path.basename(x) for x in names]))

    def initPluginType(self, folder, path):
        if not path.exists(path):
            try:
                makedirs(path)
            except:
                self.logDebug("Script folder %s not created" % folder)
                return

        for f in listdir(path):
            if f.startswith("#") or f.startswith(".") or f.startswith("_") or f.endswith("~") or f.endswith(".swp"):
                continue

            if not access(path.join(path, f), X_OK):
                self.logWarning(_("Script not executable:") + " %s/%s" % (folder, f))

            self.scripts[folder].append(path.join(path, f))

    def callScript(self, script, *args):
        try:
            cmd = [script] + [str(x) if not isinstance(x, basestring) else x for x in args]
            self.logDebug("Executing %(script)s: %(cmd)s" % {'script': path.abspath(script), 'cmd': " ".join(cmd)})
            #output goes to pyload
            subprocess.Popen(cmd, bufsize=-1)
        except Exception, e:
            self.logError(_("Error in %(script)s: %(error)s") % {'script': path.basename(script), 'error': str(e)})

    def downloadPreparing(self, pyfile):
        for script in self.scripts['download_preparing']:
            self.callScript(script, pyfile.pluginname, pyfile.url, pyfile.id)

    def downloadFinished(self, pyfile):
        for script in self.scripts['download_finished']:
            self.callScript(script, pyfile.pluginname, pyfile.url, pyfile.name,
                            safe_join(self.config.get("general", "download_folder"),
                                      pyfile.package().folder, pyfile.name), pyfile.id)

    def packageFinished(self, pypack):
        for script in self.scripts['package_finished']:
            folder = self.config.get("general", "download_folder")
            folder = safe_join(folder, pypack.folder)

            self.callScript(script, pypack.name, folder, pypack.password, pypack.id)

    def beforeReconnecting(self, ip):
        for script in self.scripts['before_reconnect']:
            self.callScript(script, ip)

    def afterReconnecting(self, ip):
        for script in self.scripts['after_reconnect']:
            self.callScript(script, ip)

    def unrarFinished(self, folder, fname):
        for script in self.scripts['unrar_finished']:
            self.callScript(script, folder, fname)

    def allDownloadsFinished(self):
        for script in self.scripts['all_dls_finished']:
            self.callScript(script)

    def allDownloadsProcessed(self):
        for script in self.scripts['all_dls_processed']:
            self.callScript(script)
