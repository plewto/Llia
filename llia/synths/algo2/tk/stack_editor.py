# llia.synths.algo2.tk.ed1
#

from __future__ import print_function
import Tkinter as tk
from llia.gui.tk.tk_subeditor import TkSubEditor
from llia.gui.tk.expslider import ExpSlider
from llia.gui.tk.freq_spinner import FrequencySpinnerControl
import llia.synths.algo2.algo2_constants as con
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf

class OpEditor(object):


    @staticmethod
    def is_carrier(n):
        return n == 1 or n == 4 or n == 7

    @staticmethod
    def is_modulator(n):
        return not OpEditor.is_carrier(n)

    @staticmethod
    def has_feedback(n):
        return n == 6 or n == 8
    
    def __init__(self, op, master, editor, y0):
        self.op = op   # op number (1,2,3,4,5,6,7 or 8)
        self.master = master
        self.editor = editor
        self.y0 = y0
        x_freq = 120
        x_bias = x_freq,
        y_bias = y0+75
        x_ampmod = x_freq + 120
        x_lfo = x_ampmod + 60
        x_env = x_lfo + 60
        x_keybreak = x_env + 75
        x_leftscale = x_keybreak + 60
        x_rightscale = x_leftscale + 60
        x_amp = x_rightscale + 75
        self._freq_spinner((x_freq, self.y0))
        if self.is_modulator(op):
            self._bias_spinner((x_bias, y_bias))
        self._norm_slider("x_amp", (x_ampmod, y0))
        self._norm_slider("lfo_amp", (x_lfo, y0))
        self._env_select_slider((x_env, y0))
        self._keybreak_slider((x_keybreak, y0))
        self._keyscale_slider("left_scale", (x_leftscale, y0))
        self._keyscale_slider("right_scale", (x_rightscale, y0))
        self._amp_slider((x_amp, y0))
        if self.has_feedback(op):
            x_fb = x_amp + 75
            self._feedback_slider("feedback", (x_fb,self.y0))
            self._feedback_slider("x_feedback", (x_fb+60, self.y0))
            self._feedback_slider("lfo_feedback", (x_fb+120, self.y0))
            self._feedback_slider("env_feedback", (x_fb+180, self.y0))
        
    def _freq_spinner(self, offset):
        param = "op%d_ratio" % self.op
        ofc = FrequencySpinnerControl(self.master, param, self.editor,
                                      from_=0, to=16)
        self.editor.add_control(param, ofc)
        ofc.layout(offset)
        return ofc
    
    def _bias_spinner(self, offset):
        param = "op%d_bias" % self.op
        bc = FrequencySpinnerControl(self.master, param, self.editor,
                                     from_=0, to=9999)
        self.editor.add_control(param, bc)
        bc.layout(offset)
        return bc

    def _norm_slider(self, param_sufix, offset):
        param = "op%s_%s" % (self.op, param_sufix)
        s = cf.normalized_slider(self.master, param, self.editor)
        self.editor.add_control(param, s)
        x,y = offset
        s.widget().place(x=x,y=y)
        return s

    def _env_select_slider(self, offset):
        if self.is_carrier(self.op):
            values = range(8)
        else:
            values = range(16)
        param = "op%s_env_select" % self.op
        s = cf.discrete_slider(self.master, param, self.editor, values)
        self.editor.add_control(param, s)
        x,y = offset
        s.widget().place(x=x,y=y)
        return s
        
    def _keybreak_slider(self, offset):
        param = "op%s_break_key" % self.op
        s = cf.discrete_slider(self.master, param, self.editor, range(128))
        self.editor.add_control(param, s)
        x,y = offset
        s.widget().place(x=x,y=y)
        return s
        
    def _keyscale_slider(self, param_suffix, offset):
        param = "op%s_%s" % (self.op, param_suffix)
        s = cf.discrete_slider(self.master, param, self.editor, range(-18,21,3))
        self.editor.add_control(param, s)
        x,y = offset
        s.widget().place(x=x,y=y)
        return s

    def _amp_slider(self, offset):
        param = "op%s_amp" % self.op
        x,y = offset
        if self.is_carrier(self.op):
            s = cf.volume_slider(self.master, param, self.editor)
            s.widget().place(x=x,y=y)
        else:
            s = ExpSlider(self.master,param, self.editor,
                          range_=16, degree=2)
            s.layout(offset, checkbutton_offset=None)
        self.editor.add_control(param, s)
        return s

    def _feedback_slider(self, param_suffix, offset):
        param = "op%s_%s" % (self.op, param_suffix)
        s = cf.linear_slider(self.master, param, self.editor, range_=(0,4))
        self.editor.add_control(param, s)
        x,y = offset
        s.widget().place(x=x,y=y)
        return s
    
class TkAlgoStackEditor(TkSubEditor):

    def __init__(self, stack_number, editor):
        stack_name = {1 : "Algo [3]->[2]->[1]",
                      4 : "Algo [5][6]->[4]",
                      7 : "Algo [8]->[7]"}[stack_number]
        image_filename = "resources/Algo2/editor_%s.png" % stack_number
        ed_frame = editor.create_tab(stack_name)
        self.main = tk.Canvas(ed_frame)
        self.main.pack(expand=True, fill='both')
        self.editor = editor
        TkSubEditor.__init__(self,self.main, editor, stack_name)
        editor.add_child_editor(stack_name, self)
        lab_panel = factory.image_label(self.main, image_filename)
        lab_panel.pack(anchor='nw', expand=False)
        
        y0, y1, y2 = 60, 280, 500
        
        if stack_number == 1:
            OpEditor(3, self.main, self, y0)
            OpEditor(2, self.main, self, y1)
            OpEditor(1, self.main, self, y2)
        elif stack_number == 4:
            OpEditor(6, self.main, self, y0)
            OpEditor(5, self.main, self, y1)
            OpEditor(4, self.main, self, y2)
        else:
            OpEditor(8, self.main, self, y0)
            OpEditor(7, self.main, self, y1)
