# llia.synths.lfo1.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.freq_spinner import FrequencySpinnerControl
from llia.gui.tk.reciprocal_slider import ReciprocalSlider


def create_editor(parent):
    panel1 = TkLfo1Panel(parent)


class TkLfo1Panel(TkSubEditor):

    NAME = "LFO1"
    IMAGE_FILE = "resources/LFO1/editor.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,852,550,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        spin_freq = FrequencySpinnerControl(canvas,"lfoFreq",editor,
                                            from_=0,to=1000)
        s_feedback = cf.normalized_slider(canvas, "lfoFeedback", editor)
        s_delay = ExpSlider(canvas, "lfoDelay", editor, range_=8)
        s_attack = ExpSlider(canvas, "lfoAttack", editor, range_=8)
        s_hold = ExpSlider(canvas, "lfoHold", editor, range_=8)
        s_release = ExpSlider(canvas, "lfoRelease", editor, range_=8)
        s_bleed = cf.normalized_slider(canvas, "lfoBleed", editor)
        sr_scale = ReciprocalSlider(canvas, "lfoScale", editor, range_=4, degree=1)
        s_bias = cf.linear_slider(canvas, "lfoBias", editor, range_=(-4,4))
        self.add_control("lfoFreq",spin_freq)
        self.add_control("lfoFeedback",s_feedback)
        self.add_control("lfoDelay",s_delay)
        self.add_control("lfoAttack",s_attack)
        self.add_control("lfoHold",s_hold)
        self.add_control("lfoRelease",s_release)
        self.add_control("lfoBleed",s_bleed)
        self.add_control("lfoScale",sr_scale)
        self.add_control("lfoBias",s_bias)
        y0 = 120
        x0 = 90
        x_freq = x0
        x_fb = x_freq + 142
        x_env = x_fb + 90
        x_delay = x_env
        x_attack = x_delay + 60
        x_hold = x_attack + 60
        x_release = x_hold + 60
        x_bleed = x_release + 90
        x_scale = x_bleed + 60
        x_bias = x_scale + 60
        spin_freq.layout(offset=(x_freq,y0))
        spin_freq.create_nudgetools(canvas,
                                    offset=(x_freq+9,y0+30),
                                    deltas=(100,10,1,0.1,0.01),
                                    constant=1,
                                    fill='#131313',
                                    outline='#a5a08a')
        s_feedback.widget().place(x=x_fb,y=y0, height=200)
        s_delay.layout(offset=(x_delay,y0),height=200,checkbutton_offset=None)
        s_attack.layout(offset=(x_attack,y0),height=200,checkbutton_offset=None)
        s_hold.layout(offset=(x_hold,y0),height=200,checkbutton_offset=None)
        s_release.layout(offset=(x_release,y0),height=200,checkbutton_offset=None)
        s_bleed.widget().place(x=x_bleed,y=y0, height=200)
        sr_scale.layout(offset=(x_scale, y0), height=200,
                        sign_offset=None,
                        invert_offset=(-4, -23))
        s_bias.widget().place(x=x_bias,y=y0, height=200)
