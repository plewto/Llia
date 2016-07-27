# llia.synths.klstr.tk.klster_ed

from __future__ import print_function
import Tkinter as tk
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cfactory
from llia.gui.tk.tk_subeditor import TkSubEditor
from llia.gui.tk.decade_control import DecadeControl
from llia.gui.tk.discreate_control import DiscreateControl
from llia.gui.tk.expslider import ExpSlider


def create_editor(parent):
    tone_panel = TkKlsterPanel(parent)

class TkKlsterPanel(TkSubEditor):

    NAME = "KLSTR"
    IMAGE_FILE = "resources/Klstr/editor.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        self.pack(expand=True, fill="both")
        lab_panel = factory.image_label(self, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)

        # Tone Spread
        s_spread = cfactory.linear_slider(frame, "spread", self, range_=(0, 4))
        s_spread_lfo = cfactory.linear_slider(frame, "spreadLfo", self, range_=(0,4))
        s_spread_env = cfactory.linear_slider(frame, "spreadEnv", self, range_=(0,4))
        self.add_control("spread", s_spread)
        self.add_control("spreadLfo", s_spread_lfo)
        self.add_control("spreadEnv", s_spread_env)


        # Tone Cluster
        s_cluster = cfactory.linear_slider(frame, "cluster", self, range_=(0,16))
        s_cluster_lfo = cfactory.linear_slider(frame, "clusterLfo", self, range_=(0,16))
        s_cluster_env = cfactory.linear_slider(frame, "clusterEnv", self, range_=(-16,16))
        s_cluster_lag = cfactory.normalized_slider(frame, "clusterLag", self)
        self.add_control("cluster", s_cluster)
        self.add_control("clusterLfo", s_cluster_lfo)
        self.add_control("clusterEnv", s_cluster_env)
        self.add_control("clusterLag", s_cluster_lag)

        # Tone PW
        s_pw = cfactory.normalized_slider(frame, "pw", self)
        s_pwm = cfactory.normalized_slider(frame, "pwLfo", self)
        self.add_control("pw", s_pw)
        self.add_control("pwLfo", s_pwm)

        # Noise
        s_noise = cfactory.mix_slider(frame, "noiseAmp", self)
        self.add_control("noiseAmp", s_noise)

        # LFO
        s_lfo_freq = ExpSlider(frame, "lfoFreq", self, range_=100, degree=3, clip=(0.001, 100))
        s_lfo_ratio = cfactory.discrete_slider(frame, "lfo2FreqRatio", self,
                                              values = [0.01, 0.1, 0.25, 0.333, 0.5, 0.667,
                                                        0.75, 1.0, 1.125, 1.25, 1.5, 1.175,
                                                        2, 3, 4, 5, 8])
        s_lfo_xmod = ExpSlider(frame, "lfoXMod", self, range_=100, degree=3)
        s_lfo_delay = cfactory.linear_slider(frame, "lfoDelay", self, range_=(0, 8))
        s_lfo_depth = cfactory.normalized_slider(frame, "lfoDepth", self)
        s_vibrato = cfactory.normalized_slider(frame, "vibrato", self)
        self.add_control("lfoFreq", s_lfo_freq)
        self.add_control("lfo2FreqRatio", s_lfo_ratio)
        self.add_control("lfoXMod", s_lfo_xmod)
        self.add_control("lfoDelay", s_lfo_delay)
        self.add_control("lfoDepth", s_lfo_depth)
        self.add_control("vibrato", s_vibrato)
        
        # Filter
        s_filter = ExpSlider(frame, "filterFreq", self, range_= 16000)
        s_filter_lfo = ExpSlider(frame, "filterLfo", self, range_ = 9999)
        s_filter_env = ExpSlider(frame, "filterEnv", self, range_ = 9999)
        s_filter_lag = cfactory.normalized_slider(frame, "filterLag", self)
        s_filter_res = cfactory.normalized_slider(frame, "res", self)
        s_filter_mix = cfactory.normalized_slider(frame, "filterMix", self)
        s_filter_env.widget("checkbutton-sign").config(background="#2c272e")
        s_filter_lfo.widget("checkbutton-sign").config(background="#2c272e")
        
        self.add_control("filterFreq", s_filter)  
        self.add_control("filterLfo", s_filter_lfo)  
        self.add_control("filterEnv", s_filter_env)  
        self.add_control("filterLag", s_filter_lag)  
        self.add_control("res", s_filter_res)  
        self.add_control("filterMix", s_filter_mix)  

        # Env
        self.var_env_mode = tk.BooleanVar()
        s_attack = ExpSlider(frame, "attack", self, range_=60, degree=3)
        s_decay = ExpSlider(frame, "decay", self, range_=60, degree=3)
        s_release = ExpSlider(frame, "release", self, range_=60, degree=3)
        s_sustain = cfactory.normalized_slider(frame, "sustain", self)
        cb_trigmode = cfactory.ControlCheckbutton(frame, "envMode", self, "Trig")
        cb_trigmode.widget().config(background="#3D3937")
        self.add_control("attack", s_attack)
        self.add_control("decay", s_decay)
        self.add_control("release", s_release)
        self.add_control("sustain", s_sustain)
        self.add_control("envMode", cb_trigmode)

        # Amp
        s_amp = cfactory.volume_slider(frame, "amp", self)
        self.add_control("amp", s_amp)
        
        y0, y1 = 50, 300
        x0 = 50
        x1 = x0 + 60
        x2 = x1 + 60
        s_spread.widget().place(x=x0, y=y0)
        s_spread_lfo.widget().place(x=x1, y=y0)
        s_spread_env.widget().place(x=x2, y=y0)

        x3 = x2 + 90
        x4 = x3 + 60
        x5 = x4 + 60
        x5b = x5 + 30
        s_cluster.widget().place(x=x3, y=y0)
        s_cluster_lfo.widget().place(x=x4, y=y0)
        s_cluster_env.widget().place(x=x5, y=y0)
        s_cluster_lag.widget().place(x=x5b, y=y0, width=14, height=75)

        x6 = x5+90
        x7 = x6+60
        s_pw.widget().place(x=x6, y=y0)
        s_pwm.widget().place(x=x7, y=y0)

        x8 = x7 + 90
        s_noise.widget().place(x=x8, y=y0)

        x9 = x8 + 90
        x10 = x9 + 60
        x11 = x10 + 60
        x12 = x11 + 60
        x13 = x12 + 60
        x14 = x13 + 60
        s_lfo_freq.layout(offset=(x9, y0), checkbutton_offset=None)
        s_lfo_ratio.widget().place(x=x10, y=y0)
        s_lfo_xmod.layout(offset=(x11, y0), checkbutton_offset=None)
        s_lfo_delay.widget().place(x=x12, y=y0)
        s_lfo_depth.widget().place(x=x13, y=y0)
        s_vibrato.widget().place(x=x14, y=y0)
        
        # ROW 2
        s_filter.layout(offset=(x0, y1), checkbutton_offset = None)
        s_filter_lfo.layout(offset=(x1, y1), checkbutton_offset = (-6, -24))
        s_filter_env.layout(offset=(x2, y1), checkbutton_offset = (-6, -24))
        s_filter_lag.widget().place(x=x2+30, y=y1, width=14, height=75)
        s_filter_res.widget().place(x=x3, y=y1)
        s_filter_mix.widget().place(x=x4, y=y1)
        


        
        x5 = x4 + 90
        x6 = x5+60
        x7 = x6+60
        x8 = x7+60
        x9 = x8+30
        s_attack.layout(offset=(x5, y1), checkbutton_offset = None)
        s_decay.layout(offset=(x6, y1), checkbutton_offset = None)
        s_sustain.widget().place(x=x7, y=y1)
        s_release.layout(offset=(x8, y1), checkbutton_offset = None)
        cb_trigmode.widget().place(x=x9, y=y1)
        
        x10 = x8+120
        s_amp.widget().place(x=x10, y=y1)
