# llia.gui.tk.tk_channel_name_editor
# 2016.05.30

from __future__ import print_function
from Tkinter import Toplevel, Label, BOTH, Frame, StringVar, W, EW, LEFT, X
import ttk

import llia.gui.tk.tk_factory as factory

class TkChannelNameEditor(Toplevel):

    def __init__(self, master, app):
        Toplevel.__init__(self, master)
        self.app = app
        self.config = app.config
        self.parser = app.ls_parser
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
        button_bar = Frame(main)
        b_accept = factory.accept_button(button_bar, command=self.accept)
        b_cancel = factory.cancel_button(button_bar, command=self.cancel)
        b_accept.pack(side=LEFT, expand=True, fill=X)
        b_cancel.pack(side=LEFT, expand=True, fill=X)
        button_bar.grid(row=17, column=0, columnspan=3, sticky=EW, padx=16, pady=8)
        self.protocol("WM_DELETE_WINDOW", None)
        self.grab_set()
        self.mainloop()

    def status(self, msg):
        self.app.main_window().status(msg)

    def warning(self, msg):
        self.app.main_window().warning(msg)
        
    # def accept(self):
    #     for i in range(16):
    #         channel = i+1
    #         name = self.vars[i].get()
    #         self.config.channel_name(channel, str(name))
    #     self.status("MIDI channel names updated")
    #     self.destroy()

    def accept(self):
        for i in range(16):
            channel = i+1
            name = self.vars[i].get().strip().replace(' ','_')
            stype = self.parser.what_is(name)
            if name == str(channel) or stype == "channel" or stype == '':
                self.parser.channel_name(channel, name)
            else:
                msg = "Illegal channel name: '%s'" % name
                self.warning(msg)
        self.destroy()
                
            
            
            
    def cancel(self):
        self.status("MIDI channel names restored")
        self.destroy()
        
