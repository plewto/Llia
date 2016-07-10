# llia.synths.xover.tk.xover_ed
#

from __future__ import print_function
#from Tkinter import Frame
from llia.synths.xover.xover_constants import *
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cfactory
from llia.gui.tk.tk_subeditor import TkSubEditor
from llia.gui.tk.decade_control import DecadeControl
from llia.gui.tk.discreate_control import DiscreateControl

def create_editor(parent):
    tone_panel = TkXOverPanel(parent)

class TkXOverPanel(TkSubEditor):

    NAME = "XOver"
    IMAGE_FILE = "resources/XOver/editor.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        self.pack(expand=True, fill="both")
        lab_panel = factory.image_label(self, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)
        dc_lfo = DecadeControl(frame, "lfoFreq", self, (0.01, 10))
        dc_crossover_ratio = DiscreateControl(frame, "lfoCrossoverRatio",
                                              self, LFO_RATIOS)
        dc_pan_ratio = DiscreateControl(frame, "lfoPanRatio",
                                        self, LFO_RATIOS)
        s_res = cfactory.normalized_slider(frame, "res", self, "Resonace")
        s_crossover = cfactory.discrete_slider(frame, "crossover", self,
                                               CROSSOVER_FREQUENCIES,
                                               "Filter crossover frequency")
        s_crossover_lfo = cfactory.normalized_slider(frame, "lfoCrossover", self,
                                                     "LFO -> crossover modulation depth")
        s_filter1_mode = cfactory.normalized_slider(frame, "lpMode", self,
                                                    "Filter 1 mode")
        s_filter1_mod = cfactory.normalized_slider(frame, "lpMod", self,
                                                   "Filter 1 LFO modulation")
        s_filter2_mode = cfactory.normalized_slider(frame, "hpMode", self,
                                                    "Filter 2 mode")
        s_filter2_mod = cfactory.normalized_slider(frame, "hpMod", self,
                                                   "Filter 2 LFO modulation")
        s_spread = cfactory.bipolar_slider(frame, "spread", self,
                                           "Pan spread")
        s_spread_lfo = cfactory.normalized_slider(frame, "lfoPanMod", self,
                                                  "LFO -> spread")
        s_dry_pan = cfactory.bipolar_slider(frame, "dryPan", self,
                                             "Dry signal pan")
        s_dry_amp = cfactory.volume_slider(frame, "dryAmp", self,
                                           "Dry signal amplitude")
        s_filter1_amp = cfactory.volume_slider(frame, "lpAmp", self,
                                               "Filter 1 amplitude")
        s_filter2_amp = cfactory.volume_slider(frame, "hpAmp", self,
                                               "Filter 2 amplitude")
        s_amp = cfactory.volume_slider(frame, "amp", self,
                                       "Main amplitude")
        self.add_control("lfoFreq", dc_lfo)
        self.add_control("lfoCrossoverRatio", dc_crossover_ratio)
        self.add_control("lfoPanRatio", dc_pan_ratio)
        self.add_control("res", s_res)
        self.add_control("crossover", s_crossover)
        self.add_control("lfoCrossover", s_crossover_lfo)
        self.add_control("lpMode", s_filter1_mode)
        self.add_control("lpMod", s_filter1_mod)
        self.add_control("hpMode", s_filter2_mode)
        self.add_control("hpMod", s_filter2_mod)
        self.add_control("spread", s_spread)
        self.add_control("lfoPanMod", s_spread_lfo)
        self.add_control("dryPan", s_dry_pan)
        self.add_control("dryAmp", s_dry_amp)
        self.add_control("lpAmp", s_filter1_amp)
        self.add_control("hpAmp", s_filter2_amp)
        self.add_control("amp", s_amp)
        dc_lfo.layout(offset=(50, 50), label_offset=(20, 100))
        dc_pan_ratio.layout(170, 50, rows=6, xdelta=65)
        dc_crossover_ratio.layout(300, 50, rows=6, xdelta=65)
        y = 50
        xres, xcrossover, xlfo = 500, 560, 620
        xf1, xf2 = 700, 760
        s_res.widget().place(x=xres, y=y)
        s_crossover.widget().place(x=xcrossover, y=y)
        s_crossover_lfo.widget().place(x=xlfo, y=y)
        s_filter1_mode.widget().place(x=xf1, y=y, width=10, height=60)
        s_filter1_mod.widget().place(x=xf1, y=y+90, width=10, height=60)
        s_filter2_mode.widget().place(x=xf2, y=y, width=10, height=60)
        s_filter2_mod.widget().place(x=xf2, y=y+90, width=10, height=60)
        y = 300
        xspread, xlfo, xdry = 50, 110, 170
        s_spread.widget().place(x=xspread, y=y)
        s_spread_lfo.widget().place(x=xlfo, y=y)
        s_dry_pan.widget().place(x=xdry, y=y)
        xdry, xf1, xf2, xamp = 260, 320, 380, 460
        s_dry_amp.widget().place(x=xdry, y=y)
        s_filter1_amp.widget().place(x=xf1, y=y)
        s_filter2_amp.widget().place(x=xf2, y=y)
        s_amp.widget().place(x=xamp, y=y)
        
