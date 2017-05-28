# llia.synths.siris.siris_proxy

from __future__ import print_function
import llia.constants
from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.siris.siris_data import program_bank
from llia.synths.siris.siris_pp import siris_pp
from llia.synths.siris.siris_random import siris_random

specs = SynthSpecs("Siris")

class SirisProxy(SynthProxy):

    def __init__(self, app):
        super(SirisProxy,self).__init__(app,specs,program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config()["gui"].upper()
        if gui == "TK":
            from llia.synths.siris.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor

pallet = Pallet(default_pallet)
pallet["BACKGROUND"] = "#2d292d"
pallet["SLIDER-OUTLINE"] = "#1f4737"
pallet["SLIDER-TROUGH"] = "#371f47"
specs["constructor"] = SirisProxy
specs["description"] = "Dual Karplus-Strong Plucked String Synth"
specs["help"] = "Siris"
specs["pretty-printer"] = siris_pp
specs["program-generator"] = siris_random
specs["pallet"] = pallet
specs["is-efx"] = False
specs["is-controller"] = False
specs["keymodes"] = ("PolyN","PolyRotate","Poly1","Mono1","MonoExclusive")
specs["audio-output-buses"] = [["outbus","out_0"]]
specs["audio-input-buses"] = []
specs["control-output-buses"] = []
specs["control-input-buses"] = [["trigbus1","null_sink"],["trigbus2","null_sink"]]
llia.constants.SYNTH_TYPES.append(specs["format"])
