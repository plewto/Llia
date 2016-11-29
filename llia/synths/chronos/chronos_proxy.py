# llia.synths.chronos.chronos_proxy

from __future__ import print_function
import llia.constants

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.chronos.chronos_data import program_bank, pp
from llia.synths.chronos.chronos_random import random_program

specs = SynthSpecs("Chronos")

class ChronosProxy(SynthProxy):

    def __init__(self, app):
        super(ChronosProxy, self).__init__(app, specs,program_bank)
        self.app = app
        
    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.chronos.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)


chronos_pallet = Pallet(default_pallet)
chronos_pallet["SLIDER-TROUGH"] = "#400137"
chronos_pallet["SLIDER-OUTLINE"] = "#10400A"

specs["constructor"] = ChronosProxy
specs["is-efx"] = True
specs["description"] = "Dual delay effect"
specs["keymodes"] = ("EFX", )
specs["pretty-printer"] = pp
specs["program-generator"] = random_program
specs["help"] = "chronos"
specs["pallet"] = chronos_pallet


specs["audio-output-buses"] = [["outbus1", "out_0"],
                               ["outbus2", "out_1"]]
specs["audio-input-buses"] = [["inbus1", "in_0"],
                              ["inbus2", "in_1"]]
specs["control-input-buses"] = [["xbus","null_sink"]]
print("\t%s" % specs["format"])
llia.constants.EFFECT_TYPES.append(specs["format"])
