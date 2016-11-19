# llia.synths.io.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB, ToggleButton
from llia.gui.tk.tumbler import Tumbler
from llia.gui.tk.expslider import ExpSlider
from llia.synths.io.io_constants import *

def create_editor(parent):
    TkIoTonePanel(parent)
    TkIoMiscPanel(parent)

class TkIoTonePanel(TkSubEditor):

    NAME = "Io"
    IMAGE_FILE = "resources/Io/editor.png"
    TAB_FILE = "resources/Io/tab.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 1500, 708, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        y0 = 50
        y1 = 300
        x0 = 75
        def norm_slider(param,x,y=y0,height=150):
            s = cf.normalized_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y,height=height)
            return s
        def linear_slider(param,range_,x,y=y0,height=150):
            s = cf.linear_slider(canvas,param,editor,range_=range_)
            self.add_control(param,s)
            s.widget().place(x=x,y=y,height=height)
            return s
        def mix_slider(param,x,y=y0,height=150):
            s = cf.mix_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y,height=height)
            return s
        def envtime_slider(param,x,y,height=200):
            s = ExpSlider(canvas,param,editor,
                          range_=MAX_ENV_SEGMENT_TIME,
                          degree=3)
            self.add_control(param,s)
            s.layout(offset=(x,y),checkbutton_offset=None,height=height)
            return s
        def tumbler(param,digits,scale,x,y):
            t = Tumbler(canvas,param,editor,digits=digits,scale=scale)
            self.add_control(param,t)
            t.layout((x,y))
            return t
        def toggle(param,text,x,y):
            t = ToggleButton(canvas,param,editor,text=text)
            self.add_control(param,t)
            t.layout((x,y))
            t.update_aspect()
            return t
        def msb_aspect(text,value):
            d = {"fill" : CFILL,
                 "foreground" : CFOREGROUND,
                 "outline" : COUTLINE,
                 "text" : text,
                 "value" : value}
            return d
        y0 = 50
        x0 = 50
        # Modulator OP4
        x_mod = x0
        y_mod = y0
        y_slider = y_mod+60
        tumbler("op4Ratio",4,0.001,x_mod,y_mod)
        linear_slider("op4Feedback",(0,3),x_mod,y_slider)
        norm_slider("op4LFO",x_mod+47,y_slider)
        # Carriers, OP1, OP2, OP3
        x_carrier = x_mod+130
        x_delta = 360
        yc0 = y0
        yc1 = yc0 + 200
        for op in (1,2,3):
            xc = x_carrier + x_delta * (op-1)
            tumbler("op%dFormant" % op, 4,1,xc,yc0)
            tumbler("op%dRatio" % op, 4,0.001,xc,yc0+60)
            toggle("op%dMode" % op, ("Ratio","Formant"),xc,yc0+120)
            x_mod = xc+100
            linear_slider("op%dModDepth" % op, (0,MAX_MOD_DEPTH),x_mod,yc0)
            norm_slider("op%dVelocity" % op, x_mod+60, yc0)
            norm_slider("op%dTremolo" % op, x_mod+120, yc0)
            norm_slider("op%dX" % op, x_mod+180, yc0, 60)
            norm_slider("op%dModLag" % op, x_mod+180, yc0+90, 60)
            param = "op%dBreakKey" % op
            msb = MSB(canvas,param,editor,len(KEY_BREAKPOINTS))
            for i,val in enumerate(KEY_BREAKPOINTS):
                msb.define_aspect(i,val, msb_aspect(str(val),val))
            self.add_control(param,msb)
            msb.layout((xc,yc1))
            msb.update_aspect()
            param1 = "op%dLeftKeyScale" % op
            param2 = "op%dRightKeyScale" % op
            msb1 = MSB(canvas,param1,editor,len(KEY_SCALES))
            msb2 = MSB(canvas,param2,editor,len(KEY_SCALES))
            self.add_control(param1,msb1)
            self.add_control(param2,msb2)
            for i,val in enumerate(KEY_SCALES):
                d = msb_aspect("%+d" % val, val)
                msb1.define_aspect(i,val,d)
                msb2.define_aspect(i,val,d)
            msb1.layout((xc,yc1+60))
            msb2.layout((xc,yc1+120))
            msb1.update_aspect()
            msb2.update_aspect()
            x_env = x_mod
            envtime_slider("op%dAttack" % op,x_env,yc1)
            envtime_slider("op%dDecay" % op,x_env+60,yc1)
            norm_slider("op%dSustain" % op,x_env+120,yc1,height=200)
            envtime_slider("op%dRelease" % op,x_env+180,yc1)
            
                                
            
class TkIoMiscPanel(TkSubEditor):

    NAME = "Misc"
    IMAGE_FILE = "resources/Io/editor2.png"
    TAB_FILE = "resources/Tabs/misc.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 1500, 708, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        y0 = 50
        y1 = 300
        x0 = 75
        def norm_slider(param,x,y=y0,height=150):
            s = cf.normalized_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y,height=height)
            return s
        def volume_slider(param,x,y=y0):
            s = cf.volume_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y)
            return s
        def linear_slider(param,range_,x,y=y0,height=150):
            s = cf.linear_slider(canvas,param,editor,range_=range_)
            self.add_control(param,s)
            s.widget().place(x=x,y=y,height=height)
            return s
        def mix_slider(param,x,y=y0,height=150):
            s = cf.mix_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y,height=height)
            return s
        def envtime_slider(param,x,y,height=150):
            s = ExpSlider(canvas,param,editor,
                          range_=MAX_BLIP_SEGMENT_TIME,
                          degree=2)
            self.add_control(param,s)
            s.layout(offset=(x,y),checkbutton_offset=None,height=height)
            return s
        def exp_slider(param,range_,x,y,degree=2,height=150):
            s = ExpSlider(canvas,param,editor,
                          range_ = range_,
                          degree = degree)
            self.add_control(param,s)
            s.layout(offset=(x,y),checkbutton_offset=None,height=height)
        def tumbler(param,digits,scale,x,y):
            t = Tumbler(canvas,param,editor,digits=digits,scale=scale)
            self.add_control(param,t)
            t.layout((x,y))
            return t
        def toggle(param,text,x,y):
            t = ToggleButton(canvas,param,editor,text=text)
            self.add_control(param,t)
            t.layout((x,y))
            t.update_aspect()
            return t
        def msb_aspect(text,value):
            d = {"fill" : CFILL,
                 "foreground" : CFOREGROUND,
                 "outline" : COUTLINE,
                 "text" : text,
                 "value" : value}
            return d
        y0 = 50
        x0 = 50
        
        x_noise = x0
        param = "noiseRatio"
        msb = MSB(canvas,param,editor,len(NOISE_RATIOS))
        self.add_control(param,msb)
        for i,v in enumerate(NOISE_RATIOS):
            d = msb_aspect(str(v),v)
            msb.define_aspect(i,v,d)
        msb.layout((x_noise,y0))
        msb.update_aspect()
        x_attack = x_noise+90
        envtime_slider("chiffAttack",x_attack,y0)
        envtime_slider("chiffDecay", x_attack+60,y0)
        norm_slider("chiffVelocity", x_attack+120,y0)
        # mix_slider("chiffAmp", x_attack+180,y0)
        # mix_slider("noiseAmp", x_attack+240,y0)

        x_blip = x_attack+200   # 320
        envtime_slider("blipAttack", x_blip, y0)
        envtime_slider("blipDecay", x_blip+60,y0)
        exp_slider("blipDepth", 1.0, x_blip+120,y0)

        x_lfo = x_blip+190
        tumbler("vfreq",5,0.001,x_lfo,y0)
        param = "tremRatio"
        msb = MSB(canvas,param,editor,len(TREMOLO_RATIOS))
        self.add_control(param,msb)
        for i,pair in enumerate(TREMOLO_RATIOS):
            value, text = pair
            d = msb_aspect(text,value)
            msb.define_aspect(i,value,d)
        msb.layout((x_lfo+8,y0+60))
        msb.update_aspect()
        toggle("vlock",("Free","Lock"),x_lfo+8,y0+120)
        x_vnoise = x_lfo+100
        norm_slider("vnoise",x_vnoise,y0)
        linear_slider("vdelay",(0,4),x_vnoise+60,y0)
        norm_slider("vsens",x_vnoise+120,y0)
        norm_slider("vdepth",x_vnoise+180,y0)
        norm_slider("xPitch",x_vnoise+240,y0)

        x_mix = x_attack
        y_mix = y0+220
        x_delta = 60
        for op in (1,2,3):
            mix_slider("op%dAmp" % op,x_mix,y_mix)
            x_mix += x_delta
        mix_slider("chiffAmp", x_mix,y_mix)
        x_mix += 60
        mix_slider("noiseAmp", x_mix,y_mix)
        x_mix += 90
        volume_slider("amp",x_mix,y_mix)

        
