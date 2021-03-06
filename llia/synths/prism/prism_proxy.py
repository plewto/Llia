# llia.synths.prism.prism_proxy

from __future__ import print_function
import llia.constants

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.prism.prism_data import program_bank,pp

specs = SynthSpecs("Prism")

class PrismProxy(SynthProxy):

    def __init__(self, app):
        super(PrismProxy, self).__init__(app, specs, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config()["gui"].upper()
        if gui == "TK":
            from llia.synths.prism.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor
            
prism_pallet = Pallet(default_pallet)

specs["constructor"] = PrismProxy
specs["is-efx"] = True
specs["is-controller"] = False
specs["description"] = "Split audio signal into 3 bands"
specs["keymodes"] = ('Efx',)
specs["pretty-printer"] = pp   
specs["help"] = "Prism"
specs["pallet"] = prism_pallet
specs["audio-output-buses"] = [["outbusLow", "out_0"],
                               ["outbusCenter", "out_0"],
                               ["outbusHigh", "out_0"]]
specs["audio-input-buses"] = [["inbus","in_0"]]
specs["control-output-buses"] = []
specs["control-input-buses"] = []
llia.constants.EFFECT_TYPES.append(specs["format"])
