# llia.synths.lfo1.lfo1_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.lfo1.lfo1_data import program_bank, pp, random_lfo1

specs = SynthSpecs("LFO1")

class Lfo1Proxy(SynthProxy):

    def __init__(self, app):
        super(Lfo1Proxy, self).__init__(app, specs,program_bank)
        self.app = app
        
    def create_subeditors(self):
        pass
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.lfo1.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            

lfo1_pallet = Pallet(default_pallet)
lfo1_pallet["SLIDER-TROUGH"] = "#432703"
lfo1_pallet["SLIDER-OUTLINE"] = "#42033E"

specs["constructor"] = Lfo1Proxy
specs["description"] = "Simple sine LFO"
specs["keymodes"] = ("EFX", )

specs["pretty-printer"] = pp
specs["program-generator"] = random_lfo1
specs["is-efx"] = True
specs["is-controller"] = True
specs["help"] = "LFO1"
specs["pallet"] = lfo1_pallet


specs["control-output-buses"] = [["outbus","null_source"]]
