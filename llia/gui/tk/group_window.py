# llia.gui.tk.group_windoe
#
# GroupWindow is a Tk Toplevel window with a Tk Notebook used for holding
# active synths. Prior to GroupWindow each synth editor had it's own Tk
# Toplevel which was cluttered and confusing.
#

from __future__ import print_function
from Tkinter import Toplevel, TclError

import llia.gui.tk.tk_factory as factory

class GroupWindow(Toplevel):

    instance_counter = 0
    
    def __init__(self, app, root, name=""):
        Toplevel.__init__(self, root)
        self.root = root
        main = factory.frame(self)
        main.pack(expand=True, fill="both")
        self.app = app
        if not name:
            name = "Group_%d" % self.instance_counter
        self.name = str(name)
        GroupWindow.instance_counter += 1
        self.notebook = factory.notebook(main)
        self.notebook.pack(expand=True, fill="both")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Destroy>", self.on_closing)
        self.withdraw() # hide initially
        
    def on_closing(self, *args):
        pass

    def show_synth_editor(self, sid):
        try:
            mw = self.app.main_window()
            swin = mw[sid]
            self.notebook.select(swin)
            self.deiconify()  # ISSUE deiconify not working ?
        except (TclError, KeyError):
            msg = "Can not find %s editor" % sid
            self.app.main_window().warning(msg)

    def lift(self):
        Toplevel.lift(self, self.root)

    def lower(self):
        Toplevel.lower(self, self.root)
