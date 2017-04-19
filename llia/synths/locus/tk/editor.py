# llia.synths.locus.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
from llia.synths.locus.tk.veditor import TkLocusVEditor,TkLocusEnvEditor
from llia.synths.locus.locus_constants import *


def create_editor(parent):
    TkLocusStackPanel(1,parent)
    TkLocusStackPanel(2,parent)
    TkLocusVEditor(parent)
    TkLocusEnvEditor(parent)

class TkLocusStackPanel(TkSubEditor):

    # stack 1 -> x-axis  ops A and C
    # stack 2 -> y-axis  ops B and D
    #
    def __init__(self,stack,editor):
        self.image_file = "resources/Locus/editor_%d.png" % stack
        self.tab_file = "resources/Locus/tab_%d.png" % stack
        self.name = "Locus %d" % stack
        frame = editor.create_tab(self.name,self.tab_file)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1148,697,self.image_file)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.name)
        editor.add_child_editor(self.name, self)
        x0 = 50
        xfm = xsub = x0+360
        y0,y1 = 75,400
        if stack == 1:
            fmop = "a"
            subop = "c"
        else:
            fmop = "b"
            subop = "d"
        self._layout_common(fmop,x0,y0)
        self._layout_fm_op(fmop,xfm,y0)
        self._layout_common(subop,x0,y1)
        self._layout_sub_op(subop,xsub,y1)
            
    def _layout_common(self,op,x,y):
        xlfo = x
        xpitch = xlfo + 100
        xdelay = xpitch + 132
        xamp = xdelay+60
        ylfo = y
        msb_lfo = self.msb("op%s_lfo_ratio" % op,len(OP_LFO_RATIOS),xlfo,ylfo)
        for i,pair in enumerate(OP_LFO_RATIOS):
            txt,value = pair
            self.msb_aspect(msb_lfo,i,value,text=txt)
        msb_lfo.update_aspect()
        self.norm_slider("op%s_lfo_wave" % op,xlfo+23,ylfo+60, height=90)
        self.linear_slider("op%s_pitch_env1" % op, (-1,1),xpitch,y)
        self.linear_slider("op%s_pitch_lfo" % op, (-1,1),xpitch+60,y)
        self.norm_slider("op%s_env_delay" % op, xdelay,y)
        self.volume_slider("op%s_amp" % op,xamp,y)

    def _layout_fm_op(self,op,x,y):
        xmod = x
        xcar = xmod+292
        self.tumbler("op%s_mod_ratio" % op, 5, 0.001, xmod,y)
        msb_scale = self.msb("op%s_mod_scale" % op, len(MODULATOR_SCALES),xmod+7,y+60)
        for i,v in enumerate(MODULATOR_SCALES):
            self.msb_aspect(msb_scale,i,v)
        msb_scale.update_aspect()
        self.norm_slider("op%s_mod_depth" % op, xmod+100,y)
        self.norm_slider("op%s_mod_env1" % op, xmod+160,y)
        self.norm_slider("op%s_mod_lfo" % op, xmod+220,y)
        # Carrier
        self.tumbler("op%s_car_ratio" % op, 5, 0.001, xcar,y)
        self.tumbler("op%s_car_bias" % op, 5, 0.001, xcar,y+75)
        self.norm_slider("op%s_feedback" % op, xcar+100,y)
        
    def _layout_sub_op(self,op,x,y):
        xtune = x
        xpwidth = xtune+120
        xnoise = xpwidth+120
        xwave = xnoise+110
        xfilter = xwave+180
        yfilter = y - 50
        self.tumbler("op%s_sine_ratio" % op, 5, 0.001, xtune, y)
        self.tumbler("op%s_pulse_ratio" % op, 5, 0.001, xtune, y+60)
        self.tumbler("op%s_saw_ratio" % op, 5, 0.001, xtune, y+120)
        self.norm_slider("op%s_pulse_width" % op,xpwidth,y)
        self.norm_slider("op%s_pulse_width_lfo" %op,xpwidth+60,y)
        self.volume_slider("op%s_noise_amp" % op,xnoise,y)
        self.exp_slider("op%s_noise_highpass" % op, MAX_NOISE_CUTOFF,xnoise+50,y,height=75)
        self.exp_slider("op%s_noise_lowpass" % op, MAX_NOISE_CUTOFF,xnoise+50,y+125,height=75)
        self.norm_slider("op%s_wave" % op, xwave,y,height=200)
        self.linear_slider("op%s_wave_env1" % op, (-1,1),xwave+60,y,height=200)
        self.linear_slider("op%s_wave_lfo" % op, (-1,1),xwave+120,y,height=200)
        self.tumbler("op%s_filter_freq" % op, 5, 1,xfilter+37,yfilter)
        self.linear_slider("op%s_filter_freq_env1" % op, (-8000,8000),xfilter+7,yfilter+50, height=200)
        self.linear_slider("op%s_filter_freq_lfo" % op, (-8000,8000),xfilter+67,yfilter+50, height=200)
        self.norm_slider("op%s_filter_res" % op, xfilter+127,yfilter+50, height=200)

