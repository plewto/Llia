# llia.gui.tk.graph.graph_config

import llia.constants as con
from llia.locked_dictionary import LockedDictionary



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

    
    # pallet
    "graph-fill" : "#202029",
    "synth-fill" : "black",
    "synth-outline" : "#292920",
    "synth-activeoutline" : "#ffffcc",
    "bus-activeoutline" : "yellow",
    

    "info-header-fill" : "white",
    "info-data-fill" : "green"

    
    }
    
    
class LliaGraphConfig(LockedDictionary):

    def __init__(self):
        super(LliaGraphConfig, self).__init__( _template)


gconfig = LliaGraphConfig()
        



