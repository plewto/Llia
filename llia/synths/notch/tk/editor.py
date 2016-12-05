# llia.synths.notch.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
from llia.gui.tk.expslider import ExpSlider
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.tumbler import Tumbler

def create_editor(parent):
    TkNotchPanel(parent)

class TkNotchPanel(TkSubEditor):

    NAME = "Notch"
    IMAGE_FILE = "resources/Notch/editor.png"
    TAB_FILE = "resources/Notch/tab.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 660, 360, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        y0 = 75
        x0 = 75
        self.exp_slider("cFreq",20000,x0,y0,degree=3)
        self.exp_slider("cFreqLfo",2000,x0+60,y0,degree=3)
        self.exp_slider("cFreqX",2000,x0+120,y0,degree=3)
        x_res = x0+210
        self.exp_slider("q", 100,x_res,y0,degree=3)
        self.exp_slider("qLfo",100,x_res+60,y0,degree=3)
        self.exp_slider("qX", 100,x_res+120,y0,degree=3)
        x_out = x_res+210
        self.linear_slider("filterGain",(-12,12),x_out,y0)
        self.norm_slider("bleed",x_out+60,y0)
        self.tumbler("lfoFreq",5,0.001,x0,y0+180)
            
            
