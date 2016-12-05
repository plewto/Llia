# tools/stkeditor.py
# Creates synth editor boilerplate

from os.path import join
from file_util import new_file

def _header(sname):
    capname = sname[0].upper()+sname[1:]
    sname = sname.lower()
    pad4 = ' '*4
    pad8 = ' '*8
    code = '# llia.synths.%s.tk.editor\n\n' % sname
    code += 'from llia.gui.tk.tk_subeditor import TkSubEditor\n'
    code += 'import llia.gui.tk.tk_factory as factory\n'
    code += 'import llia.gui.tk.control_factory as cf\n\n'
    code += 'def create_editor(parent):\n'
    code += '%sTk%sPanel(parent)\n\n' % (pad4,capname)
    return code

def _editor_class(sname):
    capname = sname[0].upper()+sname[1:]
    #sname = sname.lower()
    pad4 = ' '*4
    pad8 = ' '*8
    code = 'class Tk%sPanel(TkSubEditor):\n\n' % capname
    code += '%sNAME = "%s"\n' % (pad4,capname)
    code += '%sIMAGE_FILE = "resources/%s/editor.png"\n' % (pad4,sname)
    code += '%sTAB_FILE = "resources/%s/tab.png"\n\n' % (pad4,sname)
    code += '%sdef __init__(self,editor):\n' % pad4
    code += '%sframe = editor.create_tab(self.NAME,self.TAB_FILE)\n' % pad8
    code += '%sframe.config(background=factory.bg())\n' % pad8
    code += '%scanvas = factory.canvas(frame,1000,700,self.IMAGE_FILE)\n' % pad8
    code += '%scanvas.pack()\n' % pad8
    code += '%sTkSubEditor.__init__(self,canvas,editor,self.NAME)\n' % pad8
    code += '%seditor.add_child_editor(self.NAME, self)\n' % pad8
    code += '%sx0,y0 = 75,75\n' % pad8
    return code

def write_editor_file(devdir,sname):
    code = _header(sname)
    code += _editor_class(sname)
    sname = sname.lower()
    fn = join(devdir,"llia","synths",sname,"tk","editor.py")
    print "Writing '%s'" % fn
    fobj = open(fn,'w')
    fobj.write(code)
    fobj.close()
    new_file(join(devdir,"llia","synths",sname,"tk","__init__.py"))
    
    
