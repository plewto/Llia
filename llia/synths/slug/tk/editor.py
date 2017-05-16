# llia.synths.slug.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.synths.slug.tk.editor_fm import TkSlugFMPanel
from llia.synths.slug.tk.editor_env import TkSlugEnvPanel
from llia.synths.slug.slug_constants import *

def create_editor(parent):
    TkSlugKSPanel(parent)
    TkSlugFMPanel(parent)
    TkSlugEnvPanel(parent)
    
class TkSlugKSPanel(TkSubEditor):

    NAME = "Pulse/Pluck"
    IMAGE_FILE = "resources/Slug/editor_ks.png"
    TAB_FILE = "resources/Slug/tab_ks.png"

    def __init__(self,editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,813,562,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.NAME)
        editor.add_child_editor(self.NAME, self)
        x0 = 75
        xpw = x0
        xfilter = x0+130
        xvelocity = xfilter+360
        xscale = xfilter+420

        
        y0 = 75
        y1 = y0+80
        y2 = y0+250

        # Pulse controls
        self.tumbler("pulse_ratio",5,0.001,x0,y0)
        self.norm_slider("pulse_width", xpw, y1, height=75)
        self.norm_slider("pulse_width_env1", xpw+40, y1, height=75)
        self.norm_slider("pulse_width_lfo", xpw+80, y1, height=75)
        self.norm_slider("pulse_filter_res", xfilter, y0)
        self.exp_slider("pulse_filter_cutoff", 16000,xfilter+60,y0,degree=3)
        def filter_mod(param,x,mx=16000):
            param = "pulse_filter_%s" % param
            self.exp_slider(param,mx,x,y0,degree=3,checkbutton=(-15,150))
        filter_mod("env1",xfilter+120)
        filter_mod("penv1",xfilter+180)
        filter_mod("lfo",xfilter+240)
        filter_mod("x",xfilter+300)
        filter_mod("velocity",xvelocity)
        count = len(FILTER_KEY_SCALES)
        msb_left = self.msb("pulse_filter_left_track",count,xscale,y0)
        msb_right = self.msb("pulse_filter_right_track",count,xscale,y0+60)
        for i,p in enumerate(FILTER_KEY_SCALES):
            v,txt = p
            self.msb_aspect(msb_left,i,v,text=txt)
            self.msb_aspect(msb_right,i,v,text=txt)
        msb_left.update_aspect()
        msb_right.update_aspect()
        #self.toggle("pulse_enable",xfilter+420,y0+120)   
        self.norm_slider("pulse_amp_env",xfilter+520,y0)
        
        # KS Controls
        xexcite = x0-10
        yexcite = y2+80
        #xdecay = x0+120
        self.tumbler("pluck_ratio",5,0.001,x0,y2)
        msb_harmonic = self.msb("pluck_harmonic", len(PLUCK_HARMONICS),xexcite, yexcite)
        for i,v in enumerate(PLUCK_HARMONICS):
            self.msb_aspect(msb_harmonic,i,v)
        msb_harmonic.update_aspect()
        self.toggle("pluck_width",xexcite, yexcite+60, off=(0,"Odd"), on=(1, "Even"))
        self.norm_slider("pluck_excite",xexcite+80,yexcite,height=88)
        self.norm_slider("pluck_damp",xfilter,y2)
        self.exp_slider("pluck_decay",MAX_PLUCK_DECAY,xfilter+60,y2)
        self.norm_slider("pluck_velocity",xvelocity,y2)
        count = len(DB_KEY_SCALES)
        msb_left = self.msb("pluck_left_scale",count,xscale,y2)
        msb_right = self.msb("pluck_right_scale",count,xscale,y2+60)
        for i,v in enumerate(DB_KEY_SCALES):
            self.msb_aspect(msb_left,i,v)
            self.msb_aspect(msb_right,i,v)
        msb_left.update_aspect()
        msb_right.update_aspect()
        #self.toggle("pluck_enable",xscale,y2+120)   
