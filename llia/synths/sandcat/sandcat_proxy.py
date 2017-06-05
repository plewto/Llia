# llia.synths.sandcat.sandcat_proxy

from __future__ import print_function
import llia.constants
from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.sandcat.sandcat_data import program_bank
from llia.synths.sandcat.sandcat_pp import sandcat_pp
from llia.synths.sandcat.sandcat_random import sandcat_random

specs = SynthSpecs("Sandcat")

class SandcatProxy(SynthProxy):

    def __init__(self, app):
        super(SandcatProxy,self).__init__(app,specs,program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config()["gui"].upper()
        if gui == "TK":
            from llia.synths.sandcat.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor

pallet = Pallet(default_pallet)
#pallet["BACKGROUND"] =  
pallet["SLIDER-OUTLINE"] = "#1e4738"
pallet["SLIDER-TROUGH"] = "#2e1428"
specs["constructor"] = SandcatProxy
specs["description"] = "Hybrid Karplus-Strong/FM Synth."
specs["help"] = "Sandcat"
specs["pretty-printer"] = sandcat_pp
specs["program-generator"] = sandcat_random
specs["pallet"] = pallet
specs["is-efx"] = False
specs["is-controller"] = False
specs["keymodes"] = ("PolyN","PolyRotate","Poly1","Mono1","MonoExclusive")
specs["audio-output-buses"] = [["outbus1","out_0"],["outbus2","out_1"]]
specs["audio-input-buses"] = []
specs["control-output-buses"] = []
specs["control-input-buses"] = [["xbus1","null_sink"],["xbus2","null_sink"]]
llia.constants.SYNTH_TYPES.append(specs["format"])
