# llia.synths.fm2.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB
from llia.gui.tk.tumbler import Tumbler
from llia.gui.tk.expslider import ExpSlider
from llia.synths.fm2.tk.env_editor import TkFm2EnvEditor
from llia.synths.fm2.tk.lfo_editor import TkFm2LfoPanel
from llia.synths.fm2.fm2_constants import *


def create_editor(parent):
    TkFm2Panel1(parent)
    TkFm2EnvEditor(parent)
    TkFm2LfoPanel(parent)
    
class TkFm2Panel1(TkSubEditor):

    NAME = "FM2 OPS"
    IMAGE_FILE = "resources/FM2/fm_editor.png"
    TAB_FILE = "resources/FM2/tab_fm.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 900, 600, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        y0 = 50
        y1 = y0+250
        x0 = 50
        def tumbler(param,digits,scale,x,y):
            t = Tumbler(canvas,param,editor,digits=digits,scale=scale,
                        fill = BG,
                        foreground = CFOREGROUND,
                        outline = COUTLINE)
            self.add_control(param,t)
            t.layout((x,y))
            return y
        def msb_aspect(msb,index,value,text=None):
            d = {"fill" : CFILL,
                 "foreground" : CFOREGROUND,
                 "outline" : COUTLINE,
                 "text" : str(text or value),
                 "value" : value}
            msb.define_aspect(index,value,d)
            return d
        def msb(param,count,x,y):
            msb = MSB(canvas,param,editor,count)
            self.add_control(param,msb)
            msb.layout((x,y))
            return msb
        def norm_slider(param,x,y,height=150):
            s = cf.normalized_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y,height=height)
            return s
        def linear_slider(param,range_,x,y,height=150):
            s = cf.linear_slider(canvas,param,editor,range_=range_)
            self.add_control(param,s)
            s.widget().place(x=x,y=y,height=height)
            return s
        def exp_slider(param,range_,x,y,degree=2,height=150):
            s = ExpSlider(canvas,param,editor,range_=range_,degree=degree)
            self.add_control(param,s)
            s.layout((x,y),checkbutton_offset=None)
            return s
        def volume_slider(param,x,y):
            s = cf.volume_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y)
            return s
        # Modulator
        x_ratio = x0
        x_mod = x_ratio +90
        x_lfo = x_mod+60
        x_vel = x_lfo+60
        x_fb = x_port = x_vel+60
        x_keyscale = x_fb+75
        tumbler("op2Ratio",5,0.001,x_ratio,y0)
        tumbler("op2Bias",5,0.01,x_ratio,y0+60)
        exp_slider("op2Amp",10,x_mod,y0)
        mod_scale_count = 5
        msb_mod = msb("op2AmpRange",mod_scale_count,x_mod-24,y0+160)
        for i in range(mod_scale_count):
            v = 10**i
            msb_aspect(msb_mod,i,v,str(i+1))
        msb_mod.update_aspect()
        norm_slider("op2Lfo",x_lfo,y0)
        norm_slider("op2Velocity",x_vel,y0)
        exp_slider("op2Feedback",4,x_fb,y0,degree=1.5)
        msb_key = msb("op2Keybreak",len(KEYNUMBERS),x_keyscale,y0)
        for i,v in enumerate(KEYNUMBERS):
            msb_aspect(msb_key,i,v,str(v))
        msb_key.update_aspect()
        msb_left = msb("op2LeftScale",len(KEYSCALES),x_keyscale,y0+60)
        for i,v in enumerate(KEYSCALES):
            msb_aspect(msb_left,i,v,"%+d db" % v)
        msb_left.update_aspect()
        msb_right = msb("op2RightScale",len(KEYSCALES),x_keyscale,y0+120)
        for i,v in enumerate(KEYSCALES):
            msb_aspect(msb_right,i,v,"%+d db" % v)
        msb_right.update_aspect()
        # Carrier
        tumbler("op1Ratio",5,0.001,x_ratio,y1)
        tumbler("op1Bias",5,0.01,x_ratio,y1+60)
        volume_slider("op1Amp",x_mod,y1)
        norm_slider("op1Lfo",x_lfo,y1)
        norm_slider("op1Velocity",x_vel,y1)
        norm_slider("port",x_port,y1)
        msb_key = msb("op1Keybreak",len(KEYNUMBERS),x_keyscale,y1)
        for i,v in enumerate(KEYNUMBERS):
            msb_aspect(msb_key,i,v,str(v))
        msb_key.update_aspect()
        msb_left = msb("op1LeftScale",len(KEYSCALES),x_keyscale,y1+60)
        for i,v in enumerate(KEYSCALES):
            msb_aspect(msb_left,i,v,"%+d db" % v)
        msb_left.update_aspect()
        msb_right = msb("op1RightScale",len(KEYSCALES),x_keyscale,y1+120)
        for i,v in enumerate(KEYSCALES):
            msb_aspect(msb_right,i,v,"%+d db" % v)
        msb_right.update_aspect()
        # Modulator effects
        x_efx = x_keyscale+120
        x_dly = x_pdisp = x_efx+90
        x_fb = x_tdisp = x_dly+60
        x_lfo = x_fb+60
        x_mix = x_lfo+60
        x_efx_amp = x_mix+60
        y_mix = (y0+y1)/2
        msb_ratio = msb("efxLfoRatio",len(LFO_RATIOS),x_efx,y0)
        for i,p in enumerate(LFO_RATIOS):
            v,txt = p
            msb_aspect(msb_ratio,i,v,txt)
        msb_ratio.update_aspect()
        linear_slider("flangerDelay",(0,MAX_FLANGER_DELAY),x_dly,y0)
        linear_slider("flangerFeedback",(-1.0, 1.0),x_fb,y0)
        exp_slider("flangerLfoDepth",1.0,x_lfo,y0,degree=3)
        tumbler("psRatio",4,0.001,x_efx,y1)
        exp_slider("psPDispersion",1.0,x_pdisp,y1)
        exp_slider("psTDispersion",1.0,x_tdisp,y1)
        norm_slider("psLfoDepth",x_lfo,y1)
        linear_slider("efxMix",(1.0,-1.0),x_mix,y_mix)
        exp_slider("efxAmp",1.01,x_efx_amp,y_mix,degree=3)
