# -*- coding: utf-8 -*-

from module.plugins.Addon import Addon


class RestartFailed(Addon):
    __name__ = "RestartFailed"
    __type__ = "addon"
    __version__ = "1.55"

    __config__ = [("activated", "bool", "Activated", False),
                  ("interval", "int", "Check interval in minutes", 90)]

    __description__ = """Periodically restart all failed downloads in queue"""
    __author_name__ = "Walter Purcaro"
    __author_mail__ = "vuolter@gmail.com"

    MIN_INTERVAL = 15 * 60  #: 15m minimum check interval (value is in seconds)

    event_list = ["pluginConfigChanged"]


    def pluginConfigChanged(self, plugin, name, value):
        if name == "interval":
            interval = value * 60
            if self.MIN_INTERVAL <= interval != self.interval:
                self.core.scheduler.removeJob(self.cb)
                self.interval = interval
                self.initPeriodical()
            else:
                self.logDebug("Invalid interval value, kept current")

    def periodical(self):
        self.logInfo("Restart failed downloads")
        self.api.restartFailed()

    def setup(self):
        self.api = self.core.api
        self.interval = self.MIN_INTERVAL

    def activate(self):
        self.pluginConfigChanged(self.__name__, "interval", self.getConfig("interval"))
