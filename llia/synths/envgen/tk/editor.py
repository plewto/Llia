# llia.synths.envgen.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB, ToggleButton
from llia.gui.tk.addsr_editor import ADDSREditor


def create_editor(parent):
    TkEnvgenPanel(parent)

class TkEnvgenPanel(TkSubEditor):

    NAME = "Envgen"
    IMAGE_FILE = "resources/Envgen/editor.png"
    TAB_FILE = "resources/Envgen/tab.png"


    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 1000, 700, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)

        w = 900
        h = 300
        
        y0 = 50
        x0 = 50
        xmsb = w/2
        ymsb = h-50
        
        for i,prefix in enumerate("ab"):
            x = x0
            y = y0 + i*(300+25)
            paramlist = []
            for s in ("Attack","Decay1","Decay2","Release","Breakpoint",
                      "Sustain","Envmode"):
                paramlist.append("%s%s" % (prefix,s))
            env = ADDSREditor(canvas,i,(x,y),(w,h),paramlist,editor,12)
            self.add_child_editor("ENV%s" % prefix, env)
            env.sync()
            param = "%sInvert" % prefix
            msb = ToggleButton(canvas,param,editor,["+Pos","-Inv"])
            self.add_control(param,msb)
            msb.layout((x+xmsb,y+ymsb))
            msb.update_aspect()
            
            
                              

