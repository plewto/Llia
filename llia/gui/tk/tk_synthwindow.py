# llia.gui.tk.tk_synthwindow
# 2016.06.11


from __future__ import print_function
from Tkinter import Toplevel, BOTH, Label
#import tkk

import llia.gui.tk.tk_factory as factory
import llia.gui.pallet
from llia.gui.tk.tk_bankeditor import TkBankEditor

class TkSynthWindow(Toplevel):

    def __init__(self, sproxy):
        Toplevel.__init__(self, None)
        self.config(background=factory.bg())
        self.synth = sproxy
        self.app = sproxy.app
        self.sid = sproxy.sid
        factory.set_pallet(sproxy.specs["pallet"])
        # main = factory.frame(self)
        # main.pack(expand=True, fill=BOTH)
        main = factory.paned_window(self)
        main.pack(expand=True, fill=BOTH)

        banked = TkBankEditor(main, sproxy)
        main.add(banked)

        # FPO Right Panel
        right = factory.frame(main)
        factory.label(right, "FPO Right").pack()
        main.add(right)
