# llia.synths.carnal.tk.editor


from __future__ import print_function

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.expslider import ExpSlider

MAX_DELAY = 1.5

def create_editor(parent):
    pannel = TkCarnalPanel(parent)


    

class TkCarnalPanel(TkSubEditor):

    NAME = "Carnal Delay"
    IMAGE_FILE = "resources/CarnalDelay/editor.png"
    TAB_FILE = "resources/Tabs/delay.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 1500, 708, self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        y0, y1 = 105,358
        x_delay = 105
        x_wow = x_delay + 60
        x_wfreq = x_wow + 60
        x_flutter = x_wfreq + 60
        x_xdelay = x_flutter + 60
        x_fb = x_xdelay + 90
        x_gain = x_fb + 60
        x_threshold = x_gain + 60
        x_low = x_threshold + 60
        x_high = x_low + 60
        x_mix = x_high + 90
        x_xmix = x_mix + 60
        x_amp = x_xmix + 90
        self.linear_slider("delayTime",(0,MAX_DELAY),x_delay,y0,height=200)
        self.exp_slider("wow",1.0,x_wow,y0,height=200)
        self.exp_slider("wowFreq",5.0,x_wfreq,y0,height=200)
        self.exp_slider("flutter",1.0,x_flutter,y0,height=200)
        self.exp_slider("xDelayMod",1.0,x_xdelay,y0,height=200)
        self.norm_slider("feedback",x_fb,y0,height=200)
        self.linear_slider("gain",(0.5,2.0),x_gain,y0,height=200)
        self.exp_slider("threshold",1.0,x_threshold,y0,height=200)
        s_lowcut = cf.third_octave_slider(frame, "lowcut", editor)
        s_highcut = cf.third_octave_slider(frame, "highcut", editor)
        self.norm_slider("efxMix",x_mix,y0,height=200)
        self.norm_slider("xEfxMix",x_xmix,y0,height=200)
        self.volume_slider("amp",x_amp,y0,height=200)
        self.add_control("lowcut",s_lowcut)
        self.add_control("highcut",s_highcut)
        s_lowcut.widget().place(x=x_low, y=y0, height=200)
        s_highcut.widget().place(x=x_high, y=y0, height=200)
