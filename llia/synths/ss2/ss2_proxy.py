# llia.synths.ss2.ss2_proxy

from __future__ import print_function
import llia.constants
from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.ss2.ss2_data import program_bank
from llia.synths.ss2.ss2_pp import ss2_pp

specs = SynthSpecs("SS2")

class SS2Proxy(SynthProxy):

    def __init__(self, app):
        super(SS2Proxy,self).__init__(app,specs,program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.ss2.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor

pallet = Pallet(default_pallet)
#pallet["BACKGROUND"] =  
#pallet["SLIDER-OUTLINE"] = 
#pallet["SLIDER-TROUGH"] = 
specs["constructor"] = SS2Proxy
specs["description"] = "Simple Synth 2"
specs["help"] = "SS2"
specs["pretty-printer"] = ss2_pp
specs["program-generator"] = None
specs["pallet"] = pallet
specs["is-efx"] = False
specs["is-controller"] = False
specs["keymodes"] = ("PolyN","PolyRotate","Poly1","Mono1","MonoExclusive")
specs["audio-output-buses"] = [["outbus","out_0"]]
specs["audio-input-buses"] = []
specs["control-output-buses"] = []
specs["control-input-buses"] = []
print("\t%s" % specs["format"])
llia.constants.SYNTH_TYPES.append(specs["format"])
