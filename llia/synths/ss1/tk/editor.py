# llia.synths.ss1.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB, ToggleButton
from llia.gui.tk.tumbler import Tumbler
from llia.gui.tk.expslider import ExpSlider
from llia.synths.ss1.ss1_data import (HIGHPASS_CUTOFF,LOWPASS_CUTOFF,
                                      LOWPASS_TRACK,CFILL,CFOREGROUND,
                                      COUTLINE,MID_CUTOFF)

def create_editor(parent):
    TkSS1Panel(parent)

class TkSS1Panel(TkSubEditor):

    NAME = "SS1"
    IMAGE_FILE = "resources/SS1/editor.png"
    TAB_FILE = "resources/SS1/tab.png"


    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 1000, 700, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        y0 = 50
        x0 = 75
        def norm_slider(param,x):
            s = cf.normalized_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y0)
            return s
        def volume_slider(param,x):
            s = cf.volume_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y0)
            return s
        def linear_slider(param,range_,x):
            s = cf.linear_slider(canvas,param,editor,range_=range_)
            self.add_control(param,s)
            s.widget().place(x=x,y=y0)
            return s
        def exp_slider(param,range_,degree=2):
            s = ExpSlider(canvas,param,editor,range_,degree)
            self.add_control(param,s)
            return s
        def env_slider(param,x):
            s = exp_slider(param,6)
            s.layout(offset=(x,y0),checkbutton_offset=None)
            return s
        def msb_aspect(msb,index,text,value):
            d = {"fill" : CFILL,
                 "foreground" : CFOREGROUND,
                 "outline" : COUTLINE,
                 "text" : str(text),
                 "value" : value}
            msb.define_aspect(index,value,d)
            return d
        x_osc = x0
        x_delta = 75
        x_port = x_osc
        x_saw = x_port + 75
        x_pulse = x_saw + x_delta
        x_sub = x_pulse + x_delta
        x_noise = x_sub + x_delta
        y_msb = y0+200
        x_msb_offset = -24
        norm_slider("port",x_port)
        norm_slider("sawMix",x_saw)
        norm_slider("pulseMix",x_pulse)
        norm_slider("subMix",x_sub)
        norm_slider("noiseMix",x_noise)
        param = "chorus"
        msb = MSB(canvas,param,editor,2)
        msb_aspect(msb,0,"Off",0)
        msb_aspect(msb,1,"On",1)
        self.add_control(param,msb)
        msb.layout((x_saw+x_msb_offset,y_msb))
        msb.update_aspect()
        param = "subOctave"
        msb = MSB(canvas,param,editor,2)
        msb_aspect(msb,0,"-1",0)
        msb_aspect(msb,1,"-2",1)
        self.add_control(param,msb)
        msb.layout((x_sub+x_msb_offset,y_msb))
        msb.update_aspect()
        param = "noiseSelect"
        msb = MSB(canvas,param,editor,2)
        msb_aspect(msb,0,"White",0)
        msb_aspect(msb,1,"Pink",1)
        self.add_control(param,msb)
        msb.layout((x_noise+x_msb_offset,y_msb))
        msb.update_aspect()
        x_wave = x_noise+x_delta
        x_lfo = x_wave + 60
        x_env = x_lfo + 60
        norm_slider("wave",x_wave)
        norm_slider("waveLFO",x_lfo)
        norm_slider("waveEnv",x_env)
        x_filter = x_env+90
        x_lfo = x_filter + 90
        x_env = x_lfo + 60
        x_x = x_env + 60
        x_res = x_x + 60
        y_hp = y0 + 20
        y_ff = y_hp + 90
        y_track = y_msb
        param = "highPass"
        msb = MSB(canvas,param,editor,len(HIGHPASS_CUTOFF))
        for i,v in enumerate(HIGHPASS_CUTOFF):
            msb_aspect(msb,i,str(v),v)
        self.add_control(param,msb)
        msb.layout((x_filter, y_hp))
        msb.update_aspect()
        param = "filterFreq"
        msb = MSB(canvas,param,editor,len(LOWPASS_CUTOFF))
        for i,v in enumerate(LOWPASS_CUTOFF):
            msb_aspect(msb,i,str(v),v)
        self.add_control(param,msb)
        msb.layout((x_filter,y_ff))
        msb.update_aspect()
        param = "filterTrack"
        msb = MSB(canvas,param,editor,len(LOWPASS_TRACK))
        for i,v in enumerate(LOWPASS_TRACK):
            msb_aspect(msb,i,str(v),v)
        msb.layout((x_filter, y_track))
        msb.update_aspect()
        s = exp_slider("filterLFO",MID_CUTOFF)
        s.layout(offset=(x_lfo,y0),checkbutton_offset=None)
        s = exp_slider("filterEnv",10000)
        s.layout(offset=(x_env,y0))
        s = exp_slider("xFilter",10000)
        s.layout(offset=(x_x,y0))
        norm_slider("filterRes",x_res)
        y0 = 350
        x_lfo = x0
        x_lfo_delay = x_lfo+90
        x_lfo_amp = x_lfo_delay+60
        x_vsens = x_lfo_amp+90
        x_vdepth = x_vsens+60
        x_xpitch = x_vdepth+60
        param = "lfoFreq"
        t = Tumbler(canvas,param,editor,digits=5,scale=0.001)
        self.add_control(param,t)
        t.layout((x_lfo, y0))
        param = "lfoWave"
        msb = MSB(canvas,param,editor,3)
        self.add_control(param,msb)
        msb_aspect(msb,0,"Sine",0)
        msb_aspect(msb,1,"Square",1)
        msb_aspect(msb,2,"Random",2)
        msb.layout((x_lfo,y0+90))
        msb.update_aspect()
        linear_slider("lfoDelay",(0,3),x_lfo_delay)
        norm_slider("lfoAmp",x_lfo_amp)
        norm_slider("vsens",x_vsens)
        norm_slider("vdepth",x_vdepth)
        norm_slider("xPitch",x_xpitch)
        x_env = x_xpitch+90
        env_slider("attack",x_env)
        env_slider("decay",x_env+60)
        norm_slider("sustain",x_env+120)
        env_slider("release",x_env+180)
        x_amp = x_env+180+90
        param = "gateMode"
        msb = MSB(canvas,param,editor,2)
        msb_aspect(msb,0,"ADSR",0)
        msb_aspect(msb,1,"Gate",1)
        msb.layout((x_amp, y0+90))
        msb.update_aspect()
        volume_slider("amp",x_amp+90)
