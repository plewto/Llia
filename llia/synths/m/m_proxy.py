# llia.synths.m.m_proxy

from __future__ import print_function
import llia.constants

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.m.m_data import program_bank
from llia.synths.m.m_pp import pp
from llia.synths.m.m_random import m_random

specs = SynthSpecs("M")

class MProxy(SynthProxy):

    def __init__(self, app):
        super(MProxy, self).__init__(app, specs, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config()["gui"].upper()
        if gui == "TK":
            from llia.synths.m.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor
            
m_pallet = Pallet(default_pallet)

specs["constructor"] = MProxy
specs["is-efx"] = False
specs["is-controller"] = False
specs["description"] = "M is for obfuscation"
specs["keymodes"] = ('PolyN', 'PolyRotate', 'Poly1', 'PolyRotate', 'Mono1', 'MonoExclusive')
specs["pretty-printer"] = pp   
specs["program-generator"] = m_random
specs["help"] = "M"
specs["pallet"] = m_pallet
specs["audio-output-buses"] = [["outbus1", "out_0"],
                               ["outbus2", "out_0"]]
specs["audio-input-buses"] = []
specs["control-output-buses"] = []
specs["control-input-buses"] = [["xbus","null_sink"]]
llia.constants.SYNTH_TYPES.append(specs["format"])
