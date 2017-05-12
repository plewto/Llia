# llia.synths.rdrum_proxy

from __future__ import print_function
import llia.constants

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.rdrum.rdrum_data import program_bank
from llia.synths.rdrum.rdrum_pp import pp_rdrum
from llia.synths.rdrum.rdrum_gen import gen_rdrum_program

specs = SynthSpecs("RDrum")

class RdrumProxy(SynthProxy):

    def __init__(self, app):
        super(RdrumProxy, self).__init__(app, specs, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config()["gui"].upper()
        if gui == "TK":
            from llia.synths.rdrum.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor
            
rdrum_pallet = Pallet(default_pallet)
rdrum_pallet["slider-trough"] = "#283442"
rdrum_pallet["slider-outline"] = "#4f304f"
specs["constructor"] = RdrumProxy
specs["description"] = "Percussive synthesizer"
specs["keymodes"] = ('PolyN', 'PolyRotate','Poly1','Mono1','MonoExclusive')
specs["pretty-printer"] = pp_rdrum    
specs["program-generator"] = gen_rdrum_program
specs["help"] = "rdrum"
specs["pallet"] = rdrum_pallet
specs["audio-output-buses"] = [["outbus", "out_0"]]
llia.constants.SYNTH_TYPES.append(specs["format"])
