# llia.gui.tk.freq_spinner
#
# Defines oscilator frequency control using Spinbox


from __future__ import print_function
import Tkinter as tk
from llia.gui.abstract_control import AbstractControl
import llia.gui.tk.tk_factory as factory

class FrequencySpinnerControl(AbstractControl):

    def __init__(self, master, param, editor,
                 from_=0, to=32):
        super(FrequencySpinnerControl, self).__init__(param, editor, master)
        self.var_value = tk.StringVar()
        self.spinner = factory.float_spinbox(master, self.var_value,
                                             from_ = from_, to = to,
                                             command = self.callback)
        self.spinner.bind("<Enter>", self.enter_callback)
        self._widgets["spinbox"] = self.spinner
        self.reset()

    def reset(self):
        self.var_value.set(1.000)

    def enter_callback(self, *_):
        msg = "[%s] -> %s" % (self.param, self.var_value.get())
        self.editor.status(msg)
        
    def callback(self, *_):
        freq = float(self.var_value.get())
        self.synth.x_param_change(self.param, freq)
        self.synth.bank()[None][self.param] = freq
        self.enter_callback()

    def update_aspect(self):
        try:
            freq = abs(self._current_value)
            self.var_value.set(freq)
        except TypeError:
            pass

    def layout(self, offset=(0,0), width=75, height=24):
        x,y = offset
        self.spinner.place(x=x, y=y, width=width, height=height)
        
    
    
        
        
        
