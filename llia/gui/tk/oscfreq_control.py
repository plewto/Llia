# llia.gui.tk.oscfreq_control
#
# Defines compound control for oscillator frequency:
#     Coarse, octaves (radio buttons)
#     Transpose, slider 0 to 11 steps
#     Detune, slider, 0 to 99 cents
#     "Off" checkbutton


from __future__ import print_function
import Tkinter as tk

import llia.constants as con
from llia.util.lmath import log2, logn, log10, clip
from llia.gui.abstract_control import AbstractControl
import llia.gui.tk.tk_factory as factory

class OscFrequencyControl(AbstractControl):

    def __init__(self, master, param, editor):
        """
        Create new OscFrequencyControl object.
        Widgets are not automatically added to the Tk master.   Call the 
        layout method to place widgets using a default layout.  
        
        ARGS:
          param  - String, SC synth parameter.
          editor - An instance of TkSubEditor
          master - Tk container.
        """
        super(OscFrequencyControl, self).__init__(param, editor, master)
        octaves = [(3, "+3"),(2, "+2"),(1, "+1"),(0, " 0"),
                   (-1,"-1"),(-2,"-2"),(-3,"-3")]
        self.var_octave = tk.StringVar()  # Octave number -3 ... +3
        self.var_transpose = tk.IntVar()  # Transpose steps, 0 ... 11
        self.var_detune = tk.IntVar()     # Detune in cents 0 ... 99
        self.var_zero = tk.IntVar()       # 0 -> osc != 0,  1 -> osc freq = 0
        self.var_octave.set(0)
        self.var_transpose.set(0)
        self.var_detune.set(0)
        self.var_zero.set(0)
        self._radio_buttons = []
        for value, text in octaves:
            rb = factory.radio(master, text, self.var_octave, value,
                               command = self.callback,
                               ttip = "%s octave" % param)
            widget_key = "radio-octave-%d" % value
            self._widgets[widget_key] = rb
            self._radio_buttons.append(rb)
            rb.bind("<Enter>", self.enter_callback)
        s_step = factory.scale(master, from_=11, to=0,
                               var = self.var_transpose,
                               command = self.callback,
                               ttip = "%s transpose (steps)" % param)
        s_detune = factory.scale(master, from_=99, to=0,
                                 var = self.var_detune,
                                 command=self.callback,
                                 ttip = "%s detune (cents)" % param)
        cb_zero = factory.checkbutton(master, "Off")
        cb_zero.config(command=self.callback,var = self.var_zero)
        ## Labels
        lab_transpose = factory.label(master, "00")
        lab_detune = factory.label(master, "000")
        lab_value = factory.label(master, "1.0000")
        self._widgets["scale-transpose"] = s_step
        self._widgets["scale-detune"] = s_detune
        self._widgets["checkbutton-zero"] = cb_zero
        self._widgets["label-transpose"] = lab_transpose
        self._widgets["label-detune"] = lab_detune
        self._widgets["label-value"] = lab_value
        self._editor = editor
        self._param = param
        s_step.bind("<Enter>", self.enter_callback)
        s_detune.bind("<Enter>", self.enter_callback)

        

    def enter_callback(self, *_):
        try:
            octave = int(self.var_octave.get())
            step = self.var_transpose.get()
            detune = self.var_detune.get()
            frmt = "[%s] -> [octave %d, step %d, detune %d cents] = freq %6.4f"
            msg = frmt % (self._param, octave, step, detune, self.value())
            self._editor.status(msg)
        except TypeError:
            pass   # Values may not be assigned yet
        
    def callback(self, *_):
        octave = int(self.var_octave.get())
        step = self.var_transpose.get()
        detune = self.var_detune.get()
        cents = 1200*octave + 100*step + detune
        ratio = con.RCENT**cents
        zero = not self.var_zero.get()
        ratio *= zero
        if ratio == 0:
            self.widget("label-transpose").config(text="--")
            self.widget("label-detune").config(text="---")
            self.widget("label-value").config(text ="OFF")
        else:
            self.widget("label-transpose").config(text="%2d" % int(step))
            self.widget("label-detune").config(text="%3d" % int(detune))
            self.widget("label-value").config(text ="%6.4f" % ratio)
        self.synth.x_param_change(self.param, ratio)
        self.synth.bank()[None][self.param] = float(ratio)
        msg = "[%s] -> %s" % (self.param, ratio)
        self.editor.status(msg)
        
    def update_aspect(self):
        try:
            ratio = abs(self._current_value)
            if ratio:
                ratio = abs(ratio)
                cents = int(logn(ratio, con.RCENT))
                octave = cents/1200
                step = (cents-1200*octave)/100
                detune = cents -1200*octave - 100*step
                self.var_octave.set(octave)
                self.var_transpose.set(step)
                self.var_detune.set(detune)
                self.var_zero.set(0)
                self.widget("label-value").config(text = "%6.4f" % ratio)
                self.widget("label-transpose").config(text = "%2d" % step)
                self.widget("label-detune").config(text = "%3d" % detune)
            else:
                self.var_octave.set(-100)
                self.var_transpose.set(-1)
                self.var_detune.set(-1)
                self.var_zero.set(1)
                self.widget("label-value").config(text = "Off")
                self.widget("label-transpose").config(text = "--")
                self.widget("label-detune").config(text = "---")
        except TypeError:
            pass
    
    def layout(self, offset=(0, 0),
               octave_offset = (0, 0, 20), 
               transpose_offset = (70, 0, 14, 150), 
               detune_offset = (120, 0, 14, 150),
               off_offset = (0, 135),
               label_offsets = (0, 60, 120, 155)):
        """
        Arrange widgets on Tk master.
        ARGS:
          offset           - Tuple (x,y), sets upper left reference point 
                             for component layout, all other coordinates are 
                             relative to this point.  Default (0, 0)
          octave_offset    - Tuple (xoct, yoct, rh),   sets position of octave
                             radio buttons relative to offset point. 
                             xoct - Common x position (default 0).
                             yoct - Y position of top most button (default 0).
                             rh - Vertical button spacing (defdault 20).
                             If octave_offset is None, do not include octave
                             buttons.
          transpose_offset - Tuple (xt, yt, w, h), sets position of transpose
                             slider relative to reference point.
                             xt - slider x position, default 60
                             yt - slider y position, default 0
                             w  - slider width, default 14
                             h  - slider height, default 150
                             If transpose_offset is None, do not include
                             transpose slider. 
          detune_offset    - Tuple (xd, yd, w, h), sets position of detune 
                             slider relative to reference point.
                             xd - slider x position, default 60
                             yd - slider y position, default 0
                             w  - slider width, default 14
                             h  - slider height, default 150
                             If detune_offset is None, do not include
                             detune slider.
          off_offset       - Tuple (xz, yz),  relative position of 
                             'off' checkbutton, default (55, 130).
                             If off_offset is None, do not include off button.
          label_offset     - Tuple (xv, xt, xd, y),  sets position of 
                             value labels relative to reference point.
                             xv - x location of 'value' label, default 0.
                             xt - x location of 'transpose' label, default 60
                             xd - x location of 'detune' label, default 120
                             y - common y location, default 150
                             If label_offset id None, do not include any 
                             labels.  Individual labels may be omitted by 
                             setting xv, xt or xd to None.
        """
        x0, y0 = offset
        if octave_offset != None:
            xrb = x0 + octave_offset[0]
            yrb = y0 + octave_offset[1]
            row_height = octave_offset[2]
            rows = 7
            for row in range(rows):
                y = yrb + row * row_height
                rb = self._radio_buttons[row]
                rb.place(x=xrb, y=y)
        if transpose_offset:
            xt = x0 + transpose_offset[0]
            yt = y0 + transpose_offset[1]
            w,h = transpose_offset[2], transpose_offset[3]
            self.widget("scale-transpose").place(x=xt, y=yt, width=w, height=h)
        if detune_offset:
            xt = x0 + detune_offset[0]
            yt = y0 + detune_offset[1]
            w,h = detune_offset[2], detune_offset[3]
            self.widget("scale-detune").place(x=xt, y=yt, width=w, height=h)
        if off_offset:
            xz, yz = off_offset
            xz, yz = x0+xz, y0+yz
            self.widget("checkbutton-zero").place(x=xz, y=yz)
        if label_offsets:
            xv, xt, xd, y = label_offsets
            y = y0 + y
            if xv != None:
                xv = x0 + xv
                self.widget("label-value").place(x=xv, y=y)
            if xt != None:
                xt = x0 + xt
                self.widget("label-transpose").place(x=xt, y=y)
            if xd != None:
                xd = x0 + xd
                self.widget("label-detune").place(x=xd, y=y)
        
