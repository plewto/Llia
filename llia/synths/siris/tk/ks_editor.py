# llia.synths.siris.tk.ks_editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
from llia.synths.siris.siris_constants import *

class TkSirisKSPanel(TkSubEditor):

    NAME = "KS"
    IMAGE_FILE = "resources/Siris/editor_ks.png"
    TAB_FILE = "resources/Siris/tab_ks.png"

    def __init__(self,editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1000,700,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.NAME)
        editor.add_child_editor(self.NAME, self)
        x0 = 75
        x_excite = x0
        x_tune = x_excite + 190
        x_delay = x_tune+100
        x_env = x_delay+60
        x_clip = x_env+200
        x_amp = x_clip+120
        y0, y1 = 75, 350
        for n,y in ((1,y0),(2,y1)):
            def param(suffix):
                return "ks%d_%s" % (n,suffix)
            self.norm_slider(param("excite1"),x_excite, y)
            self.norm_slider(param("excite2"),x_excite+60, y)
            self.norm_slider(param("excite_noise"),x_excite+120,y)
            self.toggle(param("excite_white"),x_excite+96,y+175,off=(0,"Pink"),on=(1,"White"))
            self.tumbler(param("ratio"), 5, 0.001, x_tune, y)
            msb_trig = self.msb(param("trig_mode"), 4, x_tune+7, y+75)
            for i,tx in enumerate(("Gate","Trem","Sus","External")):
                self.msb_aspect(msb_trig, i, i, text=tx)
            msb_trig.update_aspect()
            self.tumbler(param("trig_ratio"), 5, 0.001, x_tune,y+175)
            if n==2:
                self.linear_slider(param("delay"),(0,MAX_DELAY),x_delay,y)
            self.exp_slider(param("attack"), MAX_ENV_SEGMENT, x_env, y)
            self.exp_slider(param("decay"), MAX_ENV_SEGMENT, x_env+60, y)
            self.linear_slider(param("coef"), (0, 0.95), x_env+120, y)
            self.linear_slider(param("clip_gain"), (1,6),x_clip,y)
            self.norm_slider(param("clip_threshold"),x_clip+60,y)
            self.toggle(param("clip_enable"),x_clip+6,y+175)
            self.norm_slider(param("velocity"),x_amp,y)
            self.volume_slider(param("amp"),x_amp+60,y)
