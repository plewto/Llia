# tools/scd.py
# Create boilerplate scd files

from os import listdir
from os.path import join,splitext

def _update_synth_install_file(devdir):
    sdir = join(devdir,"sc","SynthDefs")
    code = '/*\n'
    code += '** WARNING - This file is created automatically,\n'
    code += '** WARNING - DO NOT EDIT MANUALLY!\n'
    code += '*/\n'
    code += '(~llia_manifest=['
    files = sorted(listdir(sdir))
    terminal = files[-1]
    pad = ''
    for f in files:
        ext = splitext(f)[-1]
        if ext == ".scd":
            code += pad+'"%s"' % f
            if f == terminal:
                code += '];\n'
            else:
                code += ',\n'
                pad = ' '*17
    code += '~llia_manifest.do({|fname|\n'
    code += '    postf("Installing \'%\'\\n", fname);\n'
    code += '    fname.load;\n'
    code += '}))\n'
    return code

def _define_synth(sname,params=[]):
    sname = sname[0].upper()+sname[1:]
    code = '/*\n'
    code += '** %s\n' % sname
    code += '*/\n\n'
    code += '(SynthDef (\%s, {\n' % sname
    code += '    |\n'
    code += '     outbus = 0             // primary audio output bus\n'
    code += '     // inbus = 8           // optional audio input bus\n'
    code += '     // xbus = 1023         // optional control bus\n'
    code += '     gate = 1               // envelope gate normalized high\n'
    code += '     doneAction = 2         // doneAction determined by key mode\n'
    code += '     freq = 440             // primary frequency\n'
    code += '     keynumber = 69         // MIDI key number\n'
    code += '     detune = 1             // MIDI pitch bend ratio\n'
    code += '     velocity = 1.0         // normalized range (0..1)\n'
    if params:
        for junk,pname,dflt in params:
            code += '     %s = %s\n' % (pname,dflt)
    code += '    |\n\n\n'
    code += '}).load)\n'
    return code

def write_synthdef(devdir, sname ,params=[]):
    """
    Create SuperCollider synth boilerplate file and update the 
    synth install file.

    devdir - String, name of Llia development directory.
    sname  - String, the synth name. The synth name will be 
             altered in various places.  For the SuperCollider
             synth object the first letter is promoted to upper 
             case. For the scd file, sname is converted to lower case.

    Writes/updates two files:
        <devdir>/sc/SynthDefs/<sname>.scd
        <devdir>/sc/LliaHandler/install_synths.scd
    """
    fn = join(devdir,"sc","SynthDefs",sname.lower()+".scd")
    print "Writing synth def '%s'" % fn
    fobj = open(fn,'w')
    fobj.write(_define_synth(sname,params))
    fobj.close()
    fn = join(devdir,"sc","SynthDefs","install_synths.scd")
    print "Updating '%s'" % fn
    fobj = open(fn,'w')
    fobj.write(_update_synth_install_file(devdir))
    fobj.close()

