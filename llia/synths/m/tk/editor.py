# llia.synths.m.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.msb import MSB, ToggleButton
from llia.gui.tk.tumbler import Tumbler
from llia.synths.m.tk.env_editor import TkMEnvPanel
from llia.synths.m.tk.filter_editor import TkMFilterPanel
from llia.synths.m.m_constants import *

def create_editor(parent):
    TkMPanel(parent)
    TkMFilterPanel(parent)
    TkMEnvPanel(parent)

    
class TkMPanel(TkSubEditor):

    NAME = "M"
    IMAGE_FILE = "resources/M/editor.png"
    TAB_FILE = "resources/M/tab.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 1200, 700, self.IMAGE_FILE)
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
        def volume_slider(param,x,y):
            s = cf.volume_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y)
            return s
        def exp_slider(param,x,y,range_=100,degree=2,checkbutton=None):
            s = ExpSlider(canvas,param,editor,range_=range_,degree=degree)
            self.add_control(param,s)
            s.layout((x,y),checkbutton_offset=checkbutton)
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
        x_ratio = x0
        x_lfo = x_ratio+8
        x_q = x_ratio + 100
        x_pw = x_q + 100
        x_clk = x_pw + 100
        x_trem = x0+390
        x_keyscale = x_trem + 60
        x_mixer = x_keyscale + 100
        x_pan = x_mixer+30
        # Tone A
        tumbler("aRatio",x_ratio,y(0))
        msb_lfo = msb("aLfoRatio",len(LFO_RATIOS),x_lfo,y(1))
        msb_lfo_delay = msb("aLfoDelay",len(LFO_DELAYS),x_lfo,y(2))
        define_aspects(msb_lfo,LFO_RATIOS)
        define_aspects(msb_lfo_delay, LFO_DELAYS)
        msb_q = msb("aQuotient",len(A_QUOTIENTS),x_q, y(0))
        msb_q_lfo = msb("aQLfo",len(A_Q_LFO),x_q,y(1))
        msb_q_env = msb("aQEnv",len(A_Q_ENV),x_q,y(2))
        define_aspects(msb_q,A_QUOTIENTS)
        define_aspects(msb_q_lfo,A_Q_LFO)
        define_aspects(msb_q_env,A_Q_ENV)
        msb_pw = msb("aPulseWidth",len(A_PW),x_pw,y(0))
        msb_pw_lfo = msb("aPwmLfo",len(A_PW_LFO),x_pw,y(1))
        msb_pw_env = msb("aPwmEnv",len(A_PW_ENV),x_pw,y(2))
        define_aspects(msb_pw,A_PW)
        define_aspects(msb_pw_lfo,A_PW_LFO)
        define_aspects(msb_pw_env,A_PW_ENV)
        norm_slider("aClkMix",x_clk,y(0))
        norm_slider("aLfo",x_trem,y(0))
        m_akey = msb("aKey",len(BREAKKEYS),x_keyscale,y(0))
        m_aleft = msb("aKeyscaleLeft",len(KEYSCALES),x_keyscale,y(1)) 
        m_aright = msb("aKeyscaleRight",len(KEYSCALES),x_keyscale,y(2))
        define_aspects(m_akey,BREAKKEYS)
        define_aspects(m_aleft,KEYSCALES)
        define_aspects(m_aright,KEYSCALES)
        volume_slider("aAmp",x_mixer,y(0))
        linear_slider("aFilter",(-1,1),x_pan,y(0))
        # Tone B
        y0 = y(3)
        x_b1 = x_ratio
        x_b2 = x_b1+92
        x_bn = x_q
        x_blag = x_bn+100
        tumbler("bRatio1",x_b1,y(0))
        tumbler("bRatio2",x_b2,y(0))
        msb_lfo = msb("bLfoRatio",len(LFO_RATIOS),x_lfo,y(1))
        msb_lfo_delay = msb("bLfoDelay",len(LFO_DELAYS),x_lfo,y(2))
        define_aspects(msb_lfo,LFO_RATIOS)
        define_aspects(msb_lfo_delay, LFO_DELAYS)
        msb_n_lfo = msb("bNLfo",len(B_N_LFO),x_bn,y(1))
        msb_n_env = msb("bNEnv",len(B_N_ENV),x_bn,y(2))
        msb_n1 = msb("bN1",len(B_N),x_b1,y(3))
        msb_n2 = msb("bN2",len(B_N),x_b2,y(3))
        define_aspects(msb_n_lfo,B_N_LFO)
        define_aspects(msb_n_env,B_N_ENV)
        define_aspects(msb_n1,B_N)
        define_aspects(msb_n2,B_N)
        msb_n_lag = msb("bN2Lag",len(B_N2_LAG),x_blag,y(1))
        msb_pol = msb("b2Polarity",len(B_N2_POLARITY),x_blag,y(2))
        define_aspects(msb_n_lag,B_N2_LAG)
        define_aspects(msb_pol,B_N2_POLARITY)
        norm_slider("bLfo",x_trem,y(0))
        m_bkey = msb("bKey",len(BREAKKEYS),x_keyscale,y(0))
        m_bleft = msb("bKeyscaleLeft",len(KEYSCALES),x_keyscale,y(1)) 
        m_bright = msb("bKeyscaleRight",len(KEYSCALES),x_keyscale,y(2))
        define_aspects(m_bkey,BREAKKEYS)
        define_aspects(m_bleft,KEYSCALES)
        define_aspects(m_bright,KEYSCALES)
        norm_slider("aAmp",x_mixer,y(0))
        volume_slider("bAmp",x_mixer,y(0))
        linear_slider("bFilter",(-1,1),x_pan,y(0))

        # Noise
        x_noise = x0+660
        x_noise_lp = x_noise
        x_noise_hp = x_noise_lp + 60
        x_noise_trem = x_noise_hp + 60
        x_noise_lag = x_noise_trem + 60
        x_noise_amp = x_noise_lag + 60
        x_noise_filter = x_noise_amp + 30
       

        exp_slider("noiseLP",x_noise_lp,y(0),16000)
        exp_slider("noiseHP",x_noise_hp,y(0),16000)
        norm_slider("noiseLfo",x_noise_trem,y(0))
        norm_slider("noiseLag",x_noise_lag,y(0))
        volume_slider("noiseAmp",x_noise_amp,y(0))
        linear_slider("noiseFilter",(-1,1),x_noise_filter,y(0))
        
        # Tone C
        y0 = y(4)
        x_pratio = x_ratio+100
        x_pw = x_pratio+100
        x_fb = x_pw+100
        tumbler("cRatio",x_ratio,y(0))
        msb_lfo = msb("cLfoRatio",len(LFO_RATIOS),x_lfo,y(1))
        msb_lfo_delay = msb("cLfoDelay",len(LFO_DELAYS),x_lfo,y(2))
        define_aspects(msb_lfo,LFO_RATIOS)
        define_aspects(msb_lfo_delay, LFO_DELAYS)
        #m_pr = msb("cPulseRatio",len(C_PRATIO),x_pratio, y(0))
        tumbler("cPulseRatio",x_pratio,y(0),5,0.001)
        m_pr_lfo = msb("cPulseRatioLfo",len(C_PRATIO_LFO),x_pratio,y(1))
        m_pr_env = msb("cPulseRatioEnv",len(C_PRATIO_ENV),x_pratio,y(2))
        #define_aspects(m_pr,C_PRATIO)
        define_aspects(m_pr_lfo,C_PRATIO_LFO)
        define_aspects(m_pr_env,C_PRATIO_ENV)
        m_pw = msb("cPw",len(C_PW),x_pw,y(0))
        m_pw_lfo = msb("cPwmLfo",len(C_PW),x_pw,y(1))
        m_pw_env = msb("cPwmEnv",len(C_PW),x_pw,y(2))
        define_aspects(m_pw,C_PW)
        define_aspects(m_pw_lfo,C_PW)
        define_aspects(m_pw_env,C_PW)
        m_fb = msb("cFb",len(C_FB),x_fb,y(0))
        define_aspects(m_fb,C_FB)
        norm_slider("cInciteSelect",x_fb+24,y(1),height=100)
        norm_slider("cLfo",x_trem,y(0))
        m_ckey = msb("cKey",len(BREAKKEYS),x_keyscale,y(0))
        m_cleft = msb("cKeyscaleLeft",len(KEYSCALES),x_keyscale,y(1)) 
        m_cright = msb("cKeyscaleRight",len(KEYSCALES),x_keyscale,y(2))
        define_aspects(m_ckey,BREAKKEYS)
        define_aspects(m_cleft,KEYSCALES)
        define_aspects(m_cright,KEYSCALES)  
        volume_slider("cAmp",x_mixer,y(0))
        linear_slider("cFilter",(-1,1),x_pan,y(0))
