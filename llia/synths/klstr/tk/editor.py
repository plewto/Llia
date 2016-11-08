# llia.synths.klstr.tk.editor

from __future__ import print_function
import Tkinter as tk
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.tk_subeditor import TkSubEditor
from llia.gui.tk.expslider import ExpSlider
from llia.synths.klstr.klstr_data import LFO_RATIOS


def create_editor(parent):
    TkKlstrTonePanel(parent)
    TkKlstrModPanel(parent)


class TkKlstrTonePanel(TkSubEditor):

    NAME = "Klstr Tone"
    IMAGE_FILE = "resources/Klstr/editor_tone_panel.png"
    TAB_FILE = "resources/Tabs/pulse.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        self.pack(expand=True, fill="both")
        lab_panel = factory.image_label(self, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)
        s_spread = cf.linear_slider(frame, "spread", editor, range_=(0,4))
        s_cluster = cf.linear_slider(frame, "cluster", editor, range_=(0,16))
        s_pw = cf.normalized_slider(frame, "pw", editor)
        s_noise = cf.normalized_slider(frame, "noiseAmp", editor)
        xs_filter = ExpSlider(frame, "filterFreq", editor, range_=16000)
        s_res = cf.normalized_slider(frame, "res", editor)
        s_filter_mix = cf.normalized_slider(frame, "filterMix", editor)
        s_amp = cf.volume_slider(frame, "amp", editor)
        s_spread_env = cf.linear_slider(frame, "spreadEnv", editor, range_ = (0,4))
        s_spread_lfo = cf.linear_slider(frame, "spreadLfo", editor, range_ = (0,4))
        s_cluster_env = cf.linear_slider(frame, "clusterEnv", editor, range_ = (-16, 16))
        s_cluster_lfo = cf.linear_slider(frame, "clusterLfo", editor, range_ = (0, 16))
        s_cluster_lag = cf.normalized_slider(frame, "clusterLag", editor)
        s_pw_lfo = cf.normalized_slider(frame, "pwLfo", editor)
        xs_filter_env = ExpSlider(frame, "filterEnv", editor, range_ = 9999)
        xs_filter_lfo = ExpSlider(frame, "filterLfo", editor, range_ = 9999)
        s_filter_lag = cf.normalized_slider(frame, "filterLag", editor)
        self.add_control("spread", s_spread)
        self.add_control("cluster", s_cluster)
        self.add_control("pw", s_pw)
        self.add_control("noiseAmp", s_noise)
        self.add_control("filterFreq", xs_filter)
        self.add_control("res", s_res)
        self.add_control("filterMix", s_filter_mix)
        self.add_control("amp", s_amp)
        self.add_control("spreadEnv", s_spread_env)
        self.add_control("spreadLfo", s_spread_lfo)
        self.add_control("clusterEnv", s_cluster_env)
        self.add_control("clusterLfo", s_cluster_lfo)
        self.add_control("clusterLag", s_cluster_lag)
        self.add_control("pwLfo", s_pw_lfo)
        self.add_control("filterEnv", xs_filter_env)
        self.add_control("filterLfo", xs_filter_lfo)
        self.add_control("filterLag", s_filter_lag)
        y0 = 90
        x0 = 90
        x1 = x0 + 60
        x2 = x1 + 60
        x3 = x2 + 60
        x4 = x3 + 60
        xnoise = x4 + 75
        xfilter = xnoise + 75
        x5 = xfilter + 60
        x6 = x5 + 60
        xamp = x6 + 75
        s_spread.widget().place(x=x0, y=y0)
        s_cluster.widget().place(x=x2, y=y0)
        s_pw.widget().place(x=x4, y=y0)
        s_noise.widget().place(x=xnoise, y=y0)
        xs_filter.layout(offset=(xfilter,y0),
                         checkbutton_offset=None)
        s_res.widget().place(x=x5, y=y0)
        s_filter_mix.widget().place(x=x6, y=y0)
        s_amp.widget().place(x=xamp, y=y0)
        y1 = 320
        s_spread_env.widget().place(x=x0, y=y1)
        s_spread_lfo.widget().place(x=x1, y=y1)
        s_cluster_env.widget().place(x=x2, y=y1)
        s_cluster_lfo.widget().place(x=x3, y=y1)
        s_cluster_lag.widget().place(x=x3+30, y=y1, width=10, height=75)
        s_pw_lfo.widget().place(x=x4+30, y=y1)
        xs_filter_env.layout(offset=(xfilter, y1),
                             checkbutton_offset = (-4, -20))
        xs_filter_lfo.layout(offset=(x5, y1),
                             checkbutton_offset = (-4, -20))
        s_filter_lag.widget().place(x=x5+30, y=y1, width=10, height=75)
        

class TkKlstrModPanel(TkSubEditor):

    NAME = "Klstr Mod"
    IMAGE_FILE = "resources/Klstr/editor_mod_panel.png"
    TAB_FILE = "resources/Tabs/adsr.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        self.pack(expand=True, fill="both")
        lab_panel = factory.image_label(self, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)

        xs_attack = ExpSlider(frame, "attack", editor, range_= 32)
        xs_decay = ExpSlider(frame, "decay", editor, range_= 32)
        s_sustain = cf.normalized_slider(frame, "sustain", editor)
        xs_release = ExpSlider(frame, "release", editor, range_= 32)
        cb_envmode = cf.ControlCheckbutton(frame, "envMode", editor, values=(0,1))


        xs_lfo_freq = ExpSlider(frame, "lfoFreq", editor, range_= 100)
        ds_lfo_ratios = cf.discrete_slider(frame,"lfo2FreqRatio", editor, values=LFO_RATIOS)
        xs_lfo_xmod = ExpSlider(frame, "lfoXMod", editor, range_= 100)
        s_lfo_delay = cf.linear_slider(frame, "lfoDelay", editor, range_=(0,8))
        s_lfo_depth = cf.normalized_slider(frame, "lfoDepth", editor)
        s_vibrato = cf.normalized_slider(frame, "vibrato", editor)
                                       
        s_xspread = cf.normalized_slider(frame, "xToSpread", editor)
        s_xnoise = cf.normalized_slider(frame, "xToNoise", editor)
        s_xfilter = cf.normalized_slider(frame, "xToFilter", editor)
        s_xscale = cf.linear_slider(frame, "xScale", editor, range_=(0,4))
        
        self.add_control("attack", xs_attack)
        self.add_control("decay", xs_decay)
        self.add_control("sustain", s_sustain)
        self.add_control("release", xs_release)
        self.add_control("envMode", cb_envmode)
        self.add_control("lfoFreq",xs_lfo_freq)
        self.add_control("lfo2FreqRatio",ds_lfo_ratios)
        self.add_control("lfoXMod",xs_lfo_xmod)
        self.add_control("lfoDelay",s_lfo_delay)
        self.add_control("lfoDepth",s_lfo_depth)
        self.add_control("vibrato",s_vibrato)
                                    
        self.add_control("xToSpread", s_xspread)
        self.add_control("xToNoise", s_xnoise)
        self.add_control("xToFilter", s_xfilter)
        self.add_control("xScale", s_xscale)

        y0 = 90
        x0 = 90
        x1 = x0 + 60
        x2 = x1 + 60
        x3 = x2 + 60
        x4 = x3 + 60
        #5 = x4 + 30

        xlfo = x4 + 75
        x6 = xlfo
        x7 = x6 + 60
        x8 = x7 + 60
        x9 = x8 + 60
        x10 = x9 + 60
        x11 = x10 + 60
        
        xs_attack.layout(offset = (x0, y0), checkbutton_offset =None, height=380)
        xs_decay.layout(offset = (x1, y0), checkbutton_offset =None, height=380)
        s_sustain.widget().place(x=x2, y=y0, height=380)
        xs_release.layout(offset = (x3, y0), checkbutton_offset =None, height=380)
        cb_envmode.widget().place(x=x4, y=y0)


        xs_lfo_freq.layout(offset=(x6, y0),checkbutton_offset = None, height=380)
        xs_lfo_xmod.layout(offset=(x7, y0),checkbutton_offset = None, height=380)
        ds_lfo_ratios.widget().place(x=x8, y=y0)
        s_lfo_delay.widget().place(x=x9, y=y0)
        
        s_lfo_depth.widget().place(x=x10, y=y0)
        s_vibrato.widget().place(x=x11, y=y0)

        y1 = 320
        s_xspread.widget().place(x=x8, y=y1)
        s_xnoise.widget().place(x=x9, y=y1)
        s_xfilter.widget().place(x=x10, y=y1)
        s_xscale.widget().place(x=x11, y=y1)
