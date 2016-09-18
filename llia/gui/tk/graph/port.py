# llia.gui.tk.graph.port

from llia.gui.tk.graph.gconfig import gconfig

class Port(dict):

    def __init__(self, graph, parent_token, param=''):
        super(Port, self).__init__()
        self.graph = graph
        self.canvas = graph.canvas
        self.parent_token = parent_token
        self.param = param

    def highlight(self, *_):
        canvas = self.canvas
        canvas.itemconfig(self['pad'],fill=gconfig["port-highlight"])
        self.graph.display_info(self.info_text())
        
    def dehighlight(self, *_):
        canvas = self.canvas
        canvas.itemconfig(self['pad'],fill=self['fill'])
        self.graph.clear_info()

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

    def info_text(self):
        return self._info_text("AudioSource")
        

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

    def info_text(self):
        return self._info_text("AudioSink")
        
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

    def info_text(self):
        return self._info_text("ControlSink")
