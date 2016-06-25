# llia.gui.pallet
# 2016.05.21

from __future__ import print_function
import random


class Pallet(dict):

    def __init__(self):
        super(dict, self).__init__()
        self["BG"] = "gray5"
        self["FG"] = "#b5b5b5"
        self["ACTIVE-BG"] = "gray15"
        self["ACTIVE-FG"] = "yellow"
        
        self["BUTTON-BG"] = "#192633"
        self["BUTTON-FG"] = self["FG"]
        
        self["TAB-BG"] = self["BG"]
        self["TAB-FG"] = self["BUTTON-FG"]
        self["TAB-SELECTED-BG"] = "gray5"
        self["TAB-SELECTED-FG"] = "yellow"

        self["DIALOG-BG"] = "#191919"    # Backgroud color for modal dialogs
        self["DIALOG-FG"] = self["FG"]
        
        self["RADIO-SELECT"] = self["BG"]
        self["SCROLLBAR-BACKGROUND"] = "#344d66"
        self["SCROLLBAR-TROUGH"] = "#333333"
        self["WARNING-FG"] = "yellow"

        self["SLIDER-TROUGH"] = self["BG"]
        self["SLIDER-OUTLINE"] = self["BUTTON-BG"]
        

    def __setitem__(self, key, value):
        key = str(key).upper()
        dict.__setitem__(self, key, value)
        
    def __getitem__(self, name):
        try:
            name = str(name).upper()
            return dict.__getitem__(self, name)
        except KeyError:
            msg = "WARNING: invalid color: '%s'" % name
            print(msg)
            return "gray64"

pallet = Pallet()
