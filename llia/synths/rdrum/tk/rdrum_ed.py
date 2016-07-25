# llia.synths.rdrum.tk.rdrum_ed

from __future__ import print_function
from Tkinter import Frame

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cfactory
from llia.gui.tk.tk_subeditor import TkSubEditor
from llia.gui.tk.decade_control import DecadeControl
from llia.gui.tk.discreate_control import DiscreateControl




def create_tk_rdrum_editor(parent):
    tone_panel = TkRdrumPanel1(parent)
    #info_panel = TkRdrumInfoPanel(parent


class TkRdrumPanel1(TkSubEditor):

    NAME = "Risset Drum"
    IMAGE_FILE = "resources/RDrum/editor.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        self.pack(expand=True, fill="both")
        lab_panel = factory.image_label(self, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)
        
        # Tone A
        dc_a_ratio = cfactory.OscFrequencyControl(frame, "aRatio", self);
        s_a_clip = cfactory.normalized_slider(frame, "aTone", self, "Tone A waveform")
        s_a_attack = cfactory.linear_slider(frame, "aAttack", self, range_=(0.0, 6.0))
        s_a_decay = cfactory.linear_slider(frame, "aDecay", self, range_=(0.0, 6.0))
        s_a_bend = cfactory.bipolar_slider(frame, "aBend", self, "Tone A Pitch Bend")
        s_a_amp = cfactory.volume_slider(frame, "aAmp", self, "Tone A Amp")
        self.add_control("aRatio", dc_a_ratio)
        self.add_control("aTone", s_a_clip)
        self.add_control("aAttack", s_a_attack)
        self.add_control("aDecay", s_a_decay)
        self.add_control("aBend", s_a_bend)
        self.add_control("aAmp", s_a_amp)

        # Tone B
        dc_b_ratio = cfactory.OscFrequencyControl(frame, "bRatio", self)
        s_b_tune = cfactory.linear_slider(frame, "bTune", self, range_=(0.0, 4))
        s_b_attack = cfactory.linear_slider(frame, "bAttack", self, range_=(0.0, 6.0))
        s_b_decay = cfactory.linear_slider(frame, "bDecay", self, range_=(0.0, 6.0))
        s_b_bend = cfactory.bipolar_slider(frame, "bBend", self, "Tone B Pitch Bend")
        s_b_amp = cfactory.volume_slider(frame, "bAmp", self, "Tone B Amp")
        self.add_control("bRatio", dc_b_ratio)
        self.add_control("bTune", s_b_tune)
        self.add_control("bAttack", s_b_attack)
        self.add_control("bDecay", s_b_decay)
        self.add_control("bBend", s_b_bend)
        self.add_control("bAmp", s_b_amp)

        # Noise
        s_noise_ratio = cfactory.linear_slider(frame, "noiseRatio", self, range_=(0.0, 16))
        s_noise_bias = cfactory.third_octave_slider(frame, "noiseBias", self)
        s_noise_res = cfactory.normalized_slider(frame, "noiseRes", self)
        s_noise_attack = cfactory.linear_slider(frame, "noiseAttack", self, range_=(0.0, 6.0))
        s_noise_decay = cfactory.linear_slider(frame, "noiseDecay", self, range_=(0.0, 6.0))
        s_noise_bend = cfactory.bipolar_slider(frame, "noiseBend", self)
        s_noise_amp = cfactory.volume_slider(frame, "noiseAmp", self)
        self.add_control("noiseRatio", s_noise_ratio)
        self.add_control("noiseBias", s_noise_bias)
        self.add_control("noiseRes", s_noise_res)
        self.add_control("noiseAttack", s_noise_attack)
        self.add_control("noiseDecay", s_noise_decay)
        self.add_control("noiseBend", s_noise_bend)
        self.add_control("noiseAmp", s_noise_amp)

        # Amp
        s_amp = cfactory.volume_slider(frame, "amp", self)
        self.add_control("amp", s_amp)
        
        y0 = 50
        x0 = 50
        x1 = x0 + 120
        x2 = x1 + 60
        x3 = x2 + 60
        x4 = x3 + 60
        x5 = x4 + 60

        x6 = x5 + 120
        x7 = x6 + 120
        x8 = x7 + 60
        x9 = x8 + 60
        x10 = x9 + 60
        x11 = x10 + 60
        
        #dc_a_ratio.layout(offset=(x0, y0), label_offset=(20, 100))
        dc_a_ratio.widget().place(x=x0, y=y0)
        s_a_clip.widget().place(x=x1, y=y0)
        s_a_attack.widget().place(x=x2, y=y0)
        s_a_decay.widget().place(x=x3, y=y0)
        s_a_bend.widget().place(x=x4, y=y0)
        s_a_amp.widget().place(x=x5, y=y0)

        #dc_b_ratio.layout(offset=(x6, y0), label_offset=(20, 100))
        dc_b_ratio.widget().place(x=x6, y=y0)
        s_b_tune.widget().place(x=x7, y=y0)
        s_b_attack.widget().place(x=x8, y=y0)
        s_b_decay.widget().place(x=x9, y=y0)
        s_b_bend.widget().place(x=x10 , y=y0)
        s_b_amp.widget().place(x=x11, y=y0)

        y1 = 300
        x0 = 50
        x1 = x0 + 60
        x2 = x1 + 60
        x3 = x2 + 60
        x4 = x3 + 60
        x5 = x4 + 60
        x6 = x5 + 60
        x7 = x6 + 60
        s_noise_ratio.widget().place(x=x1, y=y1)
        s_noise_bias.widget().place(x=x2, y=y1)
        s_noise_res.widget().place(x=x3, y=y1)
        s_noise_attack.widget().place(x=x4, y=y1)
        s_noise_decay.widget().place(x=x5, y=y1)
        s_noise_bend.widget().place(x=x6, y=y1)
        s_noise_amp.widget().place(x=x7, y=y1)

        x8 = x7 + 107
        s_amp.widget().place(x=x8, y=y1)
        
