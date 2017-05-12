# llia.synths.ss2.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf

def create_editor(parent):
    TkSS2Panel(parent)

class TkSS2Panel(TkSubEditor):

    NAME = "SS2"
    IMAGE_FILE = "resources/SS2/editor.png"
    TAB_FILE = "resources/SS2/tab.png"

    def __init__(self,editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1000,700,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.NAME)
        editor.add_child_editor(self.NAME, self)
        x0 = 75
        x1 = x0+75
        x_env = x0+180
        y0, y1, y2 = 75, 150, 250

        wave = self.msb("wave",3,x0,y0)
        self.msb_aspect(wave,0,0,"Tri")
        self.msb_aspect(wave,1,1,"Pulse")
        self.msb_aspect(wave,2,2,"Saw")
        wave.update_aspect()

        pw = self.msb("pw",4,x0,y1)
        self.msb_aspect(pw,0,0.06)
        self.msb_aspect(pw,1,0.12)
        self.msb_aspect(pw,2,0.25)
        self.msb_aspect(pw,3,0.50)
        pw.update_aspect()
        
        flt = self.msb("filter",3,x1,y0)
        self.msb_aspect(flt,0,0,text="Off")
        self.msb_aspect(flt,1,1,text="Low")
        self.msb_aspect(flt,2,2,text="High")
        flt.update_aspect()

        track_values = (1,2,3,4,6,8,12,16,24,32,48,64)
        
        trk = self.msb("track",len(track_values),x1,y1)
        for i,v in enumerate(track_values):
            self.msb_aspect(trk,i,v)
        trk.update_aspect()


        etime = 4
        self.exp_slider("attack",etime,x_env,y0)
        self.exp_slider("decay",etime,x_env+60,y0)
        self.norm_slider("sustain",x_env+120,y0)
        self.exp_slider("release",etime,x_env+180,y0)
        emode = self.msb("envSelect", 2, x_env, y2)
        self.msb_aspect(emode,0,0,text="ADSR")
        self.msb_aspect(emode,1,1,text="Perc")
        emode.update_aspect()

        self.volume_slider("amp",x_env+280,y0)
