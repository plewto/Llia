# llia.constants
# 2016.02.07

VERSION = (0,2,0, "2017.12.11")

BANNER =""" 
,--.   ,--.,--.         
|  |   |  |`--' ,--,--. 
|  |   |  |,--.' ,-.  | 
|  '--.|  ||  |\ '-'  | 
`-----'`--'`--' `--`--' 
"""

HELP_PATH = "doc"
HELP_EXT = "html"                 # Help file extension

GUI_OPTIONS = (("None", "Use Llia without GUI."),
               ("TK", "Aviliable wherever Python is sold."))

KEY_MODES = ("PolyN", "PolyRotate", "Poly1", "Mono1", "MonoExclusive", "EFX")

SYNTH_TYPES = []                # Populated at startup
EFFECT_TYPES = []               # Populated at startup
CONTROLLER_SYNTH_TYPES = []     # Populated at startup

LOGO_DIMENSIONS = (96,96)
SMALL_LOGO_DIMENSIONS = (64,64)

MAX_UNDO = 10
BANK_LENGTH = 128
MAX_TRANSPOSE = 36
MAX_PITCH_BEND = 2400 # In cents
MAX_BUS_COUNT = 8   # maximum number of synth buses for -each- bus type
                    # - audio-input
                    # - audio-output
                    # - control-input
                    # - control-output


CURVES = ("Linear", "Exp", "S", "Step")
MIDI_7BIT_DOMAIN = (0, 127)
PITCHWHEEL_DOMAIN = (-8192, 8191)
NORMAL_RANGE = (0.0, 1.0)
BIPOLAR_RANGE = (-1.0, 1.0)

RHALFSTEP = 2**(1/12.0)
RCENT = 2**(1.0/1200) # ratio 1 cent

DEFAULT_SAMPLE_RATE = 41000

PROTECTED_AUDIO_OUTPUT_BUS_COUNT = 8
PROTECTED_AUDIO_INPUT_BUS_COUNT = 8


__acc = []
for i in range(PROTECTED_AUDIO_OUTPUT_BUS_COUNT):
    __acc.append("out_%d" % i)
for i in range(PROTECTED_AUDIO_INPUT_BUS_COUNT):
    __acc.append("in_%d" % i)
PROTECTED_AUDIO_BUSSES = tuple(__acc)


__acc = []
for i in ("source", "sink"):
    __acc.append("null_%s" % i)
PROTECTED_CONTROL_BUSSES = tuple(__acc)
PROTECTED_CONTROL_BUS_COUNT = len(PROTECTED_CONTROL_BUSSES)

PROTECTED_BUFFERS = ('SINE1', 'TRIANGLE', 'SAW128', 'PULSE20')
PROTECTED_BUFFER_COUNT = len(PROTECTED_BUFFERS)
DEFAULT_BUFFER_FRAME_COUNT = 1024


# LED Shapes
# BAR = 0
# ROUND = 1
# BLACK = 0
# GRAY = 1
# RED = 2
# GREEN = 3
# BLUE = 4
# YELLOW = 5
# ORANGE = 6
# PURPLE = 7
