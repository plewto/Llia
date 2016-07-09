# llia.gui.tk.control_factory
# 
# "Controls" are widgets specifically for synth editors.


from __future__ import print_function
import Tkinter as tk

import llia.constants as con
import llia.gui.abstract_control as absctrl
import llia.gui.tk.tk_factory as factory
from llia.util.lmath import log2, logn, log10, clip
from llia.curves import linear_function as linfn


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
            
#  ---------------------------------------------------------------------- 
#                      Oscillator Frequency Control (2)
#
# Compound  control:
#    octaves   -> radio buttons
#    semi-tone -> scale  0, 11
#    detune    -> scale  cents 0, 99
#

# class OscFrequencyControl2(absctrl.AbstractControl):
    
#     def __init__(self, master, param, editor, include_zero=False):
#         frame = factory.frame(master)
#         frame.config(width=187, height=201)
#         super(OscFrequencyControl2, self).__init__(param, editor, frame)
#         self.specs = self.synth.specs
#         octaves =  [(3, "+3"),
#                     (2, "+2"),
#                     (1, "+1"),
#                     (0, " 0"),
#                     (-1, "-1"),
#                     (-2, "-2"),
#                     (-3, "-3")]
#         self.var_octave = tk.StringVar()
#         self.var_transpose = tk.IntVar()
#         self.var_detune = tk.IntVar()
#         self.var_zero = tk.IntVar()
#         self.var_octave.set(0)
#         self.var_transpose.set(0)
#         self.var_detune.set(0)
#         self.var_zero.set(1)
#         self._live_widgets = []
#         row = 1
#         for value, text in octaves:
#             rb = factory.radio(frame, text, self.var_octave, value,
#                                ttip = "%s octave" % param,
#                                command = self.callback)
#             widget_key = "radio-octave-%d" % value
#             self._widgets[widget_key] = rb
#             self._live_widgets.append(rb)
#             rb.grid(row=row, column=0, sticky='w', padx=4)
#             row += 1
#         s_step = factory.scale(frame,
#                                from_=11, to=0,
#                                command=self.callback,
#                                ttip = "%s transpose (steps)" % param)
#         s_step.configure(variable = self.var_transpose)
#         s_detune = factory.scale(frame,
#                                  from_=99, to=0,
#                                  command=self.callback,
#                                  ttip = "%s detune (cents)" % param)
#         s_detune.configure(variable = self.var_detune)
#         b_reset = factory.clear_button(frame, command=self.reset_values,
#                                        ttip = "Reset %s to 1.0" % param)
#         cb_zero = factory.checkbutton(frame, "Off")
#         cb_zero.config(command=self.zero_callback, var = self.var_zero)
#         self.lab_value = factory.label(frame, "1.0000")
#         self.lab_transpose = factory.label(frame, " 0")
#         self.lab_detune = factory.label(frame, "  0")
#         s_step.grid(row=1, column=1, rowspan=7)
#         s_detune.grid(row=1, column=2, rowspan=7)
#         factory.label(frame, "Octave").grid(row=8, column=0)
#         factory.label(frame, "Step").grid(row=8, column=1)
#         factory.label(frame, "Detune").grid(row=8, column=2)
#         self.lab_value.grid(row=9, column=0)
#         self.lab_transpose.grid(row=9, column=1)
#         self.lab_detune.grid(row=9, column=2)
#         b_reset.grid(row=1, column=3, rowspan=2, padx=4, pady=4)
#         if include_zero:
#             cb_zero.grid(row=3, column=3)
#         self._widgets["scale-step"] = s_step
#         self._widgets["scale-detune"] = s_detune
#         self._widgets["button-reset"] = b_reset
#         self._widgets["checkbutton-zero"] = cb_zero
#         self._widgets["label-value"] = self.lab_value
#         self._widgets["label-transpose"] = self.lab_transpose
#         self._widgets["label-detune"] = self.lab_detune
#         self._live_widgets.append(s_step)
#         self._live_widgets.append(s_detune)
        
#     def zero_callback(self):
#         self.callback()
#         zero = self.var_zero.get()
#         self._enable_widgets(not zero)
        
#     def callback(self, *_):
#         octave = int(self.var_octave.get())
#         step = self.var_transpose.get()
#         detune = self.var_detune.get()
#         cxpose = 1200*octave + 100*step + detune
#         ratio = con.RCENT**cxpose
#         zero = not self.var_zero.get()
#         ratio *= zero
#         self.lab_transpose.config(text = "%2d" % step)
#         self.lab_detune.config(text = "%3d" % detune)
#         self.lab_value.config(text = "%7.4f" % ratio)
#         bnk = self.synth.bank()
#         program = bnk[None]
#         program[self.param] = ratio
#         self.synth.x_param_change(self.param, ratio)
#         msg = "[%s] -> %6.4f" % (self.param, ratio)
#         self.editor.status(msg)
        
#     def reset_values(self, *_):
#         self.var_octave.set(0)
#         self.var_transpose.set(0)
#         self.var_detune.set(0)
#         self.var_zero.set(0)
#         bnk = self.synth.bank()
#         program = bnk[None]
#         program[self.param] = 1.0
#         self.synth.x_param_change(self.param, 1.0)
#         msg = "[%s] -> 1.0" % self.param
#         self.editor.status(msg)
#         self._enable_widgets(True)
#         self.lab_transpose.config(text = " 0")
#         self.lab_detune.config(text = "  0")
#         self.lab_value.configure(text = "1.0000")

#     def _enable_widgets(self, flag):
#         if flag:
#             for w in self._live_widgets:
#                 w.config(state="normal")
#         else:
#             for w in self._live_widgets:
#                 w.config(state="disabled")
#             self.lab_transpose.config(text = "XX")
#             self.lab_detune.config(text = "XXX")
        
#     def update_aspect(self):
#         try:
#             ratio = abs(self._current_value)
#         except TypeError:
#             ratio = 1
#         if ratio:
#             cents = int(logn(ratio, con.RCENT))
#             octave = cents/1200
#             step = (cents-1200*octave)/100
#             detune = cents - 1200*octave - 100*step
#             self._enable_widgets(True)
#             self.var_octave.set(octave)
#             self.var_transpose.set(step)
#             self.var_detune.set(detune)
#             self.lab_value.config(text = "%6.4f" % ratio)
#             self.var_zero.set(False)
#         else:
#             self.var_zero.set(True)
#             self._enable_widgets(False)

            
    
