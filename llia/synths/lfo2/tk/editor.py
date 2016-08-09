# llia.synths.lfo2.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.decade_control import DecadeControl
from llia.gui.tk.reciprocal_slider import ReciprocalSlider
from llia.synths.lfo2.lfo2_data import RATIOS

def create_editor(parent):
    TkLfo2Panel(parent)


# clkFreq     - decade dontrol (0.01 .. 100)
# clkPw       - normal 
# clkAmp      - (ignore)

# sawRatio    - discreate harmonics
# sawSlew     - normal
# sawAmp      - linear (0 .. 4)
# sawBleed    - normal
# sawBias     - linear (-4 .. +4)

# pulseRatio  - discreate harmonics
# pulseWidth  - normal
# pulseAmp    - linerar (0 .. 4)
# pulseBleed  - normal
# pulseBias   - linear (-4 .. +4)

# lag         - normal



class TkLfo2Panel(TkSubEditor):

    NAME = "LFO 2"
    IMAGE_FILE = "resources/LFO2/editor.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        lab_panel = factory.image_label(frame, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)

        dc_clk_freq = DecadeControl(frame, "clkFreq", editor,
                                    coarse = (0.01, 10),
                                    limit = (0.01, 100))
        s_clk_pw = cf.normalized_slider(frame, "clkPw", editor)
        s_saw_ratio = cf.discrete_slider(frame, "sawRatio", editor,
                                         values = RATIOS)
        s_saw_slew = cf.normalized_slider(frame, "sawSlew", editor)
        s_saw_amp = cf.linear_slider(frame, "sawAmp", editor, range_=(0,4))
        s_saw_bleed = cf.normalized_slider(frame, "sawBleed", editor)
        s_saw_bias = cf.linear_slider(frame, "sawBias", editor, range_=(-4,4))

        s_pulse_ratio = cf.discrete_slider(frame, "pulseRatio", editor,
                                           values = RATIOS)
        s_pulse_width = cf.normalized_slider(frame, "pulseWidth", editor)
        s_pulse_amp = cf.linear_slider(frame, "pulseAmp", editor, range_=(0,4))
        s_pulse_bleed = cf.normalized_slider(frame, "pulseBleed", editor)
        s_pulse_bias = cf.linear_slider(frame, "pulseBias", editor, range_=(-4,4))
        s_lag = cf.normalized_slider(frame, "lag", editor)
        
        self.add_control("clkFreq", dc_clk_freq)
        self.add_control("clkPw", s_clk_pw)
        self.add_control("sawRatio", s_saw_ratio)
        self.add_control("sawSlew", s_saw_slew)
        self.add_control("sawAmp", s_saw_amp)
        self.add_control("sawBleed", s_saw_amp)
        self.add_control("sawBias", s_saw_bias)
        self.add_control("pulseRatio", s_pulse_ratio)
        self.add_control("pulseWidth", s_pulse_width)
        self.add_control("pulseAmp", s_pulse_amp)
        self.add_control("pulseBleed", s_pulse_amp)
        self.add_control("pulseBias", s_pulse_bias)
        self.add_control("lag", s_lag)

        
        y0 = 90
        x0 = 90
        x1 = x0 + 120

        xsaw = x1 + 90
        x2 = xsaw
        x3 = x2 + 60
        x4 = x3 + 60
        x5 = x4 + 60
        x6 = x5 + 60
        
        xpulse = x6 + 75
        x7 = xpulse
        x8 = x7 + 60
        x9 = x8 + 60
        x10 = x9 + 60
        x11 = x10 + 60

        xlag = x11 + 75
        
        dc_clk_freq.layout(offset=(x0,y0), slider_offset=(80, 0, 14, 200))
        s_clk_pw.widget().place(x=x1, y=y0, height=200)
        s_saw_ratio.widget().place(x=x2, y=y0, height=200)
        s_saw_slew.widget().place(x=x3, y=y0, height=200)
        s_saw_amp.widget().place(x=x4, y=y0, height=200)
        s_saw_bleed.widget().place(x=x5, y=y0, height=200)
        s_saw_bias.widget().place(x=x6, y=y0, height=200)
        s_pulse_ratio.widget().place(x=x7, y=y0, height=200)
        s_pulse_width.widget().place(x=x8, y=y0, height=200)
        s_pulse_amp.widget().place(x=x9, y=y0, height=200)
        s_pulse_bleed.widget().place(x=x10, y=y0, height=200)
        s_pulse_bias.widget().place(x=x11, y=y0, height=200)
        s_lag.widget().place(x=xlag, y=y0, height=200)
