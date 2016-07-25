# llia.synths.klstr_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.klstr.klstr_data import program_bank
from llia.synths.klstr.klstr_pp import pp_klstr
from llia.synths.klstr.klstr_gen import gen_klstr_program

specs = SynthSpecs("Klstr")

class KlstrProxy(SynthProxy):

    def __init__(self, app, id_):
        super(KlstrProxy, self).__init__(app, specs, id_, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.klstr.tk.klstr_ed import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            
klstr_pallet = Pallet(default_pallet)        

specs["constructor"] = KlstrProxy
specs["description"] = "Massed pulse waves"
specs["keymodes"] = ("Poly1", "Mono1")
specs["audio-output-buses"] = (("outbus", 1),)
specs["pretty-printer"] = pp_klstr    
specs["program-generator"] = gen_klstr_program
specs["help"] = "klstr"
specs["pallet"] = klstr_pallet
