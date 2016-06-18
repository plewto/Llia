# llia.gui.tk.tk_history
# 2016.05.29
#
# Defines basic lliascript text editor.

from __future__ import print_function
from Tkinter import (Toplevel, END, NW, SW, X, Y, BOTH, LEFT, RIGHT,
                     TOP, Text, Scrollbar, VERTICAL, HORIZONTAL, NS, EW)

import tkFileDialog
import ttk

import llia.gui.tk.tk_factory as factory

class TkHistoryEditor(Toplevel):

    def __init__(self, master, app):
        Toplevel.__init__(self, master)
        self.config(background=factory.bg())
        self.wm_title("Lliascript History")
        self.app = app
        self.filename = ""
        toolbar = factory.frame(self)
        south = factory.frame(self)
        toolbar.pack(side=TOP, anchor=NW, expand=True, fill=X)
        south.pack(anchor=SW, expand=True, fill=BOTH)
        b_open = factory.button(toolbar, "Open", ttip="Open lliascript file",
                                command=self.open_lliascript_file)
        b_save = factory.button(toolbar, "Save", ttip="Save lliascript file",
                                command=self.save_lliascript_file)
        b_exec = factory.button(toolbar, "Exec", ttip="Execute text",
                                command=self.exec_)
        b_compose = factory.button(toolbar, "Compose",
                                   ttip="Build script from current state",
                                   command=self.compose_current_state)
        b_help = factory.help_button(toolbar)
        b_help.config(command=self.help_)
        b_open.pack(side=LEFT, expand=True, fill=X)
        b_save.pack(side=LEFT, expand=True, fill=X)
        b_exec.pack(side=LEFT, expand=True, fill=X)
        b_compose.pack(side=LEFT, expand=True, fill=X)
        b_help.pack(side=LEFT, expand=True, fill=X)
        self.text_widget = Text(south)
        sb1 = Scrollbar(south, orient=VERTICAL, 
                        command=self.text_widget.yview)
        sb2 = Scrollbar(south, orient=HORIZONTAL, 
                        command=self.text_widget.xview)
        self.text_widget.config(yscrollcommand = sb1.set)
        self.text_widget.config(xscrollcommand = sb2.set)
        self.text_widget.grid(row=0, column=0, rowspan=5, columnspan=5)
        sb1.grid(row=0, column=5, rowspan=5, sticky=NS)
        sb2.grid(row=5, column=0, columnspan=5, sticky=EW)
        self._get_current_history()
        self.grab_set()
        self.mainloop()
        

    def _get_current_history(self):
        txt = self.app.ls_parser.get_history()
        self.text_widget.delete(1.0, END)
        self.text_widget.insert(END, txt)

    def open_lliascript_file(self):
        options = {'defaultextension' : '.py',
                   'filetypes' : [('all files', '*'), 
                                  ('Python files', '*.py')],
                   'initialfile' : self.filename,
                   'parent' : self,
                   'title' : "Open Lliascript File"}
        fname = tkFileDialog.askopenfilename(**options)
        if fname:
            try:
                with open(fname, 'r') as input:
                    data = input.read()
                    self.text_widget.delete(1.0, END)
                    self.text_widget.insert(END, data)
                    self.filename = fname
                    self.wm_title("Lliascript: '%s'" % fname)
            except Exception as ex:
                self.app.warning(ex.message)

    def save_lliascript_file(self):
        options = {'defaultextension' : '.py',
                   'filetypes' : [('all files', '*'), 
                                  ('Python files', '*.py')],
                   'initialfile' : self.filename,
                   'parent' : self,
                   'title' : "Save Lliascript File"}
        fname = tkFileDialog.asksaveasfilename(**options)
        if fname:
            try:
                with open(fname, 'w') as output:
                    data = self.text_widget.get(1.0, END)
                    output.write(data)
                    self.filename = fname
                    self.wm_title("Lliascript: '%s'" % fname)
            except Exception as ex:
                self.app.warning(ex.message)
                    
    def compose_current_state(self):
        self.app.ls_parser.compose()
        self._get_current_history()

    def exec_(self):
        code = self.text_widget.get(1.0, END)
        self.app.ls_parser.batch(code)

    def help_(self):
        self.app.main_window().display_help("history")
        
        
