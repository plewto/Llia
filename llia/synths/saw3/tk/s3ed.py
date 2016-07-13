# llia.synths.saw3.tk.s3ed

from __future__ import print_function
from Tkinter import Frame

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cfactory
from llia.gui.tk.oscfreq_control import OscFrequencyControl
from llia.gui.tk.decade_control import DecadeControl
from llia.synths.saw3.tk.s3filter import TkSaw3FilterPanel
from llia.synths.saw3.tk.s3ctrl import TkSaw3ControlPanel


def create_editor(parent):
    panel1 = TkSaw3Panel1(parent)
    panel2 = TkSaw3FilterPanel(parent)
    panel3 = TkSaw3ControlPanel(parent)
    
class TkSaw3Panel1(TkSubEditor):

    NAME = "Saw3"
    IMAGE_FILE = "resources/Saw3/editor_osc.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        lab_panel = factory.image_label(frame, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)
        # OSC1
        ofc_1 = OscFrequencyControl(frame, "osc1Freq", editor)
        s_wave1 = cfactory.normalized_slider(frame, "osc1Wave", editor, 
                                             "OSC 1 Wave")
        s_osc1_amp = cfactory.volume_slider(frame, "osc1Amp", editor, 
                                            "OSC 1 Amp")
        s_wave1_env = cfactory.bipolar_slider(frame, "osc1Wave_env1", editor, 
                                              "ENV1 -> OSC 1 Wave")
        s_wave1_lfo = cfactory.bipolar_slider(frame, "osc1Wave_lfo", editor, 
                                              "LFO -> OSC 1 Wave")
        s_osc1_amp_env = cfactory.normalized_slider(frame, "osc1Amp_env1",
                                                    editor, 
                                                    "ENV1 -> OSC 1 Amp")
        y0, y1 = 50, 300
        ofc_1.layout(offset = (50, y0), off_offset = None)
        s_wave1.widget().place(x=240, y=y0)
        s_osc1_amp.widget().place(x=300, y=y0)
        s_wave1_env.widget().place(x=180, y=y1)
        s_wave1_lfo.widget().place(x=240, y=y1)
        s_osc1_amp_env.widget().place(x=300, y=y1)
        # OSC2
        ofc_2 = OscFrequencyControl(frame, "osc2Freq", editor)
        s_wave2 = cfactory.normalized_slider(frame, "osc2Wave", editor, 
                                             "OSC 2 Wave")
        s_osc2_amp = cfactory.volume_slider(frame, "osc2Amp", editor, 
                                            "OSC 2 Amp")
        s_wave2_env = cfactory.bipolar_slider(frame, "osc2Wave_env1", editor, 
                                              "ENV1 -> OSC 2 Wave")
        s_wave2_lfo = cfactory.bipolar_slider(frame, "osc2Wave_lfo", editor, 
                                              "LFO -> OSC 2 Wave")
        s_osc2_amp_env = cfactory.normalized_slider(frame, "osc2Amp_env1", 
                                                    editor,
                                                    "ENV1 -> OSC 2 Amp")
        ofc_2.layout(offset = (350, y0), off_offset = None)
        s_wave2.widget().place(x=540, y=y0)
        s_osc2_amp.widget().place(x=600, y=y0)
        s_wave2_env.widget().place(x=480, y=y1)
        s_wave2_lfo.widget().place(x=540, y=y1)
        s_osc2_amp_env.widget().place(x=600, y=y1)
        # OSC3
        ofc_3 = OscFrequencyControl(frame, "osc3Freq", editor)
        dc_bias3 = DecadeControl(frame, "osc3Bias", editor, (0.01, 1000))
        s_wave3 = cfactory.normalized_slider(frame, "osc3Wave", editor, 
                                             "OSC 3 Wave")
        s_osc3_amp = cfactory.volume_slider(frame, "osc3Amp", editor, 
                                            "OSC 3 Amp")
        s_wave3_env = cfactory.bipolar_slider(frame, "osc3Wave_env1", editor, 
                                              "ENV1 -> OSC 3 Wave")
        s_wave3_lfo = cfactory.bipolar_slider(frame, "osc3Wave_lfo", editor, 
                                              "LFO -> OSC 3 Wave")
        s_osc3_amp_env = cfactory.normalized_slider(frame, "osc3Amp_env1", 
                                                    editor, "ENV1 -> OSC 3 Amp")
        s_osc3_amp_env = cfactory.normalized_slider(frame, "osc3Amp_env1", 
                                                    editor, "ENV1 -> OSC 3 Amp")
        s_wave3_lag = cfactory.normalized_slider(frame, "osc3WaveLag", editor, 
                                                 "OSC 3 Wave lag")
        ofc_3.layout(offset = (650, y0))
        dc_bias3.layout(offset = (650, y1),
                        label_offset = (10, 130))
        s_wave3.widget().place(x=840, y=y0)
        s_osc3_amp.widget().place(x=900, y=y0)

        s_wave3_lag.widget().place(x=870, y=y0, width=10, height=75)


        s_wave3_env.widget().place(x=780, y=y1)
        s_wave3_lfo.widget().place(x=840, y=y1)
        s_osc3_amp_env.widget().place(x=900, y=y1)
        # Noise
        s_nse_freq = cfactory.linear_slider(frame, "noiseFreq", editor,
                                            range_=(0.5, 8.0),
                                            ttip="Noise frequency")
        s_nse_bw = cfactory.normalized_slider(frame, "noiseBW", editor, 
                                              "Noise Bandwidth")
        s_nse_amp = cfactory.volume_slider(frame, "noiseAmp", editor, 
                                           "Noise amp")
        s_nse_amp_env = cfactory.normalized_slider(frame, "noiseAmp_env1", 
                                                   editor, "ENV1 -> Noise amp")
        s_nse_freq.widget().place(x=980, y=y0)
        s_nse_amp.widget().place(x=1040, y=y0)
        s_nse_bw.widget().place(x=980, y=y1)
        s_nse_amp_env.widget().place(x=1040, y=y1)
        # Port
        s_port = cfactory.normalized_slider(frame, "port", editor, "Portamento")
        s_port.widget().place(x=50, y=y1)
        self.add_control("osc1Freq", ofc_1)
        self.add_control("osc1Wave", s_wave1)
        self.add_control("osc1Amp", s_osc1_amp)
        self.add_control("osc1Wave_env1", s_wave1_env)
        self.add_control("osc1Wave_lfo", s_wave1_lfo)
        self.add_control("osc1Amp_env1", s_osc1_amp_env)
        self.add_control("osc2Freq", ofc_2)
        self.add_control("osc2Wave", s_wave2)
        self.add_control("osc2Amp", s_osc2_amp)
        self.add_control("osc2Wave_env1", s_wave2_env)
        self.add_control("osc2Wave_lfo", s_wave2_lfo)
        self.add_control("osc2Amp_env1", s_osc2_amp_env)
        self.add_control("osc3Freq", ofc_3)
        self.add_control("osc3Bias", dc_bias3)
        self.add_control("osc3Wave", s_wave3)
        self.add_control("osc3Amp", s_osc3_amp)
        self.add_control("osc3Wave_env1", s_wave3_env)
        self.add_control("osc3Wave_lfo", s_wave3_lfo)
        self.add_control("osc3Amp_env1", s_osc3_amp_env)
        self.add_control("osc3Amp_env1", s_osc3_amp_env)
        self.add_control("osc3WaveLag", s_wave3_lag)
        self.add_control("noiseFreq", s_nse_freq)
        self.add_control("noiseBW", s_nse_bw)
        self.add_control("noiseAmp", s_nse_amp)
        self.add_control("noiseAmp_env1", s_nse_amp_env)
        self.add_control("port", s_port)


      
