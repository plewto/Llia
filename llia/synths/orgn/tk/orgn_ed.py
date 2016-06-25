# llia.synths.orgn.tk.orgn_ed
# 2016.06.23

from __future__ import print_function

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cfactory

def create_tk_orgn_editor(parent):
    tone_panel = TkOrgnPanel1(parent)


class TkOrgnPanel1(TkSubEditor):

    NAME = "Tone"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        self.pack(expand=True, fill="both")

        # Vibrato
        v_frame = factory.frame(self)
        s_vfreq = cfactory.simple_lfo_freq_slider(v_frame, "vfreq", editor, "Vibrato Frequency")
        s_vsens = cfactory.normalized_slider(v_frame, "vsens", editor, "Vibrato Sensitivity")
        s_vdepth = cfactory.normalized_slider(v_frame, "vdepth", editor, "Vibrato Depth")
        w = factory.label(v_frame, "Vibrato")
        w.grid(row=0, column=0, columnspan=3)
        s_vfreq.widget().grid(row=1, column=0)
        s_vsens.widget().grid(row=1, column=1)
        s_vdepth.widget().grid(row=1, column=2)
        factory.label(v_frame, "F").grid(row=2, column=0)
        factory.label(v_frame, "S").grid(row=2, column=1)
        factory.label(v_frame, "D").grid(row=2, column=2)
        v_frame.grid(row=1, column=0, padx=16, pady=16)
        
        # Chorus
        c_frame = factory.frame(self)
        s_chorus = cfactory.normalized_slider(c_frame, "chorus", editor, "Chorus depth")
        s_chorus_delay = cfactory.normalized_slider(c_frame, "chorusDelay", editor, "Chorus delay")
        s_chorus.widget().grid(row=1, column=0)
        s_chorus_delay.widget().grid(row=1, column=1)
        factory.label(c_frame, "Chorus").grid(row=0, column=0, columnspan=3)
        c_frame.grid(row=1, column=1, padx=16, pady=16)

        # Tone A
        ta_frame = factory.label_frame(self, "A")
        car_a = cfactory.OscFrequencyControl(ta_frame, "m1", editor)
        mod_a = cfactory.OscFrequencyControl(ta_frame, "c1", editor)
        s_moda = cfactory.normalized_slider(ta_frame, "mod1", editor, "Mod Depth A")
        s_mixa = cfactory.volume_slider(ta_frame, "amp1", editor, "Tone A Mix")
        car_a.widget().grid(row=0, column=0)
        mod_a.widget().grid(row=0, column=1)
        s_moda.widget().grid(row=0, column=2)
        s_mixa.widget().grid(row=0, column=3)
        ta_frame.grid(row=2, column=0, padx=16, pady=16)

        # Tone B
        tb_frame = factory.label_frame(self, "B")
        car_b = cfactory.OscFrequencyControl(tb_frame, "m2", editor)
        mod_b = cfactory.OscFrequencyControl(tb_frame, "c2", editor)
        s_modb = cfactory.normalized_slider(tb_frame, "mod2", editor, "Mod Depth B")
        s_mixb = cfactory.volume_slider(tb_frame, "amp2", editor, "Tone B Mix")
        car_b.widget().grid(row=0, column=0)
        mod_b.widget().grid(row=0, column=1)
        s_modb.widget().grid(row=0, column=2)
        s_mixb.widget().grid(row=0, column=3)
        tb_frame.grid(row=2, column=1, padx=16, pady=16)

        # Tone C
        tc_frame = factory.label_frame(self, "C")
        car_c = cfactory.OscFrequencyControl(tc_frame, "m3", editor)
        mod_c = cfactory.OscFrequencyControl(tc_frame, "c3", editor)
        s_modc = cfactory.normalized_slider(tc_frame, "mod3", editor, "Mod Depth C")
        s_mixc = cfactory.volume_slider(tc_frame, "amp3", editor, "Tone C Mix")
        s_attack = cfactory.normalized_slider(tc_frame, "attack3", editor, "Tone C Attack")
        s_decay = cfactory.normalized_slider(tc_frame, "decay3", editor)
        s_sustain = cfactory.normalized_slider(tc_frame, "sustain3", editor)
        s_release = cfactory.normalized_slider(tc_frame, "release3", editor)
        car_c.widget().grid(row=0, column=0)
        mod_c.widget().grid(row=0, column=1)
        s_modc.widget().grid(row=0, column=2)
        s_mixc.widget().grid(row=0, column=3)
        factory.padding_label(tc_frame).grid(row=0, column=4)
        s_attack.widget().grid(row=0, column=5)
        s_decay.widget().grid(row=0, column=6)
        s_sustain.widget().grid(row=0, column=7)
        s_release.widget().grid(row=0, column=8)
        tc_frame.grid(row=2, column=2, padx=16, pady=16)

        # Misc Contrls
        misc_frame = factory.frame(self)
        s_amp = cfactory.volume_slider(misc_frame, "amp", editor, "Overall Volumne")
        s_brightness = cfactory.normalized_slider(misc_frame, "brightness", editor, "Brightness")
        s_amp.widget().grid(row=0, column=0)
        s_brightness.widget().grid(row=0, column=1)
        misc_frame.grid(row=2, column=3, padx=16)
