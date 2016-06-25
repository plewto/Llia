# llia.gui.tk.tk_subeditor
# 22-June-2016

from __future__ import print_function
from Tkinter import Frame
import abc

import llia.gui.tk.tk_factory as factory

class TkSubEditor(Frame):

    # parent - either TkSubEditor or TkSynthWindow
    # 
    def __init__(self, tk_master, parent, name):
        Frame.__init__(self, tk_master)
        self.parent = parent
        self.synth = parent.synth
        self.config(background=factory.bg())
        self._child_editors = {}
        self._controls = {}

    def add_child_editor(self, name, child):
        self._child_editors[name] = child

    def status(self, msg):
        self.parent.status(msg)

    def warning(self, msg):
        self.parent.warning(msg)

    def set_value(self, param, value):
        try:
            c = self._controls[param]
            c.value(value)
        except KeyError:
            pass
        for ed in self._child_editors.items():
            ed.set_value(param, value)
    
    @abc.abstractmethod
    def sync(self, *ignore):
        for key, ed in self._child_editors.items():
            if key not in ignore:
                ed.sync(*ignore)
        
        
        
        
