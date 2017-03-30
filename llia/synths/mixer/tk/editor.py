# llia.synths.mixer.tk.editor


from Tkinter import StringVar
from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB

def create_editor(parent):
    TkMixerPanel(parent)


class TkMixerPanel(TkSubEditor):

    NAME = "Mixer"
    IMAGE_FILE = "resources/Mixer/editor.png"
    TAB_FILE = "resources/Tabs/mixer.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 811,700,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        y0 = 60
        ypan = y0 + 350
        ymod = ypan
        ymute = ymod + 150
        yledger = ymute+60
        x0 = 120
        xmain = x0+500
        self._ledger_vars = {}

        
        def fader(chan, x):
            param = "gain%s" % chan
            s = cf.volume_slider(canvas, param, editor)
            self.add_control(param,s)
            s.widget().place(x=x, y=y0, height=300)

        def panner(chan, x):
            param = "pan%s" % chan
            s = cf.bipolar_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x, y=ypan, height=100)

        def mod_depth(chan, x):
            param = "mod%s" % chan
            s = cf.normalized_slider(canvas, param, editor)
            self.add_control(param, s)
            s.widget().place(x=x, y=ymod, height=100)

        def entry(key,x,y=yledger):
            var = StringVar()
            self._ledger_vars[key] = var
            e = factory.entry(canvas,var, index=key)
            e.place(x=x,y=y, width=74)
            e.bind("<FocusOut>", self.ledger_callback)
            self._define_annotation(key)
            
        for i,prefix in enumerate("ABCD"):
            chan = "%s" % prefix
            x = x0 + i * 120
            x_pan = x
            x_mod = x+60
            fader(chan, x+30)
            panner(chan, x_pan)
            mod_depth(chan, x_mod)
            aoff = {'fill' : 'black',
                    'foreground' : 'gray',
                    'outline' : 'gray',
                    'text' : 'Mute'}
            aon = {'fill' : '#002e00',
                   'foreground' : 'white',
                   'outline' : '#096c00',
                   'text' : 'Mute'}
            msb_mute = MSB(canvas,"mute%s"%prefix,editor,2)
            self.add_control("mute%s"%prefix,msb_mute)
            msb_mute.define_aspect(0,0,aoff)
            msb_mute.define_aspect(1,1,aon)
            msb_mute.layout((x+7,ymute))
            msb_mute.update_aspect()
            ledger_key = "IN_%s" % prefix
            entry(ledger_key,x)

        for i in range(2):
            x = xmain + i*60
            fader(str(i+1), x)

        entry("OUT_1", xmain, y=yledger-50)
        entry("OUT_2", xmain, y=yledger)
            
    def ledger_callback(self, event):
        key = event.widget.index
        var = self._ledger_vars[key]
        self._set_annotation(key, var.get())

    def annotation(self, key, text=None):
        try:
            var = self._ledger_vars[key]
            if text != None:
                var.set(text)
                self._set_annotation(key, text)
            return var.get()
        except KeyError:
            return None
