# llia.gui.tk.expslider
#
# Defines compound synth control with
# an exponential slider and optional "invert" checkbox.

from __future__ import print_function
import Tkinter as tk

from llia.util.lmath import log2, logn, log10, clip
from llia.gui.abstract_control import AbstractControl
from llia.curves import linear_function
import llia.gui.tk.tk_factory as factory



class ExpSlider(AbstractControl):

    """
    Defines compound synth control with exponential-response slider and
    optional sign checkbox.

    Widgets are not automatically placed on the parent.  Use the layout
    method to arrange widgets on the parent container.
    """

    def __init__(self, master, param, editor,
                 range_ = 1000,
                 degree = 2,
                 clip=None,
                 ttip=""):
        """
        Construct new ExpSlider object.
        ARGS:
          master - The parent Tk container.
          param  - String, synth parameter.
          editor - An instance of TkSubEditor
          range_ - Float or Int, the maximum value magnitude.  The minimum
                   magnitude is always 0.
          degree - Positive Int of Float, The exponential degree.
          ttip   - String, tool tip text.
        """
        super(ExpSlider, self).__init__(param, editor, master)
        self.degree = degree
        self.inv_degree = 1.0/degree
        if clip:
            self._clip = clip
        else:
            self._clip = (0, range_)
        self.var_aspect = tk.StringVar()
        self.var_sign = tk.IntVar()
        self.var_aspect.set(0.0)
        self.var_sign.set(0)
        self.range_ = [0,range_]
        ttip = ttip or "%s" % param
        s = factory.scale(master,
                          from_ = 1.0, to=0.0, resolution = 0.005,
                          command = self.callback,
                          var=self.var_aspect,
                          ttip=ttip)
        cb = factory.checkbutton(master, "Inv", self.var_sign,
                                 command = self.callback)
        self._widgets["slider"] = s
        self._widgets["checkbutton-sign"] = cb
        self._editor = editor
        self._param = param
        s.bind("<Enter>", self.enter_callback)

    def enter_callback(self, *_):
        msg = "[%s] -> %s" % (self._param, self.value())
        self._editor.status(msg)

    def qinvert(self):
        return self.var_sign.get() != 0
        
    def aspect_to_value(self, a):
        mn, mx = self._clip
        n = float(a)**self.degree
        v = n*self.range_[1]
        v = max(min(v, mx), mn)
        if self.qinvert(): v = -1 * v
        return v

    def value_to_aspect(self, v):
        mn, mx = self._clip
        v = abs(v)
        v = max(min(v, mx), mn)
        d = float(v)/self.range_[1]
        a = d**self.inv_degree
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
        a = self.value_to_aspect(value)
        self.var_aspect.set(a)
        
    def layout(self, offset=(0,0),
               width=14, height = 150,
               checkbutton_offset = (-5, 150)):
        """
        Arrange widgets on Tk master.
        ARGS:
          offset - Tuple (x,y), Upper left location of slider, default (0,0).
          width  - Int, slider width, default 14.
          height - Int, slider height, default 150.
          checkbutton_offset - Tuple (x1,y1), optional 'invert' checkbutton
                               location relative to offset.  Default (-5,150).
                               If None, do not draw checkbutton.
        """
        x0, y0 = offset
        self._widgets["slider"].place(x=x0, y=y0, width=width, height=height)
        if checkbutton_offset:
            x = x0 + checkbutton_offset[0]
            y = y0 + checkbutton_offset[1]
            self._widgets["checkbutton-sign"].place(x=x, y=y)
        
