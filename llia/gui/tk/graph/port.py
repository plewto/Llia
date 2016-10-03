# llia.gui.tk.graph.port

import abc
from llia.gui.tk.graph.gconfig import gconfig
from llia.thirdparty.simplegeneric import generic

class Port(dict):

    def __init__(self, graph, parent_token, param=''):
        super(Port, self).__init__()
        self.graph = graph
        self.canvas = graph.canvas
        self.parent_token = parent_token
        self.param = param

    @abc.abstractmethod
    def is_audio(self):
        return False
    
    @abc.abstractmethod
    def is_control(self):
        return not(self.is_audio())

    @abc.abstractmethod
    def is_sink(self):
        return False

    @abc.abstractmethod
    def is_source(self):
        return not(self.is_sink())
        
    # Result is nested list
    # [[token, prt],[token, prt] ....]
    # The same token may appear more then once but will be paird with a
    # different port each time. 
    def find_allied_ports(self):
        return []
        
    def highlight(self, *_):
        canvas = self.canvas
        canvas.itemconfig(self['pad'],fill=gconfig["port-highlight"])
        self.graph.display_info(self.info_text())
        allied_port_color = gconfig['allied-port-highlight']
        allied_ports = self.find_allied_ports()
        for tkn,prt in allied_ports:
            try:
                self.canvas.itemconfig(prt['pad'], fill=allied_port_color)
            except TypeError:
                pass
        self.graph.current_token_and_port = [self.parent_token, self]
        self.graph.current_allied_ports = allied_ports
        
    def dehighlight(self, *_):
        canvas = self.canvas
        canvas.itemconfig(self['pad'],fill=self['fill'])
        canvas.itemconfig("audio-source", fill=gconfig["audio-source-fill"])
        canvas.itemconfig("audio-sink", fill=gconfig["audio-sink-fill"])
        canvas.itemconfig("control-source", fill=gconfig["control-source-fill"])
        canvas.itemconfig("control-sink", fill=gconfig["control-sink-fill"])
        # self.graph.clear_info()
        # self.graph.current_token_and_port = None
        # self.graph.current_allied_ports = None

    def _init_event_bindings(self):
        canvas = self.canvas
        pad = self['pad']
        canvas.tag_bind(pad, '<Enter>', self.highlight)
        canvas.tag_bind(pad, '<Leave>', self.dehighlight)
        
    def _info_text(self, header):
        acc = "%s:\n" % header
        frmt = "id = '%s', param = '%s'"
        acc += frmt % (self.parent_token.client_id(), self.param)
        return acc
                     
    def __str__(self):
        cname = self.__class__.__name__
        s = "Port(%s '%s')" % (cname, self.parent_token.client_id())
        return s

    def __repr__(self):
        return self.__str__()
    
        
class AudioSource(Port):

    def __init__(self, graph, parent_token, position, param=''):
        super(AudioSource, self).__init__(graph, parent_token, param)
        id_ = parent_token.client_id()
        radius = gconfig["port-radius"]
        if param:
            tags = ('audio-source', id_, "%s-%s" % (id_,param))
        else:
            tags = ('audio-source', id_)
        xc,yc = position
        x0,y0 = xc-radius,yc-radius
        x1,y1 = xc+radius,yc+radius
        fill = gconfig["audio-source-fill"]
        c = self.canvas.create_oval(x0,y0,x1,y1,
                                    fill = fill,
                                    tags = tags)
        self['fill'] = fill
        self['pad'] = c
        self._init_event_bindings()

    def is_audio(self):
        return True

    def is_control(self):
        return False
    
    def is_source(self):
        return True

    def is_sink(self):
        return False
    
    def info_text(self):
        return self._info_text("AudioSource")

    def find_allied_ports(self):
        acc = []
        if self.param:
            for btkn in self.graph.audio_bus_tokens.values():
                prt = btkn["in-port"]
                acc.append((btkn,prt))
            return acc
        else:
            for sytk in self.graph.synth_tokens.values():
                for prt in sytk.audio_input_ports.values():
                    acc.append((sytk, prt[1]))
            return acc


        
class AudioSink(Port):

    def __init__(self, graph, parent_token, position, param=''):
        super(AudioSink, self).__init__(graph,parent_token,param)
        id_ = parent_token.client_id()
        radius = gconfig["port-radius"]
        if param:
            tags = ('audio-sink', id_, "%s-%s" % (id_,param))
        else:
            tags = ('audio-source', id_)
        xc,yc = position
        x0,y0 = xc-radius,yc-radius
        x1,y1 = xc+radius,yc+radius
        fill = gconfig['audio-sink-fill']
        c = self.canvas.create_oval(x0,y0,x1,y1,
                                    fill = fill,
                                    tags = tags)
        self['fill'] = fill
        self['pad'] = c
        self._init_event_bindings()

    def is_audio(self):
        return True

    def is_control(self):
        return False
    
    def is_source(self):
        return False

    def is_sink(self):
        return True
    
    def info_text(self):
        return self._info_text("AudioSink")

    def find_allied_ports(self):
        acc = []
        if self.param:
            for btkn in self.graph.audio_bus_tokens.values():
                prt = btkn['out-port']
                acc.append((btkn,prt))
        else:
            for sytkn in self.graph.synth_tokens.values():
                for prt in sytkn.audio_output_ports.values():
                    acc.append((sytkn, prt[1]))
        return acc
                    

    
class ControlSource(Port):

    def __init__(self, graph, parent_token, position, param=''):
        super(ControlSource, self).__init__(graph,parent_token,param)
        id_ = parent_token.client_id()
        radius = gconfig['port-radius']
        if param:
            tags = ('control-source', id_, "%s-%s" % (id_,param))
        else:
            tags = ('control-source', id_)
        xc,yc = position
        x0,y0 = xc-radius,yc-radius
        x1,y1 = xc+radius,yc+radius
        fill = gconfig["control-source-fill"]
        c = self.canvas.create_oval(x0,y0,x1,y1,
                                    fill = fill,
                                    tags = tags)
        self['fill'] = fill
        self['pad'] = c
        self._init_event_bindings()
        
    def info_text(self):
        return self._info_text("ControlSource")

    def is_audio(self):
        return False

    def is_control(self):
        return True
    
    def is_source(self):
        return True

    def is_sink(self):
        return False

    
    def find_allied_ports(self):
        acc =[]
        if self.param:
            for btkn in self.graph.control_bus_tokens.values():
                try:
                    prt = btkn["in-port"]
                    acc.append((btkn,prt))
                except KeyError:
                    pass # ignore 'null' buses
        else:
            for sytkn in self.graph.synth_tokens.values():
                for prt in sytkn.control_input_ports.values():
                    acc.append((sytkn, prt[1]))
        return acc

    
class ControlSink(Port):

    def __init__(self, graph, parent_token, position, param=''):
        super(ControlSink, self).__init__(graph,parent_token,param)
        id_ = parent_token.client_id()
        radius = gconfig['port-radius']
        if param:
            tags = ('control-sink', id_, "%s-%s" % (id_,param))
        else:
            tags = ('control-sink', id_)
        xc,yc = position
        x0,y0 = xc-radius,yc-radius
        x1,y1 = xc+radius,yc+radius
        fill = gconfig["control-sink-fill"]
        c = self.canvas.create_oval(x0,y0,x1,y1,
                                    fill = fill,
                                    tags = tags)
        self['fill'] = fill
        self['pad'] = c
        self._init_event_bindings()

    def is_audio(self):
        return False

    def is_control(self):
        return True
    
    def is_source(self):
        return False

    def is_sink(self):
        return True
    
    def info_text(self):
        return self._info_text("ControlSink")

    def find_allied_ports(self):
        acc = []
        if self.param:
            for btkn in self.graph.control_bus_tokens.values():
                try:
                    prt = btkn['out-port']
                    acc.append((btkn,prt))
                except KeyError:
                    pass
        else:
            for sytkn in self.graph.synth_tokens.values():
                for prt in sytkn.control_output_ports.values():
                    acc.append((sytkn, prt[1]))
        return acc

@generic
def is_port(obj):
    return False

@is_port.when_type(Port)
def _is_port(obj):
    return True
