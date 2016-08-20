# llia.synths.ghostbus.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.synths.ghostbus.ghost_data import MAX_DELAY
#from llia.gui.tk.expslider import ExpSlider
#from llia.gui.tk.decade_control import DecadeControl
#from llia.gui.tk.reciprocal_slider import ReciprocalSlider


def create_editor(parent):
    TkGhostbusPanel(parent)

class TkGhostbusPanel(TkSubEditor):

    NAME = "Ghostbus"
    IMAGE_FILE = "resources/Ghostbus/editor.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        lab_panel = factory.image_label(frame, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)
        s_delay = cf.linear_slider(frame, "delay", editor, range_=(0,MAX_DELAY))
        s_feedback = cf.linear_slider(frame, "feedback", editor, range_=(-1,1))
        s_lag = cf.normalized_slider(frame, "lag", editor)
        s_scale = cf.linear_slider(frame, "scale", editor, range_=(-4,4))
        s_bias = cf.linear_slider(frame, "scale", editor, range_=(-4,4))
        self.add_control("delay", s_delay)
        self.add_control("feedback", s_feedback)
        self.add_control("lag", s_lag)
        self.add_control("scale", s_scale)
        self.add_control("scale", s_bias)
        x0,y0 = 120, 60
        s_delay.widget().place(x=x0, y=y0, height=250)
        s_feedback.widget().place(x=x0+60, y=y0, height=250)
        s_lag.widget().place(x=x0+120, y=y0, height=250)
        s_scale.widget().place(x=x0+180, y=y0, height=250)
        s_bias.widget().place(x=x0+240, y=y0, height=250)

