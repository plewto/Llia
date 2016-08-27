# llia.synths.algo2.tk.global_editor

from __future__ import print_function
import Tkinter as tk
from llia.gui.tk.tk_subeditor import TkSubEditor
from llia.gui.tk.expslider import ExpSlider
import llia.synths.algo2.algo2_constants as con
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.freq_spinner import FrequencySpinnerControl

class TkAlgoGlobalEditor(TkSubEditor):

    def __init__(self, editor):
        name = "Algo Global"
        image_filename = "resources/Algo2/global_editor.png"
        ed_frame = editor.create_tab(name)
        self.main = tk.Canvas(ed_frame)
        self.main.pack(expand=True, fill='both')
        self.editor = editor
        TkSubEditor.__init__(self, self.main, editor, name)
        editor.add_child_editor(name, self)
        lab_panel = factory.image_label(self.main,  image_filename)
        lab_panel.pack(anchor='nw', expand=False)
        y0 = 90
        y_lfo_freq = 280
        x0 = 90
        x_port = x0
        x_xtern = x_port + 75
        x_xtern_scale = x_xtern
        x_xtern_bias = x_xtern_scale + 60
        x_xtern_pitch = x_xtern_bias + 60
        x_lfo = x_xtern_pitch + 75
        x_lfo_freq = x_lfo
        x_lfo_ratio = x_lfo
        x_lfo_mix = x_lfo_ratio+60
        x_lfo_delay = x_lfo_mix+60
        x_lfo_depth = x_lfo_delay+60
        x_vsens = x_lfo_depth+60
        x_vdepth = x_vsens+60
        x_amp = x_vdepth + 90
        self._norm_slider("port", (x_port, y0))
        self._linear_slider("x_scale", (-4,4), (x_xtern_scale, y0))
        self._linear_slider("x_bias", (-4,4), (x_xtern_bias, y0))
        self._norm_slider("x_pitch", (x_xtern_pitch, y0))
        lfo_freq_spinner = FrequencySpinnerControl(self.main, "lfo_freq", self.editor,
                                                   from_=0, to=con.MAX_LFO_FREQUENCY)
        self.add_control("lfo_freq", lfo_freq_spinner)
        lfo_freq_spinner.layout((x_lfo_freq,y_lfo_freq))
        s_lfo_ratio = cf.discrete_slider(self.main, "lfo_ratio", self.editor,
                                         values=con.LFO_RATIOS)
        self.add_control("lfo_ratio", s_lfo_ratio)
        s_lfo_ratio.widget().place(x=x_lfo_ratio,y=y0)
        self._norm_slider("lfo_mix", (x_lfo_mix, y0))
        self._linear_slider("lfo_delay", (0,4), (x_lfo_delay, y0))
        self._norm_slider("lfo_depth", (x_lfo_depth, y0))
        self._norm_slider("vsens", (x_vsens, y0))
        self._norm_slider("vdepth", (x_vdepth, y0))
        s_volume = cf.volume_slider(self.main, "amp", self.editor)
        self.add_control("amp", s_volume)
        s_volume.widget().place(x=x_amp, y=y0)

        
    def _norm_slider(self, param, offset):
        s = cf.normalized_slider(self.main, param, self.editor)
        self.add_control(param,s)
        x,y = offset
        s.widget().place(x=x,y=y)
        return s

    def _linear_slider(self, param, range_, offset):
        s = cf.linear_slider(self.main, param, self.editor,
                             range_=range_)
        self.add_control(param, s)
        x,y = offset
        s.widget().place(x=x,y=y)
        return s
