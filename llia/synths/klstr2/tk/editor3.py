# llia.synths.tk.editor2

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.addsr_editor import ADDSREditor
from llia.synths.klstr2.klstr2_constants import *

class TkKlstr2ExternalPanel(TkSubEditor):

    NAME = "Extern"
    IMAGE_FILE = "resources/Klstr2/editor3.png"
    TAB_FILE = "resources/Klstr2/tab3.png"

    def __init__(self,editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1000,700,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.NAME)
        editor.add_child_editor(self.NAME, self)

        x0 = 75
        y0 = 75
        y1 = 380

        self.norm_slider("spread_external",x0,y0)
        self.norm_slider("cluster_external",x0+60,y0)

        msb_harm = self.msb("harm2_external",len(POLAR_HARMONIC_MOD_RANGE),x0+120,y0)
        msb_filter = self.msb("f1_freq_external",len(FILTER_MOD_VALUES),x0+120,y0+122)
        for i,n in enumerate(POLAR_HARMONIC_MOD_RANGE):
            fg = None
            self.msb_aspect(msb_harm,i,n,foreground=fg)
        for i,n in enumerate(FILTER_MOD_VALUES):
            fg = None
            self.msb_aspect(msb_filter,i,n,foreground=fg)
        msb_harm.update_aspect()
        msb_filter.update_aspect()
