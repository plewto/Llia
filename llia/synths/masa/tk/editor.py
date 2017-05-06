# llia.synths.masa.tk.editor

from __future__ import print_function

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cfactory
from llia.gui.tk.expslider import ExpSlider

def create_editor(parent):
    panel1 = TkMasaPanel1(parent)

class TkMasaPanel1(TkSubEditor):

    NAME = "MASA"
    IMAGE_FILE = "resources/MASA/editor.png"
    TAB_FILE = "resources/MASA/tab.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        frame.config(background=factory.bg())
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        lab_panel = factory.image_label(frame, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)

        y0, y1, y2 = 60, 170, 280
        x0, xdelta = 60, 30        
        for i in range(9):
            j = i+1
            x = x0+i*xdelta
            pa = "a%d" % j
            self.norm_slider(pa,x,y0,height=100)
            pp = "p%d" % j
            self.norm_slider(pp,x,y1,height=100)
            px = "x%d" % j
            self.norm_slider(px,x,y2,height=100)

        # Envelope
        xenv = x0+(xdelta*10)
        self.exp_slider("attack",1.0,xenv,y0+30,height=100)
        self.exp_slider("decay",1.0,xenv,y2-30,height=100)
   
        # Vibrato
        xvib=xenv+120
        self.exp_slider("vfreq",8.0,xvib,y0)
        self.linear_slider("vdelay",(0,4),xvib+60,y0)
        self.norm_slider("vsens",xvib+120,y0)
        self.norm_slider("vdepth",xvib+180,y0)
   
        # X Bus
        xx = xvib
        self.linear_slider("xBias",(-2,2),xx,y2)
        self.linear_slider("xScale",(0,2),xx+60,y2)
        self.exp_slider("xToFreq",1.0,xx+120,y2)

        # Amp
        self.volume_slider("amp",xx+188,y2)
