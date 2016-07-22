# llia.synths.syndrum.sd_proxy

from __future__ import print_function

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.syndrm.sd_data import program_bank
# from llia.synths.orgn.orgn_pp import pp_orgn
# from llia.synths.orgn.orgn_gen import gen_orgn_program

specs = SynthSpecs("SynDrm")

class SynDrmProxy(SynthProxy):

    def __init__(self, app, id_):
        super(SynDrmProxy, self).__init__(app, specs, id_, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            pass
            # from llia.synths.orgn.tk.orgn_ed import create_tk_orgn_editor
            # appwin = self.app.main_window()
            # parent_editor = appwin[self.sid]
            # create_tk_orgn_editor(parent_editor)

sd_pallet = Pallet(default_pallet)
specs["constructor"] = SynDrmProxy
specs["description"] = "Syntheic Percussion Instruiments"
specs["keymodes"] = ("Mono1", )
specs["audio-output-buses"] = (("hhOutbus", 1),("cymOutbus", 1),
                               ("claveOutbus", 1),("drum1Outbus", 1),
                               ("rdrumOutbus", 1),("noiseOutbus", 1))
#specs["pretty-printer"] = pp_orgn    
#specs["program-generator"] = gen_orgn_program
specs["help"] = "syndrm"
specs["pallet"] = sd_pallet
