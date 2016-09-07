# llia.synths.lfo3.lfo3_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.lfo3.lfo3_data import program_bank, pp
from llia.synths.lfo3.lfo3_random import random_lfo3

specs = SynthSpecs("LFO3")

class Lfo3Proxy(SynthProxy):

    def __init__(self, app, id_):
        super(Lfo3Proxy, self).__init__(app, specs, id_, program_bank)
        self.app = app
        
    def create_subeditors(self):
        pass
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.lfo3.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            

lfo3_pallet = Pallet(default_pallet)
lfo3_pallet["SLIDER-TROUGH"] = "#432703"
lfo3_pallet["SLIDER-OUTLINE"] = "#42033E"

specs["constructor"] = Lfo3Proxy
specs["description"] = "A 3 LFO block with cross modulation"
specs["keymodes"] = ("EFX", )
specs["audio-output-buses"] = []
specs["audio-input-buses"] = []
specs["pretty-printer"] = pp
specs["program-generator"] = random_lfo3
specs["is-efx"] = True
specs["help"] = "LFO3"
specs["pallet"] = lfo3_pallet

#specs["control-output-buses"] = ("outbusA","outbusB","outbusC")
specs["control-output-buses"] = [["outbusA","CBUS_A"],
                                 ["outbusB","CBUS_A"],
                                 ["outbusC","CBUS_A"]]
