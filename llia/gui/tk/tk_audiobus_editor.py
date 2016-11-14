# llia.gui.tk.tk_audiobus_editor
# 2016.05.31
#

from __future__ import print_function
from Tkinter import Toplevel, Label, BOTH, StringVar, NS, N, END, W, EW, LEFT, RIGHT

import llia.gui.tk.tk_factory as factory


class TkAudiobusEditor(Toplevel):

    def __init__(self, master, app):
        Toplevel.__init__(self, master)
        self.wm_title = "Audio Buses"
        self.app = app
        self.proxy = app.proxy
        self.parser = app.ls_parser
        main = factory.frame(self)
        main.pack(expand=True)
        lab_title = factory.label(main, "Audio Busses")
        frame_list = factory.frame(main)
        frame_list.config(width=248, height=320)
        frame_list.pack_propagate(False)
        self.listbox = factory.listbox(frame_list, command=self.select_bus)
        self.listbox.pack(expand=True, fill=BOTH)
        sb = factory.scrollbar(main, yclient=self.listbox)
        lab_name = factory.label(main, "Name")
        self._var_name = StringVar()
        entry_name = factory.entry(main, self._var_name, ttip="Audio bus name")
        self.lab_warning = factory.warning_label(main)
        button_bar = factory.frame(main)
        #b_remove = factory.delete_button(button_bar,ttip="Delete audio bus",command=self.remove_bus)
        b_add = factory.add_button(button_bar, ttip="Add new audio bus", command=self.add_bus)
        b_accept = factory.accept_button(button_bar, command=self.accept)
        b_help = factory.help_button(button_bar, command=self.help_)
        lab_title.grid(row=0, column=0, columnspan=6, pady=8)
        frame_list.grid(row=1, column=0, rowspan=5, columnspan=5, pady=8, padx=4)
        sb.grid(row=1, column=4, rowspan=5, sticky=NS, pady=8, padx=4)
        lab_name.grid(row=6, column=0, sticky=W, padx=4)
        entry_name.grid(row=6, column=1)
        self.lab_warning.grid(row=8, column=0, columnspan=6)
        button_bar.grid(row=9, column=0, columnspan=6, padx=8, pady=4)
        #b_remove.grid(row=0, column=0)
        b_add.grid(row=0, column=1)
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
        for k in self.proxy.audio_bus_names():
            self.listbox.insert(END, k)
        
    def select_bus(self, *_):
        index = self.listbox.curselection()[0]
        bname = self.listbox.get(index).strip()
        self._var_name.set(bname)
        self._current_selection = index

    def add_bus(self, *_):
        for bname in self._var_name.get().split(" "):
            exists = self.parser.what_is(bname)
            if exists == 'abus':
                pass
            elif exists != '':
                msg = "Invalid bus name: '%s'" % bname
                self.warning(msg)
                break;
            else:
                busname = bname.strip()  # Ignore whitespace only
                if busname:
                    rs =self.parser.abus(busname)
        self._var_name.set('')
        self.refresh()
    
    # def remove_bus(self, *_):
    #     bname = self._var_name.get().strip()
    #     exists = self.parser.what_is(bname)
    #     if exists == "abus":
    #         protected = len(bname) > 3 and (bname[:3] == "in_" or bname[:3] == "out")
    #         if protected:
    #             msg = "Can not remove protected bus '%s'" % bname
    #             self.warning(msg)
    #         else:
    #             rs = self.parser.remove_bus(bname)
    #             self.refresh()
    #             self.status("Removed audiobus '%s'" % bname)
    #     else:
    #         msg = "'%s' is not an audio bus" % bname
    #         self.warning(msg)
            
    def accept(self):
        self.destroy()

    def help_(self):
        self.app.main_window().display_help("abus")
    
    def increment_selection(self, *_):
        mx = self.proxy.audio_bus_count()-1
        n = min(mx, self._current_selection+1)
        self.listbox.selection_clear(0, END)
        self.listbox.selection_set(n)
        self.select_bus()

    def decrement_selection(self, *_):
        n = max(0, self._current_selection-1)
        self.listbox.selection_clear(0, END)
        self.listbox.selection_set(n)
        self.select_bus()
    
