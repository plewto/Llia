# llia.synths.ringmodulator.rm_proxy

from __future__ import print_function
import llia.constants

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.ringmodulator.rm_data import program_bank,pp

specs = SynthSpecs("RingModulator")

class RingModulatorProxy(SynthProxy):

    def __init__(self, app):
        super(RingModulatorProxy, self).__init__(app, specs,program_bank)
        self.app = app
        
    def create_subeditors(self):
        gui = self.app.config()["gui"].upper()
        if gui == "TK":
            from llia.synths.ringmodulator.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)


ringmodulator_pallet = Pallet(default_pallet)
ringmodulator_pallet["SLIDER-TROUGH"] = "black"
ringmodulator_pallet["SLIDER-OUTLINE"] = "blue"
specs["constructor"] = RingModulatorProxy
specs["is-efx"] = True
specs["description"] = "Ring modulator effect"
specs["keymodes"] = ("EFX", )
specs["pretty-printer"] = pp
# specs["program-generator"] = random_program
specs["help"] = "ringmodulator"
specs["pallet"] = ringmodulator_pallet
specs["audio-output-buses"] = [["outbus", "out_0"]]
specs["audio-input-buses"] = [["carin", "in_0"], # carrier
                              ["xmodin","in_1"]] # external modulator in
llia.constants.EFFECT_TYPES.append(specs["format"])
