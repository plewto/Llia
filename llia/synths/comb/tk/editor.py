# llia.synths.comb.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf

def create_editor(parent):
    TkCombPanel(parent)

class TkCombPanel(TkSubEditor):

    NAME = "Comb"
    IMAGE_FILE = "resources/Comb/editor.png"
    TAB_FILE = "resources/Comb/tab.png"

    def __init__(self,editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,465,478,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.NAME)
        editor.add_child_editor(self.NAME, self)
        x0,y0 = 150, 75

        x_scale = x0
        x_delay = x0+22
        x_phase = x_scale+75
        x_wetamp = x_phase+108

        y_scale = y0+150
        y_delay = y_scale+50
        y_phase = y_scale
        y_wetamp = y_delay

        msb_scale = self.msb("delayScale",3,x_scale,y_scale)
        self.norm_slider("delay",x_delay,y_delay)

        msb_phase =self.msb("phase",2,x_phase,y_phase)
        self.volume_slider("wet",x_wetamp, y_wetamp)

        self.msb_aspect(msb_scale, 0, 0.001, "x1")
        self.msb_aspect(msb_scale, 1, 0.010, "x2")
        self.msb_aspect(msb_scale, 2, 0.100, "x3")
        msb_scale.update_aspect()
        
        self.msb_aspect(msb_phase, 0, -1, "-")
        self.msb_aspect(msb_phase, 1, 1, "+")
        msb_phase.update_aspect()
