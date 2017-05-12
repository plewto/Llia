# llia.synths.bandpass.bandpass_proxy

from __future__ import print_function
import llia.constants

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.bandpass.bandpass_data import program_bank,pp

specs = SynthSpecs("Bandpass")

class BandpassProxy(SynthProxy):

    def __init__(self, app):
        super(BandpassProxy, self).__init__(app, specs, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config()["gui"].upper()
        if gui == "TK":
            from llia.synths.bandpass.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor
            
bandpass_pallet = Pallet(default_pallet)

specs["constructor"] = BandpassProxy
specs["is-efx"] = True
specs["is-controller"] = False
specs["description"] = "Bandpass filter with LFO"
specs["keymodes"] = ('Efx',)
specs["pretty-printer"] = pp   
specs["help"] = "Bandpass"
specs["pallet"] = bandpass_pallet
specs["audio-output-buses"] = [["outbus", "out_0"]]
specs["audio-input-buses"] = [["inbus", "in_0"]]
specs["control-output-buses"] = [["lfoOutbus", "null_source"]]
specs["control-input-buses"] = [["xbus","null_sink"]]
llia.constants.EFFECT_TYPES.append(specs["format"])
