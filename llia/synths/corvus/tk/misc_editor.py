# llia.synths.corvus.tk.misc_editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB, ToggleButton
from llia.gui.tk.tumbler import Tumbler
from llia.gui.tk.addsr_editor import ADDSREditor

from llia.synths.corvus.corvus_constants import *

class TkCorvusMiscPanel(TkSubEditor):

    def __init__(self, editor):
        name = "Misc"
        image_file = "resources/Corvus/editor_misc.png"
        tab_file =   "resources/Tabs/misc.png"
        frame = editor.create_tab(name,tab_file)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 750, 357,image_file)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, name)
        editor.add_child_editor(name, self)
        self.op = n
        y0 = 50
        y_msb = 230
        x0 = 50
        x_port = x0
        x_vib = x_port+90
        x_vdelay = x_vib+90
        x_vsens = x_vdelay+60
        x_vdepth = x_vsens+60
        x_xpitch = x_vdepth+60
        x_lfo1 = x_xpitch+90
        x_lfo2 = x_lfo1 + 90
        x_amp = x_lfo2 + 90
       
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

        def msb_ratio(n,x):
            param = "lfo%d_ratio" % n
            count = len(LFO_RATIOS)
            msb = MSB(canvas,param,editor,count)
            for i,pair in enumerate(LFO_RATIOS):
                value,txt = pair
                d = {"fill" : CFILL,
                     "foreground" : CFOREGROUND,
                     "outline" : COUTLINE,
                     "value" : value,
                     "text" : txt}
                msb.define_aspect(i,value,d)
            self.add_control(param, msb)
            msb.layout((x,y_msb))
            msb.update_aspect()
            return msb
        
        norm_slider("port",x_port,y0)
        tumbler("vfreq",5,0.001,x_vib,y0)
        linear_slider("vdelay",(0,4),x_vdelay,y0)
        norm_slider("vsens",x_vsens,y0)
        norm_slider("vdepth",x_vdepth,y0)
        norm_slider("xpitch",x_xpitch,y0)
        linear_slider("lfo1_delay",(0,4),x_lfo1,y0)
        msb_ratio(1,x_lfo1-22)
        linear_slider("lfo2_delay",(0,4),x_lfo2,y0)
        msb_ratio(2,x_lfo2-22)
        volume_slider("amp",x_amp,y0)
        
        
