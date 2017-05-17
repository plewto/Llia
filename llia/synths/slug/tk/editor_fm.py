# llia.synths.slug.tk.editor2

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.synths.slug.slug_constants import *

class TkSlugFMPanel(TkSubEditor):

    NAME = "FM"
    IMAGE_FILE = "resources/Slug/editor_fm.png"
    TAB_FILE = "resources/Slug/tab_fm.png"

    def __init__(self,editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1058,603,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.NAME)
        editor.add_child_editor(self.NAME, self)
        x0 = 75
        xmod = x0
        xcar = x0+390
        for n in (1,2):
            y = {1:75, 2:325}[n]
            # modulator
            def mod(suffix):
                return "mod%d_%s" % (n,suffix)
            self.tumbler(mod("ratio"),5,0.001,xmod,y)
            self.linear_slider(mod("mod_pluck"),(0,8),xmod+100,y)
            self.norm_slider(mod("velocity"),xmod+160,y)
            count = len(DB_KEY_SCALES)
            msb_left = self.msb(mod("left_scale"),count,xmod+235,y)
            msb_right = self.msb(mod("right_scale") ,count,xmod+235,y+50)
            for i,v in enumerate(DB_KEY_SCALES):
                self.msb_aspect(msb_left,i,v)
                self.msb_aspect(msb_right,i,v)
                msb_left.update_aspect()
                msb_right.update_aspect()
            self.norm_slider(mod("env"),xmod+320,y)
            # carrier
            def car(suffix):
                return "car%d_%s" % (n,suffix)
            self.tumbler(car("ratio"),5,0.001,xcar,y)
            self.tumbler(car("bias"),5,0.001,xcar,y+60)
            xcmod = xcar+100
            self.exp_slider(car("mod_scale"),MAX_MOD_SCALE,xcmod,y,degree=3)
            self.norm_slider(car("mod_depth"),xcmod+60,y,height=125)
            self.norm_slider(car("mod_pluck"),xcmod+120,y,height=125)
            self.norm_slider(car("xmod_depth"),xcmod+180,y,height=125)
            self.norm_slider(car("velocity"),xcmod+240,y)
            msb_left = self.msb(car("left_scale"),count,xcmod+300,y)
            msb_right = self.msb(car("right_scale") ,count,xcmod+300,y+50)
            for i,v in enumerate(DB_KEY_SCALES):
                self.msb_aspect(msb_left,i,v)
                self.msb_aspect(msb_right,i,v)
                msb_left.update_aspect()
                msb_right.update_aspect()
            self.norm_slider(car("amp_env"),xcmod+400,y)
