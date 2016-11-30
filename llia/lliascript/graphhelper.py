# llia.lliascript.graphhelper
# Extends Parser with graph related commands

from __future__ import print_function


class GraphHelper(object):

    def __init__(self,parser,local_namespace):
        self.parser = parser
        self.proxy = parser.proxy
        self._init_namespace(local_namespace)
        # Ignore graph ralated commands if self.lliagraph is None
        self.lliagraph = None
        try:
            self.lliagraph = parser.app.main_window().llia_graph
        except AttributeError:
            msg = "No active graph, ignoring lliascrip graph related commands"
            parser.warning(msg)

    def _init_namespace(self, ns):
        ns["graph_defined"] = self.graph_defined
        ns["graph_synth_tokens"] = self.synth_tokens
        ns["graph_audio_bus_tokens"] = self.audio_bus_tokens
        ns["graph_control_bus_tokens"] = self.control_bus_tokens
        ns["graph_get_token"] = self.get_token
        ns["graph_whereis_token"] = self.whereis_token
        ns["graph_move_token"] = self.move_token
        ns["graph_sync"] = self.sync_graph
        ns["graph_dump"] = self.dump_graph
        
    def graph_defined(self):
        return self.lliagraph

    def synth_tokens(self):
        if self.lliagraph:
            return self.lliagraph.synth_tokens.items()
        else:
            return []

    def audio_bus_tokens(self):
        if self.lliagraph:
            return self.lliagraph.audio_bus_tokens.items()
        else:
            return []

    def control_bus_tokens(self):
        if self.lliagraph:
            return self.lliagraph.audio_bus_tokens.items()
        else:
            return []

    def get_token(self, tid):
        if self.lliagraph:
            return self.lliagraph.get_token(tid)
        else:
            return None
        
    def whereis_token(self, tid, silent=False):
        tk = self.get_token(tid)
        if tk:
            rs = tk.position()
        else:
            rs = None
        if not silent:
            msg = "Token %s position is %s" % (tid, rs)
            self.parser.status(msg)
        return rs
            
    def move_token(self,tid,x,y,sync=True):
        tk = self.get_token(tid)
        if tk:
            tk.move_to(x,y)
            if sync:
                self.lliagraph.sync()
            return tk
        else:
            return None

    def sync_graph(self):
        if self.lliagraph:
            self.lliagraph.sync()
            return True
        else:
            return False
        
    def dump_graph(self):
        if self.lliagraph:
            self.lliagraph.dump()
            
