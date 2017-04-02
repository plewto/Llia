# llia.synths.klstr2.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf

def create_editor(parent):
    TkKlstr2Panel(parent)

class TkKlstr2Panel(TkSubEditor):

    NAME = "Klstr2"
    IMAGE_FILE = "resources/Klstr2/editor.png"
    TAB_FILE = "resources/Klstr2/tab.png"

    def __init__(self,editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1000,700,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.NAME)
        editor.add_child_editor(self.NAME, self)
        x0,y0 = 75,75
