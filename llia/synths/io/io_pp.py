# llia.synths.io.io_pp

from __future__ import print_function

def _vibrato(program,pad,fval,ival):
    template = {"vfreq" : ("freq","f"),   # (arg, type(f|i))
                "vlock" : ("lock", "i"),
                "vnoise" : ("noise","f"),
                "vsens" : ("sens","f"),
                "vdepth" : ("depth","f"),
                "xPitch" : ("x","f"),
                "tremRatio" : ("tremRatio","f")}
    vcc = "%svibrato = vibrato(freq = %5.3f,\n" % (pad,fval("vfreq"))
    pad2 = pad+" "*18
    for param in ("vlock","vnoise","vsens","vdepth","xPitch","tremRatio"):
        arg,typ = template[param]
        if typ == "f":
            val=fval(param)
            vcc += "%s%s = %5.3f" % (pad2,arg,val)
        else:
            val = ival(param)
            vcc += "%s%s = %d" % (pad2,arg,val)
        if param == "tremRatio":
            vcc += "),\n"
        else:
            vcc += ",\n"
    return vcc
        

def _blip(program,pad,fval):
    alst = ("decay","depth","velocity")
    terminal = alst[-1]
    pad2 = pad+" "*12
    bcc = "%sblip = blip(attack = %5.3f,\n" % (pad,fval("blipAttack"))
    for a in alst:
        param = "blip%s" % a.capitalize()
        val = fval(param)
        bcc += "%s%s = %5.3f" % (pad2,a,val)
        if a == terminal:
            bcc += "),\n"
        else:
            bcc += ",\n"
    return bcc

def _noise(program,pad,fval):
    pad2 = pad + " "*14
    bcc = "%snoise = noise(ratio = %5.3f,\n" % (pad, fval("noiseRatio"))
    bcc += "%samp = %5.3f),\n" % (pad2, fval("noiseAmp"))
    return bcc

def _chiff(program,pad,fval):
    alst = ("decay","velocity","amp")
    terminal = alst[-1]
    pad2 = pad + " "*14
    ccc = "%schiff = chiff(attack = %5.3f,\n" % (pad,fval("chiffAttack"))
    for a in alst:
        param = "chiff%s" % a.capitalize()
        val = fval(param)
        ccc += "%s%s = %5.3f" % (pad2,a,val)
        if a == terminal:
            ccc += "),\n"
        else:
            ccc += ",\n"
    return ccc

def _modulator(program,pad,fval):
    pad2 = pad+" "*22
    ccc = "%smodulator = modulator(ratio = %5.3f,\n" % (pad,fval("op4Ratio"))
    ccc += "%sfeedback = %5.3f,\n" % (pad2,fval("op4Feedback"))
    ccc += "%slfo = %5.3f),\n" % (pad2,fval("op4LFO"))
    return ccc
    
def _carrier(op,program,pad,fval,ival):
    pad2 = pad+" "*14
    def param(suffix):
        return "op%d%s" % (op,suffix[0].upper()+suffix[1:])
    args = (("formant","i"),("ratio","f"),("mode","i"),
            ("velocity","f"),("tremolo","f"),("modDepth","f"),
            ("attack","f"),("decay","f"),("sustain","f"),("release","f"))
    ccc = "%sop%d = carrier(%d,\n" % (pad,op,op)
    for a,typ in args:
        p = param(a)
        if typ == "f":
            ccc += "%s%s = %5.3f,\n" % (pad2,a,fval(p))
        else:
            ccc += "%s%s = %d,\n" % (pad2,a,ival(p))
    ccc += "%slag = %5.3f,\n" % (pad2,fval(param("ModLag")))
    ccc += "%skey = %d,\n" % (pad2,ival(param("BreakKey")))
    ccc += "%sleftScale = %+d,\n" % (pad2,ival(param("LeftKeyScale")))
    ccc += "%srightScale = %+d,\n" % (pad2,ival(param("RightKeyScale")))
    ccc += "%sx = %5.3f,\n" % (pad2,fval(param("X")))
    ccc += "%samp = %5.3f" % (pad2,fval(param("Amp")))
    if op == 3:
        ccc += "))\n"
    else:
        ccc += "),\n"
    return ccc
        
def pp_io(program,slot):
    pad = " "*3

    def fval(key):
        return round(float(program[key]),4)

    def ival(key):
        return int(program[key])

    acc = 'io(%d,"%s",\n' % (slot,program.name)
    acc += "%samp = %5.3f,\n" % (pad,fval("amp"))
    acc += _vibrato(program,pad,fval,ival)
    acc += _blip(program,pad,fval)
    acc += _noise(program,pad,fval)
    acc += _chiff(program,pad,fval)
    acc += _modulator(program,pad,fval)
    for op in (1,2,3):
        acc += _carrier(op,program,pad,fval,ival)
    return acc
    
    
