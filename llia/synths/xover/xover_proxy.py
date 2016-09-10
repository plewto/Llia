# llia.synths.xover.xover_proxy
# 2016.07.03

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.xover.xover_data import program_bank, pp, random_xover
#from llia.synths.xover.xover_gen import gen_xover_program

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
specs["audio-output-buses"] = [["lpOutbus","out_0"],
                               ["hpOutbus","out_0"],
                               ["dryOutbus","out_0"]]
specs["audio-input-buses"] = [["inbus", "in_0"]]
specs["control-input-buses"] = [["xbus", "CBUS_B"]]
specs["control-output-buses"] = [["xoverLfoOutbus", "CBUS_A"],
                                 ["lpModLfoOutbus", "CBUS_A"],
                                 ["hpModLfoOutbus", "CBUS_A"]]
