# llia.gui.tk.control_factory
# 
# "Controls" are widgets specifically for synth editors.


from __future__ import print_function
import Tkinter as tk

import llia.constants as con
import llia.gui.abstract_control as absctrl
import llia.gui.tk.tk_factory as factory
from llia.util.lmath import log2, logn, log10, clip
from llia.curves import linear_function as linfn, normal_exp_curve


class ControlSlider(absctrl.AbstractControl):

    DEFAULT_WIDTH = 12
    DEFAULT_LENGTH = 150

    @staticmethod
    def default_client_callback(*args):
        # args --> [self, aspect, value]
        pass
    
    # curves[0] -> value_to_aspect map
    # curves[1] -> aspect_to_value map
    def __init__(self, master, param, editor, curves=(None, None),
                 domain=(200,0), orientation="vertical", ttip=""):
        self._tkscale = factory.scale(master, from_=domain[0], to=domain[1],
                                      command = self.callback, ttip=ttip)
        super(ControlSlider, self).__init__(param, editor, self._tkscale)
        self._primary_widget = self._tkscale
        self.value_to_aspect_transform = curves[0] or absctrl.norm_to_aspect
        self.aspect_to_value_transform = curves[1] or absctrl.aspect_to_norm
        self.client_callback = ControlSlider.default_client_callback

    def update_aspect(self):
        self._tkscale.set(self._current_aspect)

    def callback(self, *_):
        aspect = int(self._tkscale.get())
        value = self.aspect_to_value_transform(aspect)
        self._current_aspect = aspect
        self._current_value = value
        self.synth.x_param_change(self.param, value)
        msg = "[%s] -> %s" % (self.param, value)
        self.editor.status(msg)
        bnk = self.synth.bank()
        program = bnk[None]
        program[self.param] = value
        self.client_callback(self, aspect, value)
                 
def normalized_slider(master, param, editor, ttip=""):
    s = ControlSlider(master, param, editor, ttip=ttip)
    return s

def bipolar_slider(master, param, editor, ttip=""):
    a_to_v = absctrl.aspect_to_polar
    v_to_a = absctrl.polar_to_aspect
    s = ControlSlider(master, param, editor,
                      (v_to_a, a_to_v),
                      ttip =ttip)
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

def linear_slider(master, param, editor, domain=(0, 200), range_=(0.0, 1.0), ttip=""):
    a_to_v = linfn(domain, range_)
    v_to_a = linfn(range_, domain)
    s = ControlSlider(master, param, editor,
                      curves=(v_to_a, a_to_v),
                      ttip=ttip)
    return s


def third_octave_slider(master, param, editor, ttip=""):
    a_to_v = absctrl.aspect_to_third_octave
    v_to_a = absctrl.third_octave_to_aspect
    domain = (0, 32)
    s = ControlSlider(master, param, editor,
                      domain=(31, 0),
                      curves = (v_to_a, a_to_v),
                      ttip=ttip)
    return s
                      
def discrete_slider(master, param, editor, values=range(8), ttip=""):
    count = len(values)
    rvs_tab = {}
    for i,v in enumerate(values):
        rvs_tab[float(v)] = i

    def a_to_v(a):
        try:
            return values[a]
        except IndexError:
            if a < 0:
                return values[0]
            else:
                return values[-1]

    def v_to_a(v):
        try:
            return rvs_tab[float(v)]
        except KeyError:
            if v <= values[0]:
                return 0
            else:
                return count
                
    
    s = ControlSlider(master, param, editor,
                      domain=(count+1, 0),
                      curves=(v_to_a, a_to_v),
                      ttip = ttip)
    return s

    
#  ---------------------------------------------------------------------- 
#                         Oscillator Frequency Control (1)
#
# Coarse Radio buttons: (0) 1/8 1/4 1/2 1 2 4 8
# Fine slider domain 0...199  codomain 1.0...2.00 (resolution 0.005)
# As a finer resolution alternative, consider using gui/tk/oscfreq_control
 
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
        self.editor.status(msg)
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

class ControlCheckbutton(absctrl.AbstractControl):

    def __init__(self, master, param, editor,
                 text="", values=(0,1), ttip=""):
        self._var = tk.BooleanVar()
        self._cb = factory.checkbutton(master, text, self._var,
                                       command=self.callback, ttip=ttip)
        self._values = values
        super(ControlCheckbutton, self).__init__(param, editor, self._cb)

    def callback(self, *_):
        flg = float(self._var.get())
        if flg:
            v = self._values[1]
        else:
            v = self._values[0]
        self.synth.x_param_change(self.param, v)
        program = self.synth.bank()[None]
        program[self.param] = v
        msg = "[%s] -> %s" % (self.param, v)
        self.editor.status(msg)
        

    def update_aspect(self):
        program = self.synth.bank()[None]
        v = program[self.param]
        self._var.set(v==self._values[1])
