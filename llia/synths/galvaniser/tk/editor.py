# llia.synths.galvaniser.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf

def create_editor(parent):
    TkGalvaniserPanel(parent)

class TkGalvaniserPanel(TkSubEditor):

    NAME = "Galvaniser"
    IMAGE_FILE = "resources/Galvaniser/editor.png"
    TAB_FILE = "resources/Galvaniser/tab.png"

    def __init__(self,editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,740,343,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.NAME)
        editor.add_child_editor(self.NAME, self)
        x0,y0 = 75,75
        x_tone = x0
        x_feedback = x_tone+60
        x_bandpass = x_feedback+90
        x_filter = x_bandpass
        x_mod = x_filter+60
        x_xmod = x_mod+60
        x_res = x_xmod+60

        x_lfo = x_res+90

        x_mix = x_lfo+90
        x_amp = x_mix+60
        
        self.norm_slider("tone",x_tone,y0)
        self.linear_slider("feedback",(-1.0,1.0),x_feedback,y0)

        self.norm_slider("filter",x_filter,y0)
        self.norm_slider("modDepth",x_mod,y0)
        self.norm_slider("xmodDepth",x_xmod,y0)
        self.norm_slider("res",x_res,y0)
        self.exp_slider("lfoFreq",16,x_lfo,y0,degree=3)


        self.norm_slider("efxmix",x_mix,y0)
        self.volume_slider("amp",x_amp,y0)
