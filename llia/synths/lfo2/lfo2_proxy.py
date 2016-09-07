# llia.synths.lfo2.lfo2_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.lfo2.lfo2_data import program_bank, pp
from llia.synths.lfo2.lfo2_random import random_lfo2

specs = SynthSpecs("LFO2")

class Lfo2Proxy(SynthProxy):

    def __init__(self, app, id_):
        super(Lfo2Proxy, self).__init__(app, specs, id_, program_bank)
        self.app = app
        
    def create_subeditors(self):
        pass
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.lfo2.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            

lfo2_pallet = Pallet(default_pallet)
lfo2_pallet["SLIDER-TROUGH"] = "#432703"
lfo2_pallet["SLIDER-OUTLINE"] = "#42033E"

specs["constructor"] = Lfo2Proxy
specs["description"] = "Multi wave LFO"
specs["keymodes"] = ("EFX", )
specs["pretty-printer"] = pp
specs["program-generator"] = random_lfo2
specs["is-efx"] = True
specs["help"] = "LFO2"
specs["pallet"] = lfo2_pallet
specs["control-output-buses"] = [["outbusSaw","CBUS_A"],["outbusPulse","CBUS_B"]]
