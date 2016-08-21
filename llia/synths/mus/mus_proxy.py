# llia.synths.mus.mus_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.mus.mus_data import program_bank, pp, random_mus

specs = SynthSpecs("Mus")

class MusProxy(SynthProxy):

    def __init__(self, app, id_):
        super(MusProxy, self).__init__(app, specs, id_, program_bank)
        self.app = app
        
    def create_subeditors(self):
        pass
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.mus.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            

mus_pallet = Pallet(default_pallet)
mus_pallet["BG"] = "#101121"
mus_pallet["SLIDER-TROUGH"] = "#19060c"
mus_pallet["SLIDER-OUTLINE"] = "#54282c"

specs["constructor"] = MusProxy
specs["is-efx"] = True
specs["description"] = "Uses mouse as control source"
specs["keymodes"] = ("EFX", )
specs["audio-output-buses"] = []
specs["audio-input-buses"] = []
specs["control-output-buses"] = ("xbus","ybus","buttonBus","envBus")
specs["pretty-printer"] = pp
specs["program-generator"] = random_mus
specs["help"] = "Mus"
specs["pallet"] = mus_pallet
