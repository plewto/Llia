# llia.synths.saw3.tk.s3ed

from __future__ import print_function
from Tkinter import Frame

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.tumbler import Tumbler
from llia.synths.saw3.tk.s3filter import TkSaw3FilterPanel
from llia.gui.tk.tk_mutation_editor import TkMutationEditor

def create_editor(parent):
    panel1 = TkSaw3Panel1(parent)
    panel2 = TkSaw3FilterPanel(parent)
    panel4 = TkSaw3InfoPanel(parent)
    muteed = TkMutationEditor(parent)
    muteed.auto_allign()
    
class TkSaw3Panel1(TkSubEditor):

    NAME = "Saw3 Oscillators"
    IMAGE_FILE = "resources/Saw3/editor_osc.png"
    TAB_FILE = "resources/Saw3/tab_sine.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 1200, 600, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        y0 = 60
        y1 = 300
        yfreq_offset = 0
        ybias_offset = 100
        x0, xosc_offset = 50, 225
        x_wave_offset = 105
        x_amp_offset = x_wave_offset+60
        x_env1_wave_offset = x_wave_offset-60
        x_lfo_wave_offset = x_wave_offset
        x_env1_amp_offset = x_amp_offset
        for i, osc in enumerate(("osc1", "osc2", "osc3")):
            x = x0 + (i * xosc_offset)
            tumbler = Tumbler(canvas,osc+"Freq",editor,digits=5, scale=0.001)
            self.add_control(osc+"Freq", tumbler)
            tumbler.layout((x, y0+yfreq_offset))
            self.norm_slider(osc+"Wave", x+x_wave_offset, y0)
            self.volume_slider(osc+"Amp", x+x_amp_offset, y0)
            self.exp_slider(osc+"Wave_env1", x+x_env1_wave_offset, y1)
            self.exp_slider(osc+"Wave_lfo", x+x_lfo_wave_offset, y1)
            self.exp_slider(osc+"Amp_env1", x+x_env1_amp_offset, y1)
            xosc3 = x
        tumbler = Tumbler(canvas,"osc3Bias",editor,digits=5,scale=0.01)
        self.add_control("osc3Bias", tumbler)
        tumbler.layout((xosc3,y0+ybias_offset))
        self.norm_slider("osc3WaveLag", xosc3+x_wave_offset+25, y0, width=10, height=75)
        xnoise = xosc3 + xosc_offset + 30
        self.linear_slider("noiseFreq", xnoise, y0)
        self.volume_slider("noiseAmp", xnoise+60, y0)
        self.norm_slider("noiseBW", xnoise, y1)
        self.exp_slider("noiseAmp_env1", xnoise+60, y1)
        xpitch = xnoise+150
        self.linear_slider("port", xpitch, y0, range_=(0,2))
        self.norm_slider("xToPitch", xpitch, y1)

    def volume_slider(self, param, x, y, width=14, height=150):
        s = cf.volume_slider(self.canvas, param, self.editor)
        self.add_control(param, s)
        s.widget().place(x=x, y=y, width=width, height=height)
        return s

    def norm_slider(self, param, x, y, width=14, height=150):
        s = cf.normalized_slider(self.canvas, param, self.editor)
        self.add_control(param, s)
        s.widget().place(x=x, y=y, width=width, height=height)
        return s

    def linear_slider(self, param, x, y, range_=(0,8), width=14, height=150):
        s = cf.linear_slider(self.canvas, param, self.editor,
                             range_=range_)
        self.add_control(param, s)
        s.widget().place(x=x, y=y, width=width, height=height)
        return s

    def exp_slider(self, param, x, y, width=14, height=150, button_offset=(-5, -28)):
        s = ExpSlider(self.canvas, param, self.editor,
                      range_ = 1, degree=2)
        self.add_control(param, s)
        s.layout(offset=(x,y), width=width, height=height,
                 checkbutton_offset = button_offset)
        return s


    
class TkSaw3InfoPanel(object):

    NAME = "Saw3 Info"
    IMAGE_FILE = "resources/Saw3/editor_info.png"
    TAB_FILE = "resources/Saw3/tab_info.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        lab_panel = factory.image_label(frame, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)
        
    
