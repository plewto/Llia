# llia.locked_dictionary
# A dictionay with restricted key set.
# An attempt to add key not in the set raises KeyError


class LockedDictionary(dict):

    def __init__(self, template):
        super(LockedDictionary, self).__init__()
        for k,v in template.items():
            super(LockedDictionary, self).__setitem__(k, v)

    def __setitem__(self, key, value):
        if self.has_key(key):
            super(LockedDictinary, self).__setitem__(key, value)
        else:
            msg = "Can not ad key to LockedDictionary: %s" % key
            raise KeyError(msg)
            
