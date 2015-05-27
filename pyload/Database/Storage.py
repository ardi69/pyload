# -*- coding: utf-8 -*-
# @author: mkaay

from pyload.Database import style
from pyload.Database import DatabaseBackend


class StorageMethods(object):

    @style.queue
    def setStorage(db, identifier, key, value):
        db.c.execute("SELECT id FROM storage WHERE identifier=? AND key=?", (identifier, key))
        if db.c.fetchone() is not None:
            db.c.execute("UPDATE storage SET value=? WHERE identifier=? AND key=?", (value, identifier, key))
        else:
            db.c.execute("INSERT INTO storage (identifier, key, value) VALUES (?, ?, ?)", (identifier, key, value))


    @style.queue
    def getStorage(db, identifier, key=None):
        if key is not None:
            db.c.execute("SELECT value FROM storage WHERE identifier=? AND key=?", (identifier, key))
            row = db.c.fetchone()
            if row is not None:
                return row[0]
        else:
            db.c.execute("SELECT key, value FROM storage WHERE identifier=?", (identifier,))
            return dict((row[0], row[1]) for row in db.c)


    @style.queue
    def delStorage(db, identifier, key):
        db.c.execute("DELETE FROM storage WHERE identifier=? AND key=?", (identifier, key))


DatabaseBackend.registerSub(StorageMethods)
