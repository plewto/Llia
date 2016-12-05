# llia.synths.asplit.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB

def create_editor(parent):
    TkASplitPanel(parent)

class TkASplitPanel(TkSubEditor):

    NAME = "Audio Splitter"
    IMAGE_FILE = "resources/ASplit/editor.png"
    TAB_FILE = "resources/Tabs/spliter.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 900, 600, self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        y0,y1 = 50,364
        x0 = 100
        for i,d in enumerate("ABCD "):
            x = x0 + (70 * i)
            if d == ' ':
                d == ''
                x += 50
            param = ("gain%s" % d).strip()
            vs = self.volume_slider(param,x,y0,height=300)
            self.mute_button(d, x,y1)

    def mute_button(self,suffix,x,y):
        param = ("unmute%s" % suffix).strip()
        self.toggle(param,x-23,y,off=(0,"Mute"),on=(1,"On"))
        
