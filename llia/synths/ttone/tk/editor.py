# llia.synths.ttone.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf

def create_editor(parent):
    TkTTonePanel(parent)

class TkTTonePanel(TkSubEditor):

    NAME = "TTone"
    IMAGE_FILE = "resources/TTone/editor.png"
    TAB_FILE = "resources/TTone/tab.png"

    def __init__(self,editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1000,700,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.NAME)
        editor.add_child_editor(self.NAME, self)
        x0,y0 = 150,75
        self.tumbler("ratio",5,0.001,x0,y0)
        self.tumbler("bias",6,0.01,x0-8,y0+100)
        msb = self.msb("wave",4,x0+7,y0+200)
        for i,txt in enumerate(("Sine","Square","Saw","Noise")):
            self.msb_aspect(msb,i,i,text=txt)
        self.volume_slider("amp",x0+200,y0,height=250)
