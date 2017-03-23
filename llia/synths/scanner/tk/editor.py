# llia.synths.scanner.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf

def create_editor(parent):
    TkScannerPanel(parent)

class TkScannerPanel(TkSubEditor):

    NAME = "Scanner"
    IMAGE_FILE = "resources/Scanner/editor.png"
    TAB_FILE = "resources/Scanner/tab.png"

    def __init__(self,editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1000,700,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.NAME)
        editor.add_child_editor(self.NAME, self)
        x0,y0 = 75,75

        # LFO 
        x_lfo = x0
        x_wave = x_lfo + 100
        x_depth = x_wave+60
        x_xdepth = x_depth+60
        y_tumbler = y0+50

        self.tumbler("scanRate",5,0.001,x_lfo,y_tumbler)
        self.norm_slider("wave",x_wave,y0)
        self.norm_slider("modDepth",x_depth,y0)
        self.norm_slider("xmodDepth",x_xdepth,y0)
        
        # Delay
        x_delay = x_xdepth+90
        x_feedback = x_delay+60
        x_lowpass = x_feedback+60
        
        self.linear_slider("delay",(0.0, 0.05),x_delay,y0)
        self.linear_slider("feedback",(-0.99,0.99),x_feedback,y0)
        self.exp_slider("lowpass",16000,x_lowpass,y0,degree=4)

        # Mixer
        x_dry = x_lowpass+90
        x_wet1 = x_dry+60
        x_wet2 = x_wet1+60

        self.volume_slider("dryMix",x_dry,y0)
        self.volume_slider("wet1Mix",x_wet1,y0)
        self.volume_slider("wet2Mix",x_wet2,y0)
