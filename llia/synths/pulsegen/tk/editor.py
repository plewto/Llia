# llia.synths.pulsegen.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.decade_control import DecadeControl
from llia.gui.tk.reciprocal_slider import ReciprocalSlider
from llia.synths.pulsegen.pulsegen_data import RATIOS, AMPS


def create_editor(parent):
    TkPulseGenPanel(parent)


class TkPulseGenPanel(TkSubEditor):

    NAME = "PulseGen"
    IMAGE_FILE = "resources/PulseGen/editor.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        lab_panel = factory.image_label(frame, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)
        y0,y1,y2 = 90, 230, 370
        x0 = 90
        x1 = x0+200
        dc_freq = DecadeControl(frame, "clockFreq", editor,
                                coarse = (0.01, 10),
                                limit=(0.01, 100))
        self.add_control("clockFreq", dc_freq)
        dc_freq.layout(offset=(x0,y0), label_offset=(10, 100))
        
        for i, a in enumerate("ABCDEF"):
            x = x1 + (i * 60)
            pratio = "ratio%s" % a
            py = "yAmp%s" % a
            pz = "zAmp%s" % a
            sr = cf.discrete_slider(frame, pratio, editor, values=RATIOS)
            sy = cf.discrete_slider(frame, py, editor, values=AMPS)
            sz = cf.discrete_slider(frame, pz, editor, values=AMPS)
            self.add_control(pratio, sr)
            self.add_control(py,sy)
            self.add_control(pz,sz)
            sr.widget().place(x=x, y=y0, height=100)
            sy.widget().place(x=x, y=y1, height=100)
            sz.widget().place(x=x, y=y2, height=100)

        y1 = 318
        x2 = 670
        x3 = x2 + 60
        x4 = x3 + 60
        s_ylag = cf.normalized_slider(frame,"yLag",editor)
        s_yscale = cf.linear_slider(frame, "yScale", editor, range_=(0,4))
        s_ybias = cf.linear_slider(frame, "yBias", editor, range_=(-4,4))

        s_zlag = cf.normalized_slider(frame,"zLag",editor)
        s_zscale = cf.linear_slider(frame, "zScale", editor, range_=(0,4))
        s_zbias = cf.linear_slider(frame, "zBias", editor, range_=(-4,4))
        
        self.add_control("yLag", s_ylag)
        self.add_control("yScale", s_yscale)
        self.add_control("yBias", s_ybias)
        self.add_control("zLag", s_zlag)
        self.add_control("zScale", s_zscale)
        self.add_control("zBias", s_zbias)

        s_ylag.widget().place(x=x2, y=y0)
        s_yscale.widget().place(x=x3, y=y0)
        s_ybias.widget().place(x=x4, y=y0)


        s_zlag.widget().place(x=x2, y=y1)
        s_zscale.widget().place(x=x3, y=y1)
        s_zbias.widget().place(x=x4, y=y1)


