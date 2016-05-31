# llia.gui.tk.tk_controller_name_editor
# 2016.05.30

from __future__ import print_function
from Tkinter import Toplevel, Label, BOTH, Frame, StringVar, NS, N, END, W
import ttk

import llia.gui.tk.tk_factory as factory


class TkControllerNameEditor(Toplevel):

    def __init__(self, master, app):
        Toplevel.__init__(self, master)
        self.wm_title = "MIDI Controllers"
        self.app = app
        self.config = app.config
        self._current_controller=0
        self.protocol("WM_DELETE_WINDOW", self.accept)
        main = Frame(self)
        main.pack(expand=True)
        main.pack_propagate(False)
        lab_title = factory.label(main, "MIDI Controller Names")
        self.lab_warning = factory.warning_label(main, "")
        list_frame = Frame(main, width=248, height=320)
        list_frame.pack_propagate(False)
        self.listbox = factory.listbox(list_frame, command=self.select_controller)
        self.listbox.pack(expand=True, fill=BOTH)
        sb = factory.scrollbar(main, yclient=self.listbox)
        self.sync_list()
        self.var_name = StringVar()
        entry_name = factory.entry(main, self.var_name)
        b_help = factory.help_button(main, command = self.show_help)
        b_accept = factory.button(main, "Accept",command=self.accept)
        lab_title.grid(row=0, column=0, columnspan=4, pady=8)
        list_frame.grid(row=1, column=0, rowspan=6, columnspan=4, sticky=N)
        sb.grid(row=1, column=4, rowspan=6, sticky=NS)
        entry_name.grid(row=7, column=0, columnspan=1, sticky=W, padx=4, pady=8)
        self.lab_warning.grid(row=8, column=0, columnspan=5, sticky=W)
        b_accept.grid(row=9, column=0, columnspan=4, pady=8)
        b_help.grid(row=9, column=2, padx=4)
        
        entry_name.bind('<Return>', self.update_current)
        entry_name.bind('<Down>', self.increment_selection)
        entry_name.bind('<Up>', self.decrement_selection)
        self.listbox.bind('<Down>', self.increment_selection)
        self.listbox.bind('<Up>', self.decrement_selection)
        
    def duplicate_name_warning(self, name):
        if name:
            msg = "DUPLICATE NAME WARNING: %s" % name
            self.lab_warning.config(text=msg)
        
        
    def sync_list(self):
        names = {}
        self.listbox.delete(0, END)
        self.lab_warning.config(text="")
        for ctrl in range(128):
            name = self.config.controller_name(ctrl)
            if names.has_key(name):
                self.duplicate_name_warning(name)
            names[name] = True
            if str(name) == str(ctrl):
                name = ""
            self.listbox.insert(END, "[%3d]  %s" % (ctrl, name))
        
    def select_controller(self, *_):
        index = self.listbox.curselection()[0]
        name = self.listbox.get(index)[5:].strip()
        self.var_name.set(name)
        self._current_controller = index
        
    def increment_selection(self, *_):
        n = self._current_controller
        n = min(127, n+1)
        self.listbox.selection_clear(0, END)
        self.listbox.selection_set(n)
        self.select_controller()

    def decrement_selection(self, *_):
        n = self._current_controller
        n = max(0, n-1)
        self.listbox.selection_clear(0, END)
        self.listbox.selection_set(n)
        self.select_controller()
        
    def update_current(self, *_):
        try:
            ctrl = self._current_controller
            name = self.var_name.get().replace(" ","_")
            self.config.controller_name(ctrl, name)
            self.sync_list()
            self.increment_selection()
        except IndexError:
            pass                # Nothing selected
        
    def accept(self):
        for i in range(128):
            name = self.listbox.get(i)[5:].strip()
            self.config.controller_name(i, name)
        self.destroy()
            

    def show_help(self):
        self.app.main_window().show_help_dialog("controller_name")
