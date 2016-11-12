# llia.synths.corvus.corvus_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.corvus.corvus_data import program_bank
from llia.synths.corvus.corvus_pp import pp 
#from llia.synths.corvus.corvus_random import corvus_random

specs = SynthSpecs("Corvus")

class CorvusProxy(SynthProxy):

    def __init__(self, app):
        super(CorvusProxy, self).__init__(app, specs, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.corvus.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor
            
corvus_pallet = Pallet(default_pallet)
corvus_pallet["SLIDER-OUTLINE"] = "#008279"
specs["constructor"] = CorvusProxy
specs["is-efx"] = False
specs["is-controller"] = False
specs["description"] = "Hybrid FM Additive synth"
specs["keymodes"] = ('PolyN','PolyRotate', 'Poly1', 'PolyRotate', 'Mono1', 'MonoExclusive')
specs["pretty-printer"] = pp   
#specs["program-generator"] = corvus_random
specs["help"] = "Corvus"
specs["pallet"] = corvus_pallet
specs["audio-output-buses"] = [["outbus", "out_0"],
                               ["outbus1", "out_2"],
                               ["outbus2", "out_2"],
                               ["outbus3", "out_2"],
                               ["outbus4", "out_2"]]
specs["audio-input-buses"] = []
specs["control-output-buses"] = [["xbus","null_source"]]
specs["control-input-buses"] = []
