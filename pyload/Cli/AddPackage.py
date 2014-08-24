# -*- coding: utf-8 -*-

from pyload.Cli.Handler import Handler
from pyload.utils.printer import *


class AddPackage(Handler):
    """ let the user add packages """

    def __init__(self):
        self.name = ""
        self.urls = []

    def onEnter(self, inp):
        if inp == "0":
            self.cli.reset()

        if not self.name:
            self.name = inp
            self.setInput()
        elif inp == "END":
            #add package
            self.client.addPackage(self.name, self.urls, 1)
            self.cli.reset()
        else:
            if inp.strip():
                self.urls.append(inp)
            self.setInput()

    def renderBody(self, line):
        overline(line, white(_("Add Package:")))
        overline(line + 1, "")
        line += 2

        if not self.name:
            overline(line, _("Enter a name for the new package"))
            overline(line + 1, "")
            line += 2
        else:
            overline(line, _("Package: %s") % self.name)
            overline(line + 1, _("Parse the links you want to add."))
            overline(line + 2, _("Type %s when done.") % mag("END"))
            overline(line + 3, _("Links added: ") + mag(len(self.urls)))
            line += 4

        overline(line, "")
        overline(line + 1, mag("0.") + _(" back to main menu"))

        return line + 2
