# llia.synths.fxstack.tk.editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf

def create_editor(parent):
    TkFxstackPanel(parent)
    TkFxstackDelayPanel(parent)
    
class TkFxstackPanel(TkSubEditor):

    NAME = "Fxstack"
    IMAGE_FILE = "resources/Fxstack/editor.png"
    TAB_FILE = "resources/Fxstack/tab.png"

    def __init__(self,editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1000,700,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.NAME)
        editor.add_child_editor(self.NAME, self)
        x0,y0 = 75,75
        
        # Top row
        x_in = x0
        
        self.volume_slider("inputGain",x_in,y0)
        
        x_env = x_in+90
        self.linear_slider("envGain",(1,100),x_env,y0)
        self.linear_slider("attack",(0,2),x_env+60,y0)
        self.linear_slider("release",(0,2),x_env+120,y0)

        x_clip = x_env+210
        self.norm_slider("clipDrive",x_clip,y0)
        self.norm_slider("clipLfo1",x_clip+60,y0)
        self.norm_slider("clipMix",x_clip+120,y0)

        x_filter = x_clip+210        
        for i,p in enumerate(("Freq","Env","Lfo2","Res","Mix")):
            param = "filter%s" % p
            x = x_filter+(60*i)
            self.norm_slider(param,x,y0)
        
        # 2nd row
        y1 = 300
        x_lfo = x_env
        self.tumbler("lfo1Freq",5,0.001,x_lfo,y1)
        self.norm_slider("lfo2Mod",x_lfo+120,y1)
        self.tumbler("lfo2Freq",5,0.001,x_lfo+180,y1)
        
        x_flanger = x_filter
        for i,p in enumerate(("Delay1","Delay2","Lfo1","Feedback","Mix")):
            param = "flanger%s" % p
            x = x_flanger+(60*i)
            if p != "Feedback":
                self.norm_slider(param,x,y1)
            else:
                self.linear_slider(param,(-1,1),x,y1)
        

class TkFxstackDelayPanel(TkSubEditor):

    NAME = "Delay"
    IMAGE_FILE = "resources/Fxstack/delay_editor.png"
    TAB_FILE = "resources/Fxstack/delay_tab.png"

    def __init__(self,editor):
        frame = editor.create_tab(self.NAME,self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame,1000,700,self.IMAGE_FILE)
        canvas.pack()
        TkSubEditor.__init__(self,canvas,editor,self.NAME)
        editor.add_child_editor(self.NAME, self)
        x0,y0,y1 = 75,75,300

        x_delay = x0
        for n in (1,2):
            y = {1:y0,2:y1}[n]
            ptime = "delay%dTime" % n
            self.tumbler(ptime,4,0.001,x_delay,y,range_=(0,1000))
            for i,p in enumerate(("Lfo","Feedback","XFeedback","Filter","Mix","Pan")):
                if p == "Lfo":
                    param = "delay%dLfo%d" % (n,n)
                elif p == "Filter":
                    if n==1:
                        param = "delay1Lowpass"
                    else:
                        param = "delay2Highpass"
                else:
                    param = "delay%d%s" % (n,p)
                x = x_delay+120+(i*60)
                if p in ("Feedback","XFeedback","Pan"):
                    self.linear_slider(param,(-1,1),x,y)
                else:
                    self.norm_slider(param,x,y)
                    
        x_reverb = x_delay+530
        
        for i,p in enumerate(("RoomSize","Damping","Env","Lfo2","Mix")):
            param = "reverb%s" % p
            x = x_reverb+(i*60)
            self.norm_slider(param,x,y0)

        x_output = x_reverb+120
        self.volume_slider("outputGain",x_output,y1)
