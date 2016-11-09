# llia.synths.crusher.tk.editor


from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB, ToggleButton
#from llia.gui.tk.tumbler import Tumbler

def create_editor(parent):
    TkCrusherPanel(parent)

CLOCK_FREQS = tuple(range(1000,17000,1000))
LP_FREQS = (20000,10000,8000,4000,2000,1000,500)
    
class TkCrusherPanel(TkSubEditor):

    NAME = "Crusher"
    IMAGE_FILE = "resources/Crusher/editor.png"
    TAB_FILE = "resources/Crusher/tab.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 1000, 700, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)

        cfill = "black"
        cforeground="#c79fa1"
        coutline="blue"
        csfill = "#005c56"
        csforeground = "white"
        
        y0 = 0
        ysliders = y0+192
        ywave = y0+128
        yclock = ywave
        yfilter = yclock
        yrsenable = y0+200
        
        x0 = 75
        xgain = x0+60
        xwave = x0+143
        xclock = xwave+100
        xfilter = xclock+100
        xefx = xgain+395
        xdry = xgain+455

        def volume_slider(param,x,y):
            s = cf.volume_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y)
            return s

        def linear_slider(param,range_,x,y):
            s = cf.linear_slider(canvas,param,editor,range_=range_)
            self.add_control(param,s)
            s.widget().place(x=x,y=y)
            return s

        linear_slider("gain",(0,8),xgain,ysliders)
        
        msb_wave = MSB(canvas,"wave",editor, 5)
        for i,tx in enumerate(("Off","Soft","Clip","Fold","Wrap")):
            d = {"fill" : cfill,
                 "foreground" : cforeground,
                 "outline" : coutline,
                 "value" : i,
                 "text" : tx}
            msb_wave.define_aspect(i,i,d)
        msb_wave.layout((xwave,ywave))
        msb_wave.update_aspect()

        msb_clock = MSB(canvas,"clockFreq",editor,len(CLOCK_FREQS))
        for i,freq in enumerate(CLOCK_FREQS):
            ad = {"fill" : cfill,
                  "foreground" : cforeground,
                  "outline" : coutline,
                  "text" : str(freq),
                  "value" : freq}
            msb_clock.define_aspect(i,freq,ad)
        self.add_control("clockFreq",msb_clock)
        msb_clock.layout((xclock,yclock))
        msb_clock.update_aspect()

        msb_filter = MSB(canvas,"low",editor, len(LP_FREQS))
        for i,freq in enumerate(LP_FREQS):
            ad = {"fill" : cfill,
                  "foreground" : cforeground,
                  "outline" : coutline,
                  "text" : str(freq),
                  "value" : freq}
            msb_filter.define_aspect(i,freq,ad)
        self.add_control("low",msb_filter)
        msb_filter.layout((xfilter,yfilter))
        msb_filter.update_aspect()

        volume_slider("wet",xefx,ysliders)
        volume_slider("dry",xdry,ysliders)

        tog_rs_enable = ToggleButton(canvas,"resampleEnable",editor,
                                     fill = cfill,
                                     foreground = cforeground,
                                     outline = coutline,
                                     selected_fill = csfill,
                                     selected_foreground = csforeground,
                                     text = ["Off","On"],
                                     values = [0,1])
        self.add_control("resampleEnable", tog_rs_enable)
        tog_rs_enable.layout((xclock,yrsenable))
        tog_rs_enable.update_aspect()
