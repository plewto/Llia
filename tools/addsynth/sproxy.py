# tootls/sproxy
# Create synth proxy file

from file_util import new_file

from os.path import join

# Create contents for <sname>_proxy.py
# stype should be one of 'synth', 'efx', or 'controller'
# sname, the synths name
# Returns Python code as String
#
def _proxy_boilerplate(stype,sname):
    stype = stype.lower()
    lcname = sname.lower()
    capname = sname[0].upper()+sname[1:]
    code = '# llia.synths.%s.%s_proxy\n\n' % (lcname,lcname)
    code += 'from __future__ import print_function\n'
    code += 'import llia.constants\n'
    code += 'from llia.gui.pallet import default_pallet, Pallet\n'
    code += 'from llia.synth_proxy import SynthSpecs, SynthProxy\n'
    code += 'from llia.synths.%s.%s_data import program_bank\n' % (lcname,lcname)
    code += 'from llia.synths.%s.%s_pp import %s_pp\n' % (lcname,lcname,lcname)
    code += 'from llia.synths.%s.%s_random import %s_random\n\n' % (lcname,lcname,lcname)
    code += 'specs = SynthSpecs("%s")\n\n' % capname
    code += 'class %sProxy(SynthProxy):\n\n' % capname
    code += '    def __init__(self, app):\n'
    code += '        super(%sProxy,self).__init__(app,specs,program_bank)\n' % capname
    code += '        self._editor = None\n\n'
    code += '    def create_subeditors(self):\n'
    code += '        gui = self.app.config()["gui"].upper()\n'
    code += '        if gui == "TK":\n'
    code += '            from llia.synths.%s.tk.editor import create_editor\n' % lcname
    code += '            appwin = self.app.main_window()\n'
    code += '            parent_editor = appwin[self.sid]\n'
    code += '            create_editor(parent_editor)\n'
    code += '            return parent_editor\n\n'
    code += 'pallet = Pallet(default_pallet)\n'
    code += '#pallet["BACKGROUND"] =  \n'
    code += '#pallet["SLIDER-OUTLINE"] = \n'
    code += '#pallet["SLIDER-TROUGH"] = \n'
    code += 'specs["constructor"] = %sProxy\n' % capname
    code += 'specs["description"] = "FIXME"\n'
    code += 'specs["help"] = "%s"\n' % capname
    code += 'specs["pretty-printer"] = %s_pp\n' % lcname
    code += 'specs["program-generator"] = %s_random\n' % lcname
    code += 'specs["pallet"] = pallet\n'
    if stype == "efx":
        code += 'specs["is-efx"] = True\n'
        code += 'specs["is-controller"] = False\n'
        code += 'specs["keymodes"] = ("EFX",)\n'
        code += 'specs["audio-output-buses"] = [["outbus","out_0"]] # FIXME\n'
        code += 'specs["audio-input-buses"] = [["inbus","in_0"]] # FIXME\n'
        code += 'specs["control-output-buses"] = [] # FIXME\n'
        code += 'specs["control-input-buses"] = []  # FIXME\n'
        #code += 'print("\\t%s" % specs["format"])\n'
        code += 'llia.constants.EFFECT_TYPES.append(specs["format"])\n'
    elif stype == "controller":
        code += 'specs["is-efx"] = True\n'
        code += 'specs["is-controller"] = True\n'
        code += 'specs["keymodes"] = ("EFX",)\n'
        code += 'specs["audio-output-buses"] = []\n'
        code += 'specs["audio-input-buses"] = []\n'
        code += 'specs["control-output-buses"] = [] # FIXME\n'
        code += 'specs["control-input-buses"] = []  # FIXME\n'
        #code += 'print("\\t%s" % specs["format"])\n'
        code += 'llia.constants.CONTROLLER_SYNTH_TYPES.append(specs["format"])\n'
    else:
        code += 'specs["is-efx"] = False\n'
        code += 'specs["is-controller"] = False\n'
        code += 'specs["keymodes"] = ("PolyN","PolyRotate","Poly1","Mono1","MonoExclusive")\n'
        code += 'specs["audio-output-buses"] = [["outbus","out_0"]] # FIXME\n'
        code += 'specs["audio-input-buses"] = []\n'
        code += 'specs["control-output-buses"] = []\n'
        code += 'specs["control-input-buses"] = []  # FIXME\n'
        #code += 'print("\\t%s" % specs["format"])\n'
        code += 'llia.constants.SYNTH_TYPES.append(specs["format"])\n'
    return code

def write_synth_proxy_file(devdir,stype,sname):
    '''
    Create synth proxy file 
        <devdir>/llia/synths/<sname>/sname_proxy.py

    ARGS:
       devdir - String, LLia developement directory
       stype  - String, the synth type, one of 'synth','efx' or 'controller'
       sname  - String, synth name

    Raises IOError if directory <devdir>/llia/synths/<sname> does not exists.
    '''
    lcname = sname.lower()
    fn = join(devdir,"llia","synths",lcname,"%s_proxy.py" % lcname)
    print "Writing '%s'" % fn
    fobj = open(fn,'w')
    fobj.write(_proxy_boilerplate(stype,sname))
    fobj.close()
    new_file(join(devdir,"llia","synths",lcname,"__init__.py"))
    
