# llia.synths.controlmixer.tk.editor

from Tkinter import StringVar

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB

def create_editor(parent):
    TkControlmixerPanel(parent)

class TkControlmixerPanel(TkSubEditor):

    NAME = "ControlMixer"
    IMAGE_FILE = "resources/ControlMixer/editor.png"
    TAB_FILE = "resources/Tabs/mixer.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 770,654, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        self._ledger_vars = {}

        x0 = 75
        x_bias_offset = 60
        slider_width=14
        slider_height = 300

        y_slider = 75
        y_mute = y_slider+slider_height+40
        y_ledger = y_mute+60
        
        
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
            b.layout(offset = (x,y_mute))
            b.update_aspect()
            return b

        def entry(key,x):
            var = StringVar()
            var.set(key)
            self._ledger_vars[key] = var
            e = factory.entry(canvas,var,index=key)
            e.place(x=x+2,y=y_ledger,width=74)
            e.bind("<FocusOut>", self.ledger_callback)
            self._define_annotation(key)
            
        
        x_diff = 130
        for i,p in enumerate("ABCD"):
            x = x0 + i*x_diff
            scale_slider("scale%s" % p, x)
            bias_slider("bias%s" % p, x)
            mute_button("mute%s" % p, x)
            ledger_key = "IN_%s" % p
            entry(ledger_key,x)

        x_master = 600
        scale_slider("masterScale", x_master)
        bias_slider("masterBias", x_master)
        mute_button("masterMute", x_master)

    def ledger_callback(self, event):
        key = event.widget.index
        var = self._ledger_vars[key]
        self._set_annotation(key,var.get())

    def annotation(self, key, text=None):
        try:
            var = self._ledger_vars[key]
            if text != None:
                var.set(text)
                self._set_annotation(key, text)
            return var.get()
        except KeyError:
            return None
