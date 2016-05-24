# llia.gui.tk.pallet
# 2016.05.21

from __future__ import print_function


class Pallet(dict):

    def __init__(self):
        super(dict, self).__init__()
        self["BG"] = "gray5"
        self["FG"] = "#b5b5b5"
        self["BUTTON-BG"] = "#192633"
        self["RADIO-SELECT"] = "gray11"
        self["WARNING-FG"] = "yellow"

        
    def __getitem__(self, name):
        try:
            return dict.__getitem__(self, name)
        except KeyError:
            msg = "WARNING: invalid color: '%s'" % name
            print(msg)
            return "gray64"
