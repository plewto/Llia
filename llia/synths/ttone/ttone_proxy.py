# llia.synths.ttone.ttone_proxy

from __future__ import print_function
import llia.constants
from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.ttone.ttone_data import program_bank
from llia.synths.ttone.ttone_pp import ttone_pp

specs = SynthSpecs("TTone")

class TToneProxy(SynthProxy):

    def __init__(self, app):
        super(TToneProxy,self).__init__(app,specs,program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config()["gui"].upper()
        if gui == "TK":
            from llia.synths.ttone.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor

pallet = Pallet(default_pallet)
#pallet["BACKGROUND"] =  
#pallet["SLIDER-OUTLINE"] = 
#pallet["SLIDER-TROUGH"] = 
specs["constructor"] = TToneProxy
specs["description"] = "Test Tone Generator"
specs["help"] = "TTone"
specs["pretty-printer"] = ttone_pp
specs["program-generator"] = None
specs["pallet"] = pallet
specs["is-efx"] = False
specs["is-controller"] = False
specs["keymodes"] = ("PolyN","PolyRotate","Poly1","Mono1","MonoExclusive")
specs["audio-output-buses"] = [["outbus","out_0"]] 
specs["audio-input-buses"] = []
specs["control-output-buses"] = []
specs["control-input-buses"] = []
llia.constants.SYNTH_TYPES.append(specs["format"])
