# llia.synths.flngr2.flngr2_proxy

from __future__ import print_function
import llia.constants
from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.flngr2.flngr2_data import program_bank
from llia.synths.flngr2.flngr2_pp import flngr2_pp
# from llia.synths.flngr2.flngr2_random import flngr2_random

specs = SynthSpecs("Flngr2")

class Flngr2Proxy(SynthProxy):

    def __init__(self, app):
        super(Flngr2Proxy,self).__init__(app,specs,program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config()["gui"].upper()
        if gui == "TK":
            from llia.synths.flngr2.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor

pallet = Pallet(default_pallet)
#pallet["BACKGROUND"] =  
pallet["SLIDER-OUTLINE"] = "#A5A08A"
#pallet["SLIDER-TROUGH"] = 
specs["constructor"] = Flngr2Proxy
specs["description"] = "Dual Flanger"
specs["help"] = "Flngr2"
specs["pretty-printer"] = flngr2_pp
specs["program-generator"] = None
specs["pallet"] = pallet
specs["is-efx"] = True
specs["is-controller"] = False
specs["keymodes"] = ("EFX",)
specs["audio-output-buses"] = [["outbus1","out_0"],["outbus2","out_1"]]
specs["audio-input-buses"] = [["inbus1","in_0"],["inbus2","in_1"]]
specs["control-output-buses"] = [] 
specs["control-input-buses"] = [["xbus","null_sink"]]
llia.constants.EFFECT_TYPES.append(specs["format"])
