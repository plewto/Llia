# llia.synths.masa.masa_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.masa.masa_data import program_bank
from llia.synths.masa.masa_pp import pp_masa

specs = SynthSpecs("MASA")

class MasaProxy(SynthProxy):

    def __init__(self, app,):
        super(MasaProxy, self).__init__(app, specs, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            pass
            from llia.synths.masa.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)

masa_pallet = Pallet(default_pallet)
masa_pallet["SLIDER-TROUGH"] = "#4f3e46"
masa_pallet["SLIDER-OUTLINE"] = "#3e4f46"

specs["constructor"] = MasaProxy
specs["description"] = "Tonewheel Organ"
specs["keymodes"] = ("Poly1", "PolyRoate", "Mono1")
specs["pretty-printer"] = pp_masa  
# specs["program-generator"] = masa_gen
specs["pallet"] = masa_pallet
specs["help"] = "masa"
specs["audio-output-buses"] = [["outbus","out_0"]]
specs["control-input-buses"] = [["xbus","null_sink"]]
