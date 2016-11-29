# llia.synths.saw3.s3_proxy
# 2016.06.05

from __future__ import print_function
import llia.constants

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.saw3.s3_data import program_bank
from llia.synths.saw3.s3_pp import pp_saw3
from llia.synths.saw3.s3_gen import s3gen

specs = SynthSpecs("Saw3")

class Saw3Proxy(SynthProxy):

    def __init__(self, app):
        super(Saw3Proxy, self).__init__(app, specs, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.saw3.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)

s3_pallet = Pallet(default_pallet)
s3_pallet["BG"] = "#131313"
s3_pallet["FG"] = "#DAC0C0"
s3_pallet["SLIDER-TROUGH"] = "#1f2f40"
specs["constructor"] = Saw3Proxy
specs["description"] = "A 3 Oscillator Subtractive Synth"
specs["keymodes"] = ('PolyN', 'PolyRotate','Poly1','Mono1','MonoExclusive')
specs["pretty-printer"] = pp_saw3  
specs["program-generator"] = s3gen
specs["pallet"] = s3_pallet
specs["help"] = "saw3"
specs["audio-output-buses"] = [["outbus", "out_0"]]
specs["control-input-buses"] = [["xbus", "null_sink"]]
print("\t%s" % specs["format"])
llia.constants.SYNTH_TYPES.append(specs["format"])
