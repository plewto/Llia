# llia.synths.pitchshifter.tk.editor


from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB,ToggleButton
from llia.gui.tk.tumbler import Tumbler


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

        y,ypan = 50,250
        x0 = 100
        x1 = x0+90
        x2 = x1+60
        x3 = x2+60
        x4 = x3+60
        x5 = x4+90
        x6 = x5+60
        x7 = x6+60
        
        def norm_slider(param,x,y):
            s = cf.normalized_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y,width=14, height=150)

        def bipolar_slider(param,x,y):
            s = cf.bipolar_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y,width=14, height=75)

        def amp_slider(param,x,y):
            s = cf.volume_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y,width=14,height=150)
            
        tratio = Tumbler(canvas,"pitchRatio",editor,
                         sign=False,digits=4,scale=0.001,
                         range_=(0,4000))
        self.add_control("pitchRatio", tratio)
        tratio.layout((x0,y))
        norm_slider("pitchDispersion",x1,y)
        norm_slider("timeDispersion",x2,y)
        norm_slider("delay",x3,y)
        norm_slider("feedback",x4,y)
        amp_slider("dryAmp",x5,y)
        amp_slider("psAmp",x6,y)
        amp_slider("delayAmp",x7,y)
        bipolar_slider("dryPan",x5,ypan)
        bipolar_slider("psPan",x6,ypan)
        bipolar_slider("delayPan",x7,ypan)
        
            
