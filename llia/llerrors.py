# llia.llerrors
# 2016.05.10

class LliaError(Exception):

    def __init__(self, msg=""):
        super(LliaError, self).__init__(msg)

class LliaPingError(LliaError):

    def __init__(self, msg=""):
        super(LliaPingError, self).__init__(msg)

class LliascriptError(LliaError):

    def __init__(self, msg=""):
        super(LliascriptError, self).__init__(msg)

class LliascriptParseError(LliascriptError):

    def __init__(self, msg=""):
        super(LliascriptParseError, self).__init__(msg)

class NoSuchBusError(LliascriptError):

    def __init__(self, msg=""):
        super(NoSuchBusError, self).__init__(msg)

class NoSuchBusOrParameterError(LliascriptError):

    def __init__(self, msg=""):
        super(NoSuchBusOrParameterError, self).__init__(msg)
        
class NoSuchSynthError(LliascriptError):

    def __init__(self, msg=""):
        super(NoSuchSynthError, self).__init__(msg)
    
class NoSuchBufferError(LliascriptError):

    def __init__(self, msg=""):
        super(NoSuchBufferError, self).__init__(msg)
