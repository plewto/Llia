
import llia.gui.tk.tk_factory as factory
from llia.gui.tk.tk_subeditor import TkSubEditor
from llia.gui.tk.addsr_editor import ADDSREditor



class TkFm2EnvEditor(TkSubEditor):


    NAME = "Env"
    IMAGE_FILE = "resources/FM2/env_editor.png"
    TAB_FILE = "resources/Tabs/adsr.png"
    
    def __init__(self,editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 1000, 650, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        y0 = 25       
        x0 = 75
        dx = 200
        size = (900,dx)
        for i,prefix in enumerate(("op2","efx","op1")):
            paramlist = []
            for p in ("Attack","Decay1","Decay2","Release","Breakpoint",
                      "Sustain","GateHold"):
                paramlist.append("%s%s" % (prefix,p))
            x = x0
            y = y0+(i*dx)
            ed = ADDSREditor(canvas,i,(x,y),size,paramlist,editor)
            self.add_child_editor(prefix,ed)
            ed.sync()
        
