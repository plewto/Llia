# llia.synths.snh.snh_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.snh.snh_data import program_bank, pp, random_snh

specs = SynthSpecs("SnH")

class SnhProxy(SynthProxy):

    def __init__(self, app):
        super(SnhProxy, self).__init__(app, specs, program_bank)
        self.app = app
        
    def create_subeditors(self):
        pass
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.snh.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            

snh_pallet = Pallet(default_pallet)
snh_pallet["SLIDER-TROUGH"] = "#432703"
snh_pallet["SLIDER-OUTLINE"] = "#42033E"

specs["constructor"] = SnhProxy
specs["is-efx"] = True
specs["is-controller"] = True
specs["description"] = "Sample and Hold"
specs["keymodes"] = ("EFX", )
specs["pretty-printer"] = pp
specs["program-generator"] = random_snh
specs["help"] = "SnH"
specs["pallet"] = snh_pallet

specs["control-output-buses"] = [["outbus", "null_source"]]
