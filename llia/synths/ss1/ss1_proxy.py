# llia.synths.ss1.ss1_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.ss1.ss1_data import program_bank,pp,random_ss1
#from llia.synths.ss1.ss1_random import ss1_random

specs = SynthSpecs("SS1")

class SS1Proxy(SynthProxy):

    def __init__(self, app):
        super(SS1Proxy, self).__init__(app, specs, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.ss1.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor
            
ss1_pallet = Pallet(default_pallet)
ss1_pallet["SLIDER-TROUGH"] = "#1d3136"
ss1_pallet["SLIDER-OUTLINE"] = "#2e1d36"

specs["constructor"] = SS1Proxy
specs["is-efx"] = False
specs["is-controller"] = False
specs["description"] = "Simple Synth 1: 1 oscillator, 1 filter, 1 LFO, 1 envelope"
specs["keymodes"] = ('PolyN', 'PolyRotate', 'Poly1', 'PolyRotate', 'Mono1', 'MonoExclusive')
specs["pretty-printer"] = pp   
specs["program-generator"] = random_ss1
specs["help"] = "SS1"
specs["pallet"] = ss1_pallet
specs["audio-output-buses"] = [["outbus", "out_0"]]
specs["audio-input-buses"] = []
specs["control-output-buses"] = []
specs["control-input-buses"] = [["xbus","null_sink"]]
