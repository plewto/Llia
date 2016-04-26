# llia.synths.orgn.orgn_proxy
# 2016.04.23

from __future__ import print_function

from llia.generic import clone
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.orgn.orgn_data import program_bank
from llia.synths.orgn.orgn_pp import pp_orgn

specs = SynthSpecs("ORGN")

class OrgnProxy(SynthProxy):
    
    def __init__(self, app, id_):
        super(OrgnProxy, self).__init__(app, specs, id_, program_bank)
        gui = app.config["gui"]

specs["constructor"] = OrgnProxy
specs["description"] = "FM Combo Organ"
specs["pretty-printer"] = pp_orgn

