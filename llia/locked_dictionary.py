# llia.locked_dictionary
# A dictionary with restricted key set.
# An attempt to add key not in the set raises KeyError


class LockedDictionary(dict):

    '''
    Defines a dictionary subclass with a pre-determined set of keys.
    It is not possible to add new keys after construction time.
    '''
    
    def __init__(self, template):
        '''
        Construct new LockedDictionary.

        ARGS:
           template - dictionary which defined allowed keys and initial 
                      values.
        '''
        super(LockedDictionary, self).__init__()
        for k,v in template.items():
            super(LockedDictionary, self).__setitem__(k, v)

    def __setitem__(self, key, value):
        '''
        Sets dictionary value.

        Raises KeyError for invalid key.
        '''
        if self.has_key(key):
            super(LockedDictionary, self).__setitem__(key, value)
        else:
            msg = "Can not ad key to LockedDictionary: %s" % key
            raise KeyError(msg)
            
