# llia.synths.fm2.fm2_data

from __future__ import print_function

from llia.program import Program
from llia.bank import ProgramBank
from llia.util.lmath import clip, db_to_amp
from llia.performance_edit import performance

prototype = {
    "amp" : 0.2,           # linear amplitude
    "port" : 0.0,          # portamento time (0..1)
    
    "xPitch" : 0.0,        # external signal -> pitch (0..1)
    "xModDepth" : 0.0,     # external signal -> mod depth (0..1)
    "xScale" : 1.0,        # external signal scale factor (0..4)
    "xBias" : 0.0,         # external signal bias (-4..+4)
    
    "lfoFreq" : 5.0,       # frequency in Hz, (0..100)
    "lfoDelay" : 0.0,      # LFO onset delay in seconds (0..4)
    "vsens" : 0.1,         # vibrato sensitivity (0..1)
    "vdepth" : 0.0,        # programmed vibrato depth (0..1)
    
                           # OP1, carrier
    "op1Enable" : 1,       # 0 -> disable  1 -> enable
    "op1Ratio" : 1.0,      # frequency ratio  0 <= ratio <= 32
    "op1Bias" : 0.0,       # frequency bias   0 <= bias <= 20
    "op1Amp" : 1.0,        # linear amplitude (0..1)
    
    "op1Attack" : 0.0,     # attack time (0..12)
    "op1Decay1" : 0.0,     # initial decay time (0..12)
    "op1Decay2" : 0.0,     # seconds decay time (0..12)
    "op1Release" : 0.0,    # release time (0..12)
    "op1Breakpoint" : 1.0, # envelope breakpoint level (0..1)
    "op1Sustain" : 1.0,    # envelope sustain level (0..1)
    "op1GateHold" : 0,     # envelope gate mode, 0 -> gated, 1 -> cycle
    "op1Keybreak" : 60,    # keyscale key, MIDI key number
    "op1LeftScale" : 0,    # left keyscale depth in db/octave
    "op1RightScale" : 0,   # right keyscale depth in db/octave
    "op1Lfo" : 0.0,        # LFO -> tremolo  0.0 .. 0.5 -> 0% .. 100%
                           #                 0.5 .. 1.0 -> adds 2x freq 
    "op1Velocity" : 0.0,   # velocity scale factor (0..1)
    
    "op2Enable" : 1,       # OP2, modulator     
    "op2Ratio" : 1.0,
    "op2Bias" : 0.0,
    "op2Amp" : 1.0,        # modulation depth (0..10)
    "op2AmpRange" : 1,     # modulation range (1,10,100,1000,10000)
    "op2Attack" : 0.0,
    "op2Decay1" : 0.0,
    "op2Decay2" : 0.0,
    "op2Release" : 0.0,
    "op2Breakpoint" : 1.0,
    "op2Sustain" : 1.0,
    "op2GateHold" : 0,
    "op2Keybreak" : 60,
    "op2LeftScale" : 0,
    "op2RightScale" : 0,
    "op2Lfo" : 0.0,
    "op2Velocity" : 0.0,
    "op2Feedback": 0      # OP2 FM feedback (0..?)
    }

class FM2(Program):

    def __init__(self, name):
        super(FM2, self).__init__(name, "FM2", prototype)
        self.performance = performance()

program_bank = ProgramBank(FM2("Init"))
program_bank.enable_undo = False


def _fill_external_params(d):
    rs = {"xPitch" : float(d.get("pitch", 0.0)),
          "xModDepth" : float(d.get("mod", 0.0)),
          "xScale" : float(d.get("scale", 1.0)),
          "xBias" : float(d.get("bias", 0.0))}
    return rs


def _fill_lfo_params(d):
    rs = {"lfoFreq" : float(d.get("freq", 5)),
          "lfoDelay" : float(d.get("delay", 0)),
          "vsens" : float(d.get("vsens", 0.1)),
          "vdepth" : float(d.get("vdepth", 0.0))}
    return rs

def _fill_envelope_params(op, d):
    def param(suffix):
        return "op%s%s" % (op, suffix)
    rs = {param("Attack") : float(d.get("attack", 0.0)),
          param("Decay1") : float(d.get("decay1", 0.0)),
          param("Decay2") : float(d.get("decay2", 0.0)),
          param("Release") : float(d.get("release", 0.0)),
          param("Breakpoint") : float(d.get("breakpoint", 1.0)),
          param("Sustain") : float(d.get("sustain", 1.0))}
    if d.get("env-cycle", False):
        cycle = 1
    else:
        cycle = 0
    rs[param("GateHold")] = cycle
    return rs

def _fill_common_op_params(op, d):
    def param(suffix):
        return "op%s%s" % (op, suffix)
    if d.get("enable", True):
        enable = 1
    else:
        enable = 0
    rs = {param("Enable") : enable,
          param("Ratio") : float(d.get("ratio", 1.0)),
          param("Bias") : float(d.get("bias", 0.0)),
          param("Keybreak") : int(d.get("break-key", 60)),
          param("LeftScale") : float(d.get("left-scale", 0)),
          param("RightScale") : float(d.get("right-scale", 0)),
          param("Lfo") : float(d.get("lfo", 0.0)),
          param("Velocity") : float(d.get("velocity", 0.0))}
    return rs
          
def _fill_op1_params(d):
    rs = _fill_common_op_params(1, d)
    rs.update(_fill_envelope_params(1, d))
    rs["amp"] = int(db_to_amp(d.get("amp", 0)))
    return rs

def _fill_op2_params(d):
    rs = _fill_common_op_params(2, d)
    rs.update(_fill_envelope_params(2, d))
    rs["op2Amp"] = float(d.get("amp", 1.0))
    rs["op2AmpRange"] = int(d.get("modRange", 1))
    rs["op2Feedback"] = float(d.get("feedback", 0.0))
    return rs

def fm2(slot, name, amp=-12, port=0.0,
        external = {"scale" : 1.0,
                    "bias" : 0.0,
                    "pitch" : 0.0,
                    "mod" : 0.0},
        lfo = {"freq" : 5.0,
               "delay" : 0.0,
               "vsens" : 0.1,
               "vdepth" : 0.0},
        op1 = {"enable" : True,
               "ratio" : 1.0,
               "bias" : 0.0,
               "amp" : 0,  # in DB
               "attack" : 0.0,
               "decay1" : 0.0,
               "decay2" : 0.0,
               "release" : 0.0,
               "breakpoint" : 1.0,
               "sustain" : 1.0,
               "env-cycle" : False,
               "break-key" : 60,
               "left-scale" : 0,
               "right-scale" : 0,
               "lfo" : 0.0,
               "velocity" : 0.0},
        op2 = {"enable" : True,
               "ratio" : 1.0,
               "bias" : 0.0,
               "amp" : 0.0,    # modulation depth
               "modRange" : 1, # powers of 10
               "attack" : 0.0,
               "decay1" : 0.0,
               "decay2" : 0.0,
               "release" : 0.0,
               "breakpoint" : 1.0,
               "sustain" : 1.0,
               "env-cycle" : False,
               "break-key" : 60,
               "left-scale" : 0,
               "right-scale" : 0,
               "lfo" : 0.0,
               "velocity" : 0.0,
               "feedback" : 0.0}):
    p = FM2(name)
    p["amp"] = int(db_to_amp(amp))
    p["port"] = float(port)
    acc = _fill_external_params(external)
    acc.update(_fill_lfo_params(lfo))
    acc.update(_fill_op1_params(op1))
    acc.update(_fill_op2_params(op2))
    for param,value in acc.items():
        p[param] = value
    program_bank[slot] = p
    return p


fm2(  0, "Brazos", amp=0, port=0.000,
        external={"scale" : 1.000,
                  "bias" : 0.000,
                  "pitch" : 0.000,
                  "mod" : 0.000},
        lfo = {"freq" : 5.661,
               "delay" : 3.417,
               "vsens" : 0.100,
               "vdepth" : 0.569},
        op1 = {"enable" : True,
               "ratio" : 8.0000,
               "bias" : 0.0000,
               "attack" : 0.3129,
               "decay1" : 0.6317,
               "decay2" : 0.5482,
               "release" : 0.5345,
               "breakpoint" : 0.9664,
               "sustain" : 0.5484,
               "lfo" : 0.0000,
               "velocity" : 0.0000,
               "break-key" : 60,
               "left-scale" : 0,
               "right-scale" : -3,
               "amp" : 0,
               "env-cycle" : False},
        op2 = {"enable" : True,
               "ratio" : 2.0000,
               "bias" : 0.0000,
               "amp" : 5.0000,
               "attack" : 2.1342,
               "decay1" : 0.0599,
               "decay2" : 0.5264,
               "release" : 0.0394,
               "breakpoint" : 0.9485,
               "sustain" : 0.1755,
               "feedback" : 2.0200,
               "lfo" : 0.0000,
               "velocity" : 0.0000,
               "modRange" : 1,
               "break-key" : 60,
               "left-scale" : 0,
               "right-scale" : -12,
               "env-cycle" : True})

fm2(  1, "Yukon", amp=0, port=0.500,
        external={"scale" : 1.000,
                  "bias" : 0.000,
                  "pitch" : 0.000,
                  "mod" : 0.000},
        lfo = {"freq" : 6.673,
               "delay" : 1.464,
               "vsens" : 0.100,
               "vdepth" : 0.267},
        op1 = {"enable" : True,
               "ratio" : 1.0000,
               "bias" : 0.0000,
               "attack" : 0.1705,
               "decay1" : 0.5750,
               "decay2" : 0.3982,
               "release" : 0.3369,
               "breakpoint" : 0.9677,
               "sustain" : 0.6204,
               "lfo" : 0.3467,
               "velocity" : 0.0000,
               "break-key" : 60,
               "left-scale" : 0,
               "right-scale" : 0,
               "amp" : 0,
               "env-cycle" : False},
        op2 = {"enable" : True,
               "ratio" : 3.0000,
               "bias" : 2.8518,
               "amp" : 5.0000,
               "attack" : 0.2149,
               "decay1" : 0.0273,
               "decay2" : 0.4368,
               "release" : 0.2486,
               "breakpoint" : 0.9592,
               "sustain" : 0.3110,
               "feedback" : 0.6800,
               "lfo" : 0.0000,
               "velocity" : 0.1407,
               "modRange" : 1,
               "break-key" : 60,
               "left-scale" : 0,
               "right-scale" : 0,
               "env-cycle" : False})

fm2(  2, "Alsek", amp=0, port=0.000,
        external={"scale" : 1.000,
                  "bias" : 0.000,
                  "pitch" : 0.000,
                  "mod" : 0.000},
        lfo = {"freq" : 4.963,
               "delay" : 1.555,
               "vsens" : 0.100,
               "vdepth" : 0.249},
        op1 = {"enable" : True,
               "ratio" : 4.0000,
               "bias" : 0.0000,
               "attack" : 0.3875,
               "decay1" : 0.3483,
               "decay2" : 0.2837,
               "release" : 0.2804,
               "breakpoint" : 0.9405,
               "sustain" : 0.9657,
               "lfo" : 0.0000,
               "velocity" : 0.0000,
               "break-key" : 60,
               "left-scale" : 0,
               "right-scale" : -3,
               "amp" : 0,
               "env-cycle" : False},
        op2 = {"enable" : True,
               "ratio" : 10.0000,
               "bias" : 37.3318,
               "amp" : 5.0000,
               "attack" : 2.0403,
               "decay1" : 0.3054,
               "decay2" : 0.5513,
               "release" : 0.7926,
               "breakpoint" : 0.8495,
               "sustain" : 0.8495,
               "feedback" : 0.0000,
               "lfo" : 0.0000,
               "velocity" : 0.8241,
               "modRange" : 1,
               "break-key" : 60,
               "left-scale" : 3,
               "right-scale" : -12,
               "env-cycle" : True})

fm2(  3, "Schuylkill", amp=0, port=0.000,
        external={"scale" : 1.000,
                  "bias" : 0.000,
                  "pitch" : 0.000,
                  "mod" : 0.000},
        lfo = {"freq" : 6.128,
               "delay" : 3.102,
               "vsens" : 0.100,
               "vdepth" : 0.027},
        op1 = {"enable" : True,
               "ratio" : 2.0000,
               "bias" : 0.0000,
               "attack" : 1.9758,
               "decay1" : 3.0195,
               "decay2" : 2.3272,
               "release" : 0.6002,
               "breakpoint" : 0.9293,
               "sustain" : 0.2449,
               "lfo" : 0.0000,
               "velocity" : 0.0000,
               "break-key" : 60,
               "left-scale" : 0,
               "right-scale" : 0,
               "amp" : 0,
               "env-cycle" : True},
        op2 = {"enable" : True,
               "ratio" : 1.4580,
               "bias" : 28.2853,
               "amp" : 5.0000,
               "attack" : 0.1161,
               "decay1" : 0.9514,
               "decay2" : 1.9395,
               "release" : 3.9660,
               "breakpoint" : 0.9475,
               "sustain" : 0.5224,
               "feedback" : 3.2400,
               "lfo" : 0.0553,
               "velocity" : 0.0000,
               "modRange" : 1,
               "break-key" : 60,
               "left-scale" : 0,
               "right-scale" : 0,
               "env-cycle" : True})

fm2(  4, "Embudo", amp=0, port=0.000,
        external={"scale" : 1.000,
                  "bias" : 0.000,
                  "pitch" : 0.000,
                  "mod" : 0.000},
        lfo = {"freq" : 6.658,
               "delay" : 3.174,
               "vsens" : 0.100,
               "vdepth" : 0.642},
        op1 = {"enable" : True,
               "ratio" : 2.0000,
               "bias" : 0.0000,
               "attack" : 0.0151,
               "decay1" : 1.8147,
               "decay2" : 0.6741,
               "release" : 3.5595,
               "breakpoint" : 0.9985,
               "sustain" : 0.4044,
               "lfo" : 0.0000,
               "velocity" : 0.0000,
               "break-key" : 60,
               "left-scale" : 0,
               "right-scale" : 0,
               "amp" : 0,
               "env-cycle" : False},
        op2 = {"enable" : True,
               "ratio" : 2.2500,
               "bias" : 0.6388,
               "amp" : 5.0000,
               "attack" : 1.2827,
               "decay1" : 3.2038,
               "decay2" : 0.4847,
               "release" : 0.9320,
               "breakpoint" : 0.9696,
               "sustain" : 0.1025,
               "feedback" : 0.0000,
               "lfo" : 0.0000,
               "velocity" : 0.0000,
               "modRange" : 1,
               "break-key" : 60,
               "left-scale" : 0,
               "right-scale" : 0,
               "env-cycle" : False})

fm2(  5, "Quesnel", amp=0, port=0.000,
        external={"scale" : 1.000,
                  "bias" : 0.000,
                  "pitch" : 0.000,
                  "mod" : 0.000},
        lfo = {"freq" : 4.289,
               "delay" : 2.120,
               "vsens" : 0.000,
               "vdepth" : 0.000},
        op1 = {"enable" : True,
               "ratio" : 2.0000,
               "bias" : 0.0000,
               "attack" : 1.1618,
               "decay1" : 0.1584,
               "decay2" : 0.4013,
               "release" : 0.8519,
               "breakpoint" : 0.9612,
               "sustain" : 0.8417,
               "lfo" : 0.0000,
               "velocity" : 0.0854,
               "break-key" : 60,
               "left-scale" : 0,
               "right-scale" : 0,
               "amp" : 0,
               "env-cycle" : False},
        op2 = {"enable" : True,
               "ratio" : 1.0000,
               "bias" : 0.0000,
               "amp" : 5.0000,
               "attack" : 0.1882,
               "decay1" : 0.7621,
               "decay2" : 0.0234,
               "release" : 0.8168,
               "breakpoint" : 0.9114,
               "sustain" : 0.9196,
               "feedback" : 0.0000,
               "lfo" : 0.1809,
               "velocity" : 0.1407,
               "modRange" : 1,
               "break-key" : 72,
               "left-scale" : 3,
               "right-scale" : -3,
               "env-cycle" : False})

fm2(  6, "Nechako", amp=0, port=0.615,
        external={"scale" : 1.000,
                  "bias" : 0.000,
                  "pitch" : 0.000,
                  "mod" : 0.000},
        lfo = {"freq" : 5.475,
               "delay" : 0.162,
               "vsens" : 0.100,
               "vdepth" : 0.212},
        op1 = {"enable" : True,
               "ratio" : 2.0000,
               "bias" : 0.0000,
               "attack" : 0.0185,
               "decay1" : 0.0532,
               "decay2" : 1.5461,
               "release" : 1.8632,
               "breakpoint" : 0.9929,
               "sustain" : 0.5666,
               "lfo" : 0.0000,
               "velocity" : 0.0000,
               "break-key" : 60,
               "left-scale" : 0,
               "right-scale" : -3,
               "amp" : 0,
               "env-cycle" : True},
        op2 = {"enable" : True,
               "ratio" : 1.9805,
               "bias" : 0.0000,
               "amp" : 5.0000,
               "attack" : 1.1546,
               "decay1" : 3.1670,
               "decay2" : 2.2445,
               "release" : 3.5135,
               "breakpoint" : 0.9097,
               "sustain" : 0.0334,
               "feedback" : 0.0000,
               "lfo" : 0.0000,
               "velocity" : 0.0000,
               "modRange" : 1,
               "break-key" : 48,
               "left-scale" : 6,
               "right-scale" : -6,
               "env-cycle" : True})

fm2(  7, "Liard", amp=0, port=0.000,
        external={"scale" : 1.000,
                  "bias" : 0.000,
                  "pitch" : 0.000,
                  "mod" : 0.000},
        lfo = {"freq" : 5.170,
               "delay" : 0.877,
               "vsens" : 0.100,
               "vdepth" : 0.329},
        op1 = {"enable" : True,
               "ratio" : 0.0000,
               "bias" : 0.1024,
               "attack" : 0.3374,
               "decay1" : 0.5771,
               "decay2" : 1.8619,
               "release" : 3.4654,
               "breakpoint" : 0.9835,
               "sustain" : 0.8373,
               "lfo" : 0.0000,
               "velocity" : 0.2362,
               "break-key" : 60,
               "left-scale" : 0,
               "right-scale" : 0,
               "amp" : 0,
               "env-cycle" : True},
        op2 = {"enable" : True,
               "ratio" : 2.0000,
               "bias" : 0.0000,
               "amp" : 5.0000,
               "attack" : 0.0182,
               "decay1" : 0.2515,
               "decay2" : 3.1474,
               "release" : 2.9873,
               "breakpoint" : 0.9735,
               "sustain" : 0.8671,
               "feedback" : 1.3000,
               "lfo" : 0.0000,
               "velocity" : 0.0000,
               "modRange" : 1000,
               "break-key" : 60,
               "left-scale" : 0,
               "right-scale" : 3,
               "env-cycle" : True})

fm2(  8, "Athabasca", amp=0, port=0.025,
        external={"scale" : 1.000,
                  "bias" : 0.000,
                  "pitch" : 0.000,
                  "mod" : 0.000},
        lfo = {"freq" : 6.905,
               "delay" : 1.940,
               "vsens" : 0.040,
               "vdepth" : 0.141},
        op1 = {"enable" : True,
               "ratio" : 0.0000,
               "bias" : 0.2905,
               "attack" : 0.2189,
               "decay1" : 1.6132,
               "decay2" : 0.7291,
               "release" : 0.7329,
               "breakpoint" : 0.9061,
               "sustain" : 0.5179,
               "lfo" : 0.0000,
               "velocity" : 0.3166,
               "break-key" : 60,
               "left-scale" : 0,
               "right-scale" : 0,
               "amp" : 0,
               "env-cycle" : False},
        op2 = {"enable" : True,
               "ratio" : 3.0000,
               "bias" : 0.0000,
               "amp" : 7.2500,
               "attack" : 0.0000,
               "decay1" : 0.1907,
               "decay2" : 0.4534,
               "release" : 0.4241,
               "breakpoint" : 0.5760,
               "sustain" : 0.3211,
               "feedback" : 0.0000,
               "lfo" : 0.0000,
               "velocity" : 0.3869,
               "modRange" : 1000,
               "break-key" : 60,
               "left-scale" : 0,
               "right-scale" : 0,
               "env-cycle" : False})

fm2(  9, "Cimarron", amp=0, port=0.000,
        external={"scale" : 1.000,
                  "bias" : 0.000,
                  "pitch" : 0.000,
                  "mod" : 0.000},
        lfo = {"freq" : 44.344,
               "delay" : 0.450,
               "vsens" : 0.100,
               "vdepth" : 0.370},
        op1 = {"enable" : True,
               "ratio" : 0.0000,
               "bias" : 0.2321,
               "attack" : 0.0434,
               "decay1" : 0.2581,
               "decay2" : 3.6478,
               "release" : 2.9182,
               "breakpoint" : 0.5265,
               "sustain" : 0.3083,
               "lfo" : 0.0000,
               "velocity" : 0.3568,
               "break-key" : 60,
               "left-scale" : 0,
               "right-scale" : -6,
               "amp" : 0,
               "env-cycle" : True},
        op2 = {"enable" : True,
               "ratio" : 6.0000,
               "bias" : 0.0000,
               "amp" : 5.0000,
               "attack" : 0.0126,
               "decay1" : 0.6525,
               "decay2" : 0.7737,
               "release" : 0.7901,
               "breakpoint" : 0.9471,
               "sustain" : 0.9076,
               "feedback" : 0.0000,
               "lfo" : 0.0000,
               "velocity" : 0.9749,
               "modRange" : 10000,
               "break-key" : 84,
               "left-scale" : 0,
               "right-scale" : -3,
               "env-cycle" : True})

fm2( 10, "Kanawha", amp=0, port=0.000,
        external={"scale" : 1.000,
                  "bias" : 0.000,
                  "pitch" : 0.000,
                  "mod" : 0.000},
        lfo = {"freq" : 5.529,
               "delay" : 1.380,
               "vsens" : 0.055,
               "vdepth" : 0.070},
        op1 = {"enable" : True,
               "ratio" : 0.0000,
               "bias" : 0.8344,
               "attack" : 0.0634,
               "decay1" : 7.1194,
               "decay2" : 3.1006,
               "release" : 2.9182,
               "breakpoint" : 0.9198,
               "sustain" : 0.7417,
               "lfo" : 0.0000,
               "velocity" : 0.0000,
               "break-key" : 60,
               "left-scale" : 0,
               "right-scale" : 0,
               "amp" : 0,
               "env-cycle" : False},
        op2 = {"enable" : True,
               "ratio" : 4.0000,
               "bias" : 0.0000,
               "amp" : 5.0000,
               "attack" : 3.8411,
               "decay1" : 6.7465,
               "decay2" : 3.9130,
               "release" : 2.1887,
               "breakpoint" : 0.9203,
               "sustain" : 0.7608,
               "feedback" : 0.7200,
               "lfo" : 0.0000,
               "velocity" : 0.3166,
               "modRange" : 1000,
               "break-key" : 60,
               "left-scale" : 0,
               "right-scale" : 0,
               "env-cycle" : False})

