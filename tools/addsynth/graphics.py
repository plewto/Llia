# tools/graphics.py
# Copies graphics templates to synth resource directory.

from os.path import join
from file_util import copy_files

def copy_graphic_templates(devdir,sname):
    """
    Copies all files from 
         <devdir>/tools/templates/graphics/ 
    to 
         <devdir>/resources/<sname>

    sname is converted to lower case.
    """
    src = join(devdir,"tools","templates","graphics")
    dst = join(devdir,"resources",sname)
    copy_files(src,dst)
    print "Copied graphic templates to '%s'" % dst
