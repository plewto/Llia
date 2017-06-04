# llia.synths.sandcat.tk.editor_filter

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
from llia.synths.sandcat.sandcat_constants import *


class TkFilterPanel(TkSubEditor):

    def __init__(self,editor,trigger_msb_factory):
        name = "Filter"
        tabfile = "resources/Sandcat/tab_filter.png"
        image_file = "resources/Sandcat/editor_filter.png"
        frame = editor.create_tab(name,tabfile)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1500,700,image_file)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,name)
        editor.add_child_editor(name, self)
        x0 = 75
        xmix = x0
        xadsr = xmix+130
        xf = xadsr+230
        xvib = xf+430
        y0, y1 = 75,350
        yvib = 300
        
        for n,y in ((1,y0),(2,y1)):
            e = n+2
            self.volume_slider("ks%d_amp" % n,xmix,y, height=100)
            self.linear_slider("ks%d_pan" % n,(1,-1),xmix,y+125, height=75)
            self.volume_slider("stack%d_amp" % n,xmix+60,y,height=100)
            self.linear_slider("stack%d_pan" % n,(1,-1),xmix+60,y+125, height=75)
            self.exp_slider("env%d_attack" % e, MAX_ENV_SEGMENT, xadsr, y)
            self.exp_slider("env%d_decay" % e, MAX_ENV_SEGMENT, xadsr+30, y)
            self.norm_slider("env%d_sustain" % e, xadsr+60, y)
            self.exp_slider("env%d_decay" % e, MAX_RELEASE_SEGMENT, xadsr+90, y)
            self.toggle("env%d_trig_mode" % e ,xadsr+138,y,off=(0,"Gate"),on=(1,"Trig"))
            trigger_msb_factory(self,"env%d_trig_src" % e,xadsr+130,y+75)
            self.exp_slider("f%d_cutoff" % n, MAX_FILTER_CUTOFF, xf,y,degree=FILTER_SLIDER_DEGREE)
            self.linear_slider("f%d_track" % n, (0, MAX_FILTER_TRACK), xf+60,y)
            self.exp_slider("f%d_env%d" % (n,n+2), MAX_FILTER_MOD, xf+120,y,checkbutton=(-15,150),degree=FILTER_SLIDER_DEGREE)
            self.exp_slider("f%d_lfo%d" % (n,n),MAX_FILTER_MOD, xf+180,y,degree=FILTER_SLIDER_DEGREE)
            self.exp_slider("f%d_lfov" % n, MAX_FILTER_MOD, xf+240, y,degree=FILTER_SLIDER_DEGREE)
            self.norm_slider("f%d_res" % n, xf+300, y)
            self.linear_slider("f%d_pan" % n, (-1,1), xf+360, y)
        self.volume_slider("amp",xvib+60,y0)
        # # Vibrato
        self.tumbler("vfreq",5,0.001,xvib+92,yvib)
        self.linear_slider("vdelay",(0,2),xvib,yvib+50)
        self.norm_slider("vsens",xvib+60,yvib+50)
        self.norm_slider("vdepth",xvib+120,yvib+50)
        self.norm_slider("vxbus1",xvib+180,yvib+50)
        
        
