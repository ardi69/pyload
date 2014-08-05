# -*- coding: utf-8 -*-

from module.plugins.Base import Plugin
from module.utils import decode


class Crypter(Plugin):
    __name__ = "Crypter"
    __type__ = "crypter"
    __version__ = "0.2"

    __pattern__ = None

    __description__ = """Base decrypter plugin"""
    __author_name__ = ("mkaay", "Walter Purcaro")
    __author_mail__ = ("mkaay@mkaay.de", "vuolter@gmail.com")


    def __init__(self, pyfile):
        Plugin.__init__(self, pyfile)

        #: Put all packages here. It's a list of tuples like: ( name, [list of links], folder )
        self.packages = []

        #: List of urls, pyLoad will generate packagenames
        self.urls = []

        self.multiDL = True
        self.limitDL = 0


    def preprocessing(self, thread):
        """prepare"""
        self.setup()
        self.thread = thread

        self.decrypt(self.pyfile)

        self.createPackages()


    def decrypt(self, pyfile):
        raise NotImplementedError

    def createPackages(self):
        """ create new packages from self.packages """
        if self.urls:
            self.api.generateAndAddPackages(self.urls)
        elif not self.packages:
            self.fail(_("No link extracted"))
            return

        for pack in self.packages:
            name, links, folder = pack

            self.logDebug("Parsed package %(name)s with %(len)d links" % {'name': name, 'len': len(links)})

            links = map(lambda x: decode(x), links)

            pid = self.api.addPackage(name, links, self.pyfile.package().queue)

            if name != folder is not None:
                self.api.setPackageData(pid, {'folder': folder})  #: Due to not break api.addPackage method
                self.logDebug("Set package %(name)s folder to %(folder)s" % {'name': name, 'folder': folder})

            if self.pyfile.package().password:
                self.api.setPackageData(pid, {'password': self.pyfile.package().password})
