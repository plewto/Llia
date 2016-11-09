# llia.synths.lfo2.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.tumbler import Tumbler
from llia.synths.lfo2.lfo2_data import RATIOS

def create_editor(parent):
    TkLfo2Panel(parent)


class TkLfo2Panel(TkSubEditor):

    NAME = "LFO 2"
    IMAGE_FILE = "resources/LFO2/editor.png"
    TAB_FILE = "resources/Tabs/lfo.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1000,600,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        tumbler = Tumbler(canvas,"clkFreq",editor,digits=5, scale=0.001)
        s_clk_pw = cf.normalized_slider(canvas, "clkPw", editor)
        s_saw_ratio = cf.discrete_slider(canvas, "sawRatio", editor,
                                         values = RATIOS)
        s_saw_slew = cf.normalized_slider(canvas, "sawSlew", editor)
        s_saw_amp = cf.linear_slider(canvas, "sawAmp", editor, range_=(0,4))
        s_saw_bleed = cf.normalized_slider(canvas, "sawBleed", editor)
        s_saw_bias = cf.linear_slider(canvas, "sawBias", editor, range_=(-4,4))
        s_pulse_ratio = cf.discrete_slider(canvas, "pulseRatio", editor,
                                           values = RATIOS)
        s_pulse_width = cf.normalized_slider(canvas, "pulseWidth", editor)
        s_pulse_amp = cf.linear_slider(canvas, "pulseAmp", editor, range_=(0,4))
        s_pulse_bleed = cf.normalized_slider(canvas, "pulseBleed", editor)
        s_pulse_bias = cf.linear_slider(canvas, "pulseBias", editor, range_=(-4,4))
        s_lag = cf.normalized_slider(canvas, "lag", editor)
        self.add_control("clkFreq", tumbler)
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
        tumbler.layout((x0+5,y0+30))
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
