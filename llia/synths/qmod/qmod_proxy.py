# llia.synths.qmod.qmod_proxy

from __future__ import print_function
import llia.constants

from llia.gui.pallet import default_pallet, Pallet
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.qmod.qmod_data import program_bank,pp
#from llia.synths.qmod.qmod_random import qmod_random

specs = SynthSpecs("QMod")

class QModProxy(SynthProxy):

    def __init__(self, app):
        super(QModProxy, self).__init__(app, specs, program_bank)
        self._editor = None

    def create_subeditors(self):
        gui = self.app.config["gui"].upper()
        if gui == "TK":
            from llia.synths.qmod.tk.editor import create_editor
            appwin = self.app.main_window()
            parent_editor = appwin[self.sid]
            create_editor(parent_editor)
            return parent_editor
            
qmod_pallet = Pallet(default_pallet)

specs["constructor"] = QModProxy
specs["is-efx"] = True
specs["is-controller"] = False
specs["description"] = "Frequncy Modulation Effect"
specs["keymodes"] = ('Efx',)
specs["pretty-printer"] = pp   
#specs["program-generator"] = qmod_random
specs["help"] = "QMod"
specs["pallet"] = qmod_pallet
specs["audio-output-buses"] = [["outbus", "out_0"]]
specs["audio-input-buses"] = [["inbus","in_0"]]
specs["control-output-buses"] = []
specs["control-input-buses"] = []
print("\t%s" % specs["format"])
llia.constants.EFFECT_TYPES.append(specs["format"])
