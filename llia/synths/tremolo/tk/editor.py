# llia.synths.tremolo.tk.editor

from __future__ import print_function

import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.tk_subeditor import TkSubEditor
from llia.gui.tk.expslider import ExpSlider


def create_editor(parent):
    panel = TkTremoloPanel(parent)

class TkTremoloPanel(TkSubEditor):

    NAME = "Tremolo"
    IMAGE_FILE = "resources/Tremolo/editor.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        self.pack(expand=True, fill="both")
        lab_panel = factory.image_label(self, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)
        s_freq = ExpSlider(frame, "lfoFreq", editor, range_=10)
        s_depth = cf.normalized_slider(frame, "modDepth", editor)
        s_xdepth = cf.normalized_slider(frame, "xDepth", editor)
        s_xam = cf.normalized_slider(frame, "xLfoAmp", editor)
        s_xfm = ExpSlider(frame, "xLfoFreq", editor, range_=30)
        s_limit = cf.linear_slider(frame, "limit", editor, range_=(0,2))
        s_amp = cf.volume_slider(frame, "amp", editor)
        self.add_control("lfoFreq",s_freq)
        self.add_control("modDepth",s_depth)
        self.add_control("xDepth",s_xdepth)
        self.add_control("xLfoAmp",s_xam)
        self.add_control("xLfoFreq",s_xfm)
        self.add_control("limit",s_limit)
        self.add_control("amp",s_amp)
        y0 = 90
        x0 = 90
        x1 = x0 + 60
        x2 = x1 + 90
        x3 = x2 + 60
        x4 = x3 + 60
        x5 = x4 + 90
        x6 = x5 + 90
        s_freq.layout(offset=(x0, y0), checkbutton_offset=None)
        s_depth.widget().place(x=x1, y=y0)
        s_xdepth.widget().place(x=x2, y=y0)
        s_xam.widget().place(x=x3, y=y0)
        s_xfm.layout(offset=(x4, y0), checkbutton_offset=None)
        s_limit.widget().place(x=x5, y=y0)
        s_amp.widget().place(x=x6, y=y0)
