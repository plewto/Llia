# llia.synths.corvus.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB, ToggleButton
from llia.gui.tk.tumbler import Tumbler
from llia.gui.tk.addsr_editor import ADDSREditor

from llia.synths.corvus.tk.misc_editor import TkCorvusMiscPanel
from llia.synths.corvus.corvus_constants import *

def create_editor(parent):
    for op in (1,2,3,4):
        TkCorvusOpPanel(op,parent)
    TkCorvusMiscPanel(parent)

class TkCorvusOpPanel(TkSubEditor):

    def __init__(self, n, editor):
        name = "OP%d" % n
        image_file = "resources/Corvus/editor_%d.png" % n
        tab_file =   "resources/Corvus/tab_%d.png" % n
        frame = editor.create_tab(name,tab_file)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 1053, 663, image_file)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, name)
        editor.add_child_editor(name, self)
        self.op = n
        
        y0 = 50
        y_carrier = y0
        y_mod = y_carrier
        y_env = y0 + 250
        
        x0 = 50
        x_fm = x0
        x_mod_lfo1 = x_fm + 100
        x_mod_lfo2 = x_mod_lfo1 + 60
        x_mod_external = x_mod_lfo2 + 60
        x_mod_keyscale = x_mod_lfo2 + 100
        x_mod_amp = x_mod_keyscale + 87

        x_carrier = x_mod_amp + 100
        x_ratio = x_carrier
        x_velocity = x_ratio+120
        x_lfo1 = x_velocity+60
        x_lfo2 = x_lfo1+60
        x_external = x_lfo2+60
        x_keyscale = x_external + 60
        x_enable = x_keyscale + 90

        x_env = x0-22
       
        
        
        def norm_slider(param,x,y,height=150):
            s = cf.normalized_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y,height=height)
            return s

        def volume_slider(param,x,y,height=150):
            s = cf.volume_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y,height=height)
            return s

        def linear_slider(param,range_,x,y):
            s = cf.linear_slider(canvas,param,editor,range_=range_)
            self.add_control(param,s)
            s.widget().place(x=x,y=y)
            return s
        
        def tumbler(param,digits,scale,x,y):
            t = Tumbler(canvas,param,editor,digits=digits,scale=scale)
            self.add_control(param,t)
            t.layout((x,y))
            t.update_aspect()
            return t

        def msb_keyscale(param,x,y):
            count = len(KEYSCALES)
            msb = MSB(canvas,param,editor,count)
            for i,s in enumerate(KEYSCALES):
                d = {"fill" : CFILL,
                     "foreground" : CFOREGROUND,
                     "outline" : COUTLINE,
                     "value" : s,
                     "text" : "%+d" % s}
                msb.define_aspect(i,s,d)
            self.add_control(param,msb)
            msb.layout((x,y))
            msb.update_aspect()
            return msb

        def msb_keybreak(param,x,y):
            count = len(KEYBREAK)
            msb = MSB(canvas,param,editor,count)
            for i,s in enumerate(KEYBREAK):
                d = {"fill" : CFILL,
                     "foreground" : CFOREGROUND,
                     "outline" : COUTLINE,
                     "value" : s,
                     "text" : "%d" % s}
                msb.define_aspect(i,s,d)
            self.add_control(param,msb)
            msb.layout((x,y))
            msb.update_aspect()
            return msb

        def msb_modscale(param,x,y):
            count = len(MODSCALES)
            msb = MSB(canvas,param,editor,count)
            for i in MODSCALES:
                j = i+1
                value = 10**i
                d = {"fill" : CFILL,
                     "foreground" : CFOREGROUND,
                     "outline" : COUTLINE,
                     "value" : value,
                     "text" : "x%d" % j}
                msb.define_aspect(i,value,d)
            self.add_control(param,msb)
            msb.layout((x,y))
            msb.update_aspect()
      

        tumbler("fm%d_ratio" % n,5,0.001,x_fm,y_mod)
        norm_slider("fm%d_lfo1" % n,x_mod_lfo1,y_mod)
        norm_slider("fm%d_lfo2" % n,x_mod_lfo2,y_mod)
        norm_slider("fm%d_external" % n, x_mod_external, y_mod)
        msb_keyscale("fm%d_left" % n, x_mod_keyscale, y_mod)
        msb_keyscale("fm%d_right" % n, x_mod_keyscale, y_mod+70)
        msb_modscale("fm%d_modscale" % n, x_mod_amp, y_mod)
        norm_slider("fm%d_moddepth" % n, x_mod_amp+24, y_mod+50, height=100)
        norm_slider("fm%d_lag" % n, x_fm+30,y_mod+75,height=75)

        tumbler("op%d_ratio" % n,5,0.001,x_ratio+8,y_carrier)
        tumbler("op%d_bias" % n,6,0.001,x_ratio,y_carrier+75)
        norm_slider("op%d_velocity" % n,x_velocity,y0)
        norm_slider("op%d_lfo1" % n,x_lfo1,y0)
        norm_slider("op%d_lfo2" % n,x_lfo2,y0)
        norm_slider("op%d_external" % n,x_external,y0)
        
        
        msb_keyscale("op%d_left" % n, x_keyscale,y0)
        msb_keyscale("op%d_right" % n, x_keyscale,y0+70)
        msb_keybreak("op%d_key" % n, x_keyscale,y0+140)
        
        penable = "op%d_enable" % n
        msb_enable = ToggleButton(canvas,penable, editor,
                                  fill = CFILL,
                                  foreground = CFOREGROUND,
                                  outline = COUTLINE,
                                  text = ["Off","Enabled"])
        self.add_control(penable,msb_enable)
        msb_enable.layout((x_enable, y0))
        msb_enable.update_aspect()
        volume_slider("op%d_amp" % n,x_enable+24,y0+50,height=100)

        env_parameters = []
        for s in ("attack","decay1","decay2","release",
                  "breakpoint","sustain","env_mode"):
            p = "op%d_%s" % (n,s)
            env_parameters.append(p)
        enved = ADDSREditor(canvas,n,(x_env,y_env),
                            (800,350),
                            env_parameters,
                            editor,
                            MAX_ENV_SEGMENT)
        self.add_child_editor("OP%dENV" % n, enved)
        enved.sync()

        y_extra = y_env+30
        x_extra = x0 + 800

        if n==3:
            # Add exgtra noise controls
            count = len(NOISE_BANDWIDTHS)
            msb = MSB(canvas,"nse3_bw",editor,count)
            for i,v in enumerate(NOISE_BANDWIDTHS):
                d = {"fill" : CFILL,
                     "foreground" : CFOREGROUND,
                     "outline" : COUTLINE,
                     "value" : v,
                     "text" : str(v)}
                msb.define_aspect(i,v,d)
            self.add_control("nse3_bw",msb)
            msb.layout((x_extra,y_extra))
            msb.update_aspect()
            norm_slider("nse3_mix",x_extra+24, y_extra+75)
        if n==4:
            # Add buzz controls
            x_n = x_extra+16
            x_env = x_n+60
            x_lfo = x_env+60
            x_lag = x_env
            x_mix = x_lag+60
            linear_slider("bzz4_n",(1,128),x_n,y_extra)
            linear_slider("bzz4_env",(-128,128),x_env,y_extra)
            linear_slider("bzz4_lfo2",(0,128),x_lfo,y_extra)
            norm_slider("bzz4_lag",x_lag,y_extra+200, height=100)
            norm_slider("bzz4_mix",x_mix,y_extra+200, height=100)
