# llia.lsl.lsl_errors
#

class LliaError(Exception):

    def __init__(self, msg=""):
        super(LliaError, self).__init__(msg)

class LliaParseError(LliaError):

    def __init__(self, msg=""):
        super(LliaParseError, self).__init__(msg)

class NoSuchBusError(LliaError):

    def __init__(self, msg=""):
        super(NoSuchBusError, self).__init__(msg)
    
