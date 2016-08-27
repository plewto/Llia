# llia.synths.algo2.tk.envelope_editor

from __future__ import print_function
import Tkinter as tk
from llia.gui.tk.tk_subeditor import TkSubEditor
from llia.gui.tk.expslider import ExpSlider
import llia.synths.algo2.algo2_constants as con
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf

class TkAlgoEnvEditor(TkSubEditor):

    @staticmethod
    def env_coordinates(env_number):
        y0,y1 = 60,320
        x0,x1 = 90,520
        rs = {"a" : (x0,y0),
              "b" : (x1,y0),
              "c" : (x0,y1),
              "d" : (x1,y1)}[env_number]
        return rs
            
    def __init__(self, editor):
        name = "Envelopes"
        image_filename = "resources/Algo2/envelope_editor.png"
        ed_frame = editor.create_tab(name)
        self.main = tk.Canvas(ed_frame)
        self.main.pack(expand=True, fill="both")
        self.editor = editor
        TkSubEditor.__init__(self, self.main, editor,name)
        editor.add_child_editor(name, self)
        lab_panel = factory.image_label(self.main,  image_filename)
        lab_panel.pack(anchor='nw', expand=False)
        for env in 'abcd':
            self._init_env(env)
        
    def _init_env(self, env_number):
        x0,y0 = self.env_coordinates(env_number)
        x_attack = x0
        x_decay1 = x_attack + 60
        x_decay2 = x_decay1 + 60
        x_release = x_decay2 + 60
        x_breakpoint = x_release + 75
        x_sustain = x_breakpoint + 60
        self._time_slider(env_number, "attack", (x_attack, y0))
        self._time_slider(env_number, "decay1", (x_decay1, y0))
        self._time_slider(env_number, "decay2", (x_decay2, y0))
        self._time_slider(env_number, "release", (x_release, y0))
        self._level_slider(env_number, "breakpoint", (x_breakpoint, y0))
        self._level_slider(env_number, "sustain", (x_sustain, y0))
        
    def _time_slider(self, env_number, param_suffix, offset):
        param = "env%s_%s" % (env_number, param_suffix)
        s = ExpSlider(self.main, param, self.editor,
                      range_=30, degree=3)
        self.add_control(param, s)
        s.layout(offset, height=200, checkbutton_offset=None)
        return s

    def _level_slider(self, env_number, param_suffix, offset):
        param = "env%s_%s" % (env_number, param_suffix)
        s = cf.normalized_slider(self.main, param, self.editor)
        self.add_control(param, s)
        x,y = offset
        s.widget().place(x=x,y=y,height=200)
        return s
        

        
