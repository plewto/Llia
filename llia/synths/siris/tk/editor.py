# llia.synths.siris.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
from llia.synths.siris.tk.ks_editor import TkSirisKSPanel
from llia.synths.siris.tk.filter_editor import TkSirisFilterPanel
from llia.synths.siris.siris_constants import *

def create_editor(parent):
    TkSirisPanel(parent)
    TkSirisKSPanel(parent)
    TkSirisFilterPanel(parent)

    
class TkSirisPanel(TkSubEditor):

    NAME = "Excite"
    IMAGE_FILE = "resources/Siris/editor.png"
    TAB_FILE = "resources/Siris/tab.png"

    def __init__(self,editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1000,700,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.NAME)
        editor.add_child_editor(self.NAME, self)
        x0 = 75
        x_vib = x0+120
        x_env = x_vib
        x_pulse = x0+470
        x_pw = x_pulse+100
        y0,y1 = 75, 330
        yenv = 200
        # LFO
        self.tumbler("timebase",5, 0.001, x0,y0)
        self.norm_slider("port",x0,y1);
        self.tumbler("vratio",5,0.001,x_vib,y0)
        self.linear_slider("vdelay",(0,2),x_vib+100, y0)
        self.exp_slider("vsens",1,x_vib+160,y0)
        self.norm_slider("vdepth",x_vib+220,y0)
        # Env
        self.toggle("env_mode", x_env+7,y1,off=(0,"Gate"),on=(1,"Trig"))
        self.exp_slider("env_attack",MAX_ENV_SEGMENT,x_env+100,y1)
        self.exp_slider("env_decay",MAX_ENV_SEGMENT,x_env+160,y1)
        self.norm_slider("env_sustain",x_env+220,y1)
        self.exp_slider("env_release", MAX_ENV_SEGMENT,x_env+280,y1)
        # Excite
        self.tumbler("ex_lfo_ratio",5,0.001,x_pulse+200, y0)
        self.exp_slider("ex_env_attack", MAX_ENV_SEGMENT, x_pulse+200, y1)
        self.exp_slider("ex_env_decay", MAX_ENV_SEGMENT, x_pulse+260, y1)
        for n,y in ((1,y0),(2,y1)):
            def param(suffix):
                rs = "ex%d_%s" % (n,suffix)
                return rs
            msb_harm = self.msb(param("harmonic"),len(HARMONICS), x_pulse, y)
            msb_env = self.msb(param("harmonic_env"),len(HARMONICS_MOD), x_pulse, y+70)
            msb_lfo = self.msb(param("harmonic_lfo"),len(HARMONICS_MOD), x_pulse, y+140)
            for j,v in enumerate(HARMONICS):
                self.msb_aspect(msb_harm,j,v)
            for j,v in enumerate(HARMONICS_MOD):
                self.msb_aspect(msb_env,j,v)
                self.msb_aspect(msb_lfo,j,v)
            msb_harm.update_aspect()
            msb_env.update_aspect()
            msb_lfo.update_aspect()
            msb_pw = self.msb(param("pw"),len(PW),x_pw, y)
            msb_pwenv = self.msb(param("pwm_env"),len(PW)+1,x_pw, y+70)
            msb_pwlfo = self.msb(param("pwm_lfo"),len(PW)+1,x_pw, y+140)
            self.msb_aspect(msb_pwenv,0,0.0)
            self.msb_aspect(msb_pwlfo,0,0.0)
            for j,v in enumerate(PW):
                k = j+1
                self.msb_aspect(msb_pw,j,v)
                self.msb_aspect(msb_pwenv,k,v)
                self.msb_aspect(msb_pwlfo,k,v)
            msb_pw.update_aspect()
            msb_pwenv.update_aspect()
            msb_pwlfo.update_aspect()
            

            
