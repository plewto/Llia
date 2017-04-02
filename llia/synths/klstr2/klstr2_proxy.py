# llia.synths.klstr2.klstr2_proxy

from __future__ import print_function
import llia.constants
from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.klstr2.klstr2_data import program_bank
from llia.synths.klstr2.klstr2_pp import klstr2_pp
from llia.synths.klstr2.klstr2_random import klstr2_random

specs = SynthSpecs("Klstr2")

class Klstr2Proxy(SynthProxy):

    def __init__(self, app):
        super(Klstr2Proxy,self).__init__(app,specs,program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.klstr2.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor

pallet = Pallet(default_pallet)
#pallet["BACKGROUND"] =  
#pallet["SLIDER-OUTLINE"] = 
#pallet["SLIDER-TROUGH"] = 
specs["constructor"] = Klstr2Proxy
specs["description"] = "FIXME"
specs["help"] = "Klstr2"
specs["pretty-printer"] = klstr2_pp
specs["program-generator"] = klstr2_random
specs["pallet"] = pallet
specs["is-efx"] = False
specs["is-controller"] = False
specs["keymodes"] = ("PolyN","PolyRotate","Poly1","Mono1","MonoExclusive")
specs["audio-output-buses"] = [["outbus1","out_0"],["outbus2","out_1"]]
specs["audio-input-buses"] = []
specs["control-output-buses"] = []
specs["control-input-buses"] = [["xbus","null_sink"]]
print("\t%s" % specs["format"])
llia.constants.SYNTH_TYPES.append(specs["format"])
