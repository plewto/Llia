# llia.gui.tk.freq_spinner
#
# Defines oscilator frequency control using Spinbox
#
# Key bindings:
#   up          - increment +1
#   right       - increment +0.1
#   shift-right - increment +0.01
#   ctrl-right  - increment +0.001
#   alt-right   - scale x2
#   down        - increment -1
#   left        - increment -0.1
#   shift-left  - increment -0.01
#   ctrl-left   - increment -0.001
#   alt-left    = scale x1/2


from __future__ import print_function
import Tkinter as tk
from llia.gui.abstract_control import AbstractControl
import llia.gui.tk.tk_factory as factory

class FrequencySpinnerControl(AbstractControl):

    def __init__(self, master, param, editor,
                 from_=0, to=32):
        super(FrequencySpinnerControl, self).__init__(param, editor, master)
        self.minval = min(from_, to)
        self.maxval = max(from_, to)
        self.var_value = tk.StringVar()
        self.spinner = factory.float_spinbox(master, self.var_value,
                                             from_ = from_, to = to,
                                             command = self.callback)
        self.spinner.bind("<Enter>", self.enter_callback)
        self.spinner.bind("<Right>", lambda x: self.bump_value(0.1))
        self.spinner.bind("<Shift-Right>", lambda x: self.bump_value(0.01))
        self.spinner.bind("<Control-Right>", lambda x: self.bump_value(0.001))
        self.spinner.bind("<Alt-Right>", lambda x: self.scale_value(2))
        self.spinner.bind("<Left>", lambda x: self.bump_value(-0.1))
        self.spinner.bind("<Shift-Left>", lambda x: self.bump_value(-0.01))
        self.spinner.bind("<Control-Left>", lambda x: self.bump_value(-0.001))
        self.spinner.bind("<Alt-Left>", lambda x: self.scale_value(0.5))
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

    def bump_value(self, n):
        try:
            v = float(self.var_value.get()) + n
            v = min(max(v,self.minval),self.maxval)
            self.value(v)
            self.callback()
        except TypeError:
            msg = "Invalid %s value: '%s'"
            msg = msg % (self.param, self.var_value.get())
            self.editor.warning(msg)

    def scale_value(self, s):
        try:
            v = float(self.var_value.get())
            v = min(max(v*s,self.minval),self.maxval)
            self.value(v)
            self.callback()
        except TypeError:
            msg = "Invalid %s value: '%s'"
            self.editor.warning(msg % (self.param, self.var_value.get()))
            
    def layout(self, offset=(0,0), width=75, height=24):
        x,y = offset
        self.spinner.place(x=x, y=y, width=width, height=height)
        
    
    
        
        
        
