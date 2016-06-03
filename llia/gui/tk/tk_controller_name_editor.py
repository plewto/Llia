# llia.gui.tk.tk_controller_name_editor
# 2016.05.30

from __future__ import print_function
from Tkinter import Toplevel, Label, BOTH, Frame, StringVar, NS, N, END, W, EW, LEFT, RIGHT
import ttk

import llia.gui.tk.tk_factory as factory


class TkControllerNameEditor(Toplevel):

    def __init__(self, master, app):
        Toplevel.__init__(self, master)
        self.wm_title = "MIDI Controllers"
        self.app = app
        self.config = app.config
        self.parser = app.ls_parser
        self._current_controller=0
        self._save_backup()
        main = Frame(self)
        main.pack(expand=True)
        main.pack_propagate(False)
        lab_title = factory.label(main, "MIDI Controller Names")
        self.lab_warning = factory.warning_label(main, "")
        frame_list = Frame(main, width=248, height=320)
        frame_list.pack_propagate(False)
        self.listbox = factory.listbox(frame_list, command=self.select_controller)
        self.listbox.pack(expand=True, fill=BOTH)
        sb = factory.scrollbar(main, yclient=self.listbox)
        self.refresh()
        self.var_name = StringVar()
        entry_name = factory.entry(main, self.var_name)
        button_bar = Frame(main)
        b_refresh = factory.refresh_button(button_bar, command=self.refresh)
        b_help = factory.help_button(button_bar, command = self.show_help)
        b_accept = factory.accept_button(button_bar, command=self.accept)
        b_cancel = factory.cancel_button(button_bar, command=self.cancel)

        lab_title.grid(row=0, column=0, columnspan=4, pady=8)
        frame_list.grid(row=1, column=0, rowspan=6, columnspan=4, sticky=N)
        sb.grid(row=1, column=4, rowspan=6, sticky=NS)
        entry_name.grid(row=7, column=0, columnspan=1, sticky=W, padx=4, pady=8)
        self.lab_warning.grid(row=8, column=0, columnspan=5, sticky=W)
        button_bar.grid(row=9, column=0, columnspan=5, sticky=EW)
        b_refresh.pack(side=LEFT)
        b_help.pack(side=LEFT)
        factory.padding_label(button_bar).pack(side=LEFT)
        b_cancel.pack(side=RIGHT)
        b_accept.pack(side=RIGHT)
        entry_name.bind('<Return>', self.change_name)
        entry_name.bind('<Down>', self.increment_selection)
        entry_name.bind('<Up>', self.decrement_selection)
        self.listbox.bind('<Down>', self.increment_selection)
        self.listbox.bind('<Up>', self.decrement_selection)
        self.protocol("WM_DELETE_WINDOW", None)
        self.grab_set()
        self.mainloop()

    def _save_backup(self):
        acc = []
        for i in range(128):
            name = self.config.controller_name(i)
            acc.append(name)
        self._backup = acc
        
    def status(self, msg):
        self.app.main_window().status(msg)

    def warning(self, msg):
        self.app.main_window().warning(msg)
        msg = "WARNING: %s" % msg
        self.lab_warning.config(text=msg)

    def refresh(self):
        self.listbox.delete(0, END)
        self.lab_warning.config(text="")
        for ctrl in range(128):
            name = self.config.controller_name(ctrl)
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

    def change_name(self, *_):
        self.lab_warning.config(text="")
        try:
            ctrl = self._current_controller
            name = self.var_name.get().strip().replace(" ","_")
            self.parser.controller_name(ctrl, name, silent=True)
            self.refresh()
        except (IndexError, ValueError) as err:
            self.warning(err.message)
        
    def accept(self):
        for i in range(128):
            name = self.listbox.get(i)[5:].strip()
            self.config.controller_name(i, name)
        self.status("MIDI controller names updated.")
        self.destroy()
            
    def cancel(self):
        self.status("MIDI controller names restored.")
        for i,name in enumerate(self._backup):
            self.config.controller_name(i, name)
        self.destroy()
        
    def show_help(self):
        self.app.main_window().show_help_dialog("controller_name")
