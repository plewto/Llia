# llia.lsl.lsl_errors
#

class LliascriptError(Exception):

    def __init__(self, msg=""):
        super(LliascriptError, self).__init__(msg)

class LliascriptParseError(LliascriptError):

    def __init__(self, msg=""):
        super(LliascriptParseError, self).__init__(msg)

class NoSuchBusError(LliascriptError):

    def __init__(self, msg=""):
        super(NoSuchBusError, self).__init__(msg)
    
