# llia.synths.combo.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf

def create_editor(parent):
    TkComboPanel(parent)

class TkComboPanel(TkSubEditor):

    NAME = "Combo"
    IMAGE_FILE = "resources/Combo/editor.png"
    TAB_FILE = "resources/Combo/tab.png"

    def __init__(self,editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,803,343,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.NAME)
        editor.add_child_editor(self.NAME, self)
        x0,y0 = 75,75

        x_tab= x0
        y_tab = y0
        for i,param in enumerate(("reed16","reed8","flute8","flute4","flute3","flute2")):
            msb = self.msb(param,3,x_tab,y_tab)
            for j, value in enumerate(((0, "Off"),(1, "1"),(2,"2"))):
                mag,label = value
                self.msb_aspect(msb,j,mag,text=label)
            x_tab += 65
            if i==1: x_tab += 170
            msb.update_aspect()
        x_wave = x0 + 130
        msb = self.msb("reedWave",2,x_wave,y_tab)
        self.msb_aspect(msb,0,0.0,"Brass")
        self.msb_aspect(msb,1,1.0,"Reed")
        msb.update_aspect()
        x_chorus = x_wave+65
        self.toggle("chorus",x_chorus, y_tab,(0.0, "Off"),(1.0,"On"))
        
        x_vib = x0
        y_vib = 200
        for i,param in enumerate(("vspeed","vdepth")):
            msb = self.msb(param,3,x_vib,y_vib)
            if i == 0:
                plist = ((0.0, "Slow"),(0.5,"Med"),(1.0,"Fast"))
            else:
                plist = ((0.0, "Off"),(0.5, "Light"),(1.0, "Deep"))
            for j,value in enumerate(plist):
                mag,label = value
                self.msb_aspect(msb,j,mag,text=label)
            x_vib += 65
            msb.update_aspect()

        x_amp = x_tab+65
        self.volume_slider("amp",x_amp,y_tab)
            
