# llia.synths.carnal2.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.synths.carnal2.carnal2_constants import *

def create_editor(parent):
    TkCarnal2Panel(parent)

class TkCarnal2Panel(TkSubEditor):

    NAME = "Carnal2"
    IMAGE_FILE = "resources/Carnal2/editor.png"
    TAB_FILE = "resources/Carnal2/tab.png"

    def __init__(self,editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1000,700,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.NAME)
        editor.add_child_editor(self.NAME, self)
        x0 = 75
        xmod = x0+100
        xfb = xmod+130
        xclip = xfb+240
        xmix = xclip+130
        y0 = 75
        y1 = 340
        for n,y in ((1,y0),(2,y1)):
            def param(prefix):
                return "%s%d" % (prefix,n)
            self.tumbler(param("delayTime"),4,0.0001,x0,y)
            msb = self.msb(param("lfoRatio"),len(LFO_RATIOS),x0-7,y+60)
            for i,pair in enumerate(LFO_RATIOS):
                value,text = pair
                self.msb_aspect(msb,i,value,text=text)
            msb.update_aspect()
            self.norm_slider(param("modDepth"),xmod,y)
            self.norm_slider(param("xmodDepth"),xmod+60,y)
            self.linear_slider(param("feedback"),(-1,1),xfb,y)
            self.linear_slider(param("xfeedback"),(-1,1),xfb+60,y)
            self.exp_slider(param("lowcut"),16000,xfb+120,y,degree=3)
            self.exp_slider(param("highcut"),16000,xfb+180,y,degree=3)
            self.toggle(param("clipEnable"),xclip,y,off=(0,"Off"),on=(1,"On"))
            self.linear_slider(param("clipGain"),(0,4),xclip,y+60,height=100)
            self.norm_slider(param("clipThreshold"),xclip+47,y+60,height=100)
            self.volume_slider(param("dryMix"),xmix,y,height=100)
            self.linear_slider(param("dryPan"),(-1,1),xmix,y+130, height=75)
            self.volume_slider(param("efxMix"),xmix+60,y,height=100)
            self.linear_slider(param("efxPan"),(-1,1),xmix+60,y+130, height=75)
        self.tumbler("timebase",5,0.001,x0-14,y1+190)
