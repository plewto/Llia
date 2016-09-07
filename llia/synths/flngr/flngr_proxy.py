# llia.synths.flngr.flngr_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.flngr.flngr_data import program_bank, pp, random_flanger
# from llia.synths.flngr.flngr_gen import gen_flngr_program

specs = SynthSpecs("Flngr");

class FlngrProxy(SynthProxy):

    def __init__(self, app, id_):
        super(FlngrProxy, self).__init__(app, specs, id_, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.flngr.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)

flngr_pallet = Pallet(default_pallet)
flngr_pallet["SLIDER-OUTLINE"] = "#a5a08a"

specs["is-efx"] = True
specs["constructor"] = FlngrProxy
specs["description"] = "Flanger (Mono)"
specs["keymodes"] = ("EFX",)
specs["program-generator"] = random_flanger
specs["pretty-printer"] = pp
specs["pallet"] = flngr_pallet
specs["help"] = "flngr"

specs["audio-output-buses"] = [["outbus", "out_0"]]
specs["audio-input-buses"] = [["inbus", "in_1"]]
specs["control-input-buses"] = [["delaybus","CBUS_B"],["mixbus","CBUS_B"]]
specs["control-output-buses"] = [["lfoOutbus", "CBUS_A"]]
