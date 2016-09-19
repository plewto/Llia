# llia.gui.tk.graph.gconfig

import llia.constants as con
from llia.locked_dictionary import LockedDictionary


_logo_dimensions = con.SMALL_LOGO_DIMENSIONS
_node_image_pad = 2

_template = {
    "graph-width" : 900,
    "graph-height" : 400,
    "info-area-width" : 400,

    # Synth nodes
    "synth-node-image-padding" : _node_image_pad,
    "synth-node-width" : _logo_dimensions[0] + 2 * _node_image_pad,
    "synth-node-height" : _logo_dimensions[1] + 2 * _node_image_pad,


    # General buses
    "bus-name-font" : ("Mono", 10),
    
    # Audio buses
    "audio-bus-width" : 65,
    "audio-bus-height" : 24,
    "audio-bus-chamfer" : 12,
    "audio-path-dash" : (1,1),
    "audio-path-width" : 1,

    
    # Control buses
    "control-bus-width" : 40,
    "control-bus-height" : 40,
    #"control-bus-chamfer" : 12,
    "control-path-dash" : (8,8),
    "control-path-width" : 1,

    
    # Ports  (audio/control sources/sinks)
    "port-radius" : 4,
    
    # Pallet
    "graph-fill" : "#202429", # "#343a42",
    "info-fill" : "#292028",
    "info-warning-color" : "red",
    "info-warning-font" : ("Sans", 10),
    "highlight-color" : "yellow",
    "port-highlight" : "#ff00ff",
    "allied-port-highlight" : "yellow",
    "audio-bus-fill" : "black",
    "audio-bus-colors" : ("#ff0000","#581195","#d6a100","#b69370",
                          "#00d6a1","#ff00bf","#00bfff","#8000ff",
                          "#0000ff","#0080ff","#bf00ff","#00ffbf",
                          "#b67070","#40ff00","#82b670","#ff8000"),
    "control-bus-fill" : "black",
    "control-bus-colors" : ("#800000","#6D7F7B","#806000","#804F4F",
                            "#608000","#600080","#008060","#003F80",
                            "#006080","#007E80","#3F0080","#218000",
                            "#80007E","#7E8000","#AA8000","#803F00"),
    
    "audio-source-fill" : "#590000",
    "audio-sink-fill" : "#2d5900",
    "control-source-fill" : "#500059", #"#005959",
    "control-sink-fill" : "#290059",
    "synth-fill" : "",
    "synth-outline" : "",
    "info-text-color" : "#6f8f80",
    "info-font" : ("Mono", 10),

    "rubberband-fill" : "yellow",
    "rubberband-dash" : (1,1),

    "drop-threshold" : 30    # drag n drop distance greater then threshold ignored
}


class GraphConfig(LockedDictionary):

    def __init__(self):
        super(GraphConfig, self).__init__(_template)
        self._audio_color_pointer = 0
        self._control_color_pointer = 0

    def audio_bus_color(self):
        pallet = self["audio-bus-colors"]
        index = self._audio_color_pointer % len(pallet)
        c = pallet[index]
        self._audio_color_pointer += 1
        return c

    def control_bus_color(self):
        pallet = self["control-bus-colors"]
        index = self._control_color_pointer % len(pallet)
        c = pallet[index]
        self._control_color_pointer += 1
        return c
        
        
gconfig = GraphConfig()

