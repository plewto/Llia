# llia.synths.comb.comb_proxy

from __future__ import print_function
import llia.constants
from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.comb.comb_data import program_bank
from llia.synths.comb.comb_pp import comb_pp
from llia.synths.comb.comb_random import comb_random

specs = SynthSpecs("Comb")

class CombProxy(SynthProxy):

    def __init__(self, app):
        super(CombProxy,self).__init__(app,specs,program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config()["gui"].upper()
        if gui == "TK":
            from llia.synths.comb.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor

pallet = Pallet(default_pallet)
#pallet["BACKGROUND"] =  
#pallet["SLIDER-OUTLINE"] = 
#pallet["SLIDER-TROUGH"] = 
specs["constructor"] = CombProxy
specs["description"] = "Simple Comb Filter"
specs["help"] = "Comb"
specs["pretty-printer"] = comb_pp
specs["program-generator"] = comb_random
specs["pallet"] = pallet
specs["is-efx"] = True
specs["is-controller"] = False
specs["keymodes"] = ("EFX",)
specs["audio-output-buses"] = [["outbus","out_0"]]
specs["audio-input-buses"] = [["inbus","in_0"]]
specs["control-output-buses"] = []
specs["control-input-buses"] = []
llia.constants.EFFECT_TYPES.append(specs["format"])
