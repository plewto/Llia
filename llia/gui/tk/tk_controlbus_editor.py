# llia.gui.tk.tk_controlbus_editor
# 2016.05.31
#

from __future__ import print_function
from Tkinter import Toplevel, Label, BOTH, StringVar, NS, N, END, W, EW, LEFT, RIGHT
# import ttk

import llia.gui.tk.tk_factory as factory


class TkControlbusEditor(Toplevel):

    def __init__(self, master, app):
        Toplevel.__init__(self, master)
        self.wm_title = "Control Buses"
        self.app = app
        self.proxy = app.proxy
        self.parser = app.ls_parser
        main = factory.frame(self)
        main.pack(expand=True)
        lab_title = factory.label(main, "Control Busses")
        frame_list = factory.frame(main)
        frame_list.config(width=248, height=320)
        frame_list.pack_propagate(False)
        self.listbox = factory.listbox(frame_list, command=self.select_bus)
        self.listbox.pack(expand=True, fill=BOTH)
        sb = factory.scrollbar(main, yclient=self.listbox)
        lab_name = factory.label(main, "Name")
        lab_channels = factory.label(main, "Channels")
        self._var_name = StringVar()
        entry_name = factory.entry(main, self._var_name, ttip="Control bus name")
        self._var_chancount = StringVar()
        spin_chancount = factory.int_spinbox(main, self._var_chancount, 1, 64)
        self.lab_warning = factory.warning_label(main)
        button_bar = factory.frame(main)
        b_remove = factory.remove_button(button_bar,ttip="Delete control bus",command=self.remove_bus)
        b_add = factory.add_button(button_bar, ttip="Add new control bus", command=self.add_bus)
        b_refresh = factory.refresh_button(button_bar, ttip="Refresh bus list", command=self.refresh)
        b_accept = factory.accept_button(button_bar, command=self.accept)
        b_help = factory.help_button(button_bar, command=self.display_help)
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
        b_help.grid(row=0, column=3)
        factory.label(button_bar, "").grid(row=0, column=4, padx=16)
        b_accept.grid(row=0, column=5)
        self._current_selection = 0
        entry_name.bind('<Down>', self.increment_selection)
        entry_name.bind('<Up>', self.decrement_selection)
        entry_name.bind('<Return>', self.add_bus)
        self.listbox.bind('<Down>', self.increment_selection)
        self.listbox.bind('<Up>', self.decrement_selection)
        self.refresh()
        self.grab_set()
        self.mainloop()
        
    def status(self, msg):
        self.app.main_window().status(msg)

    def warning(self, msg):
        self.app.main_window().warning(msg)
        msg = "WARNING: %s" % msg
        self.lab_warning.config(text=msg)
        
    def refresh(self):
        self.lab_warning.config(text="")
        self.listbox.delete(0, END)
        for k in self.proxy.control_bus_keys():
            self.listbox.insert(END, k)
        
    def select_bus(self, *_):
        index = self.listbox.curselection()[0]
        bname = self.listbox.get(index).strip()
        binfo = self.proxy.control_bus_info(bname)
        chancount = binfo[2]
        self._var_name.set(bname)
        self._var_chancount.set(chancount)
        self._current_selection = index

    def add_bus(self, *_):
        bname = self._var_name.get().strip().replace(' ','_')
        exists = self.parser.what_is(bname)
        if exists == "cbus":
            self.warning("Control bus '%s' already exists" % bname)
        elif len(bname) == 0:
            msg = "Invalid bus name"
            self.warning(msg)
        elif exists != "":
            msg = "'%s' is already assigned as %s" % (bname, exists)
            self.warning(msg)
        else:
            try:
                chan_count = int(self._var_chancount.get())
                rs = self.parser.cbus(bname, chan_count)
                self.refresh()
                if rs:
                    self.status("Added control bus '%s' [%s]" % (bname, chan_count))
                else:
                    msg = "Can not add control bus '%s'" % bname
                    self.warning(msg)
            except ValueError:
                msg = "Invalid channel count: '%s'" % self._var_chancount.get()
                self.warning(msg)

    def remove_bus(self, *_):
        bname = self._var_name.get().strip()
        exists = self.parser.what_is(bname)
        if exists == "cbus":
            protected = len(bname) > 3 and (bname[:3] == "in_" or bname[:3] == "out")
            if protected:
                msg = "Can not remove protected bus '%s'" % bname
                self.warning(msg)
            else:
                rs = self.parser.remove_bus(bname)
                self.refresh()
                self.status("Removed controlbus '%s'" % bname)
        else:
            msg = "'%s' is not an control bus" % bname
            self.warning(msg)
            
    def accept(self):
        self.destroy()

    def display_help(self):
        self.app.main_window().display_help("cbus")
    
    def increment_selection(self, *_):
        mx = self.proxy.control_bus_count()-1
        n = min(mx, self._current_selection+1)
        self.listbox.selection_clear(0, END)
        self.listbox.selection_set(n)
        self.select_bus()

    def decrement_selection(self, *_):
        n = max(0, self._current_selection-1)
        self.listbox.selection_clear(0, END)
        self.listbox.selection_set(n)
        self.select_bus()
