# llia.gui.tk.tk_subeditor
# 22-June-2016

from __future__ import print_function
from Tkinter import Frame
import abc

from llia.generic import is_synth_control
import llia.gui.tk.tk_factory as factory



class TkSubEditor(Frame):

    # parent - either TkSubEditor or TkSynthWindow
    # 
    def __init__(self, tk_master, parent, name):
        Frame.__init__(self, tk_master)
        self.parent = parent
        self.synth = parent.synth
        self.bank = self.synth.bank()
        self.config(background=factory.bg())
        self._child_editors = {}
        self._controls = {}

    def add_control(self, param, sctrl):
        if is_synth_control(sctrl):
            self._controls[param] = sctrl
        else:
            msg = "Can not add %s as synth control to TkSubEditor, param = %s"
            msg = msg % (type(sctrl), param)
            raise(TypeError(msg))

    def get_control(self, param):
        acc = []
        try:
            acc.append(self._controls[param])
        except KeyError:
            pass
        for child in self._child_editors:
            acc.append(child.get_control[param])
        return acc

    def has_control(self, param):
        f = self._controls.has_key(param)
        if f:
            return True
        else:
            for child in self._child_editors:
                f = child.has_control(param)
                if f: return True
        return False
    
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
    
    def sync(self, *ignore):
        for key, ed in self._child_editors.items():
            if key not in ignore:
                ed.sync(*ignore)
        prog = self.bank[None]
        for param, sctrl in self._controls.items():
            sctrl.value(prog[param])
            
        
        
        
        
