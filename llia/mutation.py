# llia.mutation
# 2017.12.15
#

from __future__ import print_function

from llia.util.lmath import coin,approx,clip

class MutationParameter(object):

    def __init__(self, param, probability, range_, max_ratio=0.1):
        self.param = param
        self.probability = probability
        self.range_ = range_
        self.function = approx
        self.max_ratio = max_ratio

    def mutate(self, program):
        if coin(self.probability):
            current = program[self.param]
            mn,mx = self.range_
            new_value = clip(self.function(current, self.max_ratio),mn,mx)
            program[self.param] = new_value

class Mutation(object):

    def __init__(self):
        self._params = {}

    def define(self, param, prob, range_, max_ratio=0.1):
        mp = MutationParameter(param,prob,range_,max_ratio)
        self._params[param] = mp

    def weight(self,param,prob):
        try:
            mp = self._params[param]
            mp.probabilty = prob
        except KeyError:
            msg = "%s is not a defined Mutation parameter"
            raise KeyError(msg % param)

    def mutate(self, program):
        for mp in self._params.values():
            mp.mutate(program)
        return program

class __DummyMutation(object):

    def __init__(self):
        pass

    def define(self, *_):
        pass

    def weight(self, *_):
        pass

    def mutate(self, program):
        return program


DUMMY_MUTATION = __DummyMutation()
    


        

   
        
