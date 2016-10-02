# llia.synths.chronos.tk.editor


from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB,ToggleButton
from llia.gui.tk.tumbler import Tumbler
from llia.gui.tk.msb import MSB

def create_editor(parent):
    TkChronosPanel(parent)


MAX_DELAY = 2.0

LFO_RATIOS = (('1/8',0.125),('1/4',0.25),('1/2',0.5),('3/4',0.75),
              ('1',1.0),('4/3', 4/3.0),('3/2',1.5),('2',2.00),
              ('5/2', 2.5),('3',3.0),('4', 4.0),('5',5.0),
              ('6', 6.0),('8',8.0))

class TkChronosPanel(TkSubEditor):

    NAME = "Chronos"
    IMAGE_FILE = "resources/Chronos/editor.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 1400, 700, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)

        y = [50,275]
        x0 = 100
        xdelay = x0 + 180
        xmod = xdelay+90
        xfeedback = xmod+120
        xeq = xfeedback+60
        xmixer = xeq+150
        
        def add_slider(param,s,x,y,width=14,height=150):
            self.add_control(param,s)
            s.widget().place(x=x,y=y,width=width,height=height)
        
        def amp_slider(param,x,y):
            s = cf.volume_slider(canvas,param,editor)
            add_slider(param,s,x,y)

        def bipolar_slider(param,x,y, width=14, height=150):
            s = cf.bipolar_slider(canvas,param,editor)
            add_slider(param,s,x,y,width,height)

        def eq_slider(param,x,y):
            s = cf.third_octave_slider(canvas,param,editor)
            add_slider(param,s,x,y)

        def norm_slider(param,x,y):
            s = cf.normalized_slider(canvas,param,editor)
            add_slider(param,s,x,y)

        def linear_slider(param,x,y,range_=(0.0,1.0)):
            s = cf.linear_slider(canvas,param,editor,range_=range_)
            add_slider(param,s,x,y)
            
        for i in (0,1):
            n = i+1
            for j, p in enumerate(('d%dDry1In','d%dDry2In')):
                x = x0 + j*60
                param = p % n
                amp_slider(param,x,y[i])
            amp_slider('d2Delay1In',x0+60*2, y[1])
            param = 'd%dDelayTime' % n
            tumbler_delay = Tumbler(canvas, param, editor,
                                    sign=False, digits=4,scale = 0.001,
                                    range_ = (0,2000))
            self.add_control(param,tumbler_delay)
            tumbler_delay.layout((xdelay, y[i]))
            param = 'd%dLfoRatio' % n
            msb_lfo_ratio = MSB(canvas,param,editor,len(LFO_RATIOS))
            self.add_control(param, msb_lfo_ratio)
            for k,pair in enumerate(LFO_RATIOS):
                adict = {'text' : pair[0],
                         'font' : ('Times', 12),
                         'fill' : 'black',
                         'foreground' : 'white',
                         'outline' : 'white',
                         'active-fill' : 'black',
                         'active-foreground' : 'yellow',
                         'active-outline' : 'yellow'}
                msb_lfo_ratio.define_aspect(k,pair[1],adict)
                msb_lfo_ratio.layout((xdelay, y[i]+75))
                msb_lfo_ratio.update_aspect()
            norm_slider('d%dLfoModDepth' % n, xmod,y[i])
            norm_slider('d%dExternalModDepth' % n, xmod+60,y[i]) 
            bipolar_slider('d%dFeedback' % n, xfeedback,y[i])
            eq_slider('d%dLowpass' % n, xeq,y[i])
            eq_slider('d%dHighpass' % n, xeq+60,y[i])

        # Mixer
        amp_slider("dry1Amp", xmixer, y[0])
        amp_slider("dry2Amp", xmixer+60, y[0])
        amp_slider("d1Amp", xmixer+120, y[0])
        amp_slider("d2Amp", xmixer+180, y[0])

        bipolar_slider("dry1Pan", xmixer, y[1],height=75)
        bipolar_slider("dry2Pan", xmixer+60, y[1],height=75)
        bipolar_slider("d1Pan", xmixer+120, y[1],height=75)
        bipolar_slider("d2Pan", xmixer+180, y[1],height=75)

        msb_lfo_preset = MSB(canvas,"",None,7)
        for i in range(len(msb_lfo_preset)):
            adict = {'fill' : 'black',
                     'foreground' : 'white',
                     'outline' : 'white',
                     'active-fill' : 'black',
                     'active-foregeround' : 'yellow',
                     'active-outline' : 'yellow',
                     'text' : str(i+1),
                     'fomt' : ('Times', 8)}
            msb_lfo_preset.define_aspect(i,i+1,adict)
        msb_lfo_preset.layout((xmixer+160, y[1]+143),width=18,height=18)
        msb_lfo_preset.update_aspect()
        def lfo_preset_freq(*_):
            v = msb_lfo_preset.value()
            synth = self.editor.synth
            synth.x_param_change("lfoCommonFreq",v)
            synth.bank()[None]["lfoCommonFreq"] = float(v)
            tumbler_lfo.value(v)
        msb_lfo_preset.tag_bind("<Button-1>", lfo_preset_freq)
        msb_lfo_preset.tag_bind("<Button-3>", lfo_preset_freq)
            
        tumbler_lfo = Tumbler(canvas,"lfoCommonFreq",editor,
                              sign=False,digits=5, scale=0.001,
                              range_=(0,16999))
        self.add_control("lfoCommonFreq", tumbler_lfo)
        tumbler_lfo.layout((xmixer+60, y[1]+143))
        
