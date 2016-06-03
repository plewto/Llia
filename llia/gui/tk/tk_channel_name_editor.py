# llia.gui.tk.tk_channel_name_editor
# 2016.06.01
#

from __future__ import print_function
from Tkinter import Toplevel, Label, BOTH, Frame, StringVar, NS, N, END, W, EW, LEFT, RIGHT, E
import ttk

import llia.gui.tk.tk_factory as factory


class TkChannelNameEditor(Toplevel):

    def __init__(self, master, app):
        Toplevel.__init__(self, master)
        self.wm_title = "MIDI Channels"
        self.app = app
        self.config = app.config
        self.parser = app.ls_parser
        self._current_index=0
        self._save_backup()
        main = Frame(self)
        main.pack(expand=True)
        lab_title = factory.dialog_title_label(main, "MIDI Channels")
        frame_list = Frame(main, width=248, height=320)
        frame_list.pack_propagate(False)
        self.listbox = factory.listbox(frame_list, command=self.select)
        self.listbox.pack(expand=True, fill=BOTH)
        self.lab_warning = factory.warning_label(main)
        self.var_name = StringVar()
        entry_name = factory.entry(main, self.var_name)
        button_bar = Frame(main)
        b_refresh = factory.refresh_button(button_bar, command=self.refresh)
        b_help = factory.help_button(button_bar, command=self.show_help)
        b_accept = factory.accept_button(button_bar, command=self.accept)
        b_cancel = factory.cancel_button(button_bar, command=self.cancel)
        b_refresh.pack(side=LEFT)
        b_help.pack(side=LEFT)
        factory.padding_label(button_bar).pack(side=LEFT)
        b_cancel.pack(side=RIGHT)
        b_accept.pack(side=RIGHT)
        lab_title.grid(row=0, column=0, columnspan=5, pady=8)
        frame_list.grid(row=1, column=0, rowspan=5, columnspan=6, padx=4, pady=8)
        entry_name.grid(row=6, column=0, columnspan=5, sticky=W, padx=4, pady=0)
        self.lab_warning.grid(row=7, column=0, columnspan=6, sticky=W, padx=4, pady=8)
        button_bar.grid(row=8, column=0, columnspan=5, sticky=W+E, padx=4, pady=8)
        self.refresh()
        self.protocol("WM_DELETE_WINDOW", None) # ISSUE: Not Working
        entry_name.bind('<Return>', self.change_name)
        entry_name.bind('<Down>', self.increment_selection)
        entry_name.bind('<Up>', self.decrement_selection)
        self.listbox.bind('<Down>', self.increment_selection)
        self.listbox.bind('<Up>', self.decrement_selection)
        self.grab_set()
        self.mainloop()

    def _save_backup(self):
        self._backup = []
        for i in range(16):
            c = i+1
            name = self.config.channel_name(c)
            self._backup.append(name)
        
    def status(self, msg):
        self.app.main_window().status(msg)

    def warning(self, msg):
        msg = "WARNING: %s" % msg
        self.lab_warning.config(text = msg)
        self.lab_warning.update_idletasks()
        print(msg)
        
    def refresh(self):
        self.listbox.delete(0, END)
        for i in range(16):
            channel = i+1
            name = self.config.channel_name(channel)
            txt = "[%2d] " % channel
            if name == "" or name == str(channel):
                pass
            else:
                txt = txt + "%s" % name
            self.listbox.insert(END, txt)

    @staticmethod
    def split_channel_name(s):
        try:
            s = s[4:].strip()
            return s
        except IndexError:
            return ""
            
    def select(self, *_):
        index = self.listbox.curselection()[0]
        name = self.listbox.get(index)
        name = self.split_channel_name(name)
        self.var_name.set(name)
        self._current_index = index
        
    def show_help(self):
        self.app.main_window().show_help_dialog("channel_name")

    def change_name(self, *_):
        self.lab_warning.config(text="")
        try:
            channel = self.listbox.curselection()[0]+1
            new_name = self.var_name.get().strip().replace(' ','_')
            old_name = self.config.channel_name(channel)
            stype = self.parser.what_is(new_name)
            if not stype or stype == "channel":
                self.parser.forget(old_name)
                self.parser.channel_name(channel, new_name, silent=True)
            else:
                msg = "Can not use %s '%s' as channel name" % (stype, new_name)
                self.warning(msg)
        except ValueError as err:
            self.warning(err.message)
        except IndexError:
            msg = "No channel selected"
            self.warning(msg)
        self.refresh()
                    
    def increment_selection(self, *_):
        n = self._current_index
        n = min(15, n+1)
        self.listbox.selection_clear(0, END)
        self.listbox.selection_set(n)
        self.select()

    def decrement_selection(self, *_):
        n = self._current_index
        n = max(0, n-1)
        self.listbox.selection_clear(0, END)
        self.listbox.selection_set(n)
        self.select()

    def accept(self):
        msg = "MIDI Channel names changed"
        self.status(msg)
        self.destroy()

    def cancel(self):
        for i,name in enumerate(self._backup):
            self.config.channel_name(i+1, name)
        self.status("MIDI channel name change canceled")
        self.destroy()
