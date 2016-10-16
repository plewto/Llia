# llia.synths.xover.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.tumbler import Tumbler, ToggleButton
from llia.gui.tk.msb import MSB
import llia.synths.xover.xover_constants as xcon

def _msb_aspect(value, text):
    d = {'value' : value,
         'fill' : '',
         'active-fill' : '',
         'foreground' : '#c29e78',
         'active-foreground' : 'yellow',
         'outline' : '#c29e78',
         'active-outline' : 'yellow',
         'text' : text}
    return d

def create_editor(parent):
    TkXOverPanel(parent)

class TkXOverPanel(TkSubEditor):

    NAME = "XOver"
    IMAGE_FILE = "resources/XOver/editor.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1000,700,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        y0 = 75
        y1 = y0+60
        y2 = y1+60 
        y3 = y2+70
        x0=90
        x1 = x0+100
        x2 = x1+60
        x3 = x2+60
        x4 = x3+60
        x5 = x4+75
        x6 = x5+60
        xlfo = x6+75
        xmix = x6+196
        
        def norm_slider(param, x, y):
            s = cf.normalized_slider(canvas, param, editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y)
            return s

        def bipolar_slider(param, x, y, height=150):
            s = cf.bipolar_slider(canvas, param, editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y,height=height)
            return s
            
        def amp_slider(param, x, y):
            s = cf.volume_slider(canvas, param, editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y)
            return s

        def linear_slider(param, x, y, range_):
            s = cf.linear_slider(canvas, param, editor, range_=range_)
            self.add_control(param,s)
            s.widget().place(x=x,y=y)
            return s
     
        msb_xover = MSB(canvas,"xover",editor,len(xcon.CROSSOVER_FREQUENCIES))
        for i,v in enumerate(xcon.CROSSOVER_FREQUENCIES):
            d = _msb_aspect(v,str(v))
            msb_xover.define_aspect(i,v,d)
        self.add_control("xover", msb_xover)
        msb_xover.layout((x0,y0))
        msb_xover.update_aspect()
        msb_maxxover = MSB(canvas,"maxXover",editor,len(xcon.CROSSOVER_FREQUENCIES))
        for i,v in enumerate(xcon.CROSSOVER_FREQUENCIES):
            d = _msb_aspect(v,str(v))
            msb_maxxover.define_aspect(i,v,d)
        self.add_control("maxXover", msb_maxxover)
        msb_maxxover.layout((x0,y1))
        msb_maxxover.update_aspect()
        msb_minxover = MSB(canvas,"minXover",editor,len(xcon.CROSSOVER_FREQUENCIES))
        for i,v in enumerate(xcon.CROSSOVER_FREQUENCIES):
            d = _msb_aspect(v,str(v))
            msb_minxover.define_aspect(i,v,d)
        self.add_control("minXover",msb_minxover)
        msb_minxover.layout((x0,y2))
        msb_minxover.update_aspect()
        norm_slider("lfoToXover", x1,y0)
        msb_lforatio = MSB(canvas,"lfo2Ratio",editor,len(xcon.LFO_RATIOS))
        for i,p in enumerate(xcon.LFO_RATIOS):
            ratio, text = p
            d = _msb_aspect(ratio,text)
            msb_lforatio.define_aspect(i,ratio,d)
        self.add_control("lfo2Ratio", msb_lforatio)
        msb_lforatio.layout((x1-22,y3))
        msb_lforatio.update_aspect()
        norm_slider("lfo2Wave",x2,y0)
        norm_slider("externToXover",x3,y0)
        norm_slider("res",x4,y0)
        norm_slider("filterBMix",x5,y0)
        norm_slider("filterBLag",x6,y0)
        msb_b_ratio = MSB(canvas,"filterBRatio",editor,len(xcon.FILTER_B_RATIOS))
        for i,p in enumerate(xcon.FILTER_B_RATIOS):
            ratio,text = p
            d = _msb_aspect(ratio,text)
            msb_b_ratio.define_aspect(i,ratio,d)
        self.add_control("filterBRatio", msb_b_ratio)
        msb_b_ratio.layout((x5+6,y3))
        msb_b_ratio.update_aspect()
        tumbler = Tumbler(canvas,"lfoFreq",editor,digits=4,scale=0.01)
        self.add_control("lfoFreq", tumbler)
        tumbler.layout((xlfo, y1))
        msb_lfo_enable = ToggleButton(canvas,"lfoEnable",editor,
                                      fill='',foreground='#c29378',outline='#c29378',
                                      active_color='yellow',
                                      selected_fill='#825151', selected_foreground='white')
        self.add_control("lfoEnable",msb_lfo_enable)
        msb_lfo_enable.layout((xlfo, y2))
        msb_lfo_enable.update_aspect()
        amp_slider("dryAmp", xmix, y0)
        amp_slider("filterAAmp", xmix+60, y0)
        amp_slider("filterBAmp", xmix+120, y0)
        amp_slider("amp", xmix+180,y0)
        bipolar_slider("dryPan", xmix, y3)
        bipolar_slider("filterAPan", xmix+60, y3)
        bipolar_slider("filterBPan", xmix+120, y3)
        linear_slider("xscale", xlfo-7, y3, (0,4))
        linear_slider("xbias", xlfo+53, y3, (-4,4))
                      
        
        
