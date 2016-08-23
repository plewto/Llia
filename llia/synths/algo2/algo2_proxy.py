# llia.synths.algo2.algo2_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.algo2.algo2_data import program_bank
from llia.synths.algo2.algo2_pp import pp_algo2
from llia.synths.algo2.algo2_random import random_algo2

specs = SynthSpecs("Algo2")

class Algo2Proxy(SynthProxy):

    def __init__(self, app, id_):
        super(Algo2Proxy, self).__init__(app, specs, id_, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.algo2.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor
            
algo2_pallet = Pallet(default_pallet)        


specs["constructor"] = Algo2Proxy
specs["description"] = "An 8 Operator FM Synth"
specs["keymodes"] = ("Poly1", "Mono1")
specs["audio-output-buses"] = (("outbus", 1),("outbus4", 1),("outbus7", 1))
specs["control-input-buses"] = ("xbus",)
specs["pretty-printer"] = pp_algo2    
specs["program-generator"] = random_algo2
specs["help"] = "algo2"
specs["pallet"] = algo2_pallet


