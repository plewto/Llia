# llia.synths.saw3.tk.s3filter
#

from __future__ import print_function
from Tkinter import Frame

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cfactory
from llia.gui.tk.oscfreq_control import OscFrequencyControl
from llia.gui.tk.decade_control import DecadeControl
from llia.gui.tk.expslider import ExpSlider


class TkSaw3FilterPanel(TkSubEditor):

    NAME = "Filter"
    IMAGE_FILE = "resources/Saw3/editor_filter.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        lab_panel = factory.image_label(frame, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)
        # Filter Freq
        s_freq = cfactory.third_octave_slider(frame, "filterFreq", editor, "Filter frequency")
        s_keytrack = cfactory.linear_slider(frame, "filterKeytrack", editor,
                                            range_ = (0.0, 4.0),
                                            ttip="Filter keytrack")
        s_freq_env1 = ExpSlider(frame, "filterFreq_env1", editor, 
                                range_=12000, degree=4,
                                ttip="ENV1 -> Filter frequency")
        s_freq_lfo =  ExpSlider(frame, "filterFreq_lfo", editor, 
                                range_=12000, degree=4,
                                ttip="ENV1 -> Filter frequency")
        s_bandpass_offset = cfactory.linear_slider(frame, "bandpassOffset", editor,
                                                   range_ = (1, 16),
                                                   ttip="Bandpass Filter Frequency Offset")
        s_bandpass_lag = cfactory.normalized_slider(frame, "bandpassLag", editor,
                                                    ttip="Bandpass filter lag time")
        y0, y1 = 50, 300
        x0 = 60
        x1 = x0 + 60
        x2 = x1 + 60
        x3 = x2 + 40
        s_freq.widget().place(x=x0, y=y0)
        s_keytrack.widget().place(x=x1, y=y0)
        s_freq_env1.layout((x0,y1))
        s_freq_lfo.layout((x1,y1))
        s_bandpass_offset.widget().place(x=x2, y=y0)
        s_bandpass_lag.widget().place(x=x3, y=y0, width=10, height=75)
        # Filter Resonace
        s_res = cfactory.normalized_slider(frame, "filterRes", editor,
                                           ttip="Filter Resonace")
        s_res_env1 = cfactory.bipolar_slider(frame, "filterRes_env1", editor,
                                             ttip="ENV1 -> Filter Resonace")
        s_res_lfo = cfactory.bipolar_slider(frame, "filterRes_lfo", editor,
                                            ttip="LFO -> Filter Resonace")
        x4 = x3 + 40
        s_res.widget().place(x=x4, y=y0)
        s_res_env1.widget().place(x=x4-60, y=y1)
        s_res_lfo.widget().place(x=x4, y=y1)
        
        # Filter Mix
        s_filter_mix = cfactory.bipolar_slider(frame, "filterMix", editor,
                                               ttip="Mix between low and band pass filters")
        s_filter_mix_env1 = cfactory.bipolar_slider(frame, "filterMix_env1", editor,
                                                    ttip="ENV1 -> Filter mix")
        s_filter_mix_lfo = cfactory.bipolar_slider(frame, "filterMix_lfo", editor,
                                                   ttip="LFO -> Filter mix")
        x5 = x4 + 60
        x6 = x5 + 60
        s_filter_mix.widget().place(x=x5, y=y0)
        s_filter_mix_env1.widget().place(x=x5, y=y1)
        s_filter_mix_lfo.widget().place(x=x6, y=y1)
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
