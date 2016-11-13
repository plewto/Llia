# llia.synths.envgen.envgen_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.envgen.envgen_data import program_bank,pp


specs = SynthSpecs("Envgen")

class EnvgenProxy(SynthProxy):

    def __init__(self, app):
        super(EnvgenProxy, self).__init__(app, specs, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.envgen.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor
            
envgen_pallet = Pallet(default_pallet)

specs["constructor"] = EnvgenProxy
specs["is-efx"] = False
specs["is-controller"] = True
specs["description"] = "Dual ADDSR envelope control synth"
specs["keymodes"] = ('efx',)
specs["pretty-printer"] = pp
specs["help"] = "Envgen"
specs["pallet"] = envgen_pallet
specs["audio-output-buses"] = []
specs["audio-input-buses"] = []
specs["control-output-buses"] = [["outbusA", "null_source"],
                                 ["outbusB", "null_source"]]
specs["control-input-buses"] = []
