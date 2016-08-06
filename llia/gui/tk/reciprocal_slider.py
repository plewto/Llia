# llia.gui.tk.reciprocal_slider
#
# A compound synth control useful for (non-zero) scaling factors.
# The widget compliment includes a slider (tk "scale") , and two optional
# checkbuttons.
# The slider range is between 1 and a prograamed upper limit.
# The two checkbuttons modify the slider value by
#   1) negative   value = -1 * slider
#   2) reciprocal value = 1/slider
#

from __future__ import print_function
import Tkinter as tk

from llia.util.lmath import log2, logn, log10, clip
from llia.gui.abstract_control import AbstractControl
from llia.curves import linear_function
import llia.gui.tk.tk_factory as factory

class ReciprocalSlider(AbstractControl):

    def __init__(self, master, param, editor,
                 range_ = 1000,
                 degree = 2,
                 clip = None):
        super(ReciprocalSlider, self).__init__(param, editor, master)
        self.degree = degree
        self.inv_degree = 1.0/degree
        self.range_ = range_
        if clip:
            self._clip = clip
        else:
            self._clip = (1.0/range_, range_)
        self.var_aspect = tk.StringVar()
        self.var_sign = tk.IntVar()
        self.var_invert = tk.IntVar()
        self.var_aspect.set(self._clip[0])
        self.var_sign.set(0)
        self.var_invert.set(0)
        s = factory.scale(master, from_ = 1, to=0, resolution = 0.005,
                          command= self.callback,
                          var = self.var_aspect)
        cb_sign = factory.checkbutton(master, "-", self.var_sign,
                                      command = self.callback)
        cb_invert = factory.checkbutton(master, "1/n", self.var_invert,
                                        command = self.callback)
        self._widgets["slider"] = s
        self._widgets["checkbutton-sign"] = cb_sign
        self._widgets["checkbutton-invert"] = cb_invert

    def q_sign(self):
        # Return true if sign checkbutton selected
        return self.var_sign.get() != 0

    def q_invert(self):
        # Returns true if invert checkbutton selected
        return self.var_invert.get() != 0

    def aspect_to_value(self, a):
        a = float(a)
        a = a**self.degree
        v = a*(self.range_-1) + 1
        if self.q_sign(): v = -1*v
        if self.q_invert(): v = 1.0/v
        return v

    def value_to_aspect(self, v):
        v = abs(v)
        if v < 1: v = 1.0/v
        r = 1.0/(self.range_-1)
        a = v*r-r
        a = a**self.inv_degree
        return a
    
    def callback(self, *_):
        a = self.var_aspect.get()
        v = float(self.aspect_to_value(a))
        self.synth.x_param_change(self.param, v)
        program = self.synth.bank()[None]
        program[self.param] = v
        msg = "[%s] -> %6.4f" % (self.param, v)
        self.editor.status(msg)

    def update_aspect(self, *_):
        value = self._current_value
        if value < 0:
            self.var_sign.set(1)
        else:
            self.var_sign.set(0)
        if abs(value) < 1:
            self.var_invert.set(1)
            value = 1.0/value
        else:
            self.var_invert.set(0)
        a = self.value_to_aspect(value)
        self.var_aspect.set(a)

    def layout(self, offset=(0,0),
               width=14, height=150,
               sign_offset = (18, 21),
               invert_offset = (18, 0)):
        x0, y0 = offset
        self._widgets["slider"].place(x=x0, y=x0, width=width, height=height)
        if sign_offset:
            x = x0 + sign_offset[0]
            y = y0 + sign_offset[1]
            self._widgets["checkbutton-sign"].place(x=x, y=y)
        if invert_offset:
            x = x0 + invert_offset[0]
            y = y0 + invert_offset[1]
            self._widgets["checkbutton-invert"].place(x=x, y=y)
                   
            
                
                 
