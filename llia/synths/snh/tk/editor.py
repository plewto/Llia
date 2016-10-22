# llia.synths.snh.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.tumbler import Tumbler
from llia.gui.tk.msb import ToggleButton


def create_editor(parent):
    TkSnHPanel(parent)


class TkSnHPanel(TkSubEditor):

    NAME = "SnH"
    IMAGE_FILE = "resources/SnH/editor.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        canvas=factory.canvas(frame,696,361,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)

        y0 = 75
        x0 = 100
        xmix = x0 + 150
        xsaw = xmix
        xnoise = xsaw+64
        xexternal = xnoise + 60
        xlag = xexternal+90
        
        def tumbler(param,x,y):
            t = Tumbler(canvas,param,editor,digits=5,scale=0.001,
                        outline='#a5a08a',
                        foreground='#a5a08a',
                        fill='black')
            self.add_control(param,t)
            t.layout((x,y))
            return y

        def norm(param,x):
            s = cf.normalized_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y0)
            return s

        def linear_slider(param,x,range_):
            s = cf.linear_slider(canvas,param,editor,range_=range_)
            self.add_control(param,s)
            s.widget().place(x=x,y=y0)
        
        tumbler("clockRate",x0,y0)
        tumbler("sawFreq",xsaw-30,y0+160)

        tog = ToggleButton(canvas,"clockSource",editor,
                           text=["Internal","External"],
                           fill='black',foreground='#007d47',
                           selected_fill='black',selected_foreground='#007d47')
        self.add_control("clockSource", tog)
        tog.layout((x0+8,y0+36))
        tog.update_aspect()
        norm("sawMix",xsaw)
        norm("noiseMix",xnoise)
        norm("externalMix",xexternal)
        norm("lag",xlag)
        norm("scale",xlag+60)
        linear_slider("bias",xlag+120,(-4,4))

