# llia.synthgroup
# 2017.12.06
#
# Defines SynthGroup class, a collection of synths
# SynthGroup is not related to SuperCollider groups.
#

from __future__ import print_function

class SynthGroup(object):

    def __init__(self):
        super(SynthGroup,self).__init__()
        self._members = []

    def add(self, synth):
        try:
            synth.IS_SYNTH_PROXY
            self._members.append(synth)
        except AttributeError:
            msg = "Can not add %s to SynthGroup." % type(synth)
            raise TypeError(msg)

    @property
    def members(self):
        return self._members[:]


