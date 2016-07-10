# llia.gui.tk.discreate_control
#

from __future__ import print_function
import Tkinter as tk

import llia.constants as con
from llia.gui.abstract_control import AbstractControl
import llia.gui.tk.tk_factory as factory


class DiscreateControl(AbstractControl):

    # values array ((value, text)...)
    def __init__(self, master, param, editor, values):
        super(DiscreateControl, self).__init__(param, editor, master)
        self.var_value = tk.StringVar()
        self.var_value.set(values[0][0])
        self.radio_buttons = []
        for value, text in values:
            rb = factory.radio(master, text, self.var_value, value,
                               command=self.callback,
                               ttip = param)
            widget_key = "radio-%s" % value
            self.radio_buttons.append(rb)
            self._widgets[widget_key] = rb

    def callback(self):
        v = float(self.var_value.get())
        self.synth.x_param_change(self.param, v)
        self.synth.bank()[None][self.param] = v
        msg = "[%s] -> %s" % (self.param, v)
        self.editor.status(msg)

    def update_aspect(self):
        v  = self._current_value
        self.var_value.set(v)

    # def layout(self, x0=0, y0=0, ydelta=20, xdelta=40, rows=None):
    #     rows = rows or len(self(.radio_buttons)):
    #     for row in range(len(self.radio_buttons)):
    #         y = y0 + row * ydelta
    #         rb = self.radio_buttons[row]
    #         rb.place(x=x0, y=y)

    def layout(self, x0=0, y0=0, ydelta=20, xdelta=60, rows=None):
        rb_count = len(self.radio_buttons)
        rows = rows or rb_count
        row, column = 0, 0
        row_counter = 0
        for index in range(rb_count):
            x = x0 + column * xdelta
            y = y0 + row_counter * ydelta
            rb = self.radio_buttons[index]
            rb.place(x=x, y=y)
            row_counter += 1
            if row_counter > rows:
                column += 1
                row_counter = 0

    
            

        
