# llia.synths.fm2.tk.editor2

from Tkinter import Canvas

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB
from llia.gui.tk.freq_spinner import FrequencySpinnerControl



class TkFm2Panel2(TkSubEditor):

    NAME = "FM2 LFO"
    IMAGE_FILE = "resources/FM2/editor2.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 900, 600, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)

        y0 = 50
        y1 = 250
        x0 = 100
        x_port = x0
        x_lfo = x_port + 90
        x_delay = x_lfo
        x_vsens = x_delay + 60
        x_vdepth = x_vsens + 60

        x_extern = x_vdepth + 90
        x_xpitch = x_extern
        x_xdepth = x_xpitch + 60
        x_xscale = x_xdepth + 60
        x_xbias = x_xscale + 60

        x_amp = x_xbias + 90
        
        self.norm_slider("port", x0, y0)
        self.spinner("lfoFreq", x_lfo, y1)
        self.linear_slider("lfoDelay", (0,4), x_delay, y0)
        self.norm_slider("vsens", x_vsens, y0)
        self.norm_slider("vdepth", x_vdepth, y0)
        self.norm_slider("xPitch", x_xpitch, y0)
        self.norm_slider("xModDepth", x_xdepth, y0)
        self.linear_slider("xScale", (0,4), x_xscale, y0)
        self.linear_slider("xBias", (-4,4), x_xbias, y0)
        svol = cf.volume_slider(self.canvas, "amp", editor)
        self.add_control("amp", svol)
        svol.widget().place(x=x_amp, y=y0, width=14, height=150)
        
        
    def spinner(self, param, x, y, from_=0, to=300): 
        s = FrequencySpinnerControl(self.canvas,param,self.editor,from_, to)
        self.add_control(param, s)
        s.layout(offset=(x,y))
        return s

    def norm_slider(self, param, x, y, width=14, height=150):
        s = cf.normalized_slider(self.canvas, param, self.editor)
        self.add_control(param,s)
        s.widget().place(x=x,y=y,width=width, height=height)
        return s

    def linear_slider(self, param, range_, x, y, width=14, height=150):
        s = cf.linear_slider(self.canvas, param, self.editor,
                             range_=range_)
        self.add_control(param, s)
        s.widget().place(x=x,y=y,width=width, height=height)
        return s
        
