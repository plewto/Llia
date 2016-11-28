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
        def norm_slider(param,x):
            s = cf.normalized_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y0)
            return s
        def linear_slider(param,range_,x):
            s = cf.linear_slider(canvas,param,editor,range_=range_)
            self.add_control(param,s)
            s.widget().place(x=x,y=y0)
            return s
        def exp_slider(param,range_,x,degree=2):
            s = ExpSlider(canvas,param,editor,range_=range_,degree=degree)
            self.add_control(param,s)
            s.layout((x,y0),checkbutton_offset=None)
            return s
        exp_slider("cFreq",20000,x0,degree=3)
        exp_slider("cFreqLfo",2000,x0+60,degree=3)
        exp_slider("cFreqX",2000,x0+120,degree=3)
        x_res = x0+210
        exp_slider("q", 100,x_res,degree=3)
        exp_slider("qLfo",100,x_res+60,degree=3)
        exp_slider("qX", 100,x_res+120,degree=3)
        x_out = x_res+210
        linear_slider("filterGain",(-12,12),x_out)
        norm_slider("bleed",x_out+60)
        t = Tumbler(canvas,"lfoFreq",editor,digits=5,scale=0.001)
        self.add_control("lfoFreq",t)
        t.layout((x0,y0+180))
        
            
            
