# llia.synths.ss1.ss1_mutation

from __future__ import print_function

from llia.mutator import Mutator

class SS1Mutation(Mutator):

    def __init__(self):
        super(SS1Mutation,self).__init__()
        self.define("port", 0.10, (0,1), 0.01)
        self.define("vdepth", 0.10, (0,1),0.01)
        self.define("lfoFreq", 0.10, (0.001,99),0.01)
        self.define("lfoDelay", 0.10, (0,3),0.01)
        self.define("lfoAmp", 0.10,(0,1),0.01)
        self.define("lfoWave",0.00,(0,2),1.0,walker=True)
        self.define("attack", 0.80,(0,6),0.80)
        self.define("decay", 0.80,(0,6),0.80)
        self.define("sustain", 0.80,(0,1),0.80)
        self.define("release", 0.80,(0,6),0.80)
        self.define("sawMix", 0.99,(0,1),0.99)
        self.define("pulseMix", 0.99,(0,1),0.99)
        self.define("subMix", 0.99,(0,1),0.99)
        self.define("chorus", 0.10,(0,1),1.0,walker=True)
        self.define("subOctave", 0.10, (0,1),1.0,walker=True)
        self.define("noiseMix", 0.40,(0,1),0.40)
        self.define("noiseSelect",0.10,(0,1),0.01,walker=True)
        self.define("wave", 0.10,(0,1),0.01)
        self.define("waveLFO", 0.10,(0,1),0.01)
        self.define("waveEnv", 0.10,(0,1),0.01)
        self.define("filterLFO", 0.10,(0,8000),0.01)
        self.define("filterEnv", 0.10,(-10000,10000),0.01)
        self.define("filterRes", 0.10,(0,1),0.01)
