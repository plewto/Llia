# llia.synths.dirtyburger.tk.dirty_ed
# 2016.06.25

from __future__ import print_function
from Tkinter import Frame

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cfactory

def create_editor(parent):
    panel1 = TkDirtyPanel(parent)

class TkDirtyPanel(TkSubEditor):

    def __init__(self, editor):
        frame = editor.create_tab("Dirty")
        TkSubEditor.__init__(self, frame, editor, "Dirty")
        editor.add_child_editor("Dirty", self)
        self.pack(expand=True, fill="both")
        lab_panel = factory.image_label(self, "resources/DirtyBurger/editor.png")
        lab_panel.pack(anchor="nw", expand=False)
        # Delay Frame
        s_delay = cfactory.linear_slider(self, "delayTime", editor, range_=(0.0, 1.5))
        s_flutter = cfactory.normalized_slider(self, "flutter", editor)
        s_wow = cfactory.normalized_slider(self, "wow", editor)
        s_wow_freq = cfactory.simple_lfo_freq_slider(self, "wowFreq", editor)
        # Feedback Frame
        s_gain = cfactory.linear_slider(self, "gain", editor, range_=(0.5, 2))
        s_threshold = cfactory.normalized_slider(self, "threshold", editor)
        s_lowcut = cfactory.third_octave_slider(self, "lowcut", editor)
        s_highcut = cfactory.third_octave_slider(self, "highcut", editor)
        s_feedback = cfactory.normalized_slider(self, "feedback", editor)
        # Mixer Frame
        s_wet_mix = cfactory.mix_slider(self, "wetAmp", editor)
        s_wet_pan = cfactory.bipolar_slider(self, "wetPan", editor)
        s_dry_mix = cfactory.mix_slider(self, "dryAmp", editor)
        s_dry_pan = cfactory.bipolar_slider(self, "dryPan", editor)
        s_vol = cfactory.volume_slider(self, "volume", editor)
        y0 = 55
        dx = 58
        x_delay = 41
        x_flutter = x_delay + dx
        x_wow = x_flutter + dx
        x_wow_freq = x_wow + dx-1
        dx = 57
        x_gain = 264
        x_threshold = x_gain + dx
        x_lowcut = x_threshold + dx
        x_highcut = x_lowcut + dx
        x_feedback = x_highcut + dx
        dx = 56
        x_wet_mix = 544
        x_wet_pan = x_wet_mix + dx
        x_dry_mix = x_wet_pan + dx +1
        x_dry_pan = x_dry_mix + dx
        x_vol = x_dry_pan + dx + 1
        s_delay.widget().place(y=y0, x=x_delay)
        s_flutter.widget().place(y=y0, x=x_flutter)
        s_wow.widget().place(y=y0, x=x_wow)
        s_wow_freq.widget().place(y=y0, x=x_wow_freq)
        s_gain.widget().place(y=y0, x=x_gain)
        s_threshold.widget().place(y=y0, x=x_threshold)
        s_lowcut.widget().place(y=y0, x=x_lowcut)
        s_highcut.widget().place(y=y0, x=x_highcut)
        s_feedback.widget().place(y=y0, x=x_feedback)
        s_wet_mix.widget().place(y=y0, x=x_wet_mix)
        s_wet_pan.widget().place(y=y0, x=x_wet_pan)
        s_dry_mix.widget().place(y=y0, x=x_dry_mix)
        s_dry_pan.widget().place(y=y0, x=x_dry_pan)
        s_vol.widget().place(y=y0, x=x_vol)
        self.add_control("delayTime", s_delay)
        self.add_control("flutter", s_flutter)
        self.add_control("wow", s_wow)
        self.add_control("wowFreq", s_wow_freq)
        self.add_control("gain", s_gain)
        self.add_control("threshold", s_threshold)
        self.add_control("lowcut", s_lowcut)
        self.add_control("highcut", s_highcut)
        self.add_control("feedback", s_feedback)
        self.add_control("wetAmp", s_wet_mix)
        self.add_control("wetPan", s_wet_pan)
        self.add_control("dryAmp", s_dry_mix)
        self.add_control("dryPan", s_dry_pan)
        self.add_control("volume", s_vol)

   
