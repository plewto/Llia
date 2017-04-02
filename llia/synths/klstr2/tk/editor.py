# llia.synths.klstr2.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.synths.klstr2.klstr2_constants import *
from llia.synths.klstr2.tk.editor2 import TkKlstr2ModPanel
from llia.synths.klstr2.tk.editor3 import TkKlstr2ExternalPanel

def create_editor(parent):
    TkKlstr2OscPanel(parent)
    TkKlstr2ModPanel(parent)
    TkKlstr2ExternalPanel(parent)

class TkKlstr2OscPanel(TkSubEditor):

    NAME = "Klstr2"
    IMAGE_FILE = "resources/Klstr2/editor.png"
    TAB_FILE = "resources/Klstr2/tab.png"

    def __init__(self,editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1000,700,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.NAME)
        editor.add_child_editor(self.NAME, self)
        x0 = 75
        x_spread=x0
        x_cluster = x_spread+120
        x_pw = x_cluster+180
        x_harm1 = x_pw+120
        x_harm2 = x_harm1+100
        x_noise = x_harm2+100
        x_mixer = x_noise+100
        y0 = 75
        y1 = 300
        self.exp_slider("spread",1.0,x_spread,y0)
        self.exp_slider("spread_env1",1.0,x_spread,y1)
        self.exp_slider("spread_lfo1",1.0,x_spread+60,y1)
        self.norm_slider("cluster",x_cluster,y0)
        self.norm_slider("cluster_env1",x_cluster,y1)
        self.norm_slider("cluster_lfo1",x_cluster+60,y1)
        self.norm_slider("cluster_lfo2",x_cluster+120,y1)
        self.norm_slider("pw",x_pw,y0)
        self.norm_slider("pw_env1",x_pw,y1)
        self.norm_slider("pw_lfo1",x_pw+60,y1)
        msb_h1 = self.msb("harm1",len(HARMONICS),x_harm1, y0)
        msb_h2 = self.msb("harm2",len(HARMONICS),x_harm2, y0)
        for i,n in enumerate(HARMONICS):
            if n <= 6:
                fg = NORMAL_MOD_DEPTH_COLOR
            elif n <= 24:
                fg = MODERATE_MOD_DEPTH_COLOR
            else:
                fg = DEEP_MOD_DEPTH_COLOR
            self.msb_aspect(msb_h1,i,n,foreground=fg)
            self.msb_aspect(msb_h2,i,n,foreground=fg)
        msb_h1_env1 = self.msb("harm1_env1",len(POLAR_HARMONIC_MOD_RANGE),x_harm1,y0+75)
        msb_h1_env2 = self.msb("harm1_env2",len(POLAR_HARMONIC_MOD_RANGE),x_harm1,y0+150)
        msb_h2_env1 = self.msb("harm2_env1",len(POLAR_HARMONIC_MOD_RANGE),x_harm2,y0+75)
        for i,n in enumerate(POLAR_HARMONIC_MOD_RANGE):
            if n < 0:
                bg = NEGATIVE_FILL_COLOR
            else:
                bg = POSITIVE_FILL_COLOR
            if abs(n) <= 6:
                fg = NORMAL_MOD_DEPTH_COLOR
            elif abs(n) <= 24:
                fg = MODERATE_MOD_DEPTH_COLOR
            else:
                fg = DEEP_MOD_DEPTH_COLOR
            self.msb_aspect(msb_h1_env1,i,n,foreground=fg,fill=bg)
            self.msb_aspect(msb_h1_env2,i,n,foreground=fg,fill=bg)
            self.msb_aspect(msb_h2_env1,i,n,foreground=fg,fill=bg)
        msb_h1_lfo1 = self.msb("harm1_lfo1",len(HARMONIC_MOD_RANGE),x_harm1,y0+225)
        msb_h1_lfo2 = self.msb("harm1_lfo2",len(HARMONIC_MOD_RANGE),x_harm1,y0+300)
        msb_h2_lfo1 = self.msb("harm2_lfo1",len(HARMONIC_MOD_RANGE),x_harm2,y0+225)
        for i,n in enumerate(HARMONIC_MOD_RANGE):
            if n <= 6:
                fg = NORMAL_MOD_DEPTH_COLOR
            elif n <= 24:
                fg = MODERATE_MOD_DEPTH_COLOR
            else:
                fg = DEEP_MOD_DEPTH_COLOR
            self.msb_aspect(msb_h1_lfo1,i,n,foreground=fg)
            self.msb_aspect(msb_h1_lfo2,i,n,foreground=fg)
            self.msb_aspect(msb_h2_lfo1,i,n,foreground=fg)
        msb_h1.update_aspect()
        msb_h1_env1.update_aspect()
        msb_h1_env2.update_aspect()
        msb_h2.update_aspect()
        msb_h2_env1.update_aspect()
        msb_h1_lfo1.update_aspect()
        msb_h1_lfo2.update_aspect()
        msb_h2_lfo1.update_aspect()
        self.norm_slider("harm2_lag",x_harm2+23, y1+74, height=75)
        msb_noise_highpass = self.msb("noise_highpass",len(NOISE_HIGHPASS_FREQUENCIES),x_noise,y0)
        msb_noise_lowpass = self.msb("noise_lowpass",len(NOISE_LOWPASS_FREQUENCIES),x_noise, y0+75)
        for i,n in enumerate(NOISE_HIGHPASS_FREQUENCIES):
            if n < 1000:
                fg = None
            else:
                fg = DEEP_MOD_DEPTH_COLOR
            self.msb_aspect(msb_noise_highpass,i,n,foreground=fg)
        for i,n in enumerate(NOISE_LOWPASS_FREQUENCIES):
            if n < 1000:
                fg = None
            else:
                fg = DEEP_MOD_DEPTH_COLOR
            self.msb_aspect(msb_noise_lowpass,i,n,foreground=fg)
        msb_noise_env = self.msb("noise_lowpass_env1",len(NOISE_FILTER_MOD_RANGE),x_noise,y0+150)
        msb_noise_lfo = self.msb("noise_lowpass_lfo1",len(NOISE_FILTER_MOD_RANGE),x_noise,y0+225)
        for i,n in enumerate(NOISE_FILTER_MOD_RANGE):
            if n < 1000:
                fg = None
            else:
                fg = DEEP_MOD_DEPTH_COLOR
            self.msb_aspect(msb_noise_env,i,n,foreground=fg)
            self.msb_aspect(msb_noise_lfo,i,n,foreground=fg)
        msb_noise_highpass.update_aspect()
        msb_noise_lowpass.update_aspect()
        msb_noise_env.update_aspect()
        msb_noise_lfo.update_aspect()
        self.linear_slider("balance_a",(-1,1),x_mixer,y1)
        self.linear_slider("balance_b",(-1,1),x_mixer+60,y1)
        self.linear_slider("balance_noise",(-1,1),x_mixer+120,y1)
        self.volume_slider("noise_amp",x_mixer+120,y0)
