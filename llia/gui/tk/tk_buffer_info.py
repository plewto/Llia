# llia.gui.tk.tk_buffer_info.py
# 2016.06.03

from __future__ import print_function
from Tkinter import Toplevel, END, Frame, BOTH, HORIZONTAL, NS, EW, NW, BOTTOM, W, X, LEFT, RIGHT

import llia.gui.tk.tk_factory as factory


class TkBufferList(Frame):

    def __init__(self, master, app):
        Frame.__init__(self, master)
        self.config(background=factory.bg())
        self.app = app
        self.proxy = app.proxy
        self.pack_propagate(False)
        self.listbox = factory.listbox(self)
        self.listbox.config(width=75, height=20)
        sbv = factory.scrollbar(self, yclient=self.listbox)
        sbh = factory.scrollbar(self, xclient=self.listbox, orientation=HORIZONTAL)
        self.listbox.grid(row=0, column=0, rowspan=6, columnspan=8)
        sbv.grid(row=0, column=8, rowspan=6, sticky=NS)
        sbh.grid(row=6, column=0, columnspan=8, sticky=EW)
        self.refresh()
        
    def refresh(self):
        self.listbox.delete(0, END)
        keys = self.proxy.buffer_keys()
        acc = []
        for k in keys:
            acc.append(self.proxy.buffer_info(k))
        acc.sort(key = lambda obj: obj["index"])
        for bi in acc:
            index, name, sr = bi['index'], bi['name'], bi['sample-rate']
            frames, channels = bi['frames'], bi['channels']
            filename = bi['filename']
            txt = "[%3d] %-12s frames: %6d chans: %2d sr: %6d file: '%s'"
            txt = txt % (index, name, frames, channels, sr, filename)
            self.listbox.insert(END, txt)
            
        
class TkBufferListDialog(Toplevel):

    def __init__(self, master, app):
        Toplevel.__init__(self, master)
        self.wm_title("Llia Buffers")
        self.tbl = TkBufferList(self, app)
        self.tbl.pack(anchor=NW, expand=True, fill=BOTH)
        button_bar = factory.frame(self)
        button_bar.pack(side=BOTTOM, anchor=W, expand=True, fill=X)
        b_refresh = factory.refresh_button(button_bar, command=self.tbl.refresh)
        b_accept = factory.accept_button(button_bar, command=self.destroy)
        b_refresh.pack(side=LEFT)
        b_accept.pack(side=RIGHT)
        self.grab_set()
        self.mainloop()

