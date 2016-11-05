# llia.synths.algo.tk.envedit

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
import llia.gui.tk.control_factory as cf
from llia.gui.tk.addsr_editor import ADDSREditor
import llia.synths.algo.algo_constants as acon

WIDTH  = 900
HEIGHT = 200

class TkAlgoEnvelopePanel(TkSubEditor):

   
    
    def __init__(self,stack_id,editor):
        name = "Env %s" % stack_id
        image_file = "resources/Algo/envelope_editor_%s.png" % (stack_id.lower())
        frame = editor.create_tab(name)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 1000, 700, image_file)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, name)
        editor.add_child_editor(name, self)
        
        carrier = {"A":1,"B":5,"C":7}[stack_id]
        mod1 = {"A":2,"B":4,"C":8}[stack_id]
        mod2 = {"A":3,"B":6,"C":None}[stack_id]
        ec = ADDSREditor(canvas,
                         carrier,
                         self.coords(carrier),
                         (WIDTH,HEIGHT),
                         self.env_parameters(carrier),
                         self.editor,
                         acon.MAX_ENV_SEGMENT)
        self.add_child_editor("OP%sENV" % carrier, ec)
        ec.sync()

        e1 = ADDSREditor(canvas,
                         mod1,
                         self.coords(mod1),
                         (WIDTH,HEIGHT),
                         self.env_parameters(mod1),
                         self.editor,
                         acon.MAX_ENV_SEGMENT)
        self.add_child_editor("OP%sENV" % mod1, e1)
        e1.sync()

        if mod2:
            e2 = ADDSREditor(canvas,
                             mod2,
                             self.coords(mod2),
                             (WIDTH,HEIGHT),
                             self.env_parameters(mod2),
                             self.editor,
                             acon.MAX_ENV_SEGMENT)
            self.add_child_editor("OP%sENV" % mod2, e2)
            e2.sync()

    @staticmethod
    def env_parameters(op):
        frmt = "op%d_%%s" % op
        return (frmt % "attack",
                frmt % "decay1",
                frmt % "decay2",
                frmt % "release",
                frmt % "breakpoint",
                frmt % "sustain",
                frmt % "envmode")

    @staticmethod
    def coords(op):
        ydelta = HEIGHT + 5
        y0 = 50
        y2 = y0 
        y1 = y2 + ydelta
        ycarrier = y1 + ydelta
        x0 = 75
        return {1 : (x0,ycarrier),
                2 : (x0,y1),
                3 : (x0,y2),
                4 : (x0,y1),
                5 : (x0,ycarrier),
                6 : (x0,y2),
                7 : (x0,ycarrier),
                8 : (x0,y1)}[op]
        
   
    
        


