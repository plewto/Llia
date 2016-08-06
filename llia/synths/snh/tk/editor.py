# llia.synths.snh.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.decade_control import DecadeControl
from llia.gui.tk.reciprocal_slider import ReciprocalSlider


# shRate    - decade control
# srcFreq   - decade control
# srcSelect - normal slider
# shLag     - normal slider
# shBleed   - normal slider
# shDelay   - exp slider (0..4)
# shAttack  - exp slider (0..4)
# shHold    - exp slider (0..4)
# shRelease - exp slider (0..4)
# shScale   - recipricol slider control
# shBias    - linear slider



def create_editor(parent):
    panel = TkSnHPanel(parent)

class TkSnHPanel(TkSubEditor):

    NAME = "SnH"
    IMAGE_FILE = "resources/SnH/editor.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        lab_panel = factory.image_label(frame, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)

        dc_rate = DecadeControl(frame, "shRate", editor,
                                coarse = (0.01, 10), limit = (0.01,99))
        dc_srcfreq = DecadeControl(frame, "srcFreq", editor,
                                   coarse = (0.01, 10), limit = (0.01,99))
        s_src = cf.normalized_slider(frame, "srcSelect", editor)
        s_lag = cf.normalized_slider(frame, "shLag", editor)
        s_bleed = cf.normalized_slider(frame, "shBleed", editor)
        sx_delay = ExpSlider(frame, "shDelay", editor, range_=4)
        sx_attack = ExpSlider(frame, "shAtack", editor, range_=4)
        sx_hold = ExpSlider(frame, "shHold", editor, range_=4)
        sx_release = ExpSlider(frame, "shRelease", editor, range_=4)
        sr_scale = ReciprocalSlider(frame, "shScale", editor, range_=4, degree=1)
        s_bias = cf.linear_slider(frame, "shBias", editor, range_=(-4,4))
        
        self.add_control("shRate", dc_rate)
        self.add_control("srcFreq", dc_srcfreq)
        self.add_control("srcSelect", s_src)
        self.add_control("shLag", s_lag)
        self.add_control("shBleed", s_bleed)
        self.add_control("shDelay", sx_delay)
        self.add_control("shAttack", sx_attack)
        self.add_control("shHold", sx_hold)
        self.add_control("shRelease", sx_release)
        self.add_control("shScale", sr_scale)
        self.add_control("shBias", s_bias)
        
        y0 = 90
        x0 = 90
        x_rate = x0
        x_srcfreq = x_rate + 120
        x_src = x_srcfreq + 140
        x_lag = x_src + 60
        x_delay = x_lag + 90
        x_attack = x_delay + 60
        x_hold = x_attack + 60
        x_release = x_hold + 60
        x_bleed = x_release + 60
        x_scale = x_bleed + 90
        x_bias = x_scale + 75
        
        dc_rate.layout(offset=(x_rate, y0), label_offset=(0, 100),
                       slider_offset = (80, 0, 14, 200))
        dc_srcfreq.layout(offset=(x_srcfreq, y0), label_offset=(0,100),
                          slider_offset = (80, 0, 14, 200))
        s_src.widget().place(x=x_src, y=y0, height=200)
        s_lag.widget().place(x=x_lag, y=y0, height=200)
        sx_delay.layout(offset=(x_delay, y0), height=200, checkbutton_offset=None)
        sx_attack.layout(offset=(x_attack, y0), height=200, checkbutton_offset=None)
        sx_hold.layout(offset=(x_hold, y0), height=200, checkbutton_offset=None)
        sx_release.layout(offset=(x_release, y0), height=200, checkbutton_offset=None)
        s_bleed.widget().place(x=x_bleed, y=y0, height=200)
        sr_scale.layout(offset=(x_scale, y0), height=200,
                        sign_offset=None,
                        invert_offset=(-4, -23))
        s_bias.widget().place(x=x_bias, y=y0, height=200)
