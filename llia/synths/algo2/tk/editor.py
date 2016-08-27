# llia.synths.algo2.tk.editor

from llia.synths.algo2.tk.stack_editor import TkAlgoStackEditor
from llia.synths.algo2.tk.envelope_editor import TkAlgoEnvEditor
from llia.synths.algo2.tk.global_editor import TkAlgoGlobalEditor

def create_editor(parent):
    ed1 = TkAlgoStackEditor(1, parent)
    ed4 = TkAlgoStackEditor(4, parent)
    ed7 = TkAlgoStackEditor(7, parent)
    env = TkAlgoEnvEditor(parent)
    gen = TkAlgoGlobalEditor(parent)
