# llia.synths.dirtyburger.dirty_proxy
# 2016.04.26

from __future__ import print_function

from llia.generic import clone
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.dirtyburger.dirty_data import program_bank
from llia.synths.dirtyburger.dirty_pp import pp_dirty

specs = SynthSpecs("DirtyBurger")

class DirtyProxy(SynthProxy):

    def __init__(self, app, id_):
        super(DirtyProxy, self).__init__(app, specs, id_, program_bank)
        gui = app.config["gui"]

specs["constructor"] = DirtyProxy
specs["description"] = "Delay line with dirty feedback"
specs["pretty-printer"] = pp_dirty
specs["help"] = "dirtyburger"
