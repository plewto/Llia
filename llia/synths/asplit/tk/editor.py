# llia.synths.asplit.tk.editor

from Tkinter import StringVar

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB

def create_editor(parent):
    TkASplitPanel(parent)

class TkASplitPanel(TkSubEditor):

    NAME = "Audio Splitter"
    IMAGE_FILE = "resources/ASplit/editor.png"
    TAB_FILE = "resources/Tabs/spliter.png"
    
    # def __init__(self, editor):
    #     frame = editor.create_tab(self.NAME,self.TAB_FILE)
    #     frame.config(background=factory.bg())
    #     canvas = factory.canvas(frame, 900, 600, self.IMAGE_FILE)
    #     canvas.pack()
    #     TkSubEditor.__init__(self, canvas, editor, self.NAME)
    #     editor.add_child_editor(self.NAME, self)
    #     y0,y1 = 50,364
    #     x0 = 100
    #     for i,d in enumerate("ABCD "):
    #         x = x0 + (70 * i)
    #         if d == ' ':
    #             d == ''
    #             x += 50
    #         param = ("gain%s" % d).strip()
    #         vs = self.volume_slider(param,x,y0,height=300)
    #         self.mute_button(d, x,y1)

 
        

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 654, 565, self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        self._ledger_vars = {}
        #y0,y1 = 50,364
        y0,ymute,yledger = 75, 390, 450
        x0 = 100

        def mute_button(suffix,x):
            param = ("unmute%s" % suffix).strip()
            self.toggle(param,x-23,ymute,off=(0,"Mute"),on=(1,"On"))

        def ledger_entry(key,x):
            var = StringVar()
            self._ledger_vars[key] = var
            self._define_annotation(key)
            e = factory.entry(canvas,var,index=key)
            e.place(x=x-29,y=yledger,width=74)
            e.bind("<FocusOut>",self.ledger_callback)
            var.set(key)
            
        xmain = x0+50
        self.volume_slider("gain",xmain,y0,height=300)
        mute_button("",xmain)
        ledger_entry("MAIN",xmain)
        
        for i,key in enumerate("ABCD"):
            x = xmain+100+(i*80)
            param = "gain%s" % key
            self.volume_slider(param,x,y0,height=300)
            mute_button(key,x)
            ledger_entry("OUT_%s" % key, x)

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
