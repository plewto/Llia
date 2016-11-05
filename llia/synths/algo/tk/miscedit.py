# llia.synths.algo.tk.miscedit

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.tumbler import Tumbler
from llia.gui.tk.expslider import ExpSlider
import llia.synths.algo.algo_constants as acon
from llia.synths.algo.tk.envedit import TkAlgoEnvelopePanel


class TkAlgoMiscPanel(TkSubEditor):

    NAME = "Misc"
    IMAGE_FILE = "resources/Algo/misc_editor.png"

    ENV_WIDTH = 350
    ENV_HEIGHT = 150
    
    def __init__(self,editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 1000, 700, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME,self)
        
        y0 = 75
        y_tumbler = y0 + 50

        x0 = 75
        x_port = x0
        x_lfo = x_port + 75
        x_delay = x_lfo + 100
        x_vsens = x_delay + 60
        x_vdepth = x_vsens + 60
        x_xpitch= x_vdepth + 60
        x_moddepth = x_xpitch + 90
        x_xmod = x_moddepth + 60
        x_xscale = x_xmod + 90
        x_amp = x_xscale + 90
        
        def norm_slider(param,x):
            s = cf.normalized_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y0)
            return s

        def linear_slider(param,x,range_=(0,4)):
            s = cf.linear_slider(canvas,param,editor,range_=range_)
            self.add_control(param,s)
            s.widget().place(x=x,y=y0)
            return s

        def volume_slider(param,x):
            s = cf.volume_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y0)
            return s

        def tumbler(param,x):
            t = Tumbler(canvas,param,editor,digits=5,scale=0.001)
            self.add_control(param,t)
            t.layout((x,y_tumbler))
            t.update_aspect()
            return t

        norm_slider("port",x_port)
        tumbler("lfov_freq",x_lfo)
        linear_slider("lfov_delay",x_delay)
        norm_slider("vsens",x_vsens)
        norm_slider("vdepth",x_vdepth)
        norm_slider("xpitch",x_xpitch)
        norm_slider("modDepth",x_moddepth)
        norm_slider("xmod",x_xmod)
        linear_slider("xscale",x_xscale,(0,2))
        volume_slider("amp",x_amp)
