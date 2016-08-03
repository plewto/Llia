# llia.synths.orgn.tk.orgn_ed
# 2016.06.23

from __future__ import print_function
from Tkinter import Frame

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cfactory
from llia.gui.tk.oscfreq_control import OscFrequencyControl
from llia.gui.tk.expslider import ExpSlider


def create_editor(parent_editor):
    panel1 = TkOrgnPanel1(parent_editor)
    panel2 = TkOrgnPanel2(parent_editor)


class TkOrgnPanel1(TkSubEditor):

    NAME = "Tone"
    IMAGE_FILE = "resources/Orgn/editor.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        lab_panel = factory.image_label(frame, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)
        oc1 = OscFrequencyControl(frame, "r1", editor)
        oc2 = OscFrequencyControl(frame, "r2", editor)
        oc3 = OscFrequencyControl(frame, "r3", editor)
        oc4 = OscFrequencyControl(frame, "r4", editor)
        s_mix1 = cfactory.mix_slider(frame, "amp1", editor)
        s_amp2 = cfactory.normalized_slider(frame, "amp2", editor)
        s_mix3 = cfactory.mix_slider(frame, "amp3", editor)
        s_amp4 = cfactory.normalized_slider(frame, "amp4", editor)
        s_mattack = ExpSlider(frame, "mattack", editor, range_=6)
        s_mdecay = ExpSlider(frame, "mdecay", editor, range_=6)
        s_mrelease = ExpSlider(frame, "mrelease", editor, range_=6)
        s_msustain = cfactory.normalized_slider(frame, "msustain", editor)
        s_cattack = ExpSlider(frame, "cattack", editor, range_=6)
        s_cdecay = ExpSlider(frame, "cdecay", editor, range_=6)
        s_crelease = ExpSlider(frame, "crelease", editor, range_=6)
        s_csustain = cfactory.normalized_slider(frame, "csustain", editor)
        self.add_control("r1", oc1)
        self.add_control("r2", oc2)
        self.add_control("r3", oc3)
        self.add_control("r4", oc4)
        self.add_control("amp1", s_mix1)
        self.add_control("amp2", s_amp2)
        self.add_control("amp3", s_mix3)
        self.add_control("amp4", s_amp4)
        self.add_control("mattack", s_mattack)
        self.add_control("mdecay", s_mdecay)
        self.add_control("msustain", s_msustain)
        self.add_control("mrelease", s_mrelease)
        self.add_control("cattack", s_cattack)
        self.add_control("cdecay", s_cdecay)
        self.add_control("csustain", s_csustain)
        self.add_control("crelease", s_crelease)
        y0, y1 = 60, 310
        x0 = 60
        x1 = x0 + 180
        x2 = x1 + 60
        x3 = x2 + 180
        xenv = x3+90
        xa = xenv
        xd = xa+60
        xs = xd+60
        xr = xs+60
        oc2.layout(offset=(x0, y0), off_offset=None)
        s_amp2.widget().place(x=x1, y=y0)
        oc3.layout(offset=(x2, y0), off_offset=None)
        s_amp4.widget().place(x=x3, y=y0)
        s_mattack.layout(offset=(xa,y0), checkbutton_offset=None)
        s_mdecay.layout(offset=(xd,y0), checkbutton_offset=None)
        s_msustain.widget().place(x=xs, y=y0)
        s_mrelease.layout(offset=(xr,y0), checkbutton_offset=None)
        oc1.layout(offset=(x0, y1), off_offset=None)
        s_mix1.widget().place(x=x1, y=y1)
        oc4.layout(offset=(x2, y1), off_offset=None)
        s_mix3.widget().place(x=x3, y=y1)
        s_cattack.layout(offset=(xa,y1), checkbutton_offset=None)
        s_cdecay.layout(offset=(xd,y1), checkbutton_offset=None)
        s_csustain.widget().place(x=xs, y=y1)
        s_crelease.layout(offset=(xr,y1), checkbutton_offset=None)
        

class TkOrgnPanel2(TkSubEditor):

    NAME = "Common"
    IMAGE_FILE = "resources/Orgn/editor2.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        lab_panel = factory.image_label(frame, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)
        s_mod = cfactory.normalized_slider(frame, "modulationDepth", editor)
        s_xmod = cfactory.normalized_slider(frame, "xToModulationDepth", editor)
        s_cdelay = cfactory.linear_slider(frame, "chorusDelay", editor, range_=(0,4))
        s_chorus = cfactory.normalized_slider(frame, "chorus", editor)
        s_vfreq = cfactory.linear_slider(frame,"vfreq", editor, range_=(1,8))
        s_vdelay = cfactory.linear_slider(frame, "vdelay", editor, range_=(0,4))
        s_vdepth = cfactory.normalized_slider(frame, "vdepth", editor)
        s_xpitch = cfactory.normalized_slider(frame, "xToPitch", editor)
        s_amp = cfactory.volume_slider(frame, "amp", editor)
        
        self.add_control("modulationDepth", s_mod)
        self.add_control("xToModulationDepth", s_xmod)
        self.add_control("chorusDelay", s_cdelay)
        self.add_control("chorus", s_chorus)
        self.add_control("vfreq", s_vfreq)
        self.add_control("vdelay", s_vdelay)
        self.add_control("vdepth", s_vdepth)
        self.add_control("xToPitch", s_xpitch)
        self.add_control("amp", s_amp)
        
        y0 = 60
        x0 = 60
        x1 = x0 + 60

        xchorus = x1 + 90
        x2 = xchorus
        x3 = x2 + 60

        xvib = x3 + 90
        x4 = xvib
        x5 = x4 + 60
        x6 = x5 + 60
        x7 = x6 + 60

        xamp = x7 + 90
        
        s_mod.widget().place(x=x0, y=y0)
        s_xmod.widget().place(x=x1, y=y0)
        s_cdelay.widget().place(x=x2, y=y0)
        s_chorus.widget().place(x=x3, y=y0)
        s_vfreq.widget().place(x=x4, y=y0)
        s_vdelay.widget().place(x=x5, y=y0)
        s_vdepth.widget().place(x=x6, y=y0)
        s_xpitch.widget().place(x=x7, y=y0)
        s_amp.widget().place(x=xamp, y=y0)
