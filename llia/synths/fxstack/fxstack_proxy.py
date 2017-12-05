# llia.synths.fxstack.fxstack_proxy

from __future__ import print_function
import llia.constants
from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.fxstack.fxstack_data import program_bank
from llia.synths.fxstack.fxstack_pp import fxstack_pp
from llia.synths.fxstack.fxstack_random import fxstack_random

specs = SynthSpecs("Fxstack")

class FxstackProxy(SynthProxy):

    def __init__(self, app):
        super(FxstackProxy,self).__init__(app,specs,program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config()["gui"].upper()
        if gui == "TK":
            from llia.synths.fxstack.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor

pallet = Pallet(default_pallet)
#pallet["BACKGROUND"] =  
#pallet["SLIDER-OUTLINE"] = 
#pallet["SLIDER-TROUGH"] = 
specs["constructor"] = FxstackProxy
specs["description"] = "Integrated Effects Stack"
specs["help"] = "Fxstack"
specs["pretty-printer"] = fxstack_pp
specs["program-generator"] = fxstack_random
specs["pallet"] = pallet
specs["is-efx"] = True
specs["is-controller"] = False
specs["keymodes"] = ("EFX",)
specs["audio-output-buses"] = [["outbus0","out_0"],["outbus1","out_1"]]
specs["audio-input-buses"] = [["inbus","in_0"]]
specs["control-output-buses"] = []
specs["control-input-buses"] = []
print("\t%s" % specs["format"])
llia.constants.EFFECT_TYPES.append(specs["format"])
