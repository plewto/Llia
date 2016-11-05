# llia.synths.algo.algo_pp



def _vibrato(p):
    pad1 = ' '*5
    pad2 = ' '*23
    acc = '%svibrato = vibrato(freq = %5.3f,\n' % (pad1,float(p['lfov_freq']))
    for arg,param  in (("delay","lfov_delay"),
                       ("sens","vsens"),
                       ("depth","vdepth")):
        acc += '%s%s = %5.3f' % (pad2,arg,float(p[param]))
        if arg == "depth":
            acc += "),\n"
        else:
            acc += ",\n"
    return acc
    
def _stack(id_, p):
    id_ = str(id_).upper()
    pad1=' '*5
    pad2=' '*20
    cop = {"A":1,"B":5,"C":7}[id_]
    plst = (("enable","stack%s_enable" % id_),
            ("amp","op%d_amp" % cop),
            ("break_key","stack%s_key" % id_),
            ("feedback","stack%s_feedback" % id_),
            ("lfo_ratio","lfo%s_ratio" % id_),
            ("lfo_delay","lfo%s_delay" % id_),
            ("lfo_wave","lfo%s_wave" % id_))
    terminal = plst[-1][0]
    flag = p[plst[0][1]] != 0
    amp = float(p[plst[1][1]])
    acc = '%sstack%s = stack("%s", enable = %s, amp = %5.3f,\n' % (pad1,id_,id_,flag,amp)
    for arg,param in plst[2:]:
        acc += '%s%s = %5.3f' % (pad2,arg,float(p[param]))
        if arg == terminal:
            acc += '),\n'
        else:
            acc += ',\n'
    return acc


def _env(n,p):
    pad1=' '*5
    pad2=' '*15
    acc = '%senv%d = env(%d,' % (pad1,n,n)
    for k in ("attack","decay1","decay2","release"):
        param = "op%d_%s" % (n,k) 
        acc += "%5.3f, " % (float(p[param]))
    acc +='\n'
    pbp = 'op%d_breakpoint' % n
    psus = 'op%d_sustain' % n
    acc += '%sbreakpoint = %5.3f, sustain = %5.3f),\n' % (pad2,float(p[pbp]),float(p[psus]))
    return acc
    

def _op(n,p):
    pad1=' '*5
    pad2=' '*14
    is_carrier = n==1 or n==5 or n==7
    acc = '%sop%d = op(%d,' % (pad1,n,n)
    pcc = ["ratio","bias"]
    if not is_carrier:
        pcc.append("amp")
        pcc.append("mod_scale")
    for arg in pcc:
        param = "op%d_%s" % (n,arg)
        value = float(p[param])
        acc += '%s = %5.4f,' % (arg,value)
    acc += '\n%s' % pad2
    for arg in ("left","right"):
        param = "op%d_%s_scale" % (n,arg)
        value = int(p[param])
        acc += '%s = %d,' % (arg, value)
    acc += '\n%s' % pad2
    for arg in ("velocity","lfo","external"):
        param = "op%d_%s" % (n,arg)
        value = float(p[param])
        acc += '%s = %5.3f' % (arg,value)
        if arg == "external":
            acc += ')'
        else:
            acc += ','
    return acc
    

def pp(program, slot=127):
    pad1 = ' '*5
    acc = 'algo(%d,"%s",\n' % (slot,program.name)
    def fval(key):
        return float(program[key])
    def ival(key):
        return int(program[key])
    acc += '%samp = %5.3f,\n' % (pad1,fval("amp"))
    acc += '%smodDepth = %5.3f,\n' % (pad1,fval("modDepth"))
    acc += '%sport = %5.3f,\n' % (pad1,fval("port"))
    acc += '%sexternal = [%5.3f,%5.3f,%5.3f],\n' % (pad1,fval("xmod"),fval("xpitch"),fval("xscale"))
    acc += _vibrato(program)
    acc += _stack("A",program)
    acc += _stack("B",program)
    acc += _stack("C",program)
    for n in (1,2,3,4,5,6,7,8):
        acc += _env(n,program)
    for n in (1,2,3,4,5,6,7,8):
        acc += _op(n,program)
        if n == 8:
            acc += ')\n'
        else:
            acc += ',\n'
    return acc


# Debug version
# raw  dump of all parameters/values
# def pp(program,slot=127):
#     acc = ''
#     for k in sorted(program.keys()):
#         if "amp" in k:
#             v = program[k]
#             acc += "[%-12s] -> %s\n" % (k,v)
#     return acc
