# llia.synths.flngr2.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.synths.flngr2.flngr2_constants import *


def create_editor(parent):
    TkFlngr2Panel(parent)

class TkFlngr2Panel(TkSubEditor):

    NAME = "Flngr2"
    IMAGE_FILE = "resources/Flngr2/editor.png"
    TAB_FILE = "resources/Flngr2/tab.png"

    def __init__(self,editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,736,604,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.NAME)
        editor.add_child_editor(self.NAME, self)
        x0 = 75
        xlfo = x0+180
        xmix = xlfo + 320
        y0=75
        y1=340
        for n,y in ((1,y0),(2,y1)):
            def param(prefix):
                return "%s%d" % (prefix,n)
            self.linear_slider(param("delay"),(0,0.01),x0,y)
            self.exp_slider(param("depth"),1.0,x0+60,y)
            self.exp_slider(param("xmod"),1.0,x0+120,y)
            msb = self.msb(param("lfoRatio"),len(LFO_RATIOS),xlfo,y)
            for i,pair in enumerate(LFO_RATIOS):
                val,text = pair
                self.msb_aspect(msb,i,val,text=text)
            msb.update_aspect()
            self.linear_slider(param("feedback"),(-1,1),xlfo+100,y)
            self.linear_slider(param("xfeedback"),(-1,1),xlfo+160,y)
            self.exp_slider(param("lowpass"),16000,xlfo+220,y)
            self.volume_slider(param("dryMix"),xmix,y,height=100)
            self.linear_slider(param("dryPan"),(-1,1),xmix,y+130,height=75)
            self.volume_slider(param("efxMix"),xmix+60,y,height=100)
            self.linear_slider(param("efxPan"),(-1,1),xmix+60,y+130,height=75)
        self.tumbler("timebase",5,0.001,xlfo-7,y0+100)
