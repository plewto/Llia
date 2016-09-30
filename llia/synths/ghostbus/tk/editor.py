# llia.synths.ghostbus.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB
from llia.synths.ghostbus.ghost_data import MAX_DELAY

def create_editor(parent):
    TkGhostbusPanel(parent)

class TkGhostbusPanel(TkSubEditor):

    NAME = "Ghostbus"
    IMAGE_FILE = "resources/Ghostbus/editor.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 1000, 700, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)

        y_slider = 75
        x0 = 75
        x_bias_offset = 60
        slider_width=14
        slider_height = 300
        
        def scale_slider(param, x):
            s = cf.linear_slider(canvas,param,self.editor,range_=(-4.0, 4.0))
            self.add_control(param,s)
            s.widget().place(x=x,y=y_slider,
                             width=slider_width,
                             height=slider_height)
            return s

        def bias_slider(param, x):
            s = cf.linear_slider(canvas,param,self.editor,range_=(-4.0,4.0))
            self.add_control(param,s)
            s.widget().place(x=x+x_bias_offset,y=y_slider,
                             width=slider_width,
                             height=slider_height)
            return s

        def mute_button(param, x):
            b = MSB(canvas,param,self.editor,2)
            aoff = {'fill' : 'black',
                    'foreground' : 'gray',
                    'outline' : 'gray',
                    'text' : 'Mute'}
            aon = {'fill' : '#002e00',
                   'foreground' : 'white',
                   'outline' : '#096c00',
                   'text' : 'Mute'}
            b.define_aspect(0, 0, aoff)
            b.define_aspect(1, 1, aon)
            self.add_control(param,b)
            x = x + 8
            y = y_slider + slider_height + 40
            b.layout(offset = (x,y))
            b.update_aspect()
            return b
        
        x_diff = 130
        for i,p in enumerate("ABCD"):
            x = x0 + i*x_diff
            scale_slider("scale%s" % p, x)
            bias_slider("bias%s" % p, x)
            mute_button("mute%s" % p, x)

        x_master = 600
        scale_slider("masterScale", x_master)
        bias_slider("masterBias", x_master)
        mute_button("masterMute", x_master)
   

        s_lag = cf.normalized_slider(canvas,"lag",self.editor)
        s_delay = cf.normalized_slider(canvas,"delay",self.editor)
        self.add_control("lag", s_lag)
        self.add_control("delay", s_delay)
        s_delay.widget().place(x=x_master+120,y=y_slider, width=14, height=slider_height)
        s_lag.widget().place(x=x_master+180,y=y_slider, width=14, height=slider_height)
        
