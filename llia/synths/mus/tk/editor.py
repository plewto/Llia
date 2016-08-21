# llia.synths.mus.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.reciprocal_slider import ReciprocalSlider

def create_editor(parent):
    TkMusPanel(parent)


class TkMusPanel(TkSubEditor):

    NAME = "Mus"
    IMAGE_FILE = "resources/Mus/editor.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        lab_panel = factory.image_label(frame, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)

        s_xmin = ReciprocalSlider(frame, "xmin", editor, range_=16, degree=1)
        s_xmax = ReciprocalSlider(frame, "xmin", editor, range_=16, degree=1)
        cb_xcurve = cf.ControlCheckbutton(frame, "xcurve", editor,
                                          text = "Exp", values = (0,1))
        s_xlag = cf.normalized_slider(frame, "xlag", editor)
        s_ymin = ReciprocalSlider(frame, "ymin", editor, range_=16, degree=1)
        s_ymax = ReciprocalSlider(frame, "ymin", editor, range_=16, degree=1)
        cb_ycurve = cf.ControlCheckbutton(frame, "ycurve", editor,
                                          text = "Exp", values = (0,1))
        s_ylag = cf.normalized_slider(frame, "ylag", editor)

        s_button_off = ReciprocalSlider(frame, "buttonOff", editor,
                                        range_=16, degree=1)
        s_button_on = ReciprocalSlider(frame, "buttonOn", editor,
                                       range_=16, degree=1)

        s_attack = ExpSlider(frame, "attack", editor, range_=6, degree=2)
        s_decay = ExpSlider(frame, "decay", editor, range_=6, degree=2)
        s_release = ExpSlider(frame, "release", editor, range_=6, degree=2)
        s_sustain = cf.normalized_slider(frame, "sustain", editor)
        s_envscale = cf.linear_slider(frame, "envScale", editor, range_=(-4, 4))
        s_envbias = cf.linear_slider(frame, "envBias", editor, range_=(-4, 4))
        
        self.add_control("xmin", s_xmin)
        self.add_control("xmax", s_xmax)
        self.add_control("xcurve", cb_xcurve)
        self.add_control("xlag", s_xlag)
        self.add_control("ymin", s_ymin)
        self.add_control("ymax", s_ymax)
        self.add_control("ycurve", cb_ycurve)
        self.add_control("ylag", s_ylag)
        self.add_control("buttonOff", s_button_off)
        self.add_control("buttonOn", s_button_on)
        self.add_control("attack", s_attack)
        self.add_control("decay", s_attack)
        self.add_control("sustain", s_attack)
        self.add_control("release", s_attack)
        self.add_control("envScale", s_envscale)
        self.add_control("envBias", s_envbias)
        

        y0, y1 = 90, 350
        x0 = 90
        x_lag = x0
        x_curve = x_lag - 8
        x_min = x_lag + 75
        x_max = x_min + 90

        x_button = x_max + 120

        x_env = x_button+120
        x_attack = x_env
        x_decay = x_attack + 60
        x_sustain = x_decay + 60
        x_release = x_sustain + 60
        
        
        s_xlag.widget().place(x=x_lag, y=y0)
        s_xmin.layout(offset=(x_min, y0),
                      sign_offset = (-24, -25),
                      invert_offset = (8, -25))
        s_xmax.layout(offset=(x_max, y0),
                      sign_offset = (-24, -25),
                      invert_offset = (8, -25))
        cb_xcurve.widget().place(x=x_curve, y=y0-25)


        s_ylag.widget().place(x=x_lag, y=y1)
        s_ymin.layout(offset=(x_min, y1),
                      sign_offset = (-24, -25),
                      invert_offset = (8, -25))
        s_ymax.layout(offset=(x_max, y1),
                      sign_offset = (-24, -25),
                      invert_offset = (8, -25))
        cb_ycurve.widget().place(x=x_curve, y=y1-25)


        s_button_off.layout(offset = (x_button, y0))
        s_button_on.layout(offset = (x_button, y1))

        s_attack.layout(offset=(x_attack, y0),
                        checkbutton_offset = None)
        s_decay.layout(offset=(x_decay, y0),
                        checkbutton_offset = None)
        s_release.layout(offset=(x_release, y0),
                        checkbutton_offset = None)
        s_sustain.widget().place(x=x_sustain, y=y0)

        s_envscale.widget().place(x=x_attack, y=y1)
        s_envbias.widget().place(x=x_decay, y=y1)
