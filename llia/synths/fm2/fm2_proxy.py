# llia.synths.fm2.fm2_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.fm2.fm2_data import program_bank
from llia.synths.fm2.fm2_pp import pp_fm2
from llia.synths.fm2.fm2_random import fm2_random

specs = SynthSpecs("FM2")

class FM2Proxy(SynthProxy):

    def __init__(self, app, id_):
        super(FM2Proxy, self).__init__(app, specs, id_, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.fm2.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor
            
fm2_pallet = Pallet(default_pallet)        


specs["constructor"] = FM2Proxy
specs["description"] = "A 2-Operator FM Synth"
specs["keymodes"] = ("Poly1", "Mono1")
specs["audio-output-buses"] = (("outbus", 1),)
specs["control-input-buses"] = ("xbus",)
specs["pretty-printer"] = pp_fm2    
specs["program-generator"] = fm2_random
specs["help"] = "FM2"
specs["pallet"] = fm2_pallet
