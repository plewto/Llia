# llia.synths.qmod.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB, ToggleButton
from llia.gui.tk.tumbler import Tumbler
from llia.synths.qmod.qmod_data import FILTER_VALUES,MAX_INPUT_GAIN_MAGNITUDE

def create_editor(parent):
    TkQModPanel(parent)

class TkQModPanel(TkSubEditor):

    NAME = "QMod"
    IMAGE_FILE = "resources/QMod/editor.png"
    TAB_FILE = "resources/QMod/tab.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 741,700, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)

        y0 = 50
        x0 = 75
        xfilter = x0+130
        xmod = xfilter+90
        xattack = xmod + 90
        xrelease = xattack + 60
        xdry = xrelease+90
        xwet = xdry+60
               
        
        def norm_slider(param,x):
            s = cf.normalized_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y0)
            return s

        def volume_slider(param,x):
            s = cf.volume_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y0)
            return s

        def linear_slider(param,range_,x):
            s = cf.linear_slider(canvas,param,editor,range_=range_)
            self.add_control(param,s)
            s.widget().place(x=x,y=y0)
            return s

        t_freq = Tumbler(canvas,"fixedFrequency",editor,
                         digits = 4, scale=0.01)
        t_track = Tumbler(canvas,"keyTrack",editor,
                          digits=2, scale=1, range_=(0,16))
        self.add_control("fixedFrequency",t_freq)
        self.add_control("keyTrack",t_track)
        t_freq.layout((x0+25,y0+25))
        t_track.layout((x0+40,y0+100))

        cfill = 'black'
        cforeground = 'white'
        coutline = 'white'
        
        msb_filter = MSB(canvas,"inputFilter",editor,len(FILTER_VALUES))
        for i,v in enumerate(FILTER_VALUES):
            k = v/1000
            tx = "%dk" % k
            d = {"fill" : cfill,
                 "foreground" : cforeground,
                 "outline" : coutline,
                 "value" : v,
                 "text" : tx}
            msb_filter.define_aspect(i,v,d)
        self.add_control("inputFilter",msb_filter)
        msb_filter.layout((xfilter,y0+25))
        msb_filter.update_aspect()

        msb_gain = MSB(canvas,"inputGain",editor,MAX_INPUT_GAIN_MAGNITUDE)
        for i in range(MAX_INPUT_GAIN_MAGNITUDE):
            j = i+1
            v = 10**i
            tx = "x%d" % j
            d = {"fill" : cfill,
                 "foreground" : cforeground,
                 "outline" : coutline,
                 "value" : v,
                 "text" : tx}
            msb_gain.define_aspect(i,v,d)
        self.add_control("inputGain",msb_gain)
        msb_gain.layout((xfilter,y0+100))
        msb_gain.update_aspect()
        norm_slider("modDepth",xmod)
        linear_slider("attack",(0,4),xattack)
        linear_slider("release",(0,4),xrelease)

        msb_env = ToggleButton(canvas,"envelopeSelect",editor,
                               text=("Follow","ASR"),
                               values = (0,1),
                               fill=cfill,
                               selected_fill = cfill,
                               foreground=cforeground,
                               selected_foreground=cforeground,
                               outline=coutline)
                               
        self.add_control("envelopeSelect",msb_env)
        msb_env.layout((xattack+8,y0+200))
        msb_env.update_aspect()
        volume_slider("dryAmp",xdry)
        volume_slider("wetAmp",xwet)
