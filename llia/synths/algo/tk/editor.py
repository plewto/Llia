# llia.synths.algo.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB, ToggleButton
from llia.gui.tk.tumbler import Tumbler
from llia.gui.tk.expslider import ExpSlider
import llia.synths.algo.algo_constants as acon
from llia.synths.algo.tk.envedit import TkAlgoEnvelopePanel
from llia.synths.algo.tk.miscedit import TkAlgoMiscPanel

def create_editor(parent):
    TkAlgoStackPanel("A", "Stack A","resources/Algo/editor_stack_a.png",parent)
    TkAlgoEnvelopePanel("A",parent)
    TkAlgoStackPanel("B", "Stack B","resources/Algo/editor_stack_b.png",parent)
    TkAlgoEnvelopePanel("B",parent)
    TkAlgoStackPanel("C", "Stack C","resources/Algo/editor_stack_c.png",parent)
    TkAlgoEnvelopePanel("C",parent)
    TkAlgoMiscPanel(parent)
    

class TkAlgoStackPanel(TkSubEditor):

    def __init__(self,stack_id,name,imagefile,editor):
        frame = editor.create_tab(name)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 1050, 700, imagefile)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, name)
        editor.add_child_editor(name, self)
        carrier = {"A":1,"B":5,"C":7}[stack_id]
        mod1 = {"A":2,"B":4,"C":8}[stack_id]
        mod2 = {"A":3,"B":6,"C":None}[stack_id]
        self.layout_operator(carrier)
        self.layout_operator(mod1)
        if mod2: self.layout_operator(mod2)
        self.layout_stack(stack_id,carrier)

    @staticmethod
    def is_carrier(n):
        return n==1 or n == 5 or n == 7

    @staticmethod
    def op_y_ref(n):
        ya = 50
        yb = 285   # 370
        d = {1:ya,2:ya,3:yb,4:ya,
             5:ya,6:yb,7:ya,8:ya,None:None,
             "Stack":yb}
        return d[n]

    @staticmethod
    def op_x_ref(n):
        xmod = 50
        xcarrier = 530
        if n=="Stack" or TkAlgoStackPanel.is_carrier(n):
            return xcarrier
        else:
            return xmod

    # @staticmethod
    # def op_param(n,key):
    #     return "op%d_%s" % (n,key)
        
    def tumbler(self,param,is_ratio,x,y):
        if is_ratio:
            scale = 0.001
        else:
            scale = 0.01
        t = Tumbler(self.canvas,param,self.editor,
                    digits=5,scale=scale)
        self.add_control(param,t)
        t.layout((x,y))
        return t

    def msb_mod_scale(self,param,x,y):
        msb = MSB(self.canvas,param,self.editor,acon.MOD_RANGE_COUNT)
        for i in range(acon.MOD_RANGE_COUNT):
            j = i+1
            value = 10**i
            d = {"fill" : acon.CFILL,
                 "foreground" : acon.CFOREGROUND,
                 "outline" : acon.COUTLINE,
                 "value" : value,
                 "text" : "x%d" % j}
            msb.define_aspect(i,value,d)
        self.add_control(param,msb)
        msb.layout((x,y))
        msb.update_aspect()
        return msb

    def msb_keyscale(self,param,x,y):
        count = len(acon.KEYSCALES)
        msb = MSB(self.canvas,param,self.editor,count)
        for i,value in enumerate(acon.KEYSCALES):
            d = {"fill" : acon.CFILL,
                 "foreground" : acon.CFOREGROUND,
                 "outline" : acon.COUTLINE,
                 "value" : value,
                 "text" : "%+d" % value}
            msb.define_aspect(i,value,d)
        self.add_control(param,msb)
        msb.layout((x,y))
        msb.update_aspect()
        return msb

    def msb_enable(self,param,x,y):
        msb = ToggleButton(self.canvas,param,self.editor,
                           text = ["Off","On"],
                           fill=acon.CFILL,
                           foreground=acon.CFOREGROUND,
                           outline=acon.COUTLINE)
        self.add_control(param,msb)
        msb.layout((x,y))
        msb.update_aspect()
        return msb

    def msb_keybreak(self,param,x,y):
        count = len(acon.KEY_BREAKPOINTS)
        msb = MSB(self.canvas,param,self.editor,count)
        for i,val in enumerate(acon.KEY_BREAKPOINTS):
            d = {"fill" : acon.CFILL,
                 "foreground" : acon.CFOREGROUND,
                 "outline" : acon.COUTLINE,
                 "value" : val,
                 "text" : str(val)}
            msb.define_aspect(i,val,d)
        self.add_control(param,msb)
        msb.layout((x,y))
        msb.update_aspect()
        return msb
    
    def msb_lfo_ratio(self,param,x,y):
        count = len(acon.LFO_RATIOS)
        msb = MSB(self.canvas,param,self.editor,count)
        for i in range(count):
            val,txt = acon.LFO_RATIOS[i]
            d = {"fill":acon.CFILL,
                 "foreground":acon.CFOREGROUND,
                 "outline":acon.COUTLINE,
                 "value":val,
                 "text":txt}
            msb.define_aspect(i,val,d)
        self.add_control(param,msb)
        msb.layout((x,y))
        msb.update_aspect()
        return msb
    
    def norm_slider(self,param,x,y,width=14,height=150):
        s = cf.normalized_slider(self.canvas,param,self.editor)
        self.add_control(param,s)
        s.widget().place(x=x,y=y,width=width,height=height)
        return s

    def linear_slider(self,param,range_,x,y,width=14,height=150):
        s = cf.linear_slider(self.canvas,param,self.editor,range_=range_)
        self.add_control(param,s)
        s.widget().place(x=x,y=y,width=width,height=height)
        return s

    def exp_slider(self,param,x,y,range_=2.0,degree=2):
        s = ExpSlider(self.canvas,param,self.editor,
                      range_,degree)
        self.add_control(param,s)
        s.layout((x,y),checkbutton_offset=None)
        return s
    
    def volume_slider(self,param,x,y,width=14,height=150):
        s = cf.volume_slider(self.canvas,param,self.editor)
        self.add_control(param,s)
        s.widget().place(x=x,y=y,width=width,height=height)
        return s
    
    def layout_operator(self,op):
        carrier = self.is_carrier(op)
        y0 = self.op_y_ref(op)
        y_ratio = y0
        y_bias = y_ratio + 75
        y_sliders = y0
        y_mod_scale = y_sliders + 115
        y_keyscale_left = y0
        y_keyscale_right = y_keyscale_left + 75
        y_env = y0
        x0 = self.op_x_ref(op)
        x_ratio = x0
        x_bias = x_ratio
        x_amp = x_ratio + 120
        x_mod_scale = x_amp-23
        if carrier:
            x_keyscale = x_ratio+100
        else:
            x_keyscale = x_amp+50
        x_velocity = x_keyscale+100
        x_lfo = x_velocity + 60
        x_external = x_lfo + 60    
        x_env = x_external + 42
        def op_param(key):
            p = "op%d_%s" % (op,key)
            return p
        self.tumbler(op_param("ratio"),True,x_ratio,y_ratio)
        self.tumbler(op_param("bias"),False,x_bias,y_bias)
        if not carrier:
            self.norm_slider(op_param("amp"),x_amp,y_sliders,height=100)
            self.msb_mod_scale(op_param("mod_scale"),x_mod_scale,y_mod_scale)
        self.msb_keyscale(op_param("left_scale"),x_keyscale,y_keyscale_left)
        self.msb_keyscale(op_param("right_scale"),x_keyscale,y_keyscale_right)
        self.norm_slider(op_param("velocity"),x_velocity,y_sliders)
        self.norm_slider(op_param("lfo"),x_lfo,y_sliders)
        self.norm_slider(op_param("external"),x_external,y_sliders)
      
    def layout_stack(self, n, carrier):
        y0 = self.op_y_ref("Stack")
        x0 = self.op_x_ref("Stack")
        y_sliders = y0
        y_amp_slider = self.op_y_ref(1)  # Place with carrier controls
        y_enable = y0
        y_keybreak = y_enable+75
        y_lfo = y0
        x_fb = x0
        x_fb_env = x_fb+60
        x_fb_lfo = x_fb_env+60
        x_lfo = x_fb_lfo + 63
        x_lfo_delay = x_lfo+100
        x_lfo_wave = x_lfo_delay + 60
        x_amp_slider = x_lfo_wave + 84
        x_enable = x_amp_slider-24
        x_keybreak = x_enable
        if n == "C":
            self.exp_slider("stack%s_feedback" % n, x_fb,y_sliders,range_=6,degree=3)
            self.exp_slider("stack%s_env_feedback" % n, x_fb_env,y_sliders,range_=6,degree=3)
            self.exp_slider("stack%s_lfo_feedback" % n, x_fb_lfo,y_sliders,range_=6,degree=3)
        else:
            self.exp_slider("stack%s_feedback" % n, x_fb,y_sliders,degree=3)
            self.exp_slider("stack%s_env_feedback" % n, x_fb_env,y_sliders,degree=3)
            self.exp_slider("stack%s_lfo_feedback" % n, x_fb_lfo,y_sliders,degree=3)
        self.msb_lfo_ratio("lfo%s_ratio" % n, x_lfo,y_lfo)
        self.linear_slider("lfo%s_delay" % n, (0,4),x_lfo_delay,y_sliders)
        self.norm_slider("lfo%s_wave" % n, x_lfo_wave,y_sliders)
        self.volume_slider("op%s_amp" % carrier,x_amp_slider, y_amp_slider)
        self.msb_enable("stack%s_enable" % n,x_enable,y_enable)
        self.msb_keybreak("stack%s_key" % n, x_keybreak,y_keybreak)

