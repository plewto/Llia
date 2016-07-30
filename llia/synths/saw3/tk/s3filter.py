# llia.synths.saw3.tk.s3filter
# Filter, envelopes, LFOs and primary volume controls


from __future__ import print_function
from Tkinter import Frame

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cfactory
from llia.gui.tk.oscfreq_control import OscFrequencyControl
from llia.gui.tk.decade_control import DecadeControl
from llia.gui.tk.expslider import ExpSlider


class TkSaw3FilterPanel(TkSubEditor):

    NAME = "Filter/Env/LFO"
    IMAGE_FILE = "resources/Saw3/editor_filter.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        lab_panel = factory.image_label(frame, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)
        # Filter Freq
        s_freq = cfactory.third_octave_slider(frame, "filterFreq", editor, "Filter frequency")
        s_keytrack = cfactory.linear_slider(frame, "filterKeytrack", editor,range_ = (0.0, 4.0))
        s_freq_env1 = ExpSlider(frame, "filterFreq_env1", editor, range_=12000, degree=4)
        s_freq_lfo =  ExpSlider(frame, "filterFreq_lfo", editor, range_=12000, degree=4)
        s_bandpass_offset = cfactory.linear_slider(frame, "bandpassOffset", editor,range_ = (1, 16))
        s_bandpass_lag = cfactory.normalized_slider(frame, "bandpassLag", editor)
        y0, y1 = 50, 300
        x0 = 60
        x1 = x0 + 60
        x2 = x1 + 60
        x3 = x2 + 40
        s_freq.widget().place(x=x0, y=y0)
        s_keytrack.widget().place(x=x1, y=y0)
        s_freq_env1.layout((x0,y1), checkbutton_offset=(-5,-28))
        s_freq_lfo.layout((x1,y1), checkbutton_offset=(-5,-28))
        s_bandpass_offset.widget().place(x=x2, y=y0)
        s_bandpass_lag.widget().place(x=x3, y=y0, width=10, height=75)
        # Filter Resonace
        s_res = cfactory.normalized_slider(frame, "filterRes", editor)
        s_res_env1 = ExpSlider(frame, "filterRes_env1", editor, range_=1.0, degree=1)
        s_res_lfo = ExpSlider(frame, "filterRes_lfo", editor, range_=1.0, degree=1)
        x4 = x3 + 40
        s_res.widget().place(x=x4, y=y0)
        s_res_env1.layout(offset=(x4-60, y1), checkbutton_offset=(-5,-28))
        s_res_lfo.layout(offset=(x4, y1), checkbutton_offset=(-5,-28))
        # Filter Mix
        s_filter_mix = cfactory.bipolar_slider(frame, "filterMix", editor)
        s_filter_mix_env1 = ExpSlider(frame, "filterMix_env1", editor, range_=1, degree=1)
        s_filter_mix_lfo = ExpSlider(frame, "filterMix_lfo", editor, range_=1, degree=1)
        x5 = x4 + 60
        x6 = x5 + 60
        s_filter_mix.widget().place(x=x5, y=y0)
        s_filter_mix_env1.layout(offset=(x5, y1), checkbutton_offset=(-5, -28))
        s_filter_mix_lfo.layout(offset=(x6, y1), checkbutton_offset=(-5, -28))
        self.add_control("filterFreq", s_freq)
        self.add_control("filterKeytrack", s_keytrack)
        self.add_control("bandpassOffset", s_bandpass_offset)
        self.add_control("bandpassLag", s_bandpass_lag)
        self.add_control("filterFreq_env1", s_freq_env1)
        self.add_control("filterFreq_lfo", s_freq_lfo)
        self.add_control("filterRes", s_res)
        self.add_control("filterRes_env1", s_res_env1)
        self.add_control("filterRes_lfo", s_res_lfo)
        self.add_control("filterMix", s_filter_mix)
        self.add_control("filterMix_env1", s_filter_mix_env1)
        self.add_control("filterMix_lfo", s_filter_mix_lfo)
        # Env1 
        s_env1_a = ExpSlider(frame, "env1Attack", editor, range_=8, degree=2)
        s_env1_d = ExpSlider(frame, "env1Decay", editor, range_=8, degree=2)
        s_env1_r = ExpSlider(frame, "env1Release", editor, range_=8, degree=2)
        s_env1_s = cfactory.normalized_slider(frame, "env1Sustain", editor)
        self.add_control("env1Attack", s_env1_a)
        self.add_control("env1Decay", s_env1_d)
        self.add_control("env1Release", s_env1_r)
        self.add_control("env1Sustain", s_env1_s)
        xenv = x6 + 90
        xa = xenv
        xd = xa + 60
        xs = xd + 60
        xr = xs + 60
        s_env1_a.layout(offset = (xa, y0), checkbutton_offset=None)
        s_env1_d.layout(offset = (xd, y0), checkbutton_offset=None)
        s_env1_r.layout(offset = (xr, y0), checkbutton_offset=None)
        s_env1_s.widget().place(x=xs, y=y0)
        # Env2 
        s_env2_a = ExpSlider(frame, "env2Attack", editor, range_=8, degree=2)
        s_env2_d = ExpSlider(frame, "env2Decay", editor, range_=8, degree=2)
        s_env2_r = ExpSlider(frame, "env2Release", editor, range_=8, degree=2)
        s_env2_s = cfactory.normalized_slider(frame, "env2Sustain", editor)
        self.add_control("env2Attack", s_env2_a)
        self.add_control("env2Decay", s_env2_d)
        self.add_control("env2Release", s_env2_r)
        self.add_control("env2Sustain", s_env2_s)
        xenv = x6 + 90
        xa = xenv
        xd = xa + 60
        xs = xd + 60
        xr = xs + 60
        s_env2_a.layout(offset = (xa, y1), checkbutton_offset=None)
        s_env2_d.layout(offset = (xd, y1), checkbutton_offset=None)
        s_env2_r.layout(offset = (xr, y1), checkbutton_offset=None)
        s_env2_s.widget().place(x=xs, y=y1)
        # LFO
        s_lfo_freq = ExpSlider(frame, "lfoFreq", editor, range_=20, degree=2, clip=(0.01,20))
        s_lfo_delay = cfactory.linear_slider(frame, "lfoDelay", editor, range_=(0,4))
        s_lfo_depth = cfactory.normalized_slider(frame, "lfoDepth", editor)
        self.add_control("lfoFreq", s_lfo_freq)
        self.add_control("lfoDelay", s_lfo_delay)
        self.add_control("lfoDepth", s_lfo_depth)
        xlfo = xr + 90
        x1 = xlfo
        x2 = x1 + 60
        x3 = x2 + 60
        s_lfo_freq.layout(offset=(x1, y0), checkbutton_offset=None)
        s_lfo_delay.widget().place(x=x2, y=y0)
        s_lfo_depth.widget().place(x=x3, y=y0)
        # Vibrato
        s_vfreq = ExpSlider(frame, "vfreq", editor, range_=20, clip=(0.01,20))
        s_vdelay = cfactory.linear_slider(frame, "vdelay", editor, range_=(0,4))
        s_vsens = ExpSlider(frame, "vsens", editor, range_=1)
        s_vdepth = cfactory.normalized_slider(frame, "vdepth", editor)
        self.add_control("vfreq", s_vfreq)
        self.add_control("vdelay", s_vdelay)
        self.add_control("vsens", s_vsens)
        self.add_control("vdepth", s_vdepth)
        x4 = x3 + 60
        s_vfreq.layout(offset=(x1, y1), checkbutton_offset=None)
        s_vdelay.widget().place(x=x2, y=y1)
        s_vsens.layout(offset=(x3, y1), checkbutton_offset=None)
        s_vdepth.widget().place(x=x4, y=y1)
        # Primary amp
        xamp = x4 + 60
        s_amp = cfactory.volume_slider(frame, "amp", editor)
        self.add_control("amp", s_amp)
        s_amp.widget().place(x=xamp, y=y0)
