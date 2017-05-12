# llia.synths.rumklang.rumklang_proxy

from __future__ import print_function
import llia.constants

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.rumklang.rumklang_data import program_bank,pp

specs = SynthSpecs("Rumklang")

class RumklangProxy(SynthProxy):

    def __init__(self, app):
        super(RumklangProxy, self).__init__(app, specs, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config()["gui"].upper()
        if gui == "TK":
            from llia.synths.rumklang.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor
            
rumklang_pallet = Pallet(default_pallet)        
specs["constructor"] = RumklangProxy
specs["is-efx"] = True
specs["description"] = "Stereo Reverb Effect"
specs["keymodes"] = ("EFX",)
specs["pretty-printer"] = pp
#specs["program-generator"] = gen_rumklang_program
specs["help"] = "rumklang"
specs["pallet"] = rumklang_pallet
specs["audio-input-buses"] = [["inbus", "in_0"]]
specs["audio-output-buses"] = [["outbus1","out_0"],
                               ["outbus2","out_1"]]
specs["control-input-buses"] = [["xbus","null_sink"]]
llia.constants.EFFECT_TYPES.append(specs["format"])
