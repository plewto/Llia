# tools/srandom
# Creates (non-functioning) random program generator for synth proxy.

from os.path import join

def _create_content(sname):
    cpad4 = ' '*4
    code = '# llia.synths.%s.%s_random\n\n' % (sname,sname)
    code += 'from __future__ import print_function\n'
    code += 'from llia.util.lmath import (coin,rnd,pick)\n'
    code += 'from llia.synths.%s.%s_data import %s\n' % (sname,sname,sname)
    code += '#from llia.synths.%s.%s_constants import *\n' % (sname,sname)
    code += '\n'
    code += 'def %s_random(slot,*_):\n' % sname
    code += '%s# FIXME\n' % cpad4
    code += '%sreturn None\n' % cpad4
    return code
    
def write_random_generator_file(devdir,sname):
    sname = sname.lower()
    code = _create_content(sname)
    fn = join(devdir,"llia","synths",sname,"%s_random.py" % sname)
    print "Writing '%s'" % fn
    fobj = open(fn,'w')
    fobj.write(code)
    fobj.close()
    
    
