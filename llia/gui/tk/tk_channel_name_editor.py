# llia.gui.tk.tk_channel_name_editor
# 2016.05.30

from __future__ import print_function
from Tkinter import Toplevel, Label, BOTH, Frame, StringVar, W
import ttk

import llia.gui.tk.tk_factory as factory

class TkChannelNameEditor(Toplevel):

    def __init__(self, master, app):
        Toplevel.__init__(self, master)
        self.config = app.config
        self.mw_title = "MIDI Channels"
        main = Frame(self)
        main.pack(expand=True, fill=BOTH)
        self.vars = []
        for i in range(16):
            channel = i+1
            name = self.config.channel_name(channel)
            var = StringVar()
            entry = factory.entry(main, var)
            lab = factory.label(main, "Channel %02d" % channel)
            lab.grid(row=i+1, column=0, sticky=W, ipadx=8)
            entry.grid(row=i+1, column=1)
            var.set(name)
            self.vars.append(var)
        lab_title= factory.label(main, "MIDI Channel Names")
        lab_title.grid(row=0, column=0, columnspan=2, pady=16)
        b_accept = factory.button(main, "Accept", command=self.accept)
        b_accept.grid(row=17, column=0, columnspan=2, pady=16)
        self.protocol("WM_DELETE_WINDOW", self.accept)
        self.grab_set()
        self.mainloop()
    
    def accept(self):
        for i in range(16):
            channel = i+1
            name = self.vars[i].get()
            self.config.channel_name(channel, str(name))
        self.destroy()
            
