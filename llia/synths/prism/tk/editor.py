# llia.synths.prism.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.msb import MSB
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf

from llia.gui.tk.tumbler import Tumbler

def create_editor(parent):
    TkPrismPanel(parent)

class TkPrismPanel(TkSubEditor):

    NAME = "Prism"
    IMAGE_FILE = "resources/Prism/editor.png"
    TAB_FILE = "resources/Prism/tab.png"


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
        y1 = y0+180
        x0 = 75
        xlow = x0
        xcenter = xlow+54
        xhigh = xcenter+100
        def gain_slider(param,x):
            range_ = (-12,12)
            s = cf.linear_slider(canvas,param,editor,range_=range_)
            self.add_control(param,s)
            s.widget().place(x=x,y=y1,height=125)
            return s
        def frequency_slider(param,x):
            s = ExpSlider(canvas,param,editor,range_=20000,degree=3)
            self.add_control(param,s)
            s.layout((x,y0),checkbutton_offset=None)
            return s
        frequency_slider("fLow",xlow)
        frequency_slider("fHigh",xhigh)
        bwscales = ((0.333, "1/3"),(0.667,"2/3"),(1.000, "1"),
                    (1.333, "1 1/3"),(1.667, "1 2/3"),(2.00, "2"))
        param="bwScale"
        m = MSB(canvas,param,editor,len(bwscales))
        for i,p in enumerate(bwscales):
            v,txt = p
            if v >= 1:
                cfill = "green"
            else:
                cfill = "red"
            d = {"fill" : "black",
                 "foreground" :  cfill,
                 "outline" : "gray",
                 "value" : v,
                 "text" : txt}
            m.define_aspect(i,v,d)
        m.layout((xcenter,y0+50))
        m.update_aspect()
        gain_slider("gainLow",xlow)
        gain_slider("gainCenter",xcenter+23)
        gain_slider("gainHigh",xhigh)
        
        
