
# llia.synths.panner.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.expslider import ExpSlider

def create_editor(parent):
    TkPannerPanel(parent)

    
class TkPannerPanel(TkSubEditor):

    NAME = "Panner"
    IMAGE_FILE = "resources/Panner/editor.png"
    TAB_FILE = "resources/Tabs/panner.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        lab_panel = factory.image_label(frame, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)
        s_pos = cf.bipolar_slider(frame, "pos", editor)
        s_lfo_freq = ExpSlider(frame, "lfoFreq", editor, range_=100, degree=3)
        s_lfo_depth = cf.normalized_slider(frame, "lfoDepth", editor)
        s_xscale = cf.linear_slider(frame, "xscale", editor, range_=(-2, 2))
        s_xbias = cf.linear_slider(frame, "xbias", editor, range_=(-2,2))
        s_amp = cf.volume_slider(frame, "amp", editor)
        self.add_control("pos", s_pos)
        self.add_control("lfoFreq", s_lfo_freq)
        self.add_control("lfoDepth", s_lfo_depth)
        self.add_control("xscale", s_xscale)
        self.add_control("xbias", s_xbias)
        self.add_control("amp", s_amp)
        y0 = 60
        x0 = 120
        x_lfo_freq = x0 + 90
        x_lfo_depth = x_lfo_freq + 60
        x_xscale = x_lfo_depth + 90
        x_xbias = x_xscale + 60
        x_amp = x_xbias + 90
        s_pos.widget().place(x=x0, y=y0, height=200)
        s_lfo_freq.layout(offset=(x_lfo_freq, y0), height=200, checkbutton_offset=None)
        s_lfo_depth.widget().place(x=x_lfo_depth, y=y0, height=200)
        s_xscale.widget().place(x=x_xscale, y=y0, height=200)
        s_xbias.widget().place(x=x_xbias, y=y0, height=200)
        s_amp.widget().place(x=x_amp, y=y0, height=200)
        
                                
                           
        
