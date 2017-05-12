# llia.synths.panner.panner_proxy

from __future__ import print_function
import llia.constants

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.panner.panner_data import program_bank, pp, random_panner

specs = SynthSpecs("Panner")

class PannerProxy(SynthProxy):

    def __init__(self, app):
        super(PannerProxy, self).__init__(app, specs, program_bank)
        self.app = app
        
    def create_subeditors(self):
        gui = self.app.config()["gui"].upper()
        if gui == "TK":
            from llia.synths.panner.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)

panner_pallet = Pallet(default_pallet)
panner_pallet["SLIDER-TROUGH"] = "#432703"
panner_pallet["SLIDER-OUTLINE"] = "#42033E"
specs["constructor"] = PannerProxy
specs["description"] = "Audio signal panner"
specs["keymodes"] = ("EFX", )
specs["pretty-printer"] = pp
specs["program-generator"] = random_panner
specs["is-efx"] = True
specs["help"] = "Panner"
specs["pallet"] = panner_pallet
specs["audio-output-buses"] = [["outbusA","out_0"],
                               ["outbusB","out_1"]]
specs["audio-input-buses"] = [["inbus", "in_0"]]
specs["control-input-buses"] = [["xbus","null_sink"]]
specs["control-output-buses"] = [["lfoOutbus","null_source"]]
llia.constants.EFFECT_TYPES.append(specs["format"])
