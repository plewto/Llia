# llia.gui.tk.control_factory
# 2016.06.22

from __future__ import print_function
import Tkinter as tk


import llia.gui.abstract_control as absctrl
import llia.gui.tk.tk_factory as factory
from llia.util.lmath import log2
        
class ControlSlider(absctrl.AbstractControl):

    DEFAULT_WIDTH = 12
    DEFAULT_LENGTH = 150

    # curves[0] -> aspect_to_value map
    # curves[1] -> value_to_aspect map
    def __init__(self, master, param, editor, curves=(None, None),
                 range_=(200,0), orientation="vertical", ttip=""):
        self._tkscale = factory.scale(master, from_=range_[0], to=range_[1],
                                      command = self.callback, ttip=ttip)
        super(ControlSlider, self).__init__(param, editor, self._tkscale)
        self._primary_widget = self._tkscale
        self.value_to_aspect_transform = curves[0] or absctrl.norm_to_aspect
        self.aspect_to_value_transform = curves[1] or absctrl.aspect_to_norm

    def update_aspect(self):
        self._tkscale.set(self._current_aspect)

    def callback(self, *_):
        aspect = int(self._tkscale.get())
        value = self.aspect_to_value_transform(aspect)
        self._current_aspect = aspect
        self._current_value = value
        self.synth.x_param_change(self.param, value)
        msg = "[%s] -> %s" % (self.param, value)
        #self.editor.status(msg)
        bnk = self.synth.bank()
        program = bnk[None]
        program[self.param] = value
        
                 
def normalized_slider(master, param, editor, ttip=""):
    s = ControlSlider(master, param, editor, ttip=ttip)
    return s

def simple_lfo_freq_slider(master, param, editor, ttip="LFO Frequency"):
    dom = list(absctrl.SIMPLE_LFO_ASPECT_DOMAIN)
    dom.reverse()
    s = ControlSlider(master, param, editor,
                      (absctrl.simple_lfo_to_aspect,
                       absctrl.aspect_to_simple_lfo),
                      dom,ttip=ttip)
    return s
    
def volume_slider(master, param, editor, ttip=""):
    s = ControlSlider(master, param, editor,
                      (absctrl.amp_to_volume_aspect,
                       absctrl.volume_aspect_to_amp),
                      ttip=ttip)
    return s


#  ---------------------------------------------------------------------- 
#                         Oscillator Frequency Control
#
# Coarse Radio buttons: (0) 1/8 1/4 1/2 1 2 4 8
# Fine slider domain 0...199  codomain 1.0...2.00 (resolution 0.005)
#

ZERO_FREQ = -1000

class OscFrequencyControl(absctrl.AbstractControl):

    
    
    def __init__(self, master, param, editor, include_off=False, ttip=""):
        octaves =  [(3, "+3"),
                    (2, "+2"),
                    (1, "+1"),
                    (0, " 0"),
                    (-1, "-1"),
                    (-2, "-2"),
                    (-3, "-3")]
        if include_off:
            octaves.append((ZERO_FREQ, "Off"))
        frame = factory.frame(master)
        super(OscFrequencyControl, self).__init__(param, editor, frame)
        self.var_octave = tk.StringVar()
        self.var_octave.set(0)
        row = 1
        for value, text in octaves:
            rb = factory.radio(frame, text, self.var_octave, value, ttip,
                               command=self.callback)
            widget_key = "radio_coarse_%s" % value
            self._widgets[widget_key] = rb
            rb.grid(row = row, column=0, sticky="w")
            row += 1
        self.scale_fine = factory.scale(frame, command=self.callback, ttip="Fine Frequency Scale")
        self.scale_fine.grid(row=1, column=1, rowspan=row)
        self.lab_freq = factory.label(frame, "X.XXXX")
        self.lab_freq.grid(row=row+1, column=0, columnspan=2)
        
      
    def callback(self, *_):
        ov8 = float(self.var_octave.get())
        if ov8 == ZERO_FREQ:
            freq = 0
            self.scale_fine.config(state="disabled")
        else:
            self.scale_fine.config(state="normal")
            ff_aspect = self.scale_fine.get()
            ff = absctrl.aspect_to_fine_frequency(ff_aspect)
            freq = (2**ov8)*ff
        self.synth.x_param_change(self.param, freq)
        msg = "%5.4f" % freq
        self.lab_freq.config(text=msg)
        msg = "[%s] -> " % self.param + msg
        #self.editor.status(msg)
        bnk = self.synth.bank()
        program = bnk[None]
        program[self.param] = freq

            
    def update_aspect(self):
        freq = abs(self._current_value)
        if freq:
            octave = int(log2(freq))
            ff = freq/(2.0**octave)
            ff_aspect = absctrl.fine_frequency_to_aspect(ff)
            self.var_octave.set(octave)
            self.scale_fine.set(ff_aspect)
        else:
            pass
            
            
        
    
