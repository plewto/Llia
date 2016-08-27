# llia.gui.tk.decade_control
#
# Defines compound synth control with
# coarse (radio button) and fine (slider) widgets
# where coarse values are powers of 10

from __future__ import print_function
import Tkinter as tk

from llia.util.lmath import log2, logn, log10, clip
from llia.gui.abstract_control import AbstractControl
import llia.gui.tk.tk_factory as factory

class DecadeControl(AbstractControl):
    
    """
    Defines compound coarse/fine synth GUI editor control.
    Coarse control provided by radio buttons.
    Fine control provided by slider (Scale in Tk parlance).
    
    Widgets are not automatically placed on the parent to allow for
    custom layouts. Use the layout method to arrange widgets on the 
    parent container.
    """
                             
    
    def __init__(self, master, param, editor,
                 coarse = (0.001, 1000),
                 limit = (0.001, 9999)):
        """
        Constructs new DecadeControl object.
        ARGS:
           master - The TK master widget for these components.
           param  - String, synth parameter.
           editor - An instance of TkSubEditor
           coarse - Tuple (a, b) sets range of coarse controls.
                    a and b must both be powers of 10 with a < b.
                    A radio button is created for each power of 10
                    between a and b.
           limit  - Tuple (mn, mx), sets minimum and maximum value.
        """
        super(DecadeControl, self).__init__(param, editor, master)
        self._min_value, self._max_value = limit
        start, end = coarse
        start, end = min(start, end), max(start, end)
        decades = []
        value = start
        while value <= end:
            power = log10(value)
            if power == 0:
                txt = "1"
            elif power < 1:
                txt = "1/%d" % int(10**abs(power))
            else:
                txt = str(int(10**power))
            decades.append((value, txt))
            value *= 10
        decades.reverse()
        self.var_decade = tk.StringVar()
        self.var_scale = tk.IntVar()
        self.var_decade.set(start)
        self.var_scale.set(1)
        self._radio_buttons = []
        for value, txt in decades:
            rb = factory.radio(master, txt, self.var_decade, value,
                               command=self.callback,
                               ttip = "%s range" % param)
            widget_key = "radio-range-%d" % value
            self._widgets[widget_key] = rb
            self._radio_buttons.append(rb)
            rb.bind("<Enter>", self.enter_callback)
        s_scale = factory.scale(master, from_=90, to=0,
                                var = self.var_scale,
                                command = self.callback,
                                ttip = "%s scale" % param)
        s_scale.bind("<Enter>", self.enter_callback)
        self._widgets["slider"] = s_scale
        lab_value = factory.label(master, "X.XXX")
        self._widgets["label-value"] = lab_value
        self._editor = editor
        self._param = param

    def enter_callback(self, *_):
        msg = "[%s] -> %s" % (self._param, self.value())
        self._editor.status(msg)
    
    def callback(self, *_):
        d = float(self.var_decade.get())
        delta = d/10.0
        s = float(self.var_scale.get())
        value = clip(d + s*delta, self._min_value, self._max_value)
        self.synth.x_param_change(self.param, value)
        program = self.synth.bank()[None]
        program[self.param] = value
        if d <= 1:
            frmt = "%6.4f"
        else:
            frmt = "%6.0f"
        self._widgets["label-value"].config(text = frmt % value)
        msg = "[%s] -> " + frmt
        msg = msg % (self.param, value)
        self.editor.status(msg)

    def update_aspect(self, *_):
        try:
            value = self._current_value
            decade = float(10**int(log10(value)))
            ratio = decade/value
            pos = int(100 * ratio)
            self.var_decade.set(decade)
            self.var_scale.set(pos)
            if decade <= 1:
                frmt = "%6.4f"
            else:
                frmt = "%6.0f"
            self.widget("label-value").config(text = frmt % value)
        except (ValueError, ZeroDivisionError):
            self.widget("label-value").config(text="ERR")
              
            
    def layout(self, offset=(0, 0),
               button_offset = (0, 0, 20),   # x y row_height
               slider_offset = (80, 0, 14, 150),  # x y width height
               label_offset = (0, 150)):
        """
        Arrange widgets on Tk master container.
        ARGS:
          offset        - Tuple (x0,y0), upper left reference point, the 
                          location to place widgets.
          button_offset - Tuple (x, y, delta),  location of 'decade' radio
                          buttons.
                          x - horizontal offset from x0
                          y - vertical offset from y0
                          delta - vertical spacing of buttons. 
                          If None, do not include radio buttons.
          slider_offset - Tuple (x, y, w, h),  location of slider relative to 
                          (x0,y0).
                          x - horizontal offset from x0
                          y - vertical offset from y0
                          w - slider width
                          h - slider height
                          If None, do not include slider.
          label_offset  - Tuple (xw,yw), location of current value label.
                          If None, do not include label.
        """
        x0, y0 = offset
        if button_offset:
            xb, yb, ydelta = button_offset
            rows = len(self._radio_buttons)
            for row in range(rows):
                x = x0 + xb
                y = y0 + yb + row * ydelta
                rb = self._radio_buttons[row]
                rb.place(x=x, y=y)
        if slider_offset:
            xs, ys, w, h = slider_offset
            s = self.widget("slider")
            s.place(x=x0+xs, y=y0+ys, width=w, height=h)
        if label_offset:
            xw, yw = label_offset
            w = self.widget("label-value")
            w.place(x=x0+xw, y=y0+yw)
