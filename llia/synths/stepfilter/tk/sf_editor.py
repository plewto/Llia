# llia.synths.stepfilter.tk.sf_editor
#

from __future__ import print_function
from Tkinter import Frame

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
import llia.synths.stepfilter.sf_constants as sfcon


def create_stepfilter_editor(parent):
    pan1 = TkStepFilterPanel1(parent)

class TkStepFilterPanel1(TkSubEditor):

    NAME = "StepFilter"
    IMAGE_FILE = "resources/StepFilter/editor.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        self.pack(expand=True, fill="both")
        lab_panel = factory.image_label(self, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)
        # Clock
        s_clock = cf.simple_lfo_freq_slider(self, "clockFreq", editor)
        r_sliders = []
        r_labels = []
        a_sliders = []
        b_sliders = []
        x, xdelta = 0.125, 0.125
        r_values = []
        while x <= 8:
            r_values.append(x)
            x += xdelta
        x, xdelta = 0.01, 0.01
        mix_values = [0.001]
        while x <= 1:
            mix_values.append(x)
            x += xdelta
        mix_values.append(1)
        for i in range(8):
            j = i+1
            rk = "r%d" % j
            ak = "a%d" % j
            bk = "b%d" % j
            rslide = cf.discrete_slider(self, rk, editor, 
                                              r_values, ttip=rk)
            rslide.index = i
            aslide = cf.discrete_slider(self, ak, editor, 
                                              mix_values, ttip=ak)
            bslide = cf.discrete_slider(self, bk, editor, 
                                              mix_values, ttip=bk)
            self.add_control(rk, rslide)
            self.add_control(ak, aslide)
            self.add_control(bk, bslide)
            r_sliders.append(rslide)
            a_sliders.append(aslide)
            b_sliders.append(bslide)
            w = factory.label(self, text="%5.3f" % float(j))
            r_labels.append(w) 
           
            def client_callback(*args):
                absctrl, aspect, value = args
                index = absctrl.index
                lab = r_labels[index]
                lab.config(text = "%5.3f" % value)

            rslide.client_callback = client_callback

        s_alag = cf.normalized_slider(self, "aLag", editor, "A Lag time")
        s_amin = cf.discrete_slider(self, "aMin", editor, 
                                    sfcon.FILTER_FREQUENCIES, 
                                    "Minimum A frequency")
        s_amax = cf.discrete_slider(self, "aMax", editor, 
                                    sfcon.FILTER_FREQUENCIES, 
                                    "Maximum A frequency")
        s_ares = cf.normalized_slider(self, "aRes", editor, 
                                      "A Resonace")
        s_apan = cf.bipolar_slider(self, "aPan", editor, 
                                   "A Pan position")
        s_apanlfo = cf.normalized_slider(self, "panLfoA", editor, 
                                         "LFO -> A Pan")
        s_aamp = cf.volume_slider(self, "aAmp", editor, "A Filter amp")
        s_blag = cf.normalized_slider(self, "bLag", editor, 
                                      "B Lag time")
        s_bmin = cf.discrete_slider(self, "bMin", editor, 
                                    sfcon.FILTER_FREQUENCIES, 
                                    "Minimum B frequency")
        s_bmax = cf.discrete_slider(self, "bMax", editor, 
                                    sfcon.FILTER_FREQUENCIES, 
                                    "Maximum B frequency")
        s_bres = cf.normalized_slider(self, "bRes", editor, 
                                      "B Resonace")
        s_bpan = cf.bipolar_slider(self, "bPan", editor, 
                                   "B Pan position")
        s_bpanlfo = cf.normalized_slider(self, "panLfoB", editor, 
                                         "LFO -> B Pan")
        s_bpanratio = cf.linear_slider(self, "panLfoBRatio", editor, 
                                       range_=(1, 8))
        s_bamp = cf.volume_slider(self, "bAmp", editor, "B Filter Amp")
        s_drypan = cf.bipolar_slider(self, "dryPan", editor, 
                                     "Dry signal Pan")
        s_drypanlfo = cf.normalized_slider(self, "panLfoDry", editor, 
                                           "LFO -> Dry pan")
        s_dryamp = cf.volume_slider(self, "dryAmp", editor, 
                                    "Dry signal amp")
        s_amp = cf.volume_slider(self, "amp", editor, "Overall amp")
        s_lfo = cf.simple_lfo_freq_slider(self, "panLfoFreq", editor, 
                                          "Panning LFO Frequency")
        s_blfo = cf.discrete_slider(self, "panLfoBRatio", editor, 
                                    sfcon.BLFO_RATIOS, 
                                    "Panning LFO B FIlter ratio")
        self.add_control("clockFreq", s_clock)
        self.add_control("aLag", s_alag)
        self.add_control("aMin", s_amin)
        self.add_control("aMax", s_amax)
        self.add_control("aRes", s_ares)
        self.add_control("aPan", s_apan)
        self.add_control("panLfoA", s_apanlfo)
        self.add_control("aAmp", s_aamp)
        self.add_control("bLag", s_blag)
        self.add_control("bMin", s_bmin)
        self.add_control("bMax", s_bmax)
        self.add_control("bRes", s_bres)
        self.add_control("bPan", s_bpan)
        self.add_control("panLfoB", s_bpanlfo)
        self.add_control("panLfoBRatio", s_bpanratio)
        self.add_control("bAmp", s_bamp)
        self.add_control("dryPan", s_drypan)
        self.add_control("panLfoDry", s_drypanlfo)
        self.add_control("dryAmp", s_dryamp)
        self.add_control("amp", s_amp)
        self.add_control("panLfoFreq", s_lfo)
        self.add_control("panLfoBRatio", s_blfo)
        s_clock.widget().place(x=55, y=50)
        for i in range(8):
            x = 100 + i*50
            r_sliders[i].widget().place(x=x, y=50)
            r_labels[i].place(x=x-8, y=200)
            a_sliders[i].widget().place(x=x, y=225)
            b_sliders[i].widget().place(x=x, y=400)
        ydry, ya, yb = 50, 225, 400
        x1, x2, x3, x4, x5, x6 = 500, 557, 614, 671, 728, 785
        x7, x8 = 842, 899
        s_alag.widget().place(x=x1, y=ya)
        s_amin.widget().place(x=x2, y=ya)
        s_amax.widget().place(x=x3, y=ya)
        s_ares.widget().place(x=x4, y=ya)
        s_apan.widget().place(x=x5, y=ya)
        s_apanlfo.widget().place(x=x6, y=ya)
        s_aamp.widget().place(x=x7, y=ya)
        s_blag.widget().place(x=x1, y=yb)
        s_bmin.widget().place(x=x2, y=yb)
        s_bmax.widget().place(x=x3, y=yb)
        s_bres.widget().place(x=x4, y=yb)
        s_bpan.widget().place(x=x5, y=yb)
        s_bpanlfo.widget().place(x=x6, y=yb)
        s_bamp.widget().place(x=x7, y=yb)
        s_drypan.widget().place(x=x5, y=ydry)
        s_drypanlfo.widget().place(x=x6, y=ydry)
        s_dryamp.widget().place(x=x7, y=ydry)
        s_amp.widget().place(x=x8, y=ydry)
        s_lfo.widget().place(x=x2, y=ydry)
        s_blfo.widget().place(x=x3, y=ydry)
        
        
