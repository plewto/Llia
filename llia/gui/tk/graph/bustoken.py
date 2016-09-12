# llia.gui.tk.graph.bustoken
#
# class Hierarchy:
#
#  Token
#    |
#    +--- BusToken
#            |
#            +--- AudioBusToken
#            +--- ControlBusToken

from __future__ import print_function

from llia.gui.tk.graph.graph_config import gconfig
from llia.gui.tk.graph.token import Token


class BusToken(Token):

    def __init__(self, graph, app, busobj):
        super(BusToken, self).__init__(graph, app, busobj)

    def client_id(self):
        return self.client.name

    def is_protected(self):
        return self.client.is_protected()
    

class AudioBusToken(BusToken):

    def __init__(self, graph, app, abusobj):
        super(AudioBusToken, self).__init__(graph, app, abusobj)

    def is_audio_bus(self):
        return True

    def keep_hiden(self):
        c = self.client.source_count() + self.client.sink_count()
        return c == 0

    def render(self): # ISSUE: not implemented
        pass
    
class ControlBusToken(BusToken):

    def __init__(self, graph, app, cbusobj):
        super(ControlBusToken, self).__init__(graph, app, cbusobj)

    def is_control_bus(self):
        return True

    def keep_hidden(self):
        c = self.client.source_count() + self.client.sink_count()
        return self.is_protected() or c == 0

    def render(self): # ISSUE: not implemented
        pass 
