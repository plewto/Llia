# llia.synths.scanner.scanner_proxy

from __future__ import print_function
import llia.constants
from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.scanner.scanner_data import program_bank
from llia.synths.scanner.scanner_pp import scanner_pp
from llia.synths.scanner.scanner_random import scanner_random

specs = SynthSpecs("Scanner")

class ScannerProxy(SynthProxy):

    def __init__(self, app):
        super(ScannerProxy,self).__init__(app,specs,program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.scanner.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor

pallet = Pallet(default_pallet)
#pallet["BACKGROUND"] =  
#pallet["SLIDER-OUTLINE"] = 
pallet["SLIDER-TROUGH"] = "#31383d"
specs["constructor"] = ScannerProxy
specs["description"] = "Phase Shifter"
specs["help"] = "Scanner"
specs["pretty-printer"] = scanner_pp
specs["program-generator"] = scanner_random
specs["pallet"] = pallet
specs["is-efx"] = True
specs["is-controller"] = False
specs["keymodes"] = ("EFX",)
specs["audio-output-buses"] = [["outbus1","out_0"],["outbus2","out_1"]]
specs["audio-input-buses"] = [["inbus","in_0"]]
specs["control-output-buses"] = [["lfobus","null_source"]]
specs["control-input-buses"] = [["xbus","null_sink"]]
print("\t%s" % specs["format"])
llia.constants.EFFECT_TYPES.append(specs["format"])
