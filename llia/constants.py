# llia.constants
# 2016.02.07

VERSION = (0,0,1, "Alpha", "2016.05.13b")

BANNER ="""                           
,--.   ,--.,--.         
|  |   |  |`--' ,--,--. 
|  |   |  |,--.' ,-.  | 
|  '--.|  ||  |\ '-'  | 
`-----'`--'`--' `--`--' 
                            
"""


GUI_OPTIONS = (("None", "Use Llia without GUI."),
               # ("QT", "May not be avilaible on all systems."),
               ("TK", "Aviliable wherever Python is sold."))

KEY_MODES = ("Poly1", "Mono1", "EFX")
SYNTH_TYPES = ("ORGN", "BufferTest")
EFFECT_TYPES = ("Echo1", )

MAX_UNDO = 10
BANK_LENGTH = 128
MAX_TRANSPOSE = 36
MAX_PITCH_BEND = 2400 # In cents

CURVES = ("Linear", "Exp", "S", "Step")
MIDI_7BIT_DOMAIN = (0, 127)
PITCHWHEEL_DOMAIN = (-8192, 8191)
NORMAL_RANGE = (0.0, 1.0)
BIPOLAR_RANGE = (-1.0, 1.0)

RCENT = 2**(1.0/1200)


# LED Shapes
BAR = 0
ROUND = 1

BLACK = 0
GRAY = 1
RED = 2
GREEN = 3
BLUE = 4
YELLOW = 5
ORANGE = 6
PURPLE = 7
