# llia.synths.formant.tk.editor

from __future__ import print_function
from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import ToggleButton
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.tumbler import Tumbler

def create_editor(parent):
    TkFormantPanel(parent)

class TkFormantPanel(TkSubEditor):

    NAME = "Formant"
    IMAGE_FILE = "resources/Formant/editor.png"
    TAB_FILE = "resources/Formant/tab.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 1000, 700, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        y0 = 75
        yfreq = y0
        ygain = yfreq+50
        yq = ygain+180
        y_enable = yq+180
        x0 = 75
        x_shelf = x0
        def tumbler(param,x,y=yfreq):
            t = Tumbler(canvas,param,editor,digits=5,scale=1)
            self.add_control(param,t)
            t.layout((x,y))
            return t
        def q_slider(param,x,y=yq):
            s = cf.linear_slider(canvas,param,editor,range_=(1.0, 0.0))
            self.add_control(param,s)
            s.widget().place(x=x,y=y)
            return s
        def gain_slider(param,x,y=ygain):
            s = cf.linear_slider(canvas,param,editor,range_=(-36,36))
            self.add_control(param,s)
            s.widget().place(x=x,y=y)
            return s
        tumbler("hp",x_shelf,y=y0)
        tumbler("lp",x_shelf,y=y0+60)
        for i in (1,2,3,4):
            x = x_shelf + i*100
            tumbler("f%d" % i, x+6)
            gain_slider("gain%d" % i,x+37)
            q_slider("q%d" % i, x+37)
            p_enable = "enable%d" % i
            m_enable = ToggleButton(canvas,p_enable,editor,text=("Mute","On"))
            self.add_control(p_enable,m_enable)
            m_enable.layout((x+14, y_enable))
            m_enable.update_aspect()
        x_bleed = x + 150
        s = cf.normalized_slider(canvas,"bleed",editor)
        self.add_control("bleed",s)
        s.widget().place(x=x_bleed,y=ygain,height=150)
        x_amp = x_bleed+60
        gs = cf.linear_slider(canvas,"amp",editor,range_=(-12,12))
        self.add_control("amp",gs)
        gs.widget().place(x=x_amp, y=ygain)
                         
            
        
        

