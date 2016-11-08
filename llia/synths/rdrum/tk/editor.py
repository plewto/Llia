# llia.synths.rdrum.tk.editor

from __future__ import print_function
from Tkinter import Frame

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.tumbler import Tumbler
from llia.gui.tk.expslider import ExpSlider


def create_editor(parent):
    TkRDrumPanel(parent)

class TkRDrumPanel(TkSubEditor):

    NAME = "RDrum"
    IMAGE_FILE = "resources/RDrum/editor.png"
    TAB_FILE = "resources/RDrum/tab.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 1100,617, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        y0 = 100
        y1 = y0 + 250
        y_ratio_offset = 25
        y_bias_offset = 85
        x0 = 100
        xa = x0
        xatone = xa+100
        xaattack = xatone+60
        xadecay = xaattack+60
        xabend = xadecay+60
        xavelocity = xabend+60
        xaamp = xavelocity+60
        xnoise = xaamp+90
        xnseRes = xnoise+90
        xnseAttack = xnseRes+60
        xnseDecay = xnseAttack+60
        xnseBend = xnseDecay+60
        xnseVelocity = xnseBend+60
        xnseAmp = xnseVelocity+60
        self.tumbler("aRatio",5,0.001,xa,y0+y_ratio_offset)
        self.norm_slider("aTone",xatone,y0)
        self.time_slider("aAttack",xaattack,y0)
        self.time_slider("aDecay",xadecay,y0)
        self.bipolar_slider("aBend",xabend,y0)
        self.norm_slider("aVelocity",xavelocity,y0)
        self.amp_slider("aAmp",xaamp,y0)
        self.tumbler("bRatio",5,0.001,xa,y1+y_ratio_offset)
        self.linear_slider("bTune",xatone,y1)
        self.time_slider("bAttack",xaattack,y1)
        self.time_slider("bDecay",xadecay,y1)
        self.bipolar_slider("bBend",xabend,y1)
        self.norm_slider("bVelocity",xavelocity,y1)
        self.amp_slider("bAmp",xaamp,y1)
        self.tumbler("noiseRatio",5,0.001,xnoise,y0+y_ratio_offset)
        self.tumbler("noiseBias",5,1,xnoise,y0+y_bias_offset)
        self.norm_slider("noiseRes",xnseRes, y0)
        self.time_slider("noiseAttack",xnseAttack,y0)
        self.time_slider("noiseDecay",xnseDecay,y0)
        self.bipolar_slider("noiseBend",xnseBend,y0)
        self.norm_slider("noiseVelocity",xnseVelocity,y0)
        self.amp_slider("noiseAmp",xnseAmp,y0)
        self.amp_slider("amp",xnseAmp,y1)
        
        
    def tumbler(self,param,digits,scale,x,y):
        t = Tumbler(self.canvas,param,self.editor,digits=digits,scale=scale)
        self.add_control(param,t)
        t.layout((x,y))
        return t

    def linear_slider(self,param,x,y, range_=(0.0,4.0)):
        s = cf.linear_slider(self.canvas,param,self.editor,range_=range_)
        self.add_control(param,s)
        s.widget().place(x=x,y=y)
        return s
    
    def norm_slider(self,param,x,y):
        s = cf.normalized_slider(self.canvas, param, self.editor)
        self.add_control(param,s)
        s.widget().place(x=x,y=y)
        return s

    def bipolar_slider(self,param,x,y):
        s = cf.bipolar_slider(self.canvas, param, self.editor)
        self.add_control(param,s)
        s.widget().place(x=x,y=y)
        return s

    def amp_slider(self,param,x,y):
        s = cf.volume_slider(self.canvas,param,self.editor)
        self.add_control(param,s)
        s.widget().place(x=x,y=y)
        return s

    def time_slider(self,param,x,y):
        s = ExpSlider(self.canvas,param,self.editor,
                      range_=2, degree=3)
        self.add_control(param,s)
        s.layout((x,y),checkbutton_offset=None)
        return s
