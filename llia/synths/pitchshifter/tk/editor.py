# llia.synths.pitchshifter.tk.editor


from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory

def create_editor(parent):
    TkPitchShifterPanel(parent)
    
MAX_DELAY = 1.0

class TkPitchShifterPanel(TkSubEditor):

    NAME = "PitchShifter"
    IMAGE_FILE = "resources/PitchShifter/editor.png"
    TAB_FILE =   "resources/PitchShifter/tab.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 1400, 700, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        x0 = 75
        xdelay = x0+220
        xmixer = xdelay+350
        y0,y1 = 75,260
        self.tumbler("pitchRatio",4,0.001,x0,y0,range_=(0,4000))
        self.norm_slider("pitchDispersion",x0+80,y0)
        self.norm_slider("timeDispersion",x0+140,y0)
        self.toggle("delayInSelect",xdelay,y0,off=(0,"P.Shifter"),on=(1,"Drysig"))
        self.exp_slider("delay",1,xdelay+80,y0)
        self.exp_slider("delayMod",1,xdelay+140,y0)
        self.tumbler("lfoFreq",5,0.001,xdelay+110,y1)
        self.linear_slider("feedback",(-1,1),xdelay+200,y0)
        self.exp_slider("lowpass",16000,xdelay+260,y0)
        self.volume_slider("dryAmp",xmixer,y0)
        self.volume_slider("psAmp",xmixer+60,y0)
        self.volume_slider("delayAmp",xmixer+120,y0)
        self.linear_slider("dryPan",(-1,1),xmixer,y1)
        self.linear_slider("psPan",(-1,1),xmixer+60,y1)
        self.linear_slider("delayPan",(-1,1),xmixer+120,y1)
        self.toggle("feedbackDestination",xdelay,y1,off=(0,"P.shifter"),on=(1,"Delay"))
