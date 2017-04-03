# llia.synths.tk.editor2

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.addsr_editor import ADDSREditor
from llia.synths.klstr2.klstr2_constants import *

class TkKlstr2ModPanel(TkSubEditor):

    NAME = "Filter/Mod"
    IMAGE_FILE = "resources/Klstr2/editor2.png"
    TAB_FILE = "resources/Klstr2/tab2.png"

    def __init__(self,editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1000,700,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.NAME)
        editor.add_child_editor(self.NAME, self)

        x0 = 75
        x_f1 = x0
        x_f2 = x_f1+180
        x_env = x_f2+180
        x_lfo = x_env+450
        
        y0 = 75
        y1 = 380

        msb_f1_freq = self.msb("f1_freq",len(FILTER_FREQUENCIES), x_f1, y0)
        msb_f2_freq = self.msb("f2_freq",len(FILTER_FREQUENCIES), x_f2, y0)
        for i,n in enumerate(FILTER_FREQUENCIES):
            if n < 500:
                fg = NORMAL_MOD_DEPTH_COLOR
            elif n < 8000:
                fg = MODERATE_MOD_DEPTH_COLOR
            else:
                fg = DEEP_MOD_DEPTH_COLOR
            self.msb_aspect(msb_f1_freq,i,n,foreground=fg)
            self.msb_aspect(msb_f2_freq,i,n,foreground=fg)
        msb_f1_env1 = self.msb("f1_freq_env1",len(FILTER_MOD_VALUES), x_f1, y0+75)
        msb_f1_lfo1 = self.msb("f1_freq_lfo1",len(FILTER_MOD_VALUES), x_f1, y0+150)
        msb_f1_lfo2 = self.msb("f1_freq_lfo2",len(FILTER_MOD_VALUES), x_f1, y0+225)
        msb_f2_env1 = self.msb("f2_freq_env1",len(FILTER_MOD_VALUES), x_f2, y0+75)
        msb_f2_env2 = self.msb("f2_freq_env2",len(FILTER_MOD_VALUES), x_f2, y0+150)
        msb_f2_lfo1 = self.msb("f2_freq_lfo1",len(FILTER_MOD_VALUES), x_f2, y0+225)
        for i,n in enumerate(FILTER_MOD_VALUES):
            if n < 0:
                bg = NEGATIVE_FILL_COLOR
            else:
                bg = POSITIVE_FILL_COLOR
            if abs(n) < 500:
                fg = NORMAL_MOD_DEPTH_COLOR
            elif abs(n)< 8000:
                fg = MODERATE_MOD_DEPTH_COLOR
            else:
                fg = DEEP_MOD_DEPTH_COLOR
            self.msb_aspect(msb_f1_env1,i,n,foreground=fg,fill=bg)
            self.msb_aspect(msb_f1_lfo1,i,n,foreground=fg,fill=bg)
            self.msb_aspect(msb_f1_lfo2,i,n,foreground=fg,fill=bg)
            self.msb_aspect(msb_f2_env1,i,n,foreground=fg,fill=bg)
            self.msb_aspect(msb_f2_lfo1,i,n,foreground=fg,fill=bg)
            self.msb_aspect(msb_f2_env2,i,n,foreground=fg,fill=bg)
            
        msb_f1_freq.update_aspect()
        msb_f2_freq.update_aspect()
        msb_f1_env1.update_aspect()
        msb_f1_lfo1.update_aspect()
        msb_f1_lfo2.update_aspect()
        msb_f2_env1.update_aspect()
        msb_f2_lfo1.update_aspect()
        msb_f2_lfo1.update_aspect()
        
        self.norm_slider("f1_res",x_f1, y1)
        self.volume_slider("f1_amp",x_f1+60,y1)
        self.linear_slider("f1_pan",(-1,1),x_f1+120,y1)
        self.norm_slider("f2_res",x_f2,y1)
        self.volume_slider("f2_amp",x_f2+60,y1)
        self.linear_slider("f2_pan",(-1,1),x_f2+120,y1)
        self.norm_slider("f2_freq_lag",x_f2+120,y0+75)

        e1 = ADDSREditor(canvas,1,(x_env,y0),(400,250),
                         ("env1_attack","env1_decay1","env1_decay2",
                         "env1_release","env1_breakpoint","env1_sustain",
                          "env1_mode"),self,MAX_ENV_SEGMENT_TIME)
        self.add_child_editor("Env1",e1)
        e1.sync()

        e2 = ADDSREditor(canvas,2,(x_env,y1),(400,250),
                         ("env2_attack","env2_decay1","env2_decay2",
                         "env2_release","env2_breakpoint","env2_sustain",
                          "env2_mode"),self,MAX_ENV_SEGMENT_TIME)
        self.add_child_editor("Env2",e2)
        e2.sync()
        
                                                        
        tlfo = self.tumbler("lfoFreq",5,0.001,x_lfo,y0)
        msb_lfo_ratio = self.msb("lfo2Ratio",len(LFO_RATIOS),x_lfo+6,y0+75)
        for i,n in enumerate(LFO_RATIOS):
            if n < 1:
                fg = NORMAL_MOD_DEPTH_COLOR
            elif n == 1:
                fg = MODERATE_MOD_DEPTH_COLOR
            else:
                fg = DEEP_MOD_DEPTH_COLOR
            self.msb_aspect(msb_lfo_ratio,i,n,foreground=fg)
        msb_lfo_ratio.update_aspect()

        self.norm_slider("vibrato",x_lfo+30,y0+150)

        self.volume_slider("amp",x_lfo+30,y1+75)
