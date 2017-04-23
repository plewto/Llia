# llia.synths.sol.sol_proxy

from __future__ import print_function
import llia.constants
from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.sol.sol_data import program_bank
from llia.synths.sol.sol_pp import sol_pp
from llia.synths.sol.sol_random import sol_random

specs = SynthSpecs("Sol")

class SolProxy(SynthProxy):

    def __init__(self, app):
        super(SolProxy,self).__init__(app,specs,program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.sol.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor

pallet = Pallet(default_pallet)
#pallet["BACKGROUND"] =  
pallet["SLIDER-OUTLINE"] = "#777f86"
pallet["SLIDER-TROUGH"] = "#2d242d"
specs["constructor"] = SolProxy
specs["description"] = "Vector Synth"
specs["help"] = "Sol"
specs["pretty-printer"] = sol_pp
specs["program-generator"] = sol_random
specs["pallet"] = pallet
specs["is-efx"] = False
specs["is-controller"] = False
specs["keymodes"] = ("PolyN","PolyRotate","Poly1","Mono1","MonoExclusive")
specs["audio-output-buses"] = [["outbus","out_0"],["xout","out_2"],["yout","out_2"]]
specs["audio-input-buses"] = []
specs["control-output-buses"] = []
specs["control-input-buses"] = [["vxbus","null_sink"],["vybus","null_sink"],["ctrlbus","null_sink"]]
print("\t%s" % specs["format"])
llia.constants.SYNTH_TYPES.append(specs["format"])
