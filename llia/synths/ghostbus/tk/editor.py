# llia.synths.ghostbus.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import ToggleButton
from llia.synths.ghostbus.ghost_data import MAX_DELAY
from llia.gui.tk.tumbler import Tumbler

def create_editor(parent):
    TkGhostbusPanel(parent)

class TkGhostbusPanel(TkSubEditor):

    NAME = "Ghostbus"
    IMAGE_FILE = "resources/Ghostbus/editor.png"
    TAB_FILE = "resources/Ghostbus/tab.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 491, 708,self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        cfill = 'black'
        cforeground = '#d6dce6'
        cselected = cforeground
        def toggle(param,x,y):
            b = ToggleButton(canvas,param,editor,
                             fill=cfill,
                             foreground=cforeground,
                             outline=cforeground,
                             selected_fill = cfill,
                             selected_foreground = cselected)
            self.add_control(param,b)
            b.layout((x,y))
            b.update_aspect()
            return b

        def norm(param,x,y):
            s = cf.normalized_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y)
            return s

        def linear_slider(param,range_,x,y):
            s = cf.linear_slider(canvas,param,editor,range_=range_)
            self.add_control(param,s)
            s.widget().place(x=x,y=y)
            return s

        def scale_slider(param,x,y):
            return linear_slider(param,(0,4),x,y)

        def bias_slider(param,x,y):
            return linear_slider(param,(-4,4),x,y)

        def bipolar_slider(param,x,y):
            return linear_slider(param,(-1,1),x,y)

        y0 = 75
        yhp = y0+100
        x0 = 75
        xfb = x0+100
        xlag = xfb+60
        xscale = xlag+60
        xbias = xscale+60
        toggle("enableMod",x0,y0)
        toggle("enableHpA",x0,yhp)
        norm("lagA",xlag,y0)
        scale_slider("scaleA",xscale,y0)
        bias_slider("biasA",xbias,y0)
        y1 = y0+250
        yhp = y1+100
        t = Tumbler(canvas,"delay",editor,digits=4,scale=0.001,
                    fill=cfill,foreground=cforeground,outline=cforeground,
                    range_=(0,4000))
        self.add_control("delay",t)
        t.layout((x0,y1))
        toggle("enableHpDelay",x0,yhp)
        bipolar_slider("feedback",xfb,y1)
        norm("lagDelay",xlag,y1)
        scale_slider("scaleDelay",xscale,y1)
        bias_slider("biasDelay",xbias,y1)
        
        
        
