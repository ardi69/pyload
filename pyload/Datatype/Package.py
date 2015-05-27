# -*- coding: utf-8 -*-
# @author: RaNaN, mkaay

from pyload.manager.Event import UpdateEvent
from pyload.utils import safe_filename


class PyPackage(object):
    """Represents a package object at runtime"""

    def __init__(self, manager, id, name, folder, site, password, queue, order):
        self.m = manager
        self.m.packageCache[int(id)] = self

        self.id = int(id)
        self.name = name
        self._folder = folder
        self.site = site
        self.password = password
        self.queue = queue
        self.order = order
        self.setFinished = False


    @property
    def folder(self):
        return safe_filename(self._folder)


    def toDict(self):
        """
        Returns a dictionary representation of the data.

        :return: dict: {id: { attr: value }}
        """
        return {
            self.id: {
                'id': self.id,
                'name': self.name,
                'folder': self.folder,
                'site': self.site,
                'password': self.password,
                'queue': self.queue,
                'order': self.order,
                'links': {}
            }
        }


    def getChildren(self):
        """Get information about contained links"""
        return self.m.getPackageData(self.id)["links"]


    def sync(self):
        """Sync with db"""
        self.m.updatePackage(self)


    def release(self):
        """Sync and delete from cache"""
        self.sync()
        self.m.releasePackage(self.id)


    def delete(self):
        self.m.deletePackage(self.id)


    def notifyChange(self):
        e = UpdateEvent("pack", self.id, "collector" if not self.queue else "queue")
        self.m.core.pullManager.addEvent(e)
