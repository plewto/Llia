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

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        lab_panel = factory.image_label(frame, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)

        s_delay = cf.linear_slider(frame, "delayTime", editor, range_=(0, MAX_DELAY))
        s_wow = ExpSlider(frame, "wow", editor, range_=1)
        s_wowfreq = ExpSlider(frame, "wowFreq", editor, range_=5)
        s_flutter = ExpSlider(frame, "flutter", editor, range_=1)
        s_xdelay = ExpSlider(frame, "xDelayMod", editor, range_=1)
        s_feedback = cf.normalized_slider(frame, "feedback", editor)
        s_gain = cf.linear_slider(frame, "gain", editor, range_=(0.5, 2))
        s_threshold = ExpSlider(frame, "threshold", editor, range_=1)
        s_lowcut = cf.third_octave_slider(frame, "lowcut", editor)
        s_highcut = cf.third_octave_slider(frame, "highcut", editor)
        s_efxmix = cf.normalized_slider(frame, "efxMix", editor)
        s_xefxmix = cf.normalized_slider(frame, "xEfxMix", editor)
        s_amp = cf.volume_slider(frame, "amp", editor)

        self.add_control("delayTime",s_delay)
        self.add_control("wow",s_wow)
        self.add_control("wowFreq",s_wowfreq)
        self.add_control("flutter",s_flutter)
        self.add_control("xDelayMod",s_xdelay)
        self.add_control("feedback",s_feedback)
        self.add_control("gain",s_gain)
        self.add_control("threshold",s_threshold)
        self.add_control("lowcut",s_lowcut)
        self.add_control("highcut",s_highcut)
        self.add_control("efxMix",s_efxmix)
        self.add_control("xEfxMix",s_xefxmix)
        self.add_control("amp",s_amp)

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
      
        s_delay.widget().place(x=x_delay, y=y0, height=200)
        s_wow.layout(offset=(x_wow, y0), checkbutton_offset=None, height=200)
        s_wowfreq.layout(offset=(x_wfreq, y0), checkbutton_offset=None, height=200)
        s_flutter.layout(offset=(x_flutter, y0), checkbutton_offset=None, height=200)
        s_xdelay.layout(offset=(x_xdelay, y0), checkbutton_offset=None, height=200)
        s_feedback.widget().place(x=x_fb, y=y0, height=200)
        s_gain.widget().place(x=x_gain, y=y0, height=200)
        s_threshold.layout(offset=(x_threshold, y0), checkbutton_offset=None, height=200)
        s_lowcut.widget().place(x=x_low, y=y0, height=200)
        s_highcut.widget().place(x=x_high, y=y0, height=200)
        s_efxmix.widget().place(x=x_mix, y=y0, height=200)
        s_xefxmix.widget().place(x=x_xmix, y=y0, height=200)
        s_amp.widget().place(x=x_amp, y=y0, height=200)

        # b_delay = self._button(frame, x_delay, y1, self._delay_finetune_callback)


    def _button(self, master, x, y, command):
        x_shift = -8
        b = factory.button(master, "Fine", command)
        b.place(x=x+x_shift,  y=y, width=32, height=24)
        return b
        

    def _delay_finetune_callback(self):
        print("delay_finetune_callback")

    def _xdelay_finetune_callback(self):
        print("xdelay_finetune_callback")
