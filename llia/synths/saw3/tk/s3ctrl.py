# llia.synths.saw3.tk.s3ctrl
#

from __future__ import print_function
from Tkinter import Frame

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cfactory
from llia.gui.tk.decade_control import DecadeControl
from llia.gui.tk.expslider import ExpSlider

class TkSaw3ControlPanel(TkSubEditor):

    NAME = "Controllers"
    IMAGE_FILE = "resources/Saw3/editor_controllers.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        lab_panel = factory.image_label(frame, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)
        # Envelopes
        s_env1_a = ExpSlider(frame, "env1Attack", editor,range_=60, degree=5,ttip="ENV1 Attack")
        s_env1_d = ExpSlider(frame, "env1Decay", editor,range_=60, degree=5,ttip="ENV1 Decay")
        s_env1_s = cfactory.normalized_slider(frame, "env1Sustain", editor, ttip="ENV1 Sustain")
        s_env1_r = ExpSlider(frame, "env1Release", editor,range_=60, degree=5,ttip="ENV1 Release")
        s_env2_a = ExpSlider(frame, "env2Attack", editor,range_=60, degree=5,ttip="ENV2 Attack")
        s_env2_d = ExpSlider(frame, "env2Decay", editor,range_=60, degree=5,ttip="ENV2 Decay")
        s_env2_s = cfactory.normalized_slider(frame, "env2Sustain", editor, ttip="ENV2 Sustain")
        s_env2_r = ExpSlider(frame, "env2Release", editor,range_=60, degree=5,ttip="ENV2 Release")
        y0, y1 = 50, 300
        x0 = 60
        x1 = x0+60
        x2 = x1+60
        x3 = x2+60
        s_env1_a.layout((x0, y0), checkbutton_offset = None)
        s_env1_d.layout((x1, y0), checkbutton_offset = None)
        s_env1_s.widget().place(x=x2, y=y0)
        s_env1_r.layout((x3, y0), checkbutton_offset = None)
        s_env2_a.layout((x0, y1), checkbutton_offset = None)
        s_env2_d.layout((x1, y1), checkbutton_offset = None)
        s_env2_s.widget().place(x=x2, y=y1)
        s_env2_r.layout((x3, y1), checkbutton_offset = None)
        self.add_control("env1Attack", s_env1_a)
        self.add_control("env1Decay", s_env1_d)
        self.add_control("env1Sustain", s_env1_s)
        self.add_control("env1Release", s_env1_r)
        self.add_control("env2Attack", s_env2_a)
        self.add_control("env2Decay", s_env2_d)
        self.add_control("env2Sustain", s_env2_s)
        self.add_control("env2Release", s_env2_r)
        # Vibrato
        s_vfreq = cfactory.simple_lfo_freq_slider(frame,"vfreq",editor,"Vibrato frequency")
        s_vsens = cfactory.normalized_slider(frame,"vsens",editor,"Vibrato Sensitivity")
        s_vdelay = cfactory.linear_slider(frame,"vdelay",editor,range_=(0,4),ttip="Vibrato delay")
        s_vdepth = cfactory.normalized_slider(frame,"vdepth",editor,"Vibrato depth")
        x4 = x3+90
        x5 = x4+60
        x6 = x5+60
        x7 = x6+60
        s_vfreq.widget().place(x=x4, y=y0)
        s_vdelay.widget().place(x=x5, y=y0)
        s_vdepth.widget().place(x=x6, y=y0)
        s_vsens.widget().place(x=x7, y=y0)
        self.add_control("vfreq",s_vfreq)        
        self.add_control("vsens",s_vsens)        
        self.add_control("vdelay",s_vdelay)        
        self.add_control("vdepth",s_vdepth)        
        # LFO
        s_lfo_freq = cfactory.simple_lfo_freq_slider(frame,"lfoFreq",editor,"LFO Frequency")
        s_lfo_delay = cfactory.linear_slider(frame,"lfoDelay",editor,range_=(0,4),ttip="LFO delay")
        s_lfo_depth = cfactory.normalized_slider(frame,"lfoDepth",editor,"LFO depth")
        s_lfo_freq.widget().place(x=x4, y=y1)
        s_lfo_delay.widget().place(x=x5, y=y1)
        s_lfo_depth.widget().place(x=x6, y=y1)
        self.add_control("lfoFreq",s_lfo_freq)        
        self.add_control("lfoDelay",s_lfo_delay)
        self.add_control("lfoDepth",s_lfo_depth)

        # Amp
        x8 = x7+90
        s_amp = cfactory.volume_slider(frame, "amp", editor)
        s_amp.widget().place(x=x8, y=y0)
