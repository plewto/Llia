# llia.synths.xover.xover_proxy
# 2016.07.03

from __future__ import print_function
import llia.constants

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.xover.xover_data import program_bank, pp, random_xover

specs = SynthSpecs("XOver");

class XOverProxy(SynthProxy):

    def __init__(self, app):
        super(XOverProxy, self).__init__(app, specs, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.xover.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)

xover_pallet = Pallet(default_pallet)
xover_pallet["BG"] = "#131313"
xover_pallet["SLIDER-TROUGH"] = "#0a1414"
xover_pallet["SLIDER-OUTLINE"] = "#3d1e29"

specs["constructor"] = XOverProxy
specs["description"] = "Crossover Filter Effect"
specs["keymodes"] = ("EFX",)
specs["program-generator"] = random_xover
specs["is-efx"] = True
specs["pretty-printer"] = pp
specs["pallet"] = xover_pallet
specs["help"] = "xover"
specs["audio-output-buses"] = [["outbus1","out_0"],
                               ["outbus2","out_0"]]
specs["audio-input-buses"] = [["inbus","in_0"]]
specs["control-output-buses"] = [["lfo1aOutbus", "null_source"],
                                 ["lfo1bOutbus", "null_source"],
                                 ["lfo2Outbus", "null_source"]]
specs["control-input-buses"] = [["xbus", "null_sink"]]

                               
print("\t%s" % specs["format"])
llia.constants.EFFECT_TYPES.append(specs["format"])
