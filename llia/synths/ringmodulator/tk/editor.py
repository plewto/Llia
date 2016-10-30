# llia.synths.ringmodulator.tk.editor


from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB,ToggleButton
from llia.gui.tk.tumbler import Tumbler


def create_editor(parent):
    TkRingmodulatorPanel(parent)
    
MAX_DELAY = 1.0

class TkRingmodulatorPanel(TkSubEditor):

    NAME = "RingModulator"
    IMAGE_FILE = "resources/RingModulator/editor.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 1400, 700, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)

        y0 = 50
        x0 = 75
        xim = x0+120
        xxm = xim + 90
        xxbleed = xxm+60
        xcbleed = xxbleed+90
        xamp = xcbleed+90
        

        def vslider(param,x):
            s = cf.volume_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y0)
            return s

        # def norm(param,x):
        #     s = cf.normalized_slider(canvas,param,editor)
        #     self.add_control(param,s)
        #     s.widget().place(x=x,y=y0)
        #     return s
        
        
        tfreq = Tumbler(canvas,"imodfreq",editor,digits=5,scale=1)
        self.add_control("imodfreq",tfreq)
        tfreq.layout((x0,y0))

        vslider("imodamp", xim)
        vslider("xmodamp", xxm)
        vslider("xmodbleed", xxbleed)
        vslider("carbleed", xcbleed)
        vslider("amp",xamp)
        
        
        
        
        
