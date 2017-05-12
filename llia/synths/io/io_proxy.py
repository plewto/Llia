# llia.synths.io.io_proxy

from __future__ import print_function
import llia.constants

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.io.io_data import program_bank  #,pp,io_random
from llia.synths.io.io_pp import pp_io
from llia.synths.io.io_random import io_random

specs = SynthSpecs("Io")

class IoProxy(SynthProxy):

    def __init__(self, app):
        super(IoProxy, self).__init__(app, specs, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config()["gui"].upper()
        if gui == "TK":
            from llia.synths.io.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor
            
io_pallet = Pallet(default_pallet)
io_pallet["SLIDER-OUTLINE"] = "#004000"
specs["constructor"] = IoProxy
specs["is-efx"] = False
specs["is-controller"] = False
specs["description"] = "FM Fomat synth"
specs["keymodes"] = ('PolyN','PolyRotate', 'Poly1', 'PolyRotate', 'Mono1', 'MonoExclusive')
specs["pretty-printer"] = pp_io   
specs["program-generator"] = io_random
specs["help"] = "Io"
specs["pallet"] = io_pallet
specs["audio-output-buses"] = [["outbus", "out_0"]]
specs["audio-input-buses"] = []
specs["control-output-buses"] = [["xbus", "null_sink"]]
specs["control-input-buses"] = []
llia.constants.SYNTH_TYPES.append(specs["format"])
