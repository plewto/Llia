# llia.synths.m.tk.env_editor

from llia.gui.tk.tk_subeditor import TkSubEditor
import llia.gui.tk.tk_factory as factory
from llia.gui.tk.addsr_editor import ADDSREditor

from llia.synths.m.m_constants import *


class TkMEnvPanel(TkSubEditor):

    NAME = "M_ENV"
    IMAGE_FILE = "resources/M/env_editor.png"
    TAB_FILE = "resources/Tabs/adsr.png"


    def __init__(self, editor):
        frame = editor.create_tab(self.NAME, self.TAB_FILE)
        frame.config(background=factory.bg())
        canvas = factory.canvas(frame, 1000, 700, self.IMAGE_FILE)
        canvas.pack()
        self.canvas = canvas
        self.editor = editor
        TkSubEditor.__init__(self, canvas, editor, self.NAME)
        editor.add_child_editor(self.NAME, self)
        y0 = 10
        def y(n,delta=230):
            return y0+(n*delta)
            y_lfo = y0+55
        x0 = 75
        for i,n in enumerate("abc"):
            params = ("%sAttack" % n,
                      "%sDecay1" % n,
                      "%sDecay2" % n,
                      "%sRelease" % n,
                      "%sBreakpoint" % n,
                      "%sSustain" % n,
                      "%sTrigMode" % n)
            ed = ADDSREditor(canvas,i,(x0,y(i)),(900,230),params,editor)
            self.add_child_editor("env_%s" % n, ed)

            
