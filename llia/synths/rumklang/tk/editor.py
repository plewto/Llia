# llia.synths.rumklang.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.msb import ToggleButton


def create_editor(parent):
    panel1 = TkRumklangPanel(parent)



# "preDelay" : 0.01,  linear slider 0.0 .. 0.33
# "roomSize" : 0.5,   norm slider
# "damp" : 0.5,       norm slider
# "lpcutoff" : 16000, eq thirde octave
# "hpcutoff" : 10,    eq third octave
# "gatted" : 0,       MSB on/off
# "modDepth" : 0.0,   norm slider
# "wetAmp" : 1.0,     vol slider
# "wetPan" : 0.75,    bipolar slider
# "dryAmp" : 1.0,     vol slider
# "dryPan" : 0.25     bipolar slider
    
class TkRumklangPanel(TkSubEditor):

    NAME = "Rumklang"
    IMAGE_FILE = "resources/Rumklang/editor.png"
    TAB_FILE = "resources/Tabs/reverb.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,735,510,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)

        def linear_slider(param, range_, x, y):
            s = cf.linear_slider(canvas,param,editor,range_=range_)
            self.add_control(param,s)
            s.widget().place(x=x,y=y)

        def norm_slider(param,x,y):
            s = cf.normalized_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y)

        def eq_slider(param,x,y):
            s = cf.third_octave_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y)

        def amp_slider(param,x,y):
            s = cf.volume_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y)

        def pan_slider(param,x,y):
            s = cf.bipolar_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y)

        y0 = 50
        x0 = 75
        x1 = x0 + 60
        x2 = x1 + 60
        x3 = x2 + 60
        xeq = x3 + 75
        xlp = xeq
        xhp = xlp+60
        xdry = xhp+75
        xwet = xdry+120
        
        linear_slider("preDelay",(0.0,0.333),x0,y0)
        norm_slider("roomSize",x1,y0)
        norm_slider("damp",x2,y0)
        norm_slider("modDepth",x3,y0)
        eq_slider("lpcutoff",xlp,y0)
        eq_slider("hpcutoff",xhp,y0)
        amp_slider("dryAmp", xdry,y0)
        pan_slider("dryPan", xdry+60,y0)
        amp_slider("wetAmp", xwet,y0)
        pan_slider("wetPan", xwet+60,y0)
        
        msb_gate = ToggleButton(canvas,"gatted",editor,)
        self.add_control("gatted", msb_gate)
        msb_gate.layout((x0+157,y0+200))
        msb_gate.update_aspect()
                                
