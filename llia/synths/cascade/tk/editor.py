# llia.synths.cascade.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.tumbler import Tumbler
from llia.gui.tk.msb import MSB, ToggleButton

def create_editor(parent):
    TkCascadePanel(parent)

class TkCascadePanel(TkSubEditor):

    NAME = "Cascade"
    IMAGE_FILE = "resources/Cascade/editor.png"
    TAB_FILE = "resources/Cascade/tab.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1000,600,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        y0 = 75
        x0 = 75
        x1 = x0 + 160
        xdelta = 75
        x_tog_offset = -23
        y_tog_offset = 160
        self.tumbler("hold",5,0.001,x0,y0+160)
        self.tumbler("clkfreq",5,0.001,x0,y0)
        self.toggle("clksrc",x0+7,y0+40,
                    off = (0, "Internal"),
                    on = (1, "External"))
        b_half_hold = factory.button(canvas,"1/2",self.half_hold_callback)
        b_half_hold.place(x=x0+13,y=y0+194)
        for i in range(6):
            j = i+1
            x = x1 + i*xdelta
            self.norm_slider("amp%d"%j,x,y0)
            self.toggle("gate%d"%j,x+x_tog_offset,y0+y_tog_offset,
                        off = [0,"On"],
                        on = [1,"Gate"])
        xn = x + xdelta
        self.norm_slider("ampn",xn,y0)
        self.toggle("gaten",xn+x_tog_offset,y0+y_tog_offset,
                    off = [0,"On"],
                    on = [1,"Gate"])
        y_tumbler_n = y0+y_tog_offset
        self.tumbler("n",2,1,xn-8,y_tumbler_n+40)
        xlag = x+170
        xscale = xlag+60
        xbias = xscale+60
        self.norm_slider("lag",xlag,y0)
        self.norm_slider("scale",xscale,y0)
        self.linear_slider("bias",(-4,4),xbias,y0)

    def half_hold_callback(self):
        prog = self.synth.bank()[None]
        try:
            period = 1.0/prog["clkfreq"]
            prog["hold"] = period/2
            self.sync()
        except DivisionByZeroError:
            pass
