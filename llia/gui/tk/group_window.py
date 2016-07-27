# llia.gui.tk.group_windoe
#
# GroupWindow is a Tk Toplevel window with a Tk Notebook used for holding
# active synths. Prior to GroupWindow each synth editor had it's own Tk
# Toplevel which was cluttered and confusing.
#

from __future__ import print_function
from Tkinter import Toplevel

import llia.gui.tk.tk_factory as factory

class GroupWindow(Toplevel):

    def __init__(self, app):
        Toplevel.__init__(self, None)
        main = factory.frame(self)
        main.pack(expand=True, fill="both")
        self.app = app
        self.notebook = factory.notebook(main)
        self.notebook.pack(expand=True, fill="both")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Destroy>", self.on_closing)
        
    def on_closing(self, *args):
        pass
        
   
        
        
        
        
        
