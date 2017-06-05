# llia.synths.sandcat.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
from llia.synths.sandcat.sandcat_constants import *
from llia.synths.sandcat.tk.editor_filter import TkFilterPanel


    
def trigger_msb_factory(editor,param,x,y):
    msb = editor.msb(param,len(TRIGER_SOURCES),x,y,width=76)
    for i,pair in enumerate(TRIGER_SOURCES):
        val,txt = pair
        editor.msb_aspect(msb,i,val,text=txt)
    msb.update_aspect()
    return msb

def create_editor(parent):
    TkStackPanel(parent, 1)
    TkStackPanel(parent, 2)
    TkFilterPanel(parent, trigger_msb_factory)
    TkBlockDiagram(parent)


class TkStackPanel(TkSubEditor):

    def __init__(self,editor,n):
        name = "Stack %d" % n
        tabfile = "resources/Sandcat/tab_%d.png" % n
        image_file = "resources/Sandcat/editor_s%d.png" % n
        frame = editor.create_tab(name,tabfile)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1500,700,image_file)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,name)
        editor.add_child_editor(name, self)
        def ex(suffix):
            return "ex%d_%s" % (n,suffix)
        def ks(suffix):
            return "ks%d_%s" % (n,suffix)
        def stack(suffix):
            return "stack%d_%s" % (n,suffix)
        def mod(suffix):
            return "mod%d_%s" % (n,suffix)
        def car(suffix):
            return "car%d_%s" % (n,suffix)
        x0 = 75
        xex = x0
        y0, y1, y2 = 75, 350, 575

        msb_harmonic = self.msb(ex("harmonic"),len(EX_HARMONICS),xex,y0)
        msb_lfo = self.msb(ex("lfo%d" % n),len(EX_HARMONICS_MOD),xex,y0+75)
        msb_env = self.msb(ex("env%d" % n),len(EX_HARMONICS_MOD),xex,y0+150)
        for i,h in enumerate(EX_HARMONICS):
            self.msb_aspect(msb_harmonic,i,h)
        for i,h in enumerate(EX_HARMONICS_MOD):
            self.msb_aspect(msb_lfo,i,h)
            self.msb_aspect(msb_env,i,h)
        msb_harmonic.update_aspect()
        msb_lfo.update_aspect()
        msb_env.update_aspect()
        xpw = xex + 75
        msb_pw = self.msb(ex("pw"),len(EX_PW),xpw, y0)
        for i,w in enumerate(EX_PW):
            self.msb_aspect(msb_pw,i,w)
        msb_pwm = self.msb(ex("pw_lfo%d" % n),len(EX_PWM),xpw,y0+75)
        for i,w in enumerate(EX_PWM):
            self.msb_aspect(msb_pwm,i,w)
        msb_pw.update_aspect()
        msb_pwm.update_aspect()
        self.toggle(ex("noise_select"),xpw+75,y0,off=(0,"White"),on=(1,"Pink"))
        self.linear_slider(ex("source_mix"),(-1,1),xpw+99, y0+75, height=100)
        xks = xpw+150
        self.tumbler(ks("ratio"),5,0.001,xks,y0,range_=(0,16000))
        trigger_msb_factory(self,ks("trig_src"),xks,y0+75)
        xksd = xks+100
        self.exp_slider(ks("decay"),MAX_ENV_SEGMENT,xksd,y0)
        self.norm_slider(ks("coef"),xksd+60,y0)
        self.norm_slider(ks("velocity"),xksd+120,y0)
        xfm = xksd+180
        self.tumbler(mod("ratio"),5,0.001,xfm,y0,range_=(0,16000))
        self.tumbler(mod("bias"),5,0.01,xfm,y0+75,range_=(0,99999))
        self.tumbler(car("ratio"),5,0.001,xfm,y1,range_=(0,16000))
        self.tumbler(car("bias"),5,0.01,xfm,y1+75,range_=(0,99999))
        xmod = xfm+100
        self.exp_slider(mod("ks%d" % n),MAX_FM_DEPTH,xmod,y0,degree=FM_SLIDER_DEGREE)
        self.exp_slider(car("ks%d" % n),MAX_FM_DEPTH,xmod,y1,degree=FM_SLIDER_DEGREE)
        self.exp_slider(car("mod1"),MAX_FM_DEPTH,xmod+60,y1,degree=FM_SLIDER_DEGREE)
        if n==2:
            self.exp_slider(car("mod2"),MAX_FM_DEPTH,xmod+120,y1,degree=FM_SLIDER_DEGREE)
        self.exp_slider(stack("fb"),8,xmod+60,y0,degree=3)
        self.exp_slider(stack("fb_lfo%d" % n),4,xmod+120,y0)
        xenv = xmod+180
        self.norm_slider(mod("env%d" % n),xenv,y0, height=75)
        self.norm_slider(mod("lag"),xenv,y0+100,height=75)
        self.toggle(car("env_mode"),xenv-24,y1,off=(0,"Env"),on=(1,"Gate"))
        self.norm_slider(mod("lfo%d" % n), xenv+60, y0)
        self.norm_slider(car("lfo%d" % n), xenv+60, y1)
        self.norm_slider(mod("velocity"), xenv+120, y0)
        self.norm_slider(car("velocity"), xenv+120, y1)
        # msb_break = self.msb(stack("break_key"),len(BREAK_KEYS),xfm+75,y0+212)
        # for i,pair in enumerate(BREAK_KEYS):
        #     v,text = pair
        #     self.msb_aspect(msb_break,i,v,text=text)
        # msb_break.update_aspect()
        # msb_mleft = self.msb(mod("left_scale"),len(KEY_SCALES),xfm, y0+192)
        # msb_cleft = self.msb(car("left_scale"),len(KEY_SCALES),xfm, y1-72)
        # msb_mright = self.msb(mod("right_scale"),len(KEY_SCALES),xfm+150, y0+192)
        # msb_cright = self.msb(car("right_scale"),len(KEY_SCALES),xfm+150, y1-72)
        # for i,v in enumerate(KEY_SCALES):
        #     text = "%d db" % v
        #     if v>0: text = "+"+text
        #     self.msb_aspect(msb_mleft,i,v,text=text)
        #     self.msb_aspect(msb_cleft,i,v,text=text)
        #     self.msb_aspect(msb_mright,i,v,text=text)
        #     self.msb_aspect(msb_cright,i,v,text=text)
        # msb_mleft.update_aspect()
        # msb_cleft.update_aspect()
        # msb_mright.update_aspect()
        # msb_cright.update_aspect()
        # ADSR
        xadsr = x0
        yadsr = y1
        def env(suffix):
            return "env%d_%s" % (n,suffix)
        self.exp_slider(env("attack"),MAX_ENV_SEGMENT,xadsr,yadsr)
        self.exp_slider(env("decay"),MAX_ENV_SEGMENT,xadsr+30,yadsr)
        self.norm_slider(env("sustain"),xadsr+60,yadsr)
        self.exp_slider(env("release"),MAX_RELEASE_SEGMENT,xadsr+90,yadsr)
        self.toggle(env("trig_mode"),xadsr+138,yadsr,off=(0,"Gate"),on=(1,"Trig"))
        trigger_msb_factory(self,env("trig_src"),xadsr+130,yadsr+75)
        # LFO/Clock
        xlfo = xadsr+230
        ylfo = yadsr
        def lfo(suffix):
            return "lfo%d_%s" % (n,suffix)
        self.tumbler(lfo("ratio"),5,0.001,xlfo,ylfo)
        m = {1:2,2:1}[n]
        self.linear_slider(lfo("freq_lfo%d" % m),(0,MAX_LFO_XMOD),xlfo+100,ylfo)
        self.tumbler("clk%d_ratio" % n,5,0.001,xlfo,ylfo+75)
        # Key Scale
        xleft = xfm
        xright = xleft + 300
        msb_mleft = self.msb(mod("left_scale"),len(KEY_SCALES),xleft, y2)
        msb_mright = self.msb(mod("right_scale"),len(KEY_SCALES),xleft+75, y2)

        msb_cleft = self.msb(car("left_scale"),len(KEY_SCALES),xright, y2)
        msb_cright = self.msb(car("right_scale"),len(KEY_SCALES),xright+75, y2)
        for i,v in enumerate(KEY_SCALES):
            text = "%d db" % v
            if v>0: text = "+"+text
            self.msb_aspect(msb_mleft,i,v,text=text)
            self.msb_aspect(msb_cleft,i,v,text=text)
            self.msb_aspect(msb_mright,i,v,text=text)
            self.msb_aspect(msb_cright,i,v,text=text)
        msb_mleft.update_aspect()
        msb_cleft.update_aspect()
        msb_mright.update_aspect()
        msb_cright.update_aspect()

        msb_break = self.msb(stack("break_key"),len(BREAK_KEYS),xleft+188,y2)
        for i,pair in enumerate(BREAK_KEYS):
            v,text = pair
            self.msb_aspect(msb_break,i,v,text=text)
        msb_break.update_aspect()



class TkBlockDiagram(TkSubEditor):

    def __init__(self,editor):
        name = "Block Diagram"
        tabfile = "resources/Sandcat/tab.png"
        image_file = "resources/Sandcat/block_diagram.png"
        frame = editor.create_tab(name,tabfile)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1500,700,image_file)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,name)
        editor.add_child_editor(name, self)
     
