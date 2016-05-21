# llia.gui.tk.statusbar
# 2016.05.21

from Tkinter import (Button, Frame, Label)
import ttk

import llia.gui.tk.tk_factory as factory

class StatusBar(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        b_clear = Button(self, text="[x]", command=self.clear)
        b_clear.pack()
        self.label = Label(self, text = "")
        self.label.pack(fill="X")

    def clear(self):
        self.label.config(text = "")
        self.label.update_idletasks()

    def set(self, msg):
        self.label.config(text = msg)
        self.label.update_idletasks()

    def set_format(self, frmt, *args):
        self.set(frmt % args)

    def warning(self, msg):
        msg = "WARNING: %s" % msg
        self.label.config(text = msg)
        sel.label.update_ideltask()

        
