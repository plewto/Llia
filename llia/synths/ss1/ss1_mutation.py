# llia.synths.ss1.ss1_mutation

from __future__ import print_function

from llia.mutation import Mutation

class SS1Mutation(Mutation):

    def __init__(self):
        super(SS1Mutation,self).__init__()
        self.define("port", 0.10, (0,1), 0.01)
        self.define("vsens", 0.10, (0,1),0.01)
        self.define("vdepth", 0.10, (0,1),0.01)
        self.define("lfoFreq", 0.10, (0.001,99),0.01)
        self.define("lfoDelay", 0.10, (0,3),0.01)
        self.define("lfoAmp", 0.10,(0,1),0.01)
        self.define("attack", 0.10,(0,6),0.01)
        self.define("decay", 0.10,(0,6),0.01)
        self.define("sustain", 0.10,(0,1),0.01)
        self.define("release", 0.10,(0,6),0.01)
        self.define("sawMix", 0.10,(0,1),0.01)
        self.define("pulseMix", 0.10,(0,1),0.01)
        self.define("subMix", 0.10,(0,1),0.01)
        self.define("noiseMix", 0.10,(0,1),0.01)
        self.define("wave", 0.10,(0,1),0.01)
        self.define("waveLFO", 0.10,(0,1),0.01)
        self.define("waveEnv", 0.10,(0,1),0.01)
        self.define("filterLFO", 0.10,(0,8000),0.01)
        self.define("filterEnv", 0.10,(-10000,10000),0.01)
        self.define("filterRes", 0.10,(0,1),0.01)

