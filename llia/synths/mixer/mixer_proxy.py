# llia.synths.mixer.mixer_proxy


from __future__ import print_function
import llia.constants

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.mixer.mixer_data import program_bank, pp

specs = SynthSpecs("Mixer")

class MixerProxy(SynthProxy):

    def __init__(self, app):
        super(MixerProxy, self).__init__(app, specs, program_bank)
        self.app = app
        
    def create_subeditors(self):
        pass
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.mixer.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            

mixer_pallet = Pallet(default_pallet)
mixer_pallet["SLIDER-TROUGH"] = "#432703"
mixer_pallet["SLIDER-OUTLINE"] = "#42033E"

specs["constructor"] = MixerProxy
specs["description"] = "4 x 2 Mixer"
specs["keymodes"] = ("EFX", )
specs["pretty-printer"] = pp
specs["is-efx"] = True
specs["help"] = "Mixer"
specs["pallet"] = mixer_pallet


specs["audio-output-buses"] = [["outbus1","out_0"],
                               ["outbus2","out_1"]]

specs["audio-input-buses"] = [["inbusA", "in_0"],
                              ["inbusB", "in_1"],
                              ["inbusC", "in_2"],
                              ["inbusD", "in_3"]]

specs["control-input-buses"] = [["xbus","null_sink"]]
print("\t%s" % specs["format"])
llia.constants.EFFECT_TYPES.append(specs["format"])
