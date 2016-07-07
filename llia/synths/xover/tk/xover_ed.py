# llia.synths.xover.tk.xover_ed
#

from __future__ import print_function
from Tkinter import Frame

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cfactory

def create_editor(parent):
    pass
    #tone_panel = TkXOverPanel(parent)
    #info_panel = TkXOverInfoPanel(parent)

# class TkXOverPanel(TkSubEditor):

#     NAME = "XOver"
#     IMAGE_FILE = "resources/XOver/editor.png"

#     def __init__(self, editor):
#         frame = editor.create_tab(self.NAME)
#         TkSubEditor.__init__(self, frame, editor, self.NAME)
#         editor.add_child_editor(self.NAME, self)
#         self.pack(expand=True, fill="both")
#         lab_panel = factory.image_label(self, self.IMAGE_FILE)
#         lab_panel.pack(anchor="nw", expand=False)
        
#         # Filter
#         s_xover = cfactory.third_octave_slider(self, "crossover", editor, "Crossover frequency")
#         s_res = cfactory.normalized_slider(self, "res", editor, "Filter resonace")
#         s_ringmod = cfactory.normalized_slider(self, "ringmod", editor, "Ringmod/Lowpass mix")
#         s_reverb = cfactory.normalized_slider(self, "rev", editor, "Reverb/Highpass mix")
#         s_room = cfactory.normalized_slider(self, "room", editor, "Reverb room size")

#         # LFO
#         s_lfo = cfactory.simple_lfo_freq_slider(self, "lfoFreq", editor, "LFO Frequency")
#         s_phase = cfactory.normalized_slider(self, "lfoPhase", editor, "LFO Phase")

#         # Pan
#         s_drypan = cfactory.bipolar_slider(self, "dryPan", editor, "Dry pan position")
#         s_lppan = cfactory.bipolar_slider(self, "lpPan", editor, "Lowpass/ringmod pan position")
#         s_hppan = cfactory.bipolar_slider(self, "hpPan", editor, "Highpass/reverb pan position")
#         s_lfopan = cfactory.normalized_slider(self, "lfoPan", editor, "LFO -> pan depth")

#         # Mix
#         s_dryamp = cfactory.volume_slider(self, "dryAmp", editor, "Dry amplitude")
#         s_wetamp = cfactory.volume_slider(self, "wetAmp", editor, "Wet amplitude")
#         s_amp = cfactory.volume_slider(self, "amp", editor, "Overall amplitude")
#         self.add_control("crossover", s_xover)
#         self.add_control("res", s_res)
#         self.add_control("ringmod", s_ringmod)
#         self.add_control("rev", s_reverb)
#         self.add_control("room", s_room)
        
#         self.add_control("lfoFreq", s_lfo)
#         self.add_control("lfoPhase", s_phase)
#         self.add_control("dryPan", s_drypan)
#         self.add_control("lpPan", s_lppan)
#         self.add_control("hpPan", s_hppan)
#         self.add_control("lfoPan", s_lfopan)
#         self.add_control("dryAmp", s_dryamp)
#         self.add_control("wetAmp", s_wetamp)
#         self.add_control("amp", s_amp)

#         y0 = 50
#         x1,x2,x3,x4,x5 = 50, 110, 170, 230, 290

#         s_xover.widget().place(x=x1, y=y0)
#         s_res.widget().place(x=x2, y=y0)
#         s_ringmod.widget().place(x=x3, y=y0)
#         s_reverb.widget().place(x=x4, y=y0)
#         s_room.widget().place(x=x5, y=y0)

#         x6,x7 = 410, 470
#         s_lfo.widget().place(x=x6, y=y0)
#         s_phase.widget().place(x=x7, y=y0)

#         y1 = 260
#         x8,x9,x10,x11 = 50, 110, 170, 230
#         s_drypan.widget().place(x=x8, y=y1)
#         s_lppan.widget().place(x=x9, y=y1)
#         s_hppan.widget().place(x=x10, y=y1)
#         s_lfopan.widget().place(x=x11, y=y1)

#         x12,x13,x14 = 350, 410, 470
#         s_dryamp.widget().place(x=x12, y=y1)
#         s_wetamp.widget().place(x=x13, y=y1)
#         s_amp.widget().place(x=x14, y=y1)
