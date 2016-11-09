# llia.synths.lfo1.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.tumbler import Tumbler
from llia.gui.tk.msb import MSB
from llia.synths.lfo1.lfo1_data import FREQ_RATIOS


# lfoFreq    tumbler
# sineAmp    norm
# sineRatio  msb
# sawAmp     norm
# sawRatio   msb
# sawWidth   norm
# pulseAmp   norm
# pulseRatio msb
# pulseWidth norm
# lfoDelay   linear
# lfoHold    linear
# lfoBleed   norm
# lfoScale   linear
# lfoBias    linear


def create_editor(parent):
    panel1 = TkLfo1Panel(parent)


class TkLfo1Panel(TkSubEditor):

    NAME = "LFO1"
    IMAGE_FILE = "resources/LFO1/editor.png"
    TAB_FILE = "resources/Tabs/lfo.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE);
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,966,433,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)

        SLIDER_HEIGHT = 200
        y0 = 75
        y_tumbler = y0
        y_msb = y0+SLIDER_HEIGHT+40

        x0 = 75
        xsine = x0+160
        xsaw = xsine+90
        xpulse = xsaw+150
        xdelay = xpulse+150

        
        def tumbler(param,x):
            t = Tumbler(canvas,param,editor,
                        digits=5,scale=0.001,
                        fill='#140e23',
                        foreground='#8f94a9',
                        outline='#8f94a9')
            self.add_control(param,t)
            t.layout((x,y_tumbler))
            return t

        def msb(param,x):
            b = MSB(canvas,param,editor,len(FREQ_RATIOS))
            self.add_control(param,b)
            b.layout((x,y_msb))
            for i,r in enumerate(FREQ_RATIOS):
                value = float(r[0])
                txt = r[1]
                adict = {'value' : value,
                         'text' : txt,
                         'fill' : '#13302d',
                         'foreground' : '#8f94a9',
                         'outline' : '#8f94a9'}
                b.define_aspect(i,value,adict)
            b.update_aspect()
        
        def norm(param,x):
            s = cf.normalized_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y0,height=SLIDER_HEIGHT)
            return s

        def linear_slider(param,x,range_):
            s = cf.linear_slider(canvas,param,editor,range_=range_)
            self.add_control(param,s)
            s.widget().place(x=x,y=y0,height=SLIDER_HEIGHT)
            return s
        
        tumbler("lfoFreq",x0)
        msb("sineRatio", xsine-23)
        norm("sineAmp", xsine)
        msb("sawRatio", xsaw+7)
        norm("sawAmp", xsaw)
        norm("sawWidth", xsaw+60)
        msb("pulseRatio", xpulse+7)
        norm("pulseAmp", xpulse)
        norm("pulseWidth", xpulse+60)
        linear_slider("lfoDelay",xdelay,(0,4))
        linear_slider("lfoHold",xdelay+60,(0,4))
        norm("lfoBleed",xdelay+120)
        linear_slider("lfoScale",xdelay+195,(-1,1))
        linear_slider("lfoBias",xdelay+255,(-4,4))
