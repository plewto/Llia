# llia.synths.orgn.organ_proxy
# 2016.06.04

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.orgn.orgn_data import program_bank
from llia.synths.orgn.orgn_pp import pp_orgn
from llia.synths.orgn.orgn_gen import gen_orgn_program

specs = SynthSpecs("Orgn")

class OrgnProxy(SynthProxy):

    def __init__(self, app, id_):
        super(OrgnProxy, self).__init__(app, specs, id_, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.orgn.tk.orgn_ed import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor
            
orgn_pallet = Pallet(default_pallet)        

specs["constructor"] = OrgnProxy
specs["description"] = "FM Combo Organ"
specs["keymodes"] = ("Poly1", "Mono1")
specs["audio-output-buses"] = (("outbus", 1),)
specs["pretty-printer"] = pp_orgn    
specs["program-generator"] = gen_orgn_program
specs["help"] = "orgn"
specs["pallet"] = orgn_pallet


