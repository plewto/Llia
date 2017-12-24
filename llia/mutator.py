# llia.mutator
# 2017.12.15
#
# TODO:
#    Adopt approx to deal with 0 value
#    Add suport for integer arguments.

from __future__ import print_function
from collections import OrderedDict

from llia.util.lmath import coin,approx,clip,rnd




class MutationParameter(object):


    def __init__(self, param, probability, range_, max_ratio=0.1, walker=False):
        self.param = param
        self.probability = probability
        self.range_ = range_
        self.max_ratio = max_ratio
        if walker:
            self.function = self.walker
        else:
            self.function = self.approx

    # def mutate(self, program):
    #     current = program[self.param]
    #     new_value = current
    #     if coin(self.probability):
    #         mn,mx = self.range_
    #         new_value = clip(self.function(current, self.max_ratio),mn,mx)
    #         program[self.param] = new_value

    def mutate(self, program):
        current = program[self.param]
        new_value = current
        if coin(self.probability):
            mn,mx = self.range_
            new_value = clip(self.function(current), mn,mx)
            program[self.param] = new_value
        return new_value

    def _scale_approx(self, x):
        return approx(x,self.max_ratio)

    def _additive_approx(self, x):
        diff = abs(self.range_[1] - self.range_[0])
        max_value = diff*self.max_ratio
        return rnd(max_value)

    def approx(self, x):
        THRESHOLD = 0.001
        if abs(x) < THRESHOLD:
            return self._additive_approx(x)
        else:
            return self._scale_approx(x)
        
    def walker(self, x):
        return coin(0.5, x-1, x+1)
        
    def __str__(self):
        frm = "%s prob %s  range %s  max_ratio %s"
        return frm % (self.param,self.probability,self.range_,self.max_ratio)

            
class Mutator(object):

    def __init__(self):
        self._params = OrderedDict()

    def define(self, param, prob, range_, max_ratio=0.1, walker=False):
        mp = MutationParameter(param,prob,range_,max_ratio,walker=walker)
        self._params[param] = mp

    def keys(self):
        return self._params.keys()

    def items(self):
        return self._params.items()
        
    def weight(self,param,prob):
        try:
            mp = self._params[param]
            mp.probabilty = prob
        except KeyError:
            msg = "%s is not a defined Mutation parameter"
            raise KeyError(msg % param)
        
    def mutate(self, program):
        p1 = program.clone()
        program = program.clone()
        for mp in self._params.values():
            mp.mutate(program)
        # for k,v in p1.diff(program).items():
        #     print("diff  %-16s  --> %s" % (k,v))
        return program

    def dump(self):
        print("Mutation:")
        for k,v in self._params.items():
            print(k,v)

    
# class __DummyMutation(object):

#     def __init__(self):
#         pass

#     def define(self, *_):
#         pass

#     def keys(self):
#         return []

#     def items(self):
#         return []
    
#     def weight(self, *_):
#         pass

#     def mutate(self, program):
#         return program


# DUMMY_MUTATION = __DummyMutation()
    


        

   
        
