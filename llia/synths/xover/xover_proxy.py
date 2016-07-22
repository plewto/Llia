# llia.synths.xover.xover_proxy
# 2016.07.03

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.xover.xover_data import program_bank, pp_xover
from llia.synths.xover.xover_gen import gen_xover_program

specs = SynthSpecs("XOver");

class XOverProxy(SynthProxy):

    def __init__(self, app, id_):
        super(XOverProxy, self).__init__(app, specs, id_, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.xover.tk.xover_ed import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)

xover_pallet = Pallet(default_pallet)
xover_pallet["BG"] = "#131313"
xover_pallet["SLIDER-TROUGH"] = "#1f2f40"

specs["constructor"] = XOverProxy
specs["description"] = "Crossover Filter Effect"
specs["keymodes"] = ("EFX",)
specs["audio-output-buses"] = (("outbus", 1),)
specs["audio-input-buses"] = (("inbus", 1),)
specs["program-generator"] = gen_xover_program
specs["is-efx"] = True
specs["pretty-printer"] = pp_xover
specs["pallet"] = xover_pallet
specs["help"] = "xover"
