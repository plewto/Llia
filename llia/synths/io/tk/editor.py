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
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        def envtime_slider(param,x,y,height=200):
            s = ExpSlider(canvas,param,editor,
                          range_=MAX_ENV_SEGMENT_TIME,
                          degree=3)
            self.add_control(param,s)
            s.layout(offset=(x,y),checkbutton_offset=None,height=height)
            return s
        x0 = 50
        y0,y1 = 50,300
        # Modulator OP4
        x_mod = x0
        y_mod = y0
        y_slider = y_mod+60
        self.tumbler("op4Ratio",4,0.001,x_mod,y_mod)
        self.linear_slider("op4Feedback",(0,3),x_mod,y_slider)
        self.norm_slider("op4LFO",x_mod+47,y_slider)
        # Carriers, OP1, OP2, OP3
        x_carrier = x_mod+130
        x_delta = 360
        yc0 = y0
        yc1 = yc0 + 200
        for op in (1,2,3):
            xc = x_carrier + x_delta * (op-1)
            self.tumbler("op%dFormant" % op,4,1,xc,yc0)
            self.tumbler("op%dRatio" % op,4,0.001,xc,yc0+60)
            self.toggle("op%dMode" % op, xc,yc0+120,(0,"Ratio"),(1,"Formant"))
            x_mod = xc+100
            self.linear_slider("op%dModDepth" % op, (0,MAX_MOD_DEPTH),x_mod,yc0)
            self.norm_slider("op%dVelocity" % op, x_mod+60, yc0)
            self.norm_slider("op%dTremolo" % op, x_mod+120, yc0)
            self.norm_slider("op%dX" % op, x_mod+180, yc0, height=60)
            self.norm_slider("op%dModLag" % op, x_mod+180, yc0+90, height=60)
            param = "op%dBreakKey" % op
            msb0 = self.msb(param,len(KEY_BREAKPOINTS),xc,yc1)
            for i,val in enumerate(KEY_BREAKPOINTS):
                self.msb_aspect(msb0,i,val,update=False)
            msb0.update_aspect()
            param1 = "op%dLeftKeyScale" % op
            param2 = "op%dRightKeyScale" % op
            msb1 = self.msb(param1,len(KEY_SCALES),xc,yc1+60)
            msb2 = self.msb(param2,len(KEY_SCALES),xc,yc1+120)
            for i,val in enumerate(KEY_SCALES):
                self.msb_aspect(msb1,i,val,update=False)
                self.msb_aspect(msb2,i,val,update=False)
            msb1.update_aspect()
            msb2.update_aspect()
            x_env = x_mod
            envtime_slider("op%dAttack" % op,x_env,yc1)
            envtime_slider("op%dDecay" % op,x_env+60,yc1)
            self.norm_slider("op%dSustain" % op,x_env+120,yc1,height=200)
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
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        y0,y1 = 50,300
        x0 = 75
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
        y0,y1 = 50,300
        x0 = 75
        x_noise = x0
        msb0 = self.msb("noiseRatio",len(NOISE_RATIOS),x_noise,y0)
        for i,v in enumerate(NOISE_RATIOS):
            self.msb_aspect(msb0,i,v)
        msb0.update_aspect()
        x_attack = x_noise+90
        envtime_slider("chiffAttack",x_attack,y0)
        envtime_slider("chiffDecay", x_attack+60,y0)
        self.norm_slider("chiffVelocity", x_attack+120,y0)
        x_blip = x_attack+200   # 320
        envtime_slider("blipAttack", x_blip, y0)
        envtime_slider("blipDecay", x_blip+60,y0)
        self.exp_slider("blipDepth", 1.0, x_blip+120,y0)
        x_lfo = x_blip+190
        self.tumbler("vfreq",5,0.001,x_lfo,y0)
        msb1 = self.msb("tremRatio",len(TREMOLO_RATIOS),x_lfo+9,y0+60)
        for i,pair in enumerate(TREMOLO_RATIOS):
            value, text = pair
            self.msb_aspect(msb1,i,value,text)
        msb1.update_aspect()
        self.toggle("vlock",x_lfo+8,y0+120,(0,"Free"),(1,"Lock"))
        x_vnoise = x_lfo+100
        self.norm_slider("vnoise",x_vnoise,y0)
        self.linear_slider("vdelay",(0,4),x_vnoise+60,y0)
        self.norm_slider("vsens",x_vnoise+120,y0)
        self.norm_slider("vdepth",x_vnoise+180,y0)
        self.norm_slider("xPitch",x_vnoise+240,y0)
        x_mix = x0
        y_mix = y0+270
        x_delta = 60
        for op in (1,2,3):
            mix_slider("op%dAmp" % op,x_mix,y_mix)
            x_mix += x_delta
        mix_slider("chiffAmp", x_mix,y_mix)
        x_mix += 60
        mix_slider("noiseAmp", x_mix,y_mix)
        x_mix += 90
        self.volume_slider("amp",x_mix,y_mix)

        
