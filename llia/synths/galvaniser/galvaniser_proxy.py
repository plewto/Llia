# llia.synths.galvaniser.galvaniser_proxy

from __future__ import print_function
import llia.constants
from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.galvaniser.galvaniser_data import program_bank
from llia.synths.galvaniser.galvaniser_pp import galvaniser_pp
from llia.synths.galvaniser.galvaniser_random import galvaniser_random

specs = SynthSpecs("Galvaniser")

class GalvaniserProxy(SynthProxy):

    def __init__(self, app):
        super(GalvaniserProxy,self).__init__(app,specs,program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config()["gui"].upper()
        if gui == "TK":
            from llia.synths.galvaniser.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor

pallet = Pallet(default_pallet)
#pallet["BACKGROUND"] =  
#pallet["SLIDER-OUTLINE"] = 
#pallet["SLIDER-TROUGH"] = 
specs["constructor"] = GalvaniserProxy
specs["description"] = "Filter effect after Cubase VST Metalizer."
specs["help"] = "Galvaniser"
specs["pretty-printer"] = galvaniser_pp
specs["program-generator"] = galvaniser_random
specs["pallet"] = pallet
specs["is-efx"] = True
specs["is-controller"] = False
specs["keymodes"] = ("EFX",)
specs["audio-output-buses"] = [["outbus","out_0"]]
specs["audio-input-buses"] = [["inbus","in_0"]]
specs["control-output-buses"] = [["lfobus","null_source"]]
specs["control-input-buses"] = [["xbus","null_sink"]]
#print("\t%s" % specs["format"])
llia.constants.EFFECT_TYPES.append(specs["format"])
