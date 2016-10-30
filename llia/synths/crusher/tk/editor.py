# llia.synths.crusher.tk.editor


from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB, MsbAspect
#from llia.gui.tk.tumbler import Tumbler

def create_editor(parent):
    TkCrusherPanel(parent)

CLOCK_FREQS = tuple(range(1000,16000,1000))
LP_FREQS = (20000,10000,8000,4000,2000,1000,500)
    
class TkCrusherPanel(TkSubEditor):

    NAME = "Crusher"
    IMAGE_FILE = "resources/Crusher/editor.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 1400, 700, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)

        cfill = "black"
        cforeground="#c79fa1"
        coutline="blue"

        y0 = 50
        x0 = 75
        
        msb_clock = MSB(canvas,"clockFreq",editor,len(CLOCK_FREQS))
        for i,freq in enumerate(CLOCK_FREQS):
            ad = {"fill" : cfill,
                  "foreground" : cforeground,
                  "outline" : coutline,
                  "text" : str(freq),
                  "value" : freq}
            msb_clock.define_aspect(i,freq,ad)
        self.add_control("clockFreq",msb_clock)
        msb_clock.layout((x0,y0))
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
        msb_filter.layout((x0,y0+75))
        msb_filter.update_aspect()
            

        def volume_slider(param,x):
            s = cf.volume_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y0)
            return s

        xdry = x0 + 120
        volume_slider("dry",xdry)
        volume_slider("wet",xdry+60)
        volume_slider("amp",xdry+120)
            
