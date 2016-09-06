# llia.synths.carnal.crnl_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.carnal.crnl_data import program_bank, pp, random_program

specs = SynthSpecs("CarnalDelay")

class CarnalProxy(SynthProxy):

    def __init__(self, app, id_):
        super(CarnalProxy, self).__init__(app, specs, id_, program_bank)
        self.app = app
        
    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.carnal.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)


crnl_pallet = Pallet(default_pallet)
crnl_pallet["SLIDER-TROUGH"] = "#400137"
crnl_pallet["SLIDER-OUTLINE"] = "#10400A"

specs["constructor"] = CarnalProxy
specs["is-efx"] = True
specs["description"] = "An unclean delay"
specs["keymodes"] = ("EFX", )
specs["pretty-printer"] = pp
specs["program-generator"] = random_program
specs["help"] = "carnalDelay"
specs["pallet"] = crnl_pallet


specs["audio-output-buses"] = [["outbus", "out_0"]]
specs["audio-input-buses"] = [["inbus", "in_0"]]
specs["control-input-buses"] = [["efxbus","CBUS_B"],["dlybus", "CBUS_B"]]
