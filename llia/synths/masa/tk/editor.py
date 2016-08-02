# llia.synths.masa.tk.editor

from __future__ import print_function

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cfactory
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.decade_control import DecadeControl

def create_editor(parent):
    panel1 = TkMasaPanel1(parent)

class TkMasaPanel1(TkSubEditor):

    NAME = "MASA"
    IMAGE_FILE = "resources/MASA/editor.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        lab_panel = factory.image_label(frame, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)

        y0, y1, y2 = 60, 170, 280
        x0, xdelta = 60, 30        
        for i in range(9):
            j = i+1
            x = x0 + i * xdelta
            pa = "a%d" % j
            sa = cfactory.normalized_slider(frame, pa, editor)
            self.add_control(pa, sa)
            sa.widget().place(x=x, y=y0, height=100, width=10)
            pp = "p%d" % j
            sp = cfactory.normalized_slider(frame, pp, editor)
            self.add_control(pp, sp)
            sp.widget().place(x=x, y=y1, height=100, width=10)
            px = "x%d" % j
            sx = cfactory.normalized_slider(frame, px, editor)
            self.add_control(px, sx)
            sx.widget().place(x=x, y=y2, height=100, width=10)
        # Envelope
        xenv = x0 + (xdelta * 10)
        s_attack = ExpSlider(frame, "attack", editor, range_=1)
        s_decay = ExpSlider(frame, "decay", editor, range_=1)
        self.add_control("attack", s_attack)
        self.add_control("decay", s_decay)
        s_attack.layout(offset = (xenv, y0+30),
                        height = 100, width = 14,
                        checkbutton_offset = None)
        s_decay.layout(offset = (xenv, y2-30),
                       height = 100, width = 14,
                       checkbutton_offset = None)
        # Vibrato
        xvib = xenv + 120
        s_vfreq = ExpSlider(frame, "vfreq", editor, range_=8, degree=2)
        s_vdelay = cfactory.linear_slider(frame, "vdelay", editor, range_=(0,4))
        s_vsens = cfactory.normalized_slider(frame, "vsens", editor)
        s_vdepth = cfactory.normalized_slider(frame, "vdepth", editor)
        self.add_control("vfreq", s_vfreq)
        self.add_control("vdelay", s_vfreq)
        self.add_control("vdepth", s_vdepth)
        s_vfreq.layout(offset=(xvib, y0),checkbutton_offset = None)
        s_vdelay.widget().place(x=xvib+60, y=y0)
        s_vsens.widget().place(x=xvib+120, y=y0)
        s_vdepth.widget().place(x=xvib+180, y=y0)

        # X Bus
        xx = xvib
        s_xbias = cfactory.linear_slider(frame, "xBias", editor, range_=(-2,2))
        s_xscale = cfactory.linear_slider(frame, "xScale", editor, range_=(0, 2))
        s_xfreq = ExpSlider(frame, "xToFreq", editor, range_=1)
        self.add_control("xBias", s_xbias)
        self.add_control("xScale", s_xscale)
        self.add_control("xToFreq", s_xfreq)
        s_xbias.widget().place(x=xx, y=y2)
        s_xscale.widget().place(x=xx+60, y=y2)
        s_xfreq.layout(offset=(xx+120, y2), checkbutton_offset=None)

        # AMP
        s_amp = cfactory.volume_slider(frame, "amp", editor)
        self.add_control("amp", s_amp)
        s_amp.widget().place(x=xx+188, y=y2)
