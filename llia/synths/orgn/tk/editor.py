# llia.synths.orgn.tk.editor


from __future__ import print_function
from Tkinter import Frame

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
#from llia.gui.tk.freq_spinner import FrequencySpinnerControl
from llia.gui.tk.tumbler import Tumbler
from llia.gui.tk.expslider import ExpSlider


def create_editor(parent):
    TkOrgnPanel1(parent)


class TkOrgnPanel1(TkSubEditor):

    NAME = "Orgn Tone"
    IMAGE_FILE = "resources/Orgn/editor.png"
    TAB_FILENAME = "resources/Orgn/tab.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILENAME)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 946,777, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        y0 = 50
        y1 = y0 + 230
        xfreq1, yfreq_offset = 50, 0
        xamp1 = xfreq1+90
        xfreq2 = xamp1+60
        xamp2 = xfreq2+90
        xattack = xamp2+75
        xdecay = xattack+60
        xsustain = xdecay+60
        xrelease = xsustain+60
        xmod = xrelease+75
        xexternmod = xmod + 60
        xexternpitch = xexternmod + 60
        xchorus = xexternpitch + 75
        xchorus_delay = xchorus+60
        xvfreq = xmod
        xvdelay = xvfreq+60
        xvdepth = xvdelay+60
        xamp = xchorus_delay
        self.tumbler("r2", xfreq1, y0+yfreq_offset)
        self.norm_slider("amp2",xamp1,y0)
        self.tumbler("r4", xfreq2,y0+yfreq_offset)
        self.norm_slider("amp4",xamp2,y0) 
        self.env_time_slider("mattack", xattack, y0)
        self.env_time_slider("mdecay", xdecay, y0)
        self.env_time_slider("msustain", xsustain, y0)
        self.env_time_slider("mrelease", xrelease, y0)
        self.norm_slider("modulationDepth", xmod, y0)
        self.norm_slider("xToModulationDepth", xexternmod, y0)
        self.norm_slider("xToPitch", xexternpitch, y0)
        self.norm_slider("chorus", xchorus, y0)
        self.linear_slider("chorusDelay",(0,4),xchorus_delay, y0)
        self.tumbler("r1", xfreq1, y1+yfreq_offset)
        self.volume_slider("amp1", xamp1, y1)
        self.tumbler('r3', xfreq2, y1+yfreq_offset)
        self.volume_slider("amp3", xamp2, y1)
        self.env_time_slider("cattack", xattack, y1)
        self.env_time_slider("cdecay", xdecay, y1)
        self.env_time_slider("csustain", xsustain, y1)
        self.env_time_slider("crelease", xrelease, y1)
        self.linear_slider("vfreq", (0,8), xvfreq, y1)
        self.linear_slider("vdelay", (0,4), xvdepth, y1)
        self.norm_slider("vdepth", xvdelay, y1)
        self.volume_slider("amp", xamp, y1)
        
    # def spinner(self, param, x, y, from_=0.25, to=32):
    #     s = FrequencySpinnerControl(self.canvas,param,self.editor,from_,to)
    #     self.add_control(param,s)
    #     s.layout(offset=(x,y))
    #     return s

    def tumbler(self, param, x, y):
        t = Tumbler(self.canvas,param,self.editor,digits=5, scale=0.001)
        self.add_control(param,t)
        t.layout((x,y))
        return t
    
    def norm_slider(self, param, x, y, width=14, height=150):
        s = cf.normalized_slider(self.canvas, param, self.editor)
        self.add_control(param,s)
        s.widget().place(x=x,y=y,width=width, height=height)
        return s
        
    def linear_slider(self, param, range_, x, y, width=14, height=150):
        s = cf.linear_slider(self.canvas, param, self.editor,
                             range_=range_)
        self.add_control(param, s)
        s.widget().place(x=x,y=y,width=width, height=height)
        return s

        
    def volume_slider(self, param, x, y):
        s = cf.volume_slider(self.canvas, param, self.editor)
        self.add_control(param, s)
        s.widget().place(x=x, y=y, width=14, height=150)
        return s
        
    def env_time_slider(self, param, x, y):
        s = ExpSlider(self.canvas, param, self.editor,
                      range_ = 4, degree=2)
        self.add_control(param, s)
        s.layout((x,y), width=14, height=150,
                 checkbutton_offset=None)
        return s

