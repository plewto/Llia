# llia.synths.saw3.tk.s3ed

from __future__ import print_function
from Tkinter import Frame

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cfactory
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.oscfreq_control import OscFrequencyControl
from llia.gui.tk.decade_control import DecadeControl
from llia.synths.saw3.tk.s3filter import TkSaw3FilterPanel




def create_editor(parent):
    panel1 = TkSaw3Panel1(parent)
    panel2 = TkSaw3FilterPanel(parent)
    panel4 = TkSaw3InfoPanel(parent)
    
class TkSaw3Panel1(TkSubEditor):

    NAME = "Saw3"
    IMAGE_FILE = "resources/Saw3/editor_osc.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        lab_panel = factory.image_label(frame, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)
        # OSC1
        ofc_1 = OscFrequencyControl(frame, "osc1Freq", editor)
        s_wave1 = cfactory.normalized_slider(frame, "osc1Wave", editor)
        s_amp1 = cfactory.mix_slider(frame, "osc1Amp", editor)
        s_wave1_env = ExpSlider(frame, "osc1Wave_env1", editor, 1.0)
        s_wave1_lfo = ExpSlider(frame, "osc1Wave_lfo", editor, 1.0)
        s_amp1_env = ExpSlider(frame, "osc1Amp_env1", editor, 1.0)
        s_port = cfactory.normalized_slider(frame, "port", editor)
        s_xpitch = cfactory.normalized_slider(frame, 'xToPitch', editor)
        self.add_control("osc1Freq", ofc_1)
        self.add_control("osc1Wave", s_wave1)
        self.add_control("osc1Amp", s_amp1)
        self.add_control("osc1Wave_env1", s_wave1_env)
        self.add_control("osc1Wave_lfo", s_wave1_lfo)
        self.add_control("osc1Amp_env1", s_amp1_env)
        self.add_control("port", s_port)
        self.add_control('xToPitch', s_xpitch)
        y0, y1 = 50, 300
        x0 = 50
        x1 = x0 + 190
        x2 = x1 + 60
        x3 = x2 + 60
        ofc_1.layout(offset=(x0, y0), off_offset=None)
        s_wave1.widget().place(x=x1, y=y0)
        s_amp1.widget().place(x=x2, y=y0)
        x0 += 8
        x1 = x0 + 128
        x2 = x1 + 60
        x3 = x2 + 60
        s_port.widget().place(x=x0, y=y1)
        s_xpitch.widget().place(x=x0+60, y=y1)
        s_wave1_env.layout(offset=(x1, y1), checkbutton_offset=(-5,-28))
        s_wave1_lfo.layout(offset=(x2, y1), checkbutton_offset=(-5,-28))
        s_amp1_env.layout(offset=(x3, y1), checkbutton_offset=(-5,-28))
        # OSC2
        ofc_2 = OscFrequencyControl(frame, "osc2Freq", editor)
        s_wave2 = cfactory.normalized_slider(frame, "osc2Wave", editor)
        s_amp2 = cfactory.mix_slider(frame, "osc2Amp", editor)
        s_wave2_env = ExpSlider(frame, "osc2Wave_env1", editor, 1.0)
        s_wave2_lfo = ExpSlider(frame, "osc2Wave_lfo", editor, 1.0)
        s_amp2_env = ExpSlider(frame, "osc2Amp_env1", editor, 1.0)

        self.add_control("osc2Freq", ofc_2)
        self.add_control("osc2Wave", s_wave2)
        self.add_control("osc2Amp", s_amp2)
        self.add_control("osc2Wave_env1", s_wave2_env)
        self.add_control("osc2Wave_lfo", s_wave2_lfo)
        self.add_control("osc2Amp_env1", s_amp2_env)
        x0 = 390
        x1 = x0 + 190
        x2 = x1 + 60
        x3 = x2 + 60
        ofc_2.layout(offset=(x0, y0), off_offset=None)
        s_wave2.widget().place(x=x1, y=y0)
        s_amp2.widget().place(x=x2, y=y0)
        x0 += 8
        x1 = x0 + 128
        x2 = x1 + 60
        x3 = x2 + 60
        s_wave2_env.layout(offset=(x1, y1), checkbutton_offset=(-5,-28))
        s_wave2_lfo.layout(offset=(x2, y1), checkbutton_offset=(-5,-28))
        s_amp2_env.layout(offset=(x3, y1), checkbutton_offset=(-5,-28))
        # OSC3
        ofc_3 = OscFrequencyControl(frame, "osc3Freq", editor)
        dc_bias3 = DecadeControl(frame, "osc3Bias", editor, (0.01, 1000))
        s_wave3 = cfactory.normalized_slider(frame, "osc3Wave", editor)
        s_amp3 = cfactory.mix_slider(frame, "osc3Amp", editor)
        s_wave3_env = ExpSlider(frame, "osc3Wave_env1", editor, 1.0)
        s_wave3_lfo = ExpSlider(frame, "osc3Wave_lfo", editor, 1.0)
        s_amp3_env = ExpSlider(frame, "osc3Amp_env1", editor, 1.0)
        s_wave3_lag = cfactory.normalized_slider(frame, "osc3WaveLag", editor)
        self.add_control("osc3Freq", ofc_3)
        self.add_control("osc3Bias", dc_bias3)
        self.add_control("osc3Wave", s_wave3)
        self.add_control("osc3Amp", s_amp3)
        self.add_control("osc3Wave_env1", s_wave3_env)
        self.add_control("osc3Wave_lfo", s_wave3_lfo)
        self.add_control("osc3Amp_env1", s_amp3_env)
        self.add_control("osc3WaveLag", s_wave3_lag)
        x0 = 731
        x1 = x0 + 190
        x2 = x1 + 60
        x3 = x2 + 60
        ofc_3.layout(offset=(x0, y0), off_offset=None)
        s_wave3.widget().place(x=x1, y=y0)
        s_wave3_lag.widget().place(x=x1+20, y=y0, width=10, height=75)
        s_amp3.widget().place(x=x2, y=y0)
        x1 = x0 + 128
        x2 = x1 + 60
        x3 = x2 + 60
        dc_bias3.layout(offset=(x0, y1), label_offset=(10,130))
        s_wave3_env.layout(offset=(x1, y1), checkbutton_offset=(-5,-28))
        s_wave3_lfo.layout(offset=(x2, y1), checkbutton_offset=(-5,-28))
        s_amp3_env.layout(offset=(x3, y1), checkbutton_offset=(-5,-28))
        # Noise
        s_nse_freq = cfactory.linear_slider(frame, "noiseFreq", editor,range_=(0.5, 8.0))
        s_nse_bw = cfactory.normalized_slider(frame, "noiseBW", editor)
        s_nse_amp = cfactory.mix_slider(frame, "noiseAmp", editor) 
        s_nse_amp_env = ExpSlider(frame, "noiseAmp_env1", editor, range_=1.0)
        self.add_control("noiseFreq", s_nse_freq)
        self.add_control("noiseBW", s_nse_bw)
        self.add_control("noiseAmp", s_nse_amp)
        self.add_control("noiseAmp_env1", s_nse_amp_env)
        x0 += 330
        x1 = x0 + 60
        s_nse_freq.widget().place(x=x0, y=y0)
        s_nse_amp.widget().place(x=x1, y=y0)
        s_nse_bw.widget().place(x=x0, y=y1)
        s_nse_amp_env.layout(offset=(x1, y1),checkbutton_offset=(-5,-28))


class TkSaw3InfoPanel(object):

    NAME = "Info"
    IMAGE_FILE = "resources/Saw3/editor_info.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        lab_panel = factory.image_label(frame, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)
        
    
