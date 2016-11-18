# llia.synths.io.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB, ToggleButton
from llia.gui.tk.tumbler import Tumbler

def create_editor(parent):
    TkIoTonePanel(parent)

class TkIoTonePanel(TkSubEditor):

    NAME = "Io"
    IMAGE_FILE = "resources/Io/editor.png"
    TAB_FILE = "resources/Io/tab.png"

    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 888, 708, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        y0 = 50
        y1 = 300
        x0 = 75
        def norm_slider(param,x,y=y0,height=150):
            s = cf.normalized_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y,height=height)
            return s
        def volume_slider(param,x,y=y0):
            s = cf.volume_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y)
            return s
        def linear_slider(param,range_,x,y=y0):
            s = cf.linear_slider(canvas,param,editor,range_=range_)
            self.add_control(param,s)
            s.widget().place(x=x,y=y)
            return s
        def mix_slider(param,x,y=y0,height=150):
            s = cf.mix_slider(canvas,param,editor)
            self.add_control(param,s)
            s.widget().place(x=x,y=y,height=height)
        for f in (1,2,3):
            xdelta = 100
            x = x0 + (f-1)*xdelta
            y_slider = y0+50
            param = "ff%d" % f
            t = Tumbler(canvas,param,editor,
                        digits = 4,
                        scale = 1,
                        range_ = (1,9999))
            self.add_control(param,t)
            t.layout((x,y0))
            param = "amp%d" % f
            mix_slider("amp%d" % f,x,y_slider,100)
            norm_slider("lag%d" % f,x+47,y_slider,100)
        x_env = x+100
        linear_slider("attack",(0.0,2.0),x_env)
        linear_slider("decay",(0.0,2.0),x_env+60)
        linear_slider("release",(0.0,2.0),x_env+120)
        linear_slider("envScale",(0,10),x_env+180)
        norm_slider("velocityDepth",x_env+240)
        linear_slider("modDepth",(0.0,4.0),x_env+300)
        linear_slider("feedback",(0.0,4.0),x_env+360)
        linear_slider("modHP",(30,1),x_env+420)
        x_port = x0
        norm_slider("port",x0,y1)
        x_vib = x_port+60
        t = Tumbler(canvas,"vfreq",editor,
                    digits = 5, scale = 0.001)
        self.add_control("vfreq",t)
        t.layout((x_vib,y1))
        msb_vlock = ToggleButton(canvas,"vlock",editor,
                                 text = ("Unlock","Lock"))
        self.add_control("vlock",msb_vlock)
        msb_vlock.layout((x_vib+8,y1+75))
        msb_vlock.update_aspect()
        x_vdelay = x_vib+90
        linear_slider("vdelay",(0,2),x_vdelay,y1)
        norm_slider("vsens",x_vdelay+60,y1)
        norm_slider("vdepth",x_vdelay+120,y1)
        norm_slider("trem",x_vdelay+180,y1)
        x_chiff = x_vdelay+240
        linear_slider("chiffAttack",(0.0,0.5),x_chiff, y1)
        linear_slider("chiffDecay",(0.0,0.5),x_chiff+60,y1)
        norm_slider("chiffVelocity",x_chiff+120,y1)
        mix_slider("chiffAmp",x_chiff+180,y1)
        mix_slider("noiseAmp",x_chiff+240,y1)
        volume_slider("amp",x_env+420,y1)
