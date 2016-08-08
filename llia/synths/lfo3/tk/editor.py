# llia.synths.lfo3.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.decade_control import DecadeControl
from llia.gui.tk.reciprocal_slider import ReciprocalSlider


def create_editor(parent):
    TkLfo3OscPanel(parent)
    TkLfo3CommonPanel(parent)
    

class TkLfo3CommonPanel(TkSubEditor):

    NAME = "LFO3 Common"
    IMAGE_FILE = "resources/LFO3/editor_common.png"

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
        xs_delay = ExpSlider(frame, "lfoDelay", editor, range_=8)
        xs_attack = ExpSlider(frame, "lfoAttack", editor, range_=8)
        xs_hold = ExpSlider(frame, "lfoHold", editor, range_=8)
        xs_release = ExpSlider(frame, "lfoRelease", editor, range_=8)
        self.add_control("lfoFreq", dc_freq)
        self.add_control("lfoDelay", xs_delay)
        self.add_control("lfoAttack", xs_attack)
        self.add_control("lfoHold", xs_hold)
        self.add_control("lfoRelease", xs_release)
        y0 = 90
        x0 = 90
        x_delay = x0 + 200
        x_attack = x_delay + 60
        x_hold = x_attack + 60
        x_release = x_hold + 60
        dc_freq.layout(offset=(x0,y0),
                       slider_offset = (80, 0, 14, 200),
                       label_offset=(4, 150))
        xs_delay.layout(offset=(x_delay, y0),height=200,
                        checkbutton_offset=None)
        
        xs_attack.layout(offset=(x_attack, y0),height=200,
                        checkbutton_offset=None)
        
        xs_hold.layout(offset=(x_hold, y0),height=200,
                        checkbutton_offset=None)
        
        xs_release.layout(offset=(x_release, y0),height=200,
                       checkbutton_offset=None)



class TkLfo3OscPanel(TkSubEditor):

    NAME = "LFO3"
    IMAGE_FILE = "resources/LFO3/editor_A.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        lab_panel = factory.image_label(frame, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)

        y0, y1 = 90, 360
        
        
        # LFO A
        dc_ratio_a = DecadeControl(frame, "rA", editor,
                                 coarse = (0.01, 10),
                                 limit = (0.01, 100))
        s_phase_a = cf.normalized_slider(frame, "phaseA", editor)
        xs_mod_a1 = ExpSlider(frame, "bToAFreq", editor, range_=16)
        s_bleed_a = cf.normalized_slider(frame, "bleedA", editor)
        rs_scale_a = ReciprocalSlider(frame, "scaleA", editor, range_=4)
        s_bias_a = cf.linear_slider(frame, "biasA", editor, range_=(-4,4))
        self.add_control("rA", dc_ratio_a)
        self.add_control("phaseA", s_phase_a)
        self.add_control("bToAFreq", xs_mod_a1)
        self.add_control("bleedA", s_bleed_a)
        self.add_control("scaleA", rs_scale_a)
        self.add_control("biasA", s_bias_a)
        
        xa = 90
        x_phase_a = xa + 140
        x_mod_a1 = x_phase_a + 60
        x_bleed_a = xa+80
        x_scale_a = x_bleed_a + 60
        x_bias_a = x_scale_a + 60
        
        dc_ratio_a.layout(offset=(xa,y0),
                         slider_offset = (80, 0, 14, 200))
        s_phase_a.widget().place(x=x_phase_a, y=y0, height=200)
        xs_mod_a1.layout(offset=(x_mod_a1, y0), height=200, checkbutton_offset=None)
        s_bleed_a.widget().place(x=x_bleed_a, y=y1, height=200)
        rs_scale_a.layout(offset=(x_scale_a, y1), height=200,
                         sign_offset = None,
                         invert_offset = (-4, -21))
        s_bias_a.widget().place(x=x_bias_a, y=y1, height=200)
        

        # LFO B
        dc_ratio_b = DecadeControl(frame, "rB", editor,
                                 coarse = (0.01, 10),
                                 limit = (0.01, 100))
        s_phase_b = cf.normalized_slider(frame, "phaseB", editor)
        xs_mod_b1 = ExpSlider(frame, "envToFreqB", editor, range_=16)
        xs_mod_b2 = ExpSlider(frame, "aToBFreq", editor, range_=16)
        s_mod_b3 = cf.normalized_slider(frame, "cToBAmp", editor)        
        s_bleed_b = cf.normalized_slider(frame, "bleedB", editor)
        rs_scale_b = ReciprocalSlider(frame, "scaleB", editor, range_=4)
        s_bias_b = cf.linear_slider(frame, "biasB", editor, range_=(-4,4))
        
        self.add_control("rB", dc_ratio_b)
        self.add_control("phaseB", s_phase_b)
        self.add_control("envToFreqB", xs_mod_b1)
        self.add_control("aToBFreq", xs_mod_b2)
        self.add_control("cToBAmp", s_mod_b3)
        self.add_control("bleedB", s_bleed_b)
        self.add_control("scaleB", rs_scale_b)
        self.add_control("biasB", s_bias_b)
        
        xb = x_bias_a + 60
        x_phase_b = xb + 140
        x_mod_b1 = x_phase_b + 60
        x_mod_b2 = x_mod_b1 + 60
        x_mod_b3 = x_mod_b2 + 60
        x_bleed_b = xb+80
        x_scale_b = x_bleed_b + 60
        x_bias_b = x_scale_b + 60
        
        dc_ratio_b.layout(offset=(xb,y0),
                         slider_offset = (80, 0, 14, 200))
        s_phase_b.widget().place(x=x_phase_b, y=y0, height=200)
        xs_mod_b1.layout(offset=(x_mod_b1, y0), height=200, checkbutton_offset=None)
        xs_mod_b2.layout(offset=(x_mod_b2, y0), height=200, checkbutton_offset=None)
        s_mod_b3.widget().place(x=x_mod_b3, y=y0, height=200)
        s_bleed_b.widget().place(x=x_bleed_b, y=y1, height=200)
        rs_scale_b.layout(offset=(x_scale_b, y1), height=200,
                         sign_offset = None,
                         invert_offset = (-4, -21))
        s_bias_b.widget().place(x=x_bias_b, y=y1, height=200)
        
        # LFO C
        dc_ratio_c = DecadeControl(frame, "rC", editor,
                                 coarse = (0.01, 10),
                                 limit = (0.01, 100))
        s_phase_c = cf.normalized_slider(frame, "phaseC", editor)
        s_mod_c1 = cf.normalized_slider(frame, "bToCAmp", editor)        
        s_bleed_c = cf.normalized_slider(frame, "bleedB", editor)
        rs_scale_c = ReciprocalSlider(frame, "scaleC", editor, range_=4)
        s_bias_c = cf.linear_slider(frame, "biasC", editor, range_=(-4,4))
        
        self.add_control("rC", dc_ratio_c)
        self.add_control("phaseC", s_phase_c)
        self.add_control("bToCAmp", s_mod_c1)

        self.add_control("bleedC", s_bleed_c)
        self.add_control("scaleC", rs_scale_c)
        self.add_control("biasC", s_bias_c)
        
        xc = x_mod_b3 + 60
        x_phase_c = xc + 140
        x_mod_c1 = x_phase_c + 60
        x_bleed_c = xc+80
        x_scale_c = x_bleed_c + 60
        x_bias_c = x_scale_c + 60
        
        dc_ratio_c.layout(offset=(xc,y0),
                         slider_offset = (80, 0, 14, 200))
        s_phase_c.widget().place(x=x_phase_c, y=y0, height=200)
        s_mod_c1.widget().place(x=x_mod_c1, y=y0, height=200)
        s_bleed_c.widget().place(x=x_bleed_c, y=y1, height=200)
        rs_scale_c.layout(offset=(x_scale_c, y1), height=200,
                         sign_offset = None,
                         invert_offset = (-4, -21))
        s_bias_c.widget().place(x=x_bias_c, y=y1, height=200)
        
