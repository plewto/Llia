# llia.synths.cascade.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.tumbler import Tumbler
from llia.gui.tk.msb import MSB, ToggleButton



# clkfreq : 1.000,          # float, tumbler (0,99.999)
# clksrc : 0,               # int toggle (0=interna;,1=external)
# hold : 1.0,               # float, tumbler (0,99.999) ?

# amp1 : 1.00,              # float, norm
# amp2 : 1.00,
# amp3 : 1.00,
# amp4 : 1.00,
# amp5 : 1.00,
# amp6 : 1.00,

# gate1 : 0,                # int, toggle (0=off, 1=gate)
# gate2 : 0,
# gate3 : 0,
# gate4 : 0,
# gate5 : 0,
# gate6 : 0,

# n : 8,                    # int, msb (7,32)
# ampn : 1.00,
# gaten : 0,

# scale : 1.0,              # float, norm
# bias : 0,                 # float linear (-4,+4)
# lag : 0.0}                # float norm


def create_editor(parent):
    TkCascadePanel(parent)


class TkCascadePanel(TkSubEditor):

    NAME = "Cascade"
    IMAGE_FILE = "resources/Cascade/editor.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1000,600,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)

        def tumbler(param,x,y):
            t = Tumbler(canvas,param,editor,digits=5,scale=0.001,
                        foreground="#c8cbec",
                        outline="#c8cbec",
                        fill="#222228")
            self.add_control(param,t)
            t.layout((x,y))
            return t

        def toggle(param,text,x,y):
            tog = ToggleButton(canvas,param,editor,text,
                               fill="#222228",
                               foreground="#c8cbec",
                               outline="#c8cbec",
                               selected_fill="#140033",
                               selected_foreground="#00bfa9")
            self.add_control(param,tog)
            tog.layout((x,y))
            tog.update_aspect()
            return tog

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

        y0 = 75
        x0 = 75
        x1 = x0 + 160
        xdelta = 75
        x_tog_offset = -23
        y_tog_offset = 160
        tumbler("clkfreq",x0,y0)
        toggle("clksrc",["Internal","External"],x0+7,y0+40)
        tumbler("hold",x0,y0+160)
        b_half_hold = factory.button(canvas,"1/2",self.half_hold_callback)
        b_half_hold.place(x=x0+13,y=y0+194)


        
        for i in range(6):
            j = i+1
            x = x1 + i*xdelta
            s = norm("amp%d"%j,x,y0)
            t = toggle("gate%d"%j,["On","Gate"],x+x_tog_offset,y0+y_tog_offset)

        xn = x + xdelta
        norm("ampn",xn,y0)
        toggle("gaten",["On","Gate"],xn+x_tog_offset,y0+y_tog_offset)
    
        y_tumbler_n = y0+y_tog_offset
        tumbler_n = Tumbler(canvas,"n",editor,digits=2,scale=1)
        self.add_control("n",tumbler_n)
        tumbler_n.layout((xn-8,y_tumbler_n+40))
        xlag = x+170
        xscale = xlag+60
        xbias = xscale+60
        norm("lag",xlag,y0)
        norm("scale",xscale,y0)
        linear_slider("bias",(-4,4),xbias,y0)


    def half_hold_callback(self):
        prog = self.synth.bank()[None]
        try:
            period = 1.0/prog["clkfreq"]
            prog["hold"] = period/2
            self.sync()
        except DivisionByZeroError:
            pass
