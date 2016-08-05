# llia.synths.lfo1.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.decade_control import DecadeControl

def create_editor(parent):
    panel1 = TkLfo1Panel(parent)

# class TkLfo1Panel(TkSubEditor):
#
#     NAME = "LFO1"
#     IMAGE_FILE = "resources/LFO1/editor.png"
#
#     def __init__(self, editor):
#         frame = editor.create_tab(self.NAME)
#         frame.config(background=factory.bg())
#         TkSubEditor.__init__(self, frame, editor, self.NAME)
#         editor.add_child_editor(self.NAME, self)
#         lab_panel = factory.image_label(frame, self.IMAGE_FILE)
#         lab_panel.pack(anchor="nw", expand=False)
#         y0 = 60
#         x0 = 60
#         x1 = x0 + 120
#         xenv = x1 + 90
#         xdelay = xenv
#         xattack = xdelay + 60
#         xhold = xattack + 60
#         xrelease = xhold + 60
#         xbias = xrelease + 90
#         xscale = xbias + 60
#         xamp = xscale + 60
#         dc_freq = DecadeControl(frame, "lfoFreq", editor,
#                                 coarse = (0.01, 10),
#                                 limit = (0.01, 100))
#         s_wave = cfactory.normalized_slider(frame, "lfoWave", editor)
#         s_delay = ExpSlider(frame, "lfoDelay", editor, range_=15)
#         s_attack = ExpSlider(frame, "lfoAttack", editor, range_=15)
#         s_hold = ExpSlider(frame, "lfoHold", editor, range_=15)
#         s_release = ExpSlider(frame, "lfoRelease", editor, range_=15)
#         s_bias = cfactory.linear_slider(frame, "lfoBias", editor, range_=(-2,2))
#         s_scale = ExpSlider(frame, "lfoScale", editor, range_=2)
#         s_amp = cfactory.normalized_slider(frame, "lfoAmp", editor)
#         self.add_control("lfoFreq", dc_freq)
#         self.add_control("lfoWave", s_wave)
#         self.add_control("lfoDelay", s_delay)
#         self.add_control("lfoAttack", s_attack)
#         self.add_control("lfoHold", s_hold)
#         self.add_control("lfoRelease", s_release)
#         self.add_control("lfoBias", s_bias)
#         self.add_control("lfoScale", s_scale)
#         self.add_control("lfoAmp", s_amp)
#         dc_freq.layout(offset=(x0, y0), label_offset = (10,100))
#         s_wave.widget().place(x=x1+15, y=y0)
#         s_delay.layout(offset=(xdelay, y0), checkbutton_offset = None)
#         s_attack.layout(offset=(xattack, y0), checkbutton_offset = None)
#         s_hold.layout(offset=(xhold, y0), checkbutton_offset = None)
#         s_release.layout(offset=(xrelease, y0), checkbutton_offset = None)
#         s_bias.widget().place(x=xbias, y=y0)
#         s_scale.layout(offset=(xscale, y0), checkbutton_offset=None)
#         s_amp.widget().place(x=xamp, y=y0)

class TkLfo1Panel(TkSubEditor):

    NAME = "LFO1"
    IMAGE_FILE = "resources/LFO1/editor.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        lab_panel = factory.image_label(frame, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)

        dc_freq = DecadeControl(frame, "lfoFreq", editor,
                                coarse = (0.01, 10),
                                limit = (0.01, 100))
        s_feedback = cf.normalized_slider(frame, "lfoFeedback", editor)
        s_delay = ExpSlider(frame, "lfoDelay", editor, range_=8)
        s_attack = ExpSlider(frame, "lfoAttack", editor, range_=8)
        s_hold = ExpSlider(frame, "lfoHold", editor, range_=8)
        s_release = ExpSlider(frame, "lfoRelease", editor, range_=8)
        s_bleed = cf.normalized_slider(frame, "lfoBleed", editor)
        s_scale = cf.linear_slider(frame, "lfoScale", editor, range_=(0.25,4))
        s_bias = cf.linear_slider(frame, "lfoBias", editor, range_=(-2,2))

        self.add_control("lfoFreq",dc_freq)
        self.add_control("lfoFeedback",s_feedback)
        self.add_control("lfoDelay",s_delay)
        self.add_control("lfoAttack",s_attack)
        self.add_control("lfoHold",s_hold)
        self.add_control("lfoRelease",s_release)
        self.add_control("lfoBleed",s_bleed)
        self.add_control("lfoScale",s_scale)
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

        
        dc_freq.layout(offset=(x_freq,y0),
                       slider_offset=(80,0,14,200),
                       label_offset = (10, 150))
        s_feedback.widget().place(x=x_fb,y=y0, height=200)
        s_delay.layout(offset=(x_delay,y0),height=200,checkbutton_offset=None)
        s_attack.layout(offset=(x_attack,y0),height=200,checkbutton_offset=None)
        s_hold.layout(offset=(x_hold,y0),height=200,checkbutton_offset=None)
        s_release.layout(offset=(x_release,y0),height=200,checkbutton_offset=None)
        s_bleed.widget().place(x=x_bleed,y=y0, height=200)
        s_scale.widget().place(x=x_scale,y=y0, height=200)
        s_bias.widget().place(x=x_bias,y=y0, height=200)
