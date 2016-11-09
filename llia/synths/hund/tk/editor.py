# llia.synths.hund.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB, ToggleButton
from llia.gui.tk.tumbler import Tumbler
from llia.synths.hund.hund_data import FILTER_FREQUENCIES,GAINS

def create_editor(parent):
    TkHundPanel(parent)

class TkHundPanel(TkSubEditor):

    NAME = "Hund"
    IMAGE_FILE = "resources/Hund/editor.png"
    TAB_FILE = "resources/Hund/tab.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 760, 708,self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)

        y0 = 50
        x0 = 75

        xres = x0+75
        xenv = xres+90
        xattack = xenv+75
        xxmod = xattack+208
        xout = xxmod+90

        def norm_slider(param,x):
            s = cf.normalized_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y0)
            return s

        def volume_slider(param,x): # auto build indent, mover 1->
            s = cf.volume_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y0)
            return s

        def linear_slider(param,range_,x): # auto build indent, mover 1->
            s = cf.linear_slider(canvas,param,editor,range_=range_) # auto build missing closing )
            self.add_control(param,s)
            s.widget().place(x=x,y=y0)
            return s

        def bipolar_slider(param,x):
            return linear_slider(param,(-1.0,+1.0),x)
        
        cfill = "black"
        cforeground="#aae1aa"
        coutline="blue"
        
        msb_filter = MSB(canvas,"filterFreq",editor,len(FILTER_FREQUENCIES))
        for i,ff in enumerate(FILTER_FREQUENCIES):
            d = {"value":int(ff),
                 "fill" : cfill,
                 "foreground" : cforeground,
                 "outline" : coutline,
                 "text" : str(ff)}
            msb_filter.define_aspect(i,ff,d)
        self.add_control("filterFreq",msb_filter)
        msb_filter.layout((x0,y0))
        msb_filter.update_aspect()

        msb_gain = MSB(canvas,"pregain",editor,len(GAINS))
        for i,g in enumerate(GAINS):
            val,tx = g
            d = {"value":float(val),
                 "fill" : cfill,
                 "foreground" : cforeground,
                 "outline" : coutline,
                 "text" : tx}
            msb_gain.define_aspect(i,float(val),d)
        self.add_control("pregain",msb_gain)
        msb_gain.layout((xenv,y0))
        msb_gain.update_aspect()
        norm_slider("res",xres)
        linear_slider("attack",(0.01,4.0),xattack)
        linear_slider("release",(0.01,4.0),xattack+60)
        bipolar_slider("modDepth",xattack+120)
        bipolar_slider("xmod",xxmod)
        volume_slider("dryamp",xout)
        volume_slider("wetamp",xout+60)
