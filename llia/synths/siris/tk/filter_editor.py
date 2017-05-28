# llia.synths.siris.tk.ks_editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
from llia.synths.siris.siris_constants import *

class TkSirisFilterPanel(TkSubEditor):

    NAME = "Filter"
    IMAGE_FILE = "resources/Siris/editor_filter.png"
    TAB_FILE = "resources/Siris/tab_filter.png"

    def __init__(self,editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,686,487,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.NAME)
        editor.add_child_editor(self.NAME, self)
        x0 = 75
        x_filter = x0+330
        y0, y1 = 75, 250
        self.volume_slider("nse_amp", x0, y0)
        self.volume_slider("ex1_amp", x0+60,y0)
        self.volume_slider("ex2_amp", x0+120,y0)
        self.exp_slider("nse_lowpass", 16000, x0+180, y0)
        self.exp_slider("nse_highpass", 16000, x0+240,y0)
        self.norm_slider("nse_velocity", x0, y1)
        self.exp_slider("nse_attack", MAX_ENV_SEGMENT, x0+60, y1)
        self.exp_slider("nse_decay", MAX_ENV_SEGMENT, x0+120, y1)
        self.exp_slider("filter_cutoff", 16000, x_filter, y0, degree=3)
        self.linear_slider("filter_track",(0,4),x_filter+60,y0)
        self.norm_slider("filter_res", x_filter+120, y0)
        self.exp_slider("filter_env", 16000, x_filter, y1, degree=3, checkbutton=(-15,150))
        self.exp_slider("filter_vlfo", 16000, x_filter+60, y1, degree=3, checkbutton=(-15,150))
        self.exp_slider("filter_velocity", 16000, x_filter+120, y1, degree=3, checkbutton=(-15,150))
        self.volume_slider("amp", x_filter+200, y0)

        
