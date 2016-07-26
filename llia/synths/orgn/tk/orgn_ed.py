# llia.synths.orgn.tk.orgn_ed
# 2016.06.23

from __future__ import print_function
from Tkinter import Frame

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cfactory



def create_tk_orgn_editor(parent):
    tone_panel = TkOrgnPanel1(parent)
    info_panel = TkOrgnInfoPanel(parent)


class TkOrgnPanel1(TkSubEditor):

    NAME = "Tone"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        self.pack(expand=True, fill="both")
        # Tone 1
        ta_frame = factory.label_frame(self, " Tone 1")
        car_a = cfactory.OscFrequencyControl(ta_frame, "c1", editor)
        mod_a = cfactory.OscFrequencyControl(ta_frame, "m1", editor)
        s_moda = cfactory.normalized_slider(ta_frame, "mod1", editor, "Mod Depth A")
        s_mixa = cfactory.mix_slider(ta_frame, "amp1", editor, "Tone A Mix")
        car_a.widget().grid(row=0, column=0, padx=4)
        mod_a.widget().grid(row=0, column=1, padx=4)
        s_moda.widget().grid(row=0, column=2, padx=4)
        s_mixa.widget().grid(row=0, column=3, padx=4)
        factory.label(ta_frame, "carrier").grid(row=1, column=0, pady=1)
        factory.label(ta_frame, "modulator").grid(row=1, column=1, pady=1)
        factory.label(ta_frame, "depth").grid(row=1, column=2, pady=1)
        factory.label(ta_frame, "mix").grid(row=1, column=3, pady=1)
        ta_frame.grid(row=1, column=0, columnspan=2 ,padx=8, pady=16)
        # Tone B
        tb_frame = factory.label_frame(self, " Tone 2")
        car_b = cfactory.OscFrequencyControl(tb_frame, "c2", editor)
        mod_b = cfactory.OscFrequencyControl(tb_frame, "m2", editor)
        s_modb = cfactory.normalized_slider(tb_frame, "mod2", editor, "Mod Depth B")
        s_mixb = cfactory.mix_slider(tb_frame, "amp2", editor, "Tone B Mix")
        car_b.widget().grid(row=0, column=0)
        mod_b.widget().grid(row=0, column=1)
        s_modb.widget().grid(row=0, column=2)
        s_mixb.widget().grid(row=0, column=3)
        factory.label(tb_frame, "carrier").grid(row=1, column=0, pady=1)
        factory.label(tb_frame, "modulator").grid(row=1, column=1, pady=1)
        factory.label(tb_frame, "depth").grid(row=1, column=2, pady=1)
        factory.label(tb_frame, "mix").grid(row=1, column=3, pady=1)
        tb_frame.grid(row=1, column=2, columnspan=2,padx=0, pady=16)
        # Tone C
        tc_frame = factory.label_frame(self, "Tone 3")
        car_c = cfactory.OscFrequencyControl(tc_frame, "c3", editor)
        mod_c = cfactory.OscFrequencyControl(tc_frame, "m3", editor)
        s_modc = cfactory.normalized_slider(tc_frame, "mod3", editor, "Mod Depth C")
        s_mixc = cfactory.mix_slider(tc_frame, "amp3", editor, "Tone C Mix")
        s_attack = cfactory.normalized_slider(tc_frame, "attack3", editor, "Tone C Attack")
        s_decay = cfactory.normalized_slider(tc_frame, "decay3", editor)
        s_sustain = cfactory.normalized_slider(tc_frame, "sustain3", editor)
        s_release = cfactory.normalized_slider(tc_frame, "release3", editor)
        car_c.widget().grid(row=0, column=0)
        mod_c.widget().grid(row=0, column=1)
        s_modc.widget().grid(row=0, column=2)
        s_mixc.widget().grid(row=0, column=3)
        factory.padding_label(tc_frame, modal=False).grid(row=0, column=4, padx=8)
        s_attack.widget().grid(row=0, column=5)
        s_decay.widget().grid(row=0, column=6)
        s_sustain.widget().grid(row=0, column=7)
        s_release.widget().grid(row=0, column=8)
        factory.label(tc_frame, "carrier").grid(row=1, column=0, pady=1)
        factory.label(tc_frame, "modulator").grid(row=1, column=1, pady=1)
        factory.label(tc_frame, "depth").grid(row=1, column=2, pady=1)
        factory.label(tc_frame, "mix").grid(row=1, column=3, pady=1)
        factory.label(tc_frame, "A").grid(row=1, column=5)
        factory.label(tc_frame, "D").grid(row=1, column=6)
        factory.label(tc_frame, "S").grid(row=1, column=7)
        factory.label(tc_frame, "R").grid(row=1, column=8)
        tc_frame.grid(row=1, column=4, columnspan=3, padx=8, pady=16)
        # Vibrato
        v_frame = factory.label_frame(self, "Vibrato")
        s_vfreq = cfactory.simple_lfo_freq_slider(v_frame, "vfreq", editor, "Vibrato Frequency")
        s_vsens = cfactory.normalized_slider(v_frame, "vsens", editor, "Vibrato Sensitivity")
        s_vdepth = cfactory.normalized_slider(v_frame, "vdepth", editor, "Vibrato Depth")
        s_vfreq.widget().grid(row=1, column=0)
        s_vsens.widget().grid(row=1, column=1)
        s_vdepth.widget().grid(row=1, column=2)
        factory.label(v_frame, "freq").grid(row=2, column=0)
        factory.label(v_frame, "sens").grid(row=2, column=1)
        factory.label(v_frame, "depth").grid(row=2, column=2)
        v_frame.grid(row=2, column=0, padx=8, pady=16)
        # Chorus
        c_frame = factory.label_frame(self, "Chorus")
        s_chorus = cfactory.normalized_slider(c_frame, "chorus", editor, "Chorus depth")
        s_chorus_delay = cfactory.normalized_slider(c_frame, "chorusDelay", editor, "Chorus delay")
        s_chorus.widget().grid(row=1, column=0)
        s_chorus_delay.widget().grid(row=1, column=1)
        factory.label(c_frame, "detune").grid(row=2, column=0)
        factory.label(c_frame, "delay").grid(row=2, column=1)
        c_frame.grid(row=2, column=1, padx=0, pady=16)
        # Main
        misc_frame = factory.label_frame(self, "Main")
        s_amp = cfactory.volume_slider(misc_frame, "amp", editor, "Overall Volumne")
        s_brightness = cfactory.normalized_slider(misc_frame, "brightness", editor, "Brightness")
        s_brightness.widget().grid(row=0, column=0)
        s_amp.widget().grid(row=0, column=1)
        factory.label(misc_frame, "Brightness").grid(row=1, column=0)
        factory.label(misc_frame, "Amp").grid(row=1, column=1)
        misc_frame.grid(row=2, column=2, padx=8)
        self.add_control("c1", car_a)
        self.add_control("m1", mod_a)
        self.add_control("mod1", s_moda)
        self.add_control("amp1", s_mixa)
        self.add_control("c2", car_b)
        self.add_control("m2", mod_b)
        self.add_control("mod2", s_modb)
        self.add_control("amp2", s_mixb)
        self.add_control("c3", car_c)
        self.add_control("m3", mod_c)
        self.add_control("mod3", s_modc)
        self.add_control("amp3", s_mixc)
        self.add_control("attack3", s_attack)
        self.add_control("decay3", s_decay)
        self.add_control("sustain3", s_sustain)
        self.add_control("release3", s_release)
        self.add_control("vfreq", s_vfreq)
        self.add_control("vsens", s_vsens)
        self.add_control("vdepth", s_vdepth)
        self.add_control("chorus", s_chorus)
        self.add_control("chorusDelay", s_chorus_delay)
        self.add_control("amp", s_amp)
        self.add_control("brightness", s_brightness)
     

class TkOrgnInfoPanel(Frame):

    def __init__(self, editor):
        Frame.__init__(self, editor.notebook)
        self.config(background=factory.bg())
        ifname = "resources/Orgn/info.png"
        w = factory.image_label(self, ifname)
        w.pack(expand=True, fill="both")
        editor.notebook.add(self, text="Info")
