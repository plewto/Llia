# llia.synths.slug.tk.editor2

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.synths.slug.slug_constants import *

class TkSlugEnvPanel(TkSubEditor):

    NAME = "Env/Mix"
    IMAGE_FILE = "resources/Slug/editor_env.png"
    TAB_FILE = "resources/Slug/tab_env.png"

    def __init__(self,editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,842,598,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.NAME)
        editor.add_child_editor(self.NAME, self)
        x0 = 75
        xenv = x0
        xlfo = xenv+370
        y0 = 75
        y1 = 300
        # Envelopes
        for n in (1,2):
            y = {1:y0, 2:y1}[n]
            def time_slider(suffix,xoffset):
                param = "env%d_%s" % (n,suffix)
                self.exp_slider(param,MAX_ENV_SEGMENT_TIME,xenv+xoffset,y)
            time_slider("attack",0)
            time_slider("decay",60)
            time_slider("release",180)
            self.norm_slider("env%d_sustain" % n,xenv+120,y)
            self.linear_slider("env%d_velocity_attack" % n,(-1,1),xenv+240,y,height=75)
            self.linear_slider("env%d_key_attack" % n,(-1,1),xenv+240,y+80,height=75)
            self.exp_slider("penv%d_decay" % n,MAX_ENV_SEGMENT_TIME,xenv+300,y)
        self.toggle("env_mode",xenv,y1+200,off=(0,"Gate"),on=(1,"Trig"))

        # LFO
        ylfo1 = y0+60
        self.tumbler("vfreq",5,0.001,xlfo, y0)
        self.linear_slider("vdelay",(0,2),xlfo,ylfo1, height=100)
        self.norm_slider("vsens",xlfo+60,ylfo1, height=100)
        self.norm_slider("vdepth",xlfo+120,y0)
        self.norm_slider("vnoise",xlfo+180,y0)
        self.norm_slider("xpitch",xlfo+240,y0)
        # Misc
        xmisc = xlfo
        self.norm_slider("port",xmisc,y1)
        self.norm_slider("velocity_port",xmisc+60,y1)
        msb_break = self.msb("break_key",len(BREAK_KEYS),xmisc,y1+200)
        for i,p in enumerate(BREAK_KEYS):
            v,txt = p
            self.msb_aspect(msb_break,i,v,text=txt)
        msb_break.update_aspect()
        # Mixers
        xmix = x = xlfo+120
        y = y1
        for p in ("pulse_","pluck_","car1_","car2_"):
            param = "%samp" % p
            self.volume_slider(param,x,y)
            x += 60
        self.volume_slider("amp", xlfo+300, y0)
        
