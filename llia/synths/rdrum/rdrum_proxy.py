# llia.synths.rdrum_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.rdrum.rdrum_data import program_bank
from llia.synths.rdrum.rdrum_pp import pp_rdrum
from llia.synths.rdrum.rdrum_gen import gen_rdrum_program

specs = SynthSpecs("RDrum")

class RdrumProxy(SynthProxy):

    def __init__(self, app, id_):
        super(RdrumProxy, self).__init__(app, specs, id_, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            pass
            # from llia.synths.rdrum.tk.rdrum_ed import create_tk_rdrum_editor
            # appwin = self.app.main_window()
            # parent_editor = appwin[self.sid]
            # create_tk_rdrum_editor(parent_editor)
            
rdrum_pallet = Pallet(default_pallet)        

specs["constructor"] = RdrumProxy
specs["description"] = "Massed pulse waves"
specs["keymodes"] = ("Poly1", "Mono1")
specs["audio-output-buses"] = (("outbus", 1),)
specs["pretty-printer"] = pp_rdrum    
specs["program-generator"] = gen_rdrum_program
specs["help"] = "rdrum"
specs["pallet"] = rdrum_pallet
