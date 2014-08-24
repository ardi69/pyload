# -*- coding: utf-8 -*-

import time

from os import listdir, makedirs, path
from shutil import move

from pyload.plugins.Addon import Addon


class HotFolder(Addon):
    __name__ = "HotFolder"
    __type__ = "addon"
    __version__ = "0.11"

    __config__ = [("activated", "bool", "Activated", False),
                  ("folder", "str", "Folder to observe", "container"),
                  ("watch_file", "bool", "Observe link file", False),
                  ("keep", "bool", "Keep added containers", True),
                  ("file", "str", "Link file", "links.txt")]

    __description__ = """Observe folder and file for changes and add container and links"""
    __author_name__ = "RaNaN"
    __author_mail__ = "RaNaN@pyload.de"


    def setup(self):
        self.interval = 10

    def periodical(self):
        if not path.exists(path.join(self.getConfig("folder"), "finished")):
            makedirs(path.join(self.getConfig("folder"), "finished"))

        if self.getConfig("watch_file"):

            if not path.exists(self.getConfig("file")):
                f = open(self.getConfig("file"), "wb")
                f.close()

            f = open(self.getConfig("file"), "rb")
            content = f.read().strip()
            f.close()
            f = open(self.getConfig("file"), "wb")
            f.close()
            if content:
                name = "%s_%s.txt" % (self.getConfig("file"), time.strftime("%H-%M-%S_%d%b%Y"))

                f = open(path.join(self.getConfig("folder"), "finished", name), "wb")
                f.write(content)
                f.close()

                self.api.addPackage(f.name, [f.name], 1)

        for f in listdir(self.getConfig("folder")):
            filename = path.join(self.getConfig("folder"), f)

            if not path.isfile(filename) or f.endswith("~") or f.startswith("#") or f.startswith("."):
                continue

            new_filename = path.join(self.getConfig("folder"), "finished", f if self.getConfig("keep") else "tmp_" + f)
            move(filename, new_filename)

            self.logInfo(_("Added %s from HotFolder") % f)
            self.api.addPackage(f, [new_filename], 1)
