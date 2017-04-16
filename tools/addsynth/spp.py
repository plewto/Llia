# tools/spp.py
# Creates synth proxy pp (pretty printer) file

from os.path import join

def _file_header(sname):
    lcname = sname.lower()
    code = '# llia.synths.%s.%s_pp\n\n' % (sname,sname)
    return code

_simple_template =\
"""
def %s_pp(program,slot):
    acc = ""
    # FIXME
    return acc
"""

def _pp_with_params(sname,params):
    sname = sname.lower()
    n = len(sname)+1
    cpad4 = ' '*4
    cpad8 = ' '*8
    code = 'def %s_pp(program,slot):\n' % sname
    code += '%spad=" "*%d\n' % (cpad4,n)
    code += '%sdef fval(key):\n' % cpad4
    code += '%sreturn round(float(program[key]),4)\n' % cpad8
    code += '%sdef ival(key):\n' % cpad4
    code += '%sreturn int(program[key])\n' % cpad8
    code += '%sacc = \'%s(%%d,"%%s",\\n\' %% (slot,program.name)\n' % (cpad4,sname)
    terminal = params[-1][1]
    for ftype,param,junk in params:
        if param == terminal:
            if ftype=='f':
                code += "%sacc += '%%s%%s = %%5.4f)\\n' %% (pad,'%s',fval('%s'))\n" % (cpad4,param,param)
            else:
                code += "%sacc += '%%s%%s = %%d)\\n' %% (pad,'%s',ival('%s'))\n" % (cpad4,param,param)
        else:
            if ftype=='f':
                code += "%sacc += '%%s%%s = %%5.4f,\\n' %% (pad,'%s',fval('%s'))\n" % (cpad4,param,param)
            else:
                code += "%sacc += '%%s%%s = %%d,\\n' %% (pad,'%s',ival('%s'))\n" % (cpad4,param,param)
    code += '%sreturn acc\n' % cpad4
    return code

def write_pp_file(devdir,sname,params=[]):
    """
    Creates file <devdir>/llia/synths/<sname>/<sname>_pp.py
         <sname> is converted to lower case

    ARGS:
      devdir  - String, Llia development directory
      sname   - String, synth name
      params  - Optional list of parameters
                params list should have form
                [[t1,p1,v1],[t2,p2,v2],...,[tn,pn,vn]]
                Where:
                   ti - type, either 'f' (float) or  'i' (int)
                   pi - synth parameter
                   vi - default value 
    
    Raise IOError if <devdir>/llia/synths/<sname> does not exists.
    """
    sname = sname.lower()
    code = _file_header(sname)
    if params:
        code += _pp_with_params(sname,params)
    else:
        code += _simple_template % sname
    code += '\n'
    fn = join(devdir,"llia","synths",sname,"%s_pp.py" % sname)
    print "Writing '%s'" % fn
    fobj = open(fn,'w')
    fobj.write(code)
    fobj.close()

