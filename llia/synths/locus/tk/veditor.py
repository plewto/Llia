# llia.synths.locus.tk.veditor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
from llia.gui.tk.addsr_editor import ADDSREditor
from llia.synths.locus.locus_constants import *


class TkLocusVEditor(TkSubEditor):

    def __init__(self,editor):
        self.image_file = "resources/Locus/editor_v.png"
        self.tab_file = "resources/Locus/tab_v.png"
        self.name = "Vector"
        frame = editor.create_tab(self.name,self.tab_file)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1200,800,self.image_file)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.name)
        editor.add_child_editor(self.name, self)
        x0 = 75
        y0,y1 = 75,300
        self.tumbler("vfreq",5,0.001,x0,y0)
        self.norm_slider("vdelay",x0+30,y0+48,height=100)
        self.norm_slider("vsens",x0+100,y0)
        self.norm_slider("vdepth",x0+160,y0)
        x_xvector = x0+232
        y_xvector = y0
        x_yvector = x_xvector
        y_yvector = y1
        msb_xratio = self.msb("lfox_ratio",len(VECTOR_LFO_RATIOS),x_xvector,y_xvector)
        msb_yratio = self.msb("lfoy_ratio",len(VECTOR_LFO_RATIOS),x_yvector,y_yvector)
        for i,pair in enumerate(VECTOR_LFO_RATIOS):
            text,value = pair
            self.msb_aspect(msb_xratio,i,value,text=text)
            self.msb_aspect(msb_yratio,i,value,text=text)
        msb_xratio.update_aspect()
        msb_yratio.update_aspect()
        for v in "xy":
            if v == 'x':
                xpos, ypos = x_xvector,y_xvector
            else:
                xpos, ypos = x_yvector,y_yvector
            self.norm_slider("lfo%s_delay" % v, xpos+24,ypos+48,height=100)
            self.linear_slider("%spos" % v, (-1,1),xpos+100,ypos)
            self.linear_slider("%spos_env1" % v, (-1,1),xpos+160,ypos)
            self.linear_slider("%spos_lfo" % v, (-1,1),xpos+220,ypos)
            self.linear_slider("%spos_%sbus" % (v,v),(-1,1),xpos+280,ypos)
            self.volume_slider("%samp" % v,xpos+340,ypos)

        x_main_amp = 750
        self.volume_slider("amp",x_main_amp,y0)

            
        
class TkLocusEnvEditor(TkSubEditor):

    def __init__(self,editor):
        self.image_file = "resources/Locus/editor_env.png"
        self.tab_file = "resources/Locus/tab_env.png"
        self.name = "Envelopes"
        frame = editor.create_tab(self.name,self.tab_file)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1200,800,self.image_file)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.name)
        editor.add_child_editor(self.name, self)
        w,h = 900,250
        x0,y0 = 75,50
        y1,y2 = y0,y0+h+40
        e1 = ADDSREditor(canvas,1,(x0,y1),(w,h),
                         ("env1_attack","env1_decay1","env1_decay2",
                          "env1_release","env1_breakpoint","env1_sustain",
                          "env1_mode"),self,MAX_ENV_SEGMENT_TIME)
        e2 = ADDSREditor(canvas,2,(x0,y2),(w,h),
                         ("env2_attack","env2_decay1","env2_decay2",
                          "env2_release","env2_breakpoint","env2_sustain",
                          "env2_mode"),self,MAX_ENV_SEGMENT_TIME)
        self.add_child_editor("Env1",e1)
        self.add_child_editor("Env2",e2)
        e1.sync()
        e2.sync()
        

        
        
