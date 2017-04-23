# llia.synths.sol.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
# import llia.gui.tk.control_factory as cf
from llia.synths.sol.tk.mod_editor import TkSolModEditor,TkSolVectorEditor
from llia.synths.sol.sol_constants import *

def create_editor(parent):
    TkSolPanel('x',parent)
    TkSolPanel('y',parent)
    TkSolVectorEditor(parent)
    TkSolModEditor(parent)

class TkSolPanel(TkSubEditor):

    def __init__(self,stack,editor):
        self.name = "Sol %s" % stack
        self.image_file = "resources/Sol/editor_%s.png" % stack
        self.tab_file = "resources/Sol/tab_%s.png" % stack
        frame = editor.create_tab(self.name,self.tab_file)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1000,700,self.image_file)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.name)
        editor.add_child_editor(self.name, self)

        x0 = 50
        xop = x0
        xfilter = 640
        y0 = 75
        y1 = 300

        if stack == 'x':
            self.init_fm_op('a',xop,y0)
            self.init_fm_op('b',xop,y1)
        else:
            self.init_wv_op('c',xop,y0)
            self.init_wv_op('d',xop,y1)

        self.init_stack_filter(stack,xfilter,y0,y1)
            
    def init_fm_op(self,op,x,y):
        mod = op
        self.tumbler("op%s_mod_ratio" % op, 5, 0.001, x, y)
        msb_scale = self.msb("op%s_mod_scale" % op,len(MOD_SCALES),x,y+60)
        for i,v in enumerate(MOD_SCALES):
            self.msb_aspect(msb_scale,i,v)
        msb_scale.update_aspect()
        self.norm_slider("op%s_mod_depth" % op,x+100,y)
        self.norm_slider("op%s_mod_%senv" % (op,mod),x+160,y)
        self.norm_slider("op%s_mod_%slfo" % (op,mod),x+220,y)
        xc = x+280
        self.tumbler("op%s_car_ratio" % op,5,0.001,xc,y)
        self.tumbler("op%s_car_bias" % op,5,0.001,xc,y+60)
        self.tumbler("op%s_feedback" % op,5,0.001,xc+100,y)
        self.tumbler("op%s_cross_feedback" % op,5,0.001,xc+100,y+60)
        self.volume_slider("op%s_amp" % op,xc+230,y)

   
    def init_stack_filter(self,stack,x,y0,y1):
        mod = {'x':'a','y':'b'}[stack]
        self.exp_slider("%sfilter_freq" % stack,16000,x,y0)
        track_values = (0,0.5,1,2)
        msb = self.msb("%sfilter_track" % stack,len(track_values),x+60,y0+60)
        for i,v in enumerate(track_values):
            self.msb_aspect(msb,i,v)
        msb.update_aspect()
        self.norm_slider("%sfilter_res" % stack,x+160,y0)
        self.exp_slider("%sfilter_freq_%senv" % (stack,mod),16000,x,y1,checkbutton=(-15,184))
        self.exp_slider("%sfilter_freq_cenv" % stack,16000,x+60,y1,checkbutton=(-15,184))
        self.exp_slider("%sfilter_freq_%slfo" % (stack,mod),8000,x+120,y1,checkbutton=(-15,184))
        self.exp_slider("%sfilter_freq_vlfo" % stack,8000,x+180,y1,checkbutton=(-15,184))
        
    def init_wv_op(self,op,x,y):
        mod = {'c':'a','d':'b'}[op]
        self.tumbler("op%s_saw_ratio" % op, 5,0.001,x,y)
        self.tumbler("op%s_pulse_ratio" % op, 5,0.001,x,y+75)
        self.norm_slider("op%s_pulse_width" % op, x+100,y,height=75)
        self.norm_slider("op%s_pulse_width_%slfo" % (op,mod),x+100,y+100,height=75)
        xwave = x+170
        self.linear_slider("op%s_wave" % op,(0,1),xwave,y)
        self.linear_slider("op%s_wave_%senv" % (op,mod),(-1,1),xwave+60,y)
        self.linear_slider("op%s_wave_%slfo" % (op,mod),(-1,1),xwave+120,y)
        xnoise = xwave+190
        self.volume_slider("op%s_noise_amp" % op,xnoise,y)
        xfilter = xnoise+60
        tracks = (1,2,3,4,5,6,7,8,9,12,16,24,32,64)
        msb_track=self.msb("op%s_filter_track" % op,len(tracks),xfilter,y)
        msb_env  =self.msb("op%s_filter_%senv" % (op,mod),len(tracks)+1,xfilter,y+75)
        for i,v in enumerate(tracks):
            self.msb_aspect(msb_track,i,v)
            self.msb_aspect(msb_env,i,v)
        self.msb_aspect(msb_env,len(tracks),0)
        msb_track.update_aspect()
        msb_env.update_aspect()
        self.volume_slider("op%s_amp" %op,xfilter+100,y)
        
