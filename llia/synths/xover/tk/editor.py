# llia.synths.xover.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.decade_control import DecadeControl
from llia.synths.xover.xover_data import LF_RATIOS, CROSSOVER_FREQUENCIES


def create_editor(parent):
    TkXOverPanel(parent)

class TkXOverPanel(TkSubEditor):

    NAME = "XOver"
    IMAGE_FILE = "resources/XOver/editor.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME)
        frame.config(background=factory.bg())
        TkSubEditor.__init__(self, frame, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        lab_panel = factory.image_label(frame, self.IMAGE_FILE)
        lab_panel.pack(anchor="nw", expand=False)
        y0,y1 = 60, 300
        x0 = 60
        x_crossover = x0 + 150
        x_minx = x_crossover+50
        x_maxx = x_minx + 50
        x_lfo_ratio = x_maxx + 60
        x_lfo_depth = x_lfo_ratio + 60
        x_external = x_lfo_depth + 60
        x_res = x_external + 60
        
        def discrete_slider(param, x, y, values):
            s = cf.discrete_slider(frame, param, editor, values=values)
            self.add_control(param, s)
            s.widget().place(x=x, y=y)
            return s

        def norm_slider(param, x, y):
            s = cf.normalized_slider(frame, param, editor)
            self.add_control(param, s)
            s.widget().place(x=x, y=y)
            return s

        def amp_slider(param, x, y):
            s = cf.volume_slider(frame, param, editor)
            self.add_control(param, s)
            s.widget().place(x=x,y=y)
            return s

        def linear_slider(param, x, y, range_):
            s = cf.linear_slider(frame, param, editor, range_=range_)
            self.add_control(param, s)
            s.widget().place(x=x,y=y)
            return s
        
        dc_lfo_freq = DecadeControl(frame, "lfoFreq", editor,
                                      coarse = (0.01, 10),
                                      limit = (0.01, 100))
        self.add_control("lfoFreq", dc_lfo_freq)
        dc_lfo_freq.layout(offset=(x0,y0), label_offset=(0, 100))
        discrete_slider("crossover",x_crossover, y0, CROSSOVER_FREQUENCIES)
        discrete_slider("minCrossover",x_minx, y0, CROSSOVER_FREQUENCIES)
        discrete_slider("maxCrossover",x_maxx, y0, CROSSOVER_FREQUENCIES)
        discrete_slider("xoverLfoRatio",x_lfo_ratio, y0, LF_RATIOS)
        norm_slider("xoverLfoDepth", x_lfo_depth, y0)
        norm_slider("xoverX", x_external, y0)
        norm_slider("res", x_res, y0)

        x_scale = x_res + 90
        x_bias = x_scale + 60
        linear_slider("xScale", x_scale, y0, (0.0, 4.0))
        linear_slider("xBias", x_bias, y0, (-4.0, 4.0))
        
        x_lp = x0
        x_lp_lfo_ratio = x_lp + 60
        x_lp_lfo_depth = x_lp_lfo_ratio + 60
        x_lp_external = x_lp_lfo_depth + 60
        x_lp_mix = x_lp_external + 60
        norm_slider("lpMode", x_lp, y1)
        discrete_slider("lpLfoRatio", x_lp_lfo_ratio, y1,LF_RATIOS)
        norm_slider("lpMixLfo", x_lp_lfo_depth, y1)
        norm_slider("lpMixX", x_lp_external, y1)
        amp_slider("lpMix", x_lp_mix, y1)
        
        x_hp = x_lp_mix + 90
        x_hp_lfo_ratio = x_hp + 60
        x_hp_lfo_depth = x_hp_lfo_ratio + 60
        x_hp_external = x_hp_lfo_depth + 60
        x_hp_mix = x_hp_external + 60
        norm_slider("hpMode", x_hp, y1)
        discrete_slider("hpLfoRatio", x_hp_lfo_ratio, y1,LF_RATIOS)
        norm_slider("hpMixLfo", x_hp_lfo_depth, y1)
        norm_slider("hpMixX", x_hp_external, y1)
        amp_slider("hpMix", x_hp_mix, y1)

        x_dry_mix = x_hp_mix + 90
        x_amp = x_dry_mix + 60
        amp_slider("dryMix", x_dry_mix, y1)
        amp_slider("amp", x_amp, y1)
            
