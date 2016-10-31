# llia.synths.qmod.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB, ToggleButton
from llia.gui.tk.tumbler import Tumbler

def create_editor(parent):
    TkQModPanel(parent)

class TkQModPanel(TkSubEditor):

    NAME = "QMod"
    IMAGE_FILE = "resources/QMod/editor.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 1000, 700, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)

        y0 = 50
        x0 = 75

        def norm_slider(param,x):
            s = cf.normalized_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y0)
            return s

        def volume_slider(param,x):
            s = cf.volume_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y0)
            return s

        def linear_slider(param,range_,x):
            s = cf.linear_slider(canvas,param,editor,range_=range_)
            self.add_control(param,s)
            s.widget().place(x=x,y=y0)
            return s

