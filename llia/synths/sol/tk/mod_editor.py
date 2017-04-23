# llia.synths.sol.tk.mod_editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
from llia.gui.tk.addsr_editor import ADDSREditor
from llia.synths.sol.sol_constants import *


class TkSolModEditor(TkSubEditor):

    def __init__(self,editor):
        self.name = "Sol Mod"
        self.image_file = "resources/Sol/editor_mod.png" 
        self.tab_file = "resources/Sol/tab_mod.png"
        frame = editor.create_tab(self.name,self.tab_file)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1200,700,self.image_file)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.name)
        editor.add_child_editor(self.name, self)
        x0 = 50
        y0 = 75
        y1 = 330
        self.tumbler("timebase",5,0.001,x0,y0)
        self.norm_slider("port",x0+30,y1)
        xvib = x0+100
        msb_vratio = self.msb("vratio",len(LFO_RATIOS),xvib,y0)
        self.linear_slider("vdelay",(0,MAX_LFO_DELAY),xvib+100,y0)
        self.norm_slider("vsens",xvib+160,y0)
        self.norm_slider("vdepth",xvib+220,y0)
        self.norm_slider("pitch_ctrlbus",xvib+280,y0)
        msb_aratio = self.msb("alfo_ratio",len(LFO_RATIOS),xvib,y1)
        self.linear_slider("alfo_delay",(0,MAX_LFO_DELAY),xvib+100,y1)
        msb_bratio = self.msb("blfo_ratio",len(LFO_RATIOS),xvib+180,y1)
        self.linear_slider("blfo_delay",(0,MAX_LFO_DELAY),xvib+280,y1)
        lfo_ratio_msblist = (msb_vratio,msb_aratio,msb_bratio)
        for i,r in enumerate(LFO_RATIOS):
            n,d = r.numerator,r.denominator
            if d == 1:
                txt = "%d" % n
            else:
                txt = "%d/%d" % (n,d)
            for msb in lfo_ratio_msblist:
                self.msb_aspect(msb,i,float(r),text=txt)
        for msb in lfo_ratio_msblist:
            msb.update_aspect()
        def env_slider(param,x,y):
            self.exp_slider(param,MAX_ENV_SEGMENT_TIME,x,y)
        xenv = xvib+340
        for q in "ab":
            if q == 'a':
                y = y0
            else:
                y = y1
            env_slider("%senv_attack" % q,xenv,y)
            env_slider("%senv_decay" % q,xenv+40,y)
            self.norm_slider("%senv_sustain" % q,xenv+80,y)
            env_slider("%senv_release" % q,xenv+120,y)
            self.toggle("%senv_lfo_trig" % q,xenv,y+175)
        xcenv = xenv+170
        cenv = ADDSREditor(canvas,1,(xcenv,y0),(400,400),
                           ("cenv_attack","cenv_decay1","cenv_decay2",
                            "cenv_release","cenv_breakpoint","cenv_sustain",
                            "cenv_trig_mode"),
                           self,MAX_ENV_SEGMENT_TIME)
        self.add_child_editor("Cenv",cenv)
        cenv.sync()


class TkSolVectorEditor(TkSubEditor):

    def __init__(self,editor):
        self.name = "Sol Vector"
        self.image_file = "resources/Sol/editor_vector.png" 
        self.tab_file = "resources/Sol/tab_vector.png"
        frame = editor.create_tab(self.name,self.tab_file)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1000,700,self.image_file)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.name)
        editor.add_child_editor(self.name, self)
        x0 = 50
        y0 = 75
        y1 = 330

        def env_slider(param,x,y):
            self.exp_slider(param,MAX_ENV_SEGMENT_TIME,x,y)
        
        for v in "xy":
            if v=='x':
                y = y0
            else:
                y = y1
            msb = self.msb("%slfo_ratio" % v, len(LFO_RATIOS),x0,y)
            for i,r in enumerate(LFO_RATIOS):
                n,d = r.numerator,r.denominator
                if d == 1:
                    txt = "%d" % n
                else:
                    txt = "%d/%d" % (n,d)
                self.msb_aspect(msb,i,float(r),text=txt)
            msb.update_aspect()
            self.norm_slider("%slfo_wave" % v,x0+100,y)
            self.linear_slider("%slfo_delay" % v,(0,MAX_LFO_DELAY),x0+160,y)
            xenv = x0+220
            env_slider("%senv_attack" % v,xenv,y)
            env_slider("%senv_decay" % v, xenv+40,y)
            self.norm_slider("%senv_sustain" % v, xenv+80,y)
            env_slider("%senv_release" % v, xenv+120,y)
            self.toggle("%senv_lfo_trig" % v,xenv,y+175)

            xpos = xenv+180
            self.linear_slider("%spos" % v, (-1,1),xpos,y)
            self.linear_slider("%spos_%senv" % (v,v),(-1,1),xpos+60,y)
            self.linear_slider("%spos_%slfo" % (v,v),(-1,1),xpos+120,y)
            self.linear_slider("%spos_v%sbus" % (v,v),(-1,1),xpos+180,y)
            self.volume_slider("%samp" % v,xpos+240,y)

        self.volume_slider("amp",x0+720,(y0+y1)/2)

                
                
