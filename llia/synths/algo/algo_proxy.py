# llia.synths.algo.algo_proxy

from __future__ import print_function
import llia.constants

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.algo.algo_data import program_bank
from llia.synths.algo.algo_pp import pp
from llia.synths.algo.algogen.algo_random import algogen

specs = SynthSpecs("Algo")

class AlgoProxy(SynthProxy):

    def __init__(self, app):
        super(AlgoProxy, self).__init__(app, specs, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.algo.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor
            
algo_pallet = Pallet(default_pallet)
algo_pallet["SLIDER-OUTLINE"] = "#008279"
specs["constructor"] = AlgoProxy
specs["is-efx"] = False
specs["is-controller"] = False
specs["description"] = "An 8-operator FM Synth"
specs["keymodes"] = ('PolyN','PolyRotate','Poly1','Mono1','MonoExclusive')
specs["pretty-printer"] = pp   
specs["program-generator"] = algogen
specs["help"] = "Algo"
specs["pallet"] = algo_pallet
specs["audio-output-buses"] = [["outbus", "out_0"],
                               ["outbusA", "out_2"],
                               ["outbusB", "out_2"],
                               ["outbusC", "out_2"]]
specs["audio-input-buses"] = []
specs["control-output-buses"] = []
specs["control-input-buses"] = [["xbus","null_sink"]]
print("\t%s" % specs["format"])
llia.constants.SYNTH_TYPES.append(specs["format"])
