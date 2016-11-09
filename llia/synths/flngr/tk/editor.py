# llia.synths.flngr.tk.editor

from __future__ import print_function

import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.tk_subeditor import TkSubEditor
from llia.gui.tk.expslider import ExpSlider

def create_editor(parent):
    panel = TkFlngrPanel(parent)

class TkFlngrPanel(TkSubEditor):

    NAME = "Flangr"
    IMAGE_FILE = "resources/Flngr/editor.png"
    TAB_FILE = "resources/Flngr/tab.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        self.pack(expand=True, fill="both")
        lab_panel = factory.image_label(self, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)
        s_delay = cf.normalized_slider(frame, "delay", editor)
        s_mod_depth = ExpSlider(frame, "imodDepth", editor, range_=1, degree=2)
        s_mod_freq = ExpSlider(frame, "imodFreq", editor, range_=10, degree=3)
        s_xmod_depth = ExpSlider(frame, "xmodDepth", editor, range_=1, degree=2)
        s_feedback = cf.bipolar_slider(frame, "feedback", editor)
        s_low_eq = cf.third_octave_slider(frame, "feedbackLowpass", editor)
        s_high_eq = cf.third_octave_slider(frame, "feedbackHighpass", editor)
        s_mix = cf.normalized_slider(frame, "efxMix", editor)
        s_xmix = cf.normalized_slider(frame, "xmixScale", editor)
        s_amp = cf.volume_slider(frame, "amp", editor)
        self.add_control("delay", s_delay)
        self.add_control("imodDepth", s_mod_depth)
        self.add_control("imodFreq", s_mod_freq)
        self.add_control("xmodDepth", s_xmod_depth)
        self.add_control("feedback", s_feedback)
        self.add_control("feedbackLowpass", s_low_eq)
        self.add_control("feedbackHighpass", s_high_eq)
        self.add_control("efxMix", s_mix)
        self.add_control("xmixScale", s_xmix)
        self.add_control("amp", s_amp)
        y0 = 120
        x0 = 120
        x1 = x0 + 90
        x2 = x1 + 60
        x3 = x2 + 60
        xfb = x3 + 90
        x4 = xfb
        x5 = x4 + 60
        x6 = x5 + 60
        xmix = x6 + 90
        x7 = xmix
        x8 = x7+60
        xamp = x8+90
        s_delay.widget().place(x=x0, y=y0, height=175)
        s_mod_depth.layout(offset=(x1,y0), height=175, checkbutton_offset=None)
        s_mod_freq.layout(offset=(x2,y0), height = 175, checkbutton_offset=None)
        s_xmod_depth.layout(offset=(x3, y0), height=175, checkbutton_offset=None)
        s_feedback.widget().place(x=x4, y=y0, height=175)
        s_low_eq.widget().place(x=x5, y=y0, height=175)
        s_high_eq.widget().place(x=x6, y=y0, height=175)
        s_mix.widget().place(x=x7, y=y0, height=175)
        s_xmix.widget().place(x=x8, y=y0, height=175)
        s_amp.widget().place(x=xamp, y=y0, height=175)
    
