# llia.synths.algo6.a6_proxy


from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.algo6.a6_data import program_bank
from llia.synths.algo6.a6_pp import pp_algo6
from llia.synths.algo6.a6_gen import a6gen

specs = SynthSpecs("Algo6")

class Algo6Proxy(SynthProxy):

    def __init__(self, app, id_):
        super(Algo6Proxy, self).__init__(app, specs, id_, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            pass
            # from llia.synths.algo6.tk.a6ed import create_editor
            # appwin = self.app.main_window()
            # parent_editor = appwin[self.sid]
            # create_editor(parent_editor)

a6_pallet = Pallet(default_pallet)

            
specs["constructor"] = Algo6Proxy
specs["description"] = "A 6-operator FM synth"
specs["keymodes"] = ("Poly1", "Mono1")
specs["audio-output-buses"] = (("outbus", 1),)
specs["control-input-buses"] = ("aBus",)
specs["pretty-printer"] = pp_algo6  
specs["program-generator"] = a6gen
specs["pallet"] = a6_pallet
specs["help"] = "algo6"
