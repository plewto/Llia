# llia.gui.tk.graph.graph_config

import llia.constants as con
from llia.locked_dictionary import LockedDictionary
#from llia.gui.colorutil import Color


__TOKEN_IMAGE_PAD = 2
__SYNTH_TOKEN_WIDTH = con.SMALL_LOGO_DIMENSIONS[0]+__TOKEN_IMAGE_PAD*2
__SYNTH_TOKEN_HEIGHT = con.SMALL_LOGO_DIMENSIONS[1]+__TOKEN_IMAGE_PAD*2
__GRAPH_WIDTH, __GRAPH_HEIGHT = 900, 400

_template = {
    "graph-width" : 900,
    "graph-height" : 400,

    "info-enabled" : True,
    "info-x" : 500,
    "info-x-indent" : 8,
    "info-y" : 30,
    "info-y-delta" : 20,  # line spacing
    "info-font" : ("Mono", 9),
    "token-image-padding" : 2,

    "synth-token-width" : __SYNTH_TOKEN_WIDTH,
    "synth-token-height" : __SYNTH_TOKEN_HEIGHT,
    "bus-token-width" : 64,
    "bus-token-height" : 32,
    
    "audio-bus-width" : 64,
    "audio-bus-height" : 32,
    "bus-name-font" : ("Mono", 9),
    
    "audio-dash-pattern" : (1,1),
    "control-dash-pattern" : (8,4),
    
    # pallet
    "graph-fill" : "#202429",
    "synth-fill" : "#202429",
    "synth-outline" : "#292920",
    "synth-activeoutline" : "#ffffcc",
    "bus-activeoutline" : "yellow",
    "io-node-fill" : "blue",               # DEPRECIATED
    "io-audio-source" : "#8A1D1D",
    "io-audio-sink" : "#538A1D",
    "io-control-source" : "#1D8A8A",
    "io-control-sink" : "#531D8A",

    "info-header-fill" : "white",
    "info-data-fill" : "green"

    
    }

_audio_bus_colors = ("#f41010",
                     "#645938",
                     "#691748",
                     "#ed8d8d",
                     "#4c27ed",
                     "#0a70ff",  # 
                     "#7c7276",
                     "#9f8ded")

_control_bus_colors = ("#48ed27",
                       "#13400a",
                       "#566752",
                       "#9ded8d",
                       "#1adad8",
                       "#bff5f4",
                       "#7c7276",
                       "#125251")

def _cycle(seq, index):
    a = index % len(seq)
    return seq[a]
    

class LliaGraphConfig(LockedDictionary):

    def __init__(self):
        super(LliaGraphConfig, self).__init__( _template)
        self._audio_color_pointer = 0
        self._control_color_pointer = 0

    def audio_bus_color(self):
        c =  _cycle(_audio_bus_colors, self._audio_color_pointer)
        self._audio_color_pointer += 1
        return c

    def control_bus_color(self):
        c =  _cycle(_control_bus_colors, self._control_color_pointer)
        self._control_color_pointer += 1
        return c
        

gconfig = LliaGraphConfig()
        



