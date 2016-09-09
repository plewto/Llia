# llia.llia_buffer

from llia.locked_dictionary import LockedDictionary

_TEMPLATE = {
    "name" : "",
    "frames" : None,
    "channels" : None,
    "is-wavetable" : None,
    "is-protected" : None,
    "sample-rate" : None,
    "filename" : None,
    "index" : None}


class BufferProxy(LockedDictionary):

    
    def __init__(self, name):
        super(BufferProxy, self).__init__(_TEMPLATE)
        self['name'] = str(name)

        
    def __str__(self):
        return 'BufferProxy("%s")' % self['name']
