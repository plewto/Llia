# llia.synths.m.tk.filter_editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.msb import MSB, ToggleButton
from llia.gui.tk.tumbler import Tumbler
from llia.synths.m.m_constants import *


class TkMFilterPanel(TkSubEditor):

    NAME = "M_FILTER"
    IMAGE_FILE = "resources/M/filter_editor.png"
    TAB_FILE = "resources/M/filter_tab.png"


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
        def y(n,delta=55):
            return y0+(n*delta)
            y_lfo = y0+55
        x0 = 75
        x_freq = x0
        def norm_slider(param,x,y, height=150):
            s = cf.normalized_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y,height=height)
            return s
        def linear_slider(param,range_,x,y):
            s = cf.linear_slider(canvas,param,editor,range_=range_)
            self.add_control(param,s)
            s.widget().place(x=x,y=y)
            return s
        def exp_slider(param,x,y,range_=100,degree=2,checkbutton=None):
            s = ExpSlider(canvas,param,editor,range_=range_,degree=degree)
            self.add_control(param,s)
            s.layout((x,y),checkbutton_offset=checkbutton)
            return s
        def volume_slider(param,x,y):
            s = cf.volume_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y)
            return s
        def tumbler(param,x,y,digits=5,scale=0.001):
            t = Tumbler(canvas,param,editor,digits=digits,scale=scale)
            self.add_control(param,t)
            t.layout((x,y))
            return t
        def msb(param,count,x,y):
            msb = MSB(canvas,param,editor,count)
            self.add_control(param,msb)
            msb.layout((x,y))
            return msb
        for f in (1,2):
            ys = y((f-1)*4)
            if f == 1:
                plfo1 = "f1FreqLfoA"
                plfo2 = "f1FreqLfoB"
                penv1 = "f1FreqEnvA"
                penv2 = "f1FreqEnvB"
            else:
                plfo1 = "f2FreqLfoB"
                plfo2 = "f2FreqLfoC"
                penv1 = "f2FreqEnvB"
                penv2 = "f2FreqEnvC"
            exp_slider("f%dFreq"%f,x_freq,ys,20000)
            exp_slider(plfo1,x_freq+60,ys,2000)
            exp_slider(plfo2,x_freq+120,ys,2000)
            exp_slider(penv1,x_freq+180,ys,20000,checkbutton=(-5,150))
            exp_slider(penv2,x_freq+240,ys,20000,checkbutton=(-5,150))
            norm_slider("f%dRes" % f,x_freq+300,ys)
            linear_slider("f%dPan" % f,(-1,1),x_freq+360,ys)
        # Vibrato LFO & Misc
        x_vib = x_freq+450
        norm_slider("port",x_vib,y(0))
        tumbler("vfreq",x_vib+30,y(0),5,0.001)
        m_trem = msb("tremoloLag",len(TREMOLO),x_vib+38,y(1))
        define_aspects(m_trem,TREMOLO)
        linear_slider("vdelay",(0,4),x_vib+130,y(0))
        norm_slider("vsens",x_vib+190,y(0))
        norm_slider("vdepth",x_vib+250,y(0))
        x_amp = x_vib+250+90
        volume_slider("amp",x_amp,y(0))

        # External controls
        xx = x_vib
        linear_slider("xPitch",(-1,1),xx,y(4))
        linear_slider("aQExternal",(-16,16),xx+60,y(4))
        linear_slider("aPwmExternal",(-8,8),xx+120,y(4))
        linear_slider("bNExternal",(0,32),xx+180,y(4))
        linear_slider("cPulseRatioExternal",(-16,16),xx+240,y(4))
        exp_slider("f1FreqExternal",16000,xx+300,y(4))
        exp_slider("f2FreqExternal",16000,xx+360,y(4))
        
