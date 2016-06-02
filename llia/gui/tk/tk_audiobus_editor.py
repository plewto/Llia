# llia.gui.tk.tk_audiobus_editor
# 2016.05.31
#

from __future__ import print_function
from Tkinter import Toplevel, Label, BOTH, Frame, StringVar, NS, N, END, W, EW, LEFT, RIGHT
import ttk

import llia.gui.tk.tk_factory as factory


class TkAudiobusEditor(Toplevel):

    def __init__(self, master, app):
        Toplevel.__init__(self, master)
        self.wm_title = "Audio Buses"
        self.app = app
        self.proxy = app.proxy
        self.parser = app.ls_parser
        main = Frame(self)
        main.pack(expand=True)
        lab_title = factory.label(main, "Audio Busses")
        frame_list = Frame(main, width=248, height=320)
        frame_list.pack_propagate(False)
        self.listbox = factory.listbox(frame_list, command=self.select_bus)
        self.listbox.pack(expand=True, fill=BOTH)
        sb = factory.scrollbar(main, yclient=self.listbox)
        lab_name = factory.label(main, "Name")
        lab_channels = factory.label(main, "Channels")
        self._var_name = StringVar()
        entry_name = factory.entry(main, self._var_name, ttip="Audio bus name")
        self._var_chancount = StringVar()
        spin_chancount = factory.int_spinbox(main, self._var_chancount, 1, 64)
        
        self.lab_warning = factory.warning_label(main)
        button_bar = Frame(main)
        b_remove = factory.remove_button(button_bar,ttip="Delete audio bus",command=self.remove_bus)
        b_add = factory.add_button(button_bar, ttip="Add new audio bus", command=self.add_bus)
        b_refresh = factory.refresh_button(button_bar, ttip="Refresh bus list", command=self.update_list)
        b_accept = factory.accept_button(button_bar)
        b_cancel = factory.cancel_button(button_bar)
        b_help = factory.help_button(button_bar)

        lab_title.grid(row=0, column=0, columnspan=6, pady=8)
        frame_list.grid(row=1, column=0, rowspan=5, columnspan=5, pady=4)
        sb.grid(row=1, column=4, rowspan=5, sticky=NS)
        lab_name.grid(row=6, column=0, sticky=W)
        entry_name.grid(row=6, column=1)
        lab_channels.grid(row=7, column=0, sticky=W, pady=8)
        spin_chancount.grid(row=7, column=1)
        self.lab_warning.grid(row=8, column=0, columnspan=6)
        button_bar.grid(row=9, column=0, columnspan=6, padx=8, pady=4)

        b_remove.grid(row=0, column=0)
        b_add.grid(row=0, column=1)
        b_refresh.grid(row=0, column=2)
        factory.label(button_bar, "").grid(row=0, column=3, padx=16)
        b_accept.grid(row=0, column=4)
        b_cancel.grid(row=0, column=5)
        b_help.grid(row=0, column=6)
        

        self.update_list()
        self.grab_set()
        self.mainloop()

        
    def status(self, msg):
        self.app.main_window().status(msg)

    def warning(self, msg):
        self.app.main_window().warning(msg)
        msg = "WARNING: %s" % msg
        self.lab_warning.config(text=msg)
        
    def update_list(self):
        self.lab_warning.config(text="")
        self.listbox.delete(0, END)
        for k in self.proxy.audio_bus_keys():
            self.listbox.insert(END, k)
        
    def select_bus(self, *_):
        index = self.listbox.curselection()[0]
        bname = self.listbox.get(index).strip()
        binfo = self.proxy.audio_bus_info(bname)
        chancount = binfo[2]
        self._var_name.set(bname)
        self._var_chancount.set(chancount)

    def add_bus(self, *_):
        bname = self._var_name.get().strip().replace(' ','_')
        exists = self.parser.what_is(bname)
        if exists == "abus":
            self.warning("Audio bus '%s' already exists" % bname)
        elif len(bname) == 0:
            msg = "Invalid bus name"
            self.warning(msg)
        elif exists != "":
            msg = "'%s' is already assigned as %s" % (bname, exists)
            self.warning(msg)
        else:
            try:
                chan_count = int(self._var_chancount.get())
                rs = self.parser.abus(bname, chan_count)
                self.update_list()
                if rs:
                    self.status("Added audio bus '%s' [%s]" % (bname, chan_count))
                else:
                    msg = "Can not add audio bus '%s'" % bname
                    self.warning(msg)
            except ValueError:
                msg = "Invalid channel count: '%s'" % self._var_chancount.get()
                self.warning(msg)

    # ISSUE: Once an audio bus has been removed, a new bus with the same name
    # ISSUE: can not be added.  This is true even though the previous bus
    # ISSUE: does not appear in a data dump.
    # ISSUE: Check consistency between host and client after bus removal.
    # ISSUE: It looks like the bus still exists on the host but not on the
    # ISSUE: client. 
    def remove_bus(self, *_):
        bname = self._var_name.get().strip()
        exists = self.parser.what_is(bname)
        if exists == "abus":
            protected = len(bname) > 3 and (bname[:3] == "in_" or bname[:3] == "out")
            if protected:
                msg = "Can not remove protected bus '%s'" % bname
                self.warning(msg)
            else:
                rs = self.parser.remove_bus(bname)
                self.update_list()
                self.status("Removed audiobus '%s'" % bname)
        else:
            msg = "'%s' is not an audio bus" % bname
            self.warning(msg)
            
