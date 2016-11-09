# llia.synths.cutil.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB
from llia.gui.tk.tumbler import Tumbler

def create_editor(parent):
    TkCUtilPanel(parent)

class TkCUtilPanel(TkSubEditor):

    NAME = "CUtil"
    IMAGE_FILE = "resources/CUtil/editor.png"
    TAB_FILE = "resources/Tabs/util.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 700, 250, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)

        y0 = 100
        ymsb = y0
        ytumbler = y0
        ylag = y0-18

        x0 = 75
        xwave = x0+25
        xpol = xwave + 100
        xclip = xpol + 100
        xlag = xclip + 100
        xscale = xlag + 50
        xbias = xscale + 100
        
        cfill = "black"
        cforeground = "white"
        coutline = "white"
        
        def norm_slider(param,x,y):
            s = cf.normalized_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y, width=10, height=75)
            return s

        # def volume_slider(param,x):
        #     s = cf.volume_slider(canvas,param,editor)
        #     self.add_control(param,s)
        #     s.widget().place(x=x,y=y0)
        #     return s

        # def linear_slider(param,range_,x):
        #     s = cf.linear_slider(canvas,param,editor,range_=range_)
        #     self.add_control(param,s)
        #     s.widget().place(x=x,y=y0)
        #     return s

        def tumbler(param,x,y):
            t = Tumbler(canvas,param,editor,digits=3,scale = 0.01,sign=True)
            self.add_control(param,t)
            t.layout((x,y))
            t.update_aspect()
            return t
        
        WAVES = ("off","abs","cube")
        msb_wave = MSB(canvas,"wave",editor,len(WAVES))
        for i,w in enumerate(WAVES):
            d = {"fill":cfill,
                 "foreground":cforeground,
                 "outline":coutline,
                 "value":i,
                 "text":w}
            msb_wave.define_aspect(i,i,d)
        self.add_control("wave",msb_wave)
        msb_wave.layout((xwave,ymsb))
        msb_wave.update_aspect()

        POLS = ("off","->bipolar","->polar")
        msb_pol = MSB(canvas,"polarityComp",editor,len(POLS))
        for i,w in enumerate(POLS):
            d = {"fill":cfill,
                 "foreground":cforeground,
                 "outline":coutline,
                 "value":i,
                 "text":w}
            msb_pol.define_aspect(i,i,d)
        self.add_control("polarityComp",msb_pol)
        msb_pol.layout((xpol,ymsb))
        msb_pol.update_aspect()

        tumbler("clipMax",xclip,ytumbler-10)
        tumbler("clipMin",xclip,ytumbler+14)
        norm_slider("lag",xlag,ylag)
        tumbler("scale",xscale,ytumbler)
        tumbler("bias",xbias,ytumbler)
