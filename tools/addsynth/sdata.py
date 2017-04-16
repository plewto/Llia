# tools/sdata
# Creates synth proxy data file

from os.path import join

def _file_header(sname):
    code = '# llia.synths.%s.%s_data\n\n' % (sname,sname)
    code += 'from __future__ import print_function\n'
    code += 'from llia.program import Program\n'
    code += 'from llia.bank import ProgramBank\n'
    code += 'from llia.performance_edit import performance\n\n'
    return code

def _prototype(params=[]):
    code = 'prototype = {\n'
    if params:
        terminal = params[-1][1]
        for junk,param,dflt in params:
            code += '    "%s" : %s' % (param,dflt)
            if param == terminal:
                code += '}\n'
            else:
                code += ',\n'
    else:
        code += '    # FIXME\n'
        code += '}\n'
    code += '\n'
    return code

def _program_class(sname):
    sname = sname[0].upper()+sname[1:]
    pad = ' '*4
    pad2 = ' '*8
    code = 'class %s(Program):\n\n' % sname
    code += '%sdef __init__(self,name):\n' % pad
    code += '%ssuper(%s,self).__init__(name,%s,prototype)\n' % (pad2,sname,sname)
    code += '%sself.performance = performance()\n\n' % pad2
    code += 'program_bank = ProgramBank(%s("Init"))\n' % sname
    code += 'program_bank.enable_undo = False\n\n'
    return code

def _program_function_sans_params(sname):
    capname = sname[0].upper()+sname[1:]
    sname = sname.lower()
    pad = ' '*(len(sname)+1)
    pad2 = ' '*4
    code = 'def %s(slot, name,\n' % sname
    code += '%s):\n' % pad
    code += '%sp = %s(name)\n' % (pad2,capname)
    code += '%s# FIXME\n' % pad2
    code += '%sprogram_bank[slot] = p\n' % pad2
    code += '%sreturn p\n\n' % pad2
    return code
    
def _program_function_with_params(sname,params):
    capname = sname[0].upper()+sname[1:]
    sname = sname.lower()
    argpad = ' '*(len(sname)+5)
    pad4 = ' '*4
    pad8 = ' '*8
    code = 'def %s(slot, name,\n' % sname
    terminal = params[-1][1]
    args = ''
    acc = ''
    for ptype,param,dflt in params:
        args += '%s%s = %s' % (argpad,param,dflt)
        if ptype == 'f':
            value = 'fval(%s)' % param
        elif ptype == 'i':
            value = 'int(%s)' % param
        else:
            msg = "Invalid parameter type (%s,%s,%s)" % (ptype,param,dflt)
            raise ValueError(msg)
        acc += '%sp["%s"] = %s\n' % (pad4,param,value)
        if param == terminal:
            args += '):\n'
        else:
            args += ',\n'
    code += args
    code += '%sdef fval(x):\n' % pad4
    code += '%sreturn round(float(x),4)\n' % pad8
    code += '%sp = %s(name)\n' % (pad4,capname)
    code += acc
    code += '%sprogram_bank[slot] = p\n' % pad4
    code += '%sreturn p\n\n' % pad4
    return code

def write_synth_data_file(devdir,sname,params=[]):
    """
    Creates file <devdir>/llia/synths/<sname>/<sname>_data.py
       <sname> is converted to lower case

    ARGS:
      devdir - String, Llia development directory
      sname  - String, synth name
      params - Optional list of parameters/defaults
               If specified params must be nested list of form
               [[t1,p1,v1],[t2,p2,v2],...,[tn,pn,vn]]
               Where:
                   ti - type, either 'f' (float) or  'i' (int)
                   pi - synth parameter
                   vi - default value 
    
    Raise IOError if <devdir>/llia/synths/<sname>  directory does 
    not exists.
    """
    code = _file_header(sname)
    code += _prototype(params)
    code += _program_class(sname)
    if params:
        code += _program_function_with_params(sname,params)
    else:
        code += _program_function_sans_params(sname)
    code += '%s(0,"Init")\n' % sname.lower()
    lcname = sname.lower()
    fn = join(devdir,"llia","synths",lcname,"%s_data.py" % lcname)
    print("Writing '%s'" % fn)
    fobj = open(fn,'w')
    fobj.write(code)
    fobj.close()
