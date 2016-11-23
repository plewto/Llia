# llia.synths.fm2.tk.lfo_editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.tumbler import Tumbler
from llia.synths.fm2.fm2_constants import *


class TkFm2LfoPanel(TkSubEditor):

    NAME = "LFO"
    IMAGE_FILE = "resources/FM2/lfo_editor.png"
    TAB_FILE = "resources/Tabs/lfo.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 626, 562,self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        y0 = 50
        x0 = 50
        x_delay = x0+90
        x_sens = x_delay+60
        x_depth = x_sens+60
        x_xpitch = x_depth+90
        x_xmod = x_xpitch+60
        x_amp = x_xmod+90
        def tumbler(param,digits,scale,x,y):
            t = Tumbler(canvas,param,editor,digits=digits,scale=scale)
            self.add_control(param,t)
            t.layout((x,y))
            return y
        def norm_slider(param,x,y,height=150):
            s = cf.normalized_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y,height=height)
            return s
        def linear_slider(param,range_,x,y,height=150):
            s = cf.linear_slider(canvas,param,editor,range_=range_)
            self.add_control(param,s)
            s.widget().place(x=x,y=y,height=height)
            return s
        def volume_slider(param,x,y):
            s = cf.volume_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y)
            return s
        tumbler("lfoFreq",5,0.001,x0,y0)
        linear_slider("lfoDelay",(0,4),x_delay,y0)
        norm_slider("vsens",x_sens,y0)
        norm_slider("vdepth",x_depth,y0)
        norm_slider("xPitch",x_xpitch,y0)
        norm_slider("xModDepth",x_xmod,y0)
        volume_slider("amp",x_amp,y0)
            
