# llia.synths.fm2.tk.editor

from Tkinter import Canvas

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.msb import MSB
from llia.gui.tk.addsr_editor import ADDSREditor
from llia.gui.tk.tumbler import Tumbler
from llia.synths.fm2.tk.editor2 import TkFm2Panel2


def create_editor(parent):
    TkFm2Panel1(parent)
    TkFm2Panel2(parent)

class TkFm2Panel1(TkSubEditor):

    NAME = "FM2 OPS"
    IMAGE_FILE = "resources/FM2/editor1.png"
    TAB_FILE = "resources/FM2/tab_ops.png"
    
    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 900, 600, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)

        y0 = 50
        y1 = y0+230
        xfreq, yfreq_offset  = 50, 0
        xbias, ybias_offset  = xfreq, 100
        xamp, yamp_offset = xfreq + 120, ybias_offset
        xlfo = xamp+60
        xvelocity = xlfo+60
        xfeedback = xvelocity + 60
        xkeyscale = xfeedback + 60
        xenv = xkeyscale+90
        msb_common = {'fill' : 'black',
                      'foreground' : 'white',
                      'outline' : 'blue',
                      'active-foreground' : 'yellow',
                      'active-outline' : 'yellow',
                      'font' : ('Times', 12)}
        
        # OP2 Modulator
        self.ratio_tumbler('op2Ratio', xfreq,y0+yfreq_offset)
        self.bias_tumbler('op2Bias', xbias, y0+ybias_offset)
        self.linear_slider('op2Amp', (0,10), xamp, y0, height=110)
        msb_2amp = MSB(self.canvas, "op2AmpRange", editor, 5)
        self.add_control("op2AmpRange", msb_2amp)
        a0 = {'text' : '1'}
        a1 = {'text' : '2'}
        a2 = {'text' : '3'}
        a3 = {'text' : '4'}
        a4 = {'text' : '5'}
        a0.update(msb_common)
        a1.update(msb_common)
        a2.update(msb_common)
        a3.update(msb_common)
        a4.update(msb_common)
        a4['fill'] = '#f1f513'
        a4['foreground'] = 'black'
        a3['fill'] = '#cf7311'
        a2['fill'] = '#693108'
        msb_2amp.define_aspect(0, 1, a0)
        msb_2amp.define_aspect(1, 10, a1)
        msb_2amp.define_aspect(2, 100, a2)
        msb_2amp.define_aspect(3, 1000, a3)
        msb_2amp.define_aspect(4, 10000, a4)
        msb_2amp.layout((xamp-23, y0+yamp_offset+20))
        msb_2amp.update_aspect()                
        self.norm_slider("op2Lfo", xlfo, y0)
        self.norm_slider("op2Velocity", xvelocity, y0)
        self.linear_slider("op2Feedback", (0,4), xfeedback, y0)
        msb_2keybreak = MSB(self.canvas, "op2Keybreak", editor, 7)
        self.add_control("op2Keybreak", msb_2keybreak)
        a0 = dict(msb_common)
        a1 = dict(msb_common)
        a2 = dict(msb_common)
        a3 = dict(msb_common)
        a4 = dict(msb_common)
        a5 = dict(msb_common)
        a6 = dict(msb_common)
        a0['text']='24'
        a1['text']='36'
        a2['text']='48'
        a3['text']='60'
        a4['text']='72'
        a5['text']='84'
        a6['text']='96'
        msb_2keybreak.define_aspect(0, 24, a0)
        msb_2keybreak.define_aspect(1, 36, a1)
        msb_2keybreak.define_aspect(2, 48, a2)
        msb_2keybreak.define_aspect(3, 60, a3)
        msb_2keybreak.define_aspect(4, 72, a4)
        msb_2keybreak.define_aspect(5, 84, a5)
        msb_2keybreak.define_aspect(6, 96, a6)
        msb_2keybreak.layout((xkeyscale, y0))
        msb_2keybreak.update_aspect()
        msb_2left = MSB(self.canvas, "op2LeftScale", self.editor, 9)
        msb_2right = MSB(self.canvas, "op2RightScale", self.editor, 9)
        self.add_control("op2LeftScale", msb_2left)
        self.add_control("op2RightScale", msb_2right)
        db = -12
        db_fill_colors = {-12 : '#0000ff',
                          -9 : '#0000cc',
                          -6 : '#000075',
                          -3 : '#000021',
                          0 : 'black',
                          +3 : '#2b0001',
                          +6 : '#820004',
                          +9 : '#d60007',
                          +12 : '#ff0008'}
        for i in range(9):
            fill = db_fill_colors[db]
            a = dict(msb_common)
            a['text'] = "%+d" % db
            a['fill'] = fill
            msb_2left.define_aspect(i, db, a)
            msb_2right.define_aspect(i, db, a)
            db += 3
        msb_2left.layout((xkeyscale, y0+60))
        msb_2right.layout((xkeyscale, y0+120))
        msb_2left.update_aspect()
        msb_2right.update_aspect()
        env2 = ADDSREditor(canvas, 2, (xenv, y0),(350, 200),
                              ('op2Attack', 'op2Decay1',
                               'op2Decay2', 'op2Release',
                               'op2Breakpoint', 'op2Sustain',
                               'op2GateHold'),
                           editor)
        self.add_child_editor("OP2ENV", env2)
        env2.sync()
        
        # OP1 Carrier
        self.ratio_tumbler('op1Ratio',xfreq,y1+yfreq_offset)
        self.bias_tumbler('op1Bias',xbias,y1+ybias_offset)
        s_amp1 = cf.volume_slider(canvas, "op1Amp", editor)
        self.add_control("op1Amp", s_amp1)
        s_amp1.widget().place(x=xamp, y=y1)
        self.norm_slider("op1Lfo", xlfo, y1)
        self.norm_slider("op1Velocity", xvelocity, y1)
        msb_1keybreak = MSB(self.canvas, "op2Keybreak", editor, 7)
        self.add_control("op1Keybreak", msb_1keybreak)
        a0 = dict(msb_common)
        a1 = dict(msb_common)
        a2 = dict(msb_common)
        a3 = dict(msb_common)
        a4 = dict(msb_common)
        a5 = dict(msb_common)
        a6 = dict(msb_common)
        a0['text']='24'
        a1['text']='36'
        a2['text']='48'
        a3['text']='60'
        a4['text']='72'
        a5['text']='84'
        a6['text']='96'
        msb_1keybreak.define_aspect(0, 24, a0)
        msb_1keybreak.define_aspect(1, 36, a1)
        msb_1keybreak.define_aspect(2, 48, a2)
        msb_1keybreak.define_aspect(3, 60, a3)
        msb_1keybreak.define_aspect(4, 72, a4)
        msb_1keybreak.define_aspect(5, 84, a5)
        msb_1keybreak.define_aspect(6, 96, a6)
        msb_1keybreak.layout((xkeyscale, y1))
        msb_1keybreak.update_aspect()
        msb_1left = MSB(self.canvas, "op1LeftScale", self.editor, 9)
        msb_1right = MSB(self.canvas, "op1RightScale", self.editor, 9)
        self.add_control("op1LeftScale", msb_1left)
        self.add_control("op1RightScale", msb_1right)
        db = -12
        for i in range(9):
            fill = db_fill_colors[db]
            a = dict(msb_common)
            a['text'] = "%+d" % db
            a['fill'] = fill
            msb_1left.define_aspect(i, db, a)
            msb_1right.define_aspect(i, db, a)
            db += 3
        msb_1left.layout((xkeyscale, y1+60))
        msb_1right.layout((xkeyscale, y1+120))
        msb_1left.update_aspect()
        msb_1right.update_aspect()
        env1 = ADDSREditor(canvas, 1, (xenv, y1),(350, 200),
                              ('op1Attack', 'op1Decay1',
                               'op1Decay2', 'op1Release',
                               'op1Breakpoint', 'op1Sustain',
                               'op1GateHold'),
                           editor)
        self.add_child_editor("OP1ENV", env1)
        env1.sync()


    def ratio_tumbler(self, param, x, y):
        t = Tumbler(self.canvas,param,self.editor,
                    digits=5,scale=0.001)
        self.add_control(param, t)
        t.layout((x,y))
        return t

    def bias_tumbler(self, param, x, y):
        t = Tumbler(self.canvas,param,self.editor,
                    digits=5,scale=0.01)
        self.add_control(param,t)
        t.layout((x,y))
    
    def norm_slider(self, param, x, y, width=14, height=150):
        s = cf.normalized_slider(self.canvas, param, self.editor)
        self.add_control(param,s)
        s.widget().place(x=x,y=y,width=width, height=height)
        return s

    def linear_slider(self, param, range_, x, y, width=14, height=150):
        s = cf.linear_slider(self.canvas, param, self.editor,
                             range_=range_)
        self.add_control(param, s)
        s.widget().place(x=x,y=y,width=width, height=height)
        return s
        
