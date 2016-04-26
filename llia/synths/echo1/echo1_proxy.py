# llia.synths.echo1.echo1_proxy
# 2016.04.26

from __future__ import print_function

from llia.generic import clone
from llia.synth_proxy import SynthSpecs, SynthProxy
from llia.synths.echo1.echo1_data import program_bank
# from llia.synths.orgn.orgn_pp import pp_orgn

specs = SynthSpecs("Echo1")

class Echo1Proxy(SynthProxy):

    def __init__(self, app, id_):
        super(Echo1Proxy, self).__init__(app, specs, id_, program_bank)
        gui = app.config["gui"]

specs["constructor"] = Echo1Proxy
